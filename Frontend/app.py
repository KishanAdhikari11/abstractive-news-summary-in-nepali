from flask import Flask, render_template, request
import requests
from flask_cors import CORS
from flask import jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
# from dotenv import load_dotenv
import os
from Scrapper.onlinekhabar import OnlinekhabarScraper
from Scrapper.ekantipur import EkantipurkhabarScraper
from Scrapper.nayapatrika import NayaPatrikaScraper
from Scrapper.ratopati import RatopatiScraper
from Scrapper.setopati import SetopatiScraper



app = Flask(__name__)
CORS(app)

#loading mT5 model
tokenizer = AutoTokenizer.from_pretrained("Adarsh203/new_mT5_Sum")
model = AutoModelForSeq2SeqLM.from_pretrained("Adarsh203/new_mT5_Sum")
# Loading mBART model
tokenizer2 = AutoTokenizer.from_pretrained("Kishan11/mBART_SUM")
model2 = AutoModelForSeq2SeqLM.from_pretrained("Kishan11/mBART_SUM")

API_KEY = "b990dbcbaf50a594e0f123cdd9f976706c7e4e5c"


#extracting news through url
# def get_newsfrom_url(url):

#   endpoint = "https://extractorapi.com/api/v1/extractor"
#   params = {
#     "apikey": API_KEY,
#     "url": url
#   }
#   r = requests.get(endpoint, params=params)
#   resp=r.json()
#   try:
#     news=resp['text']
#   except:
#     news="Error"
#   return news

def extract_portal_name(url):
    portal_name = re.search(r"https?://(?:www\.)?(\w+)\.", url)
    if portal_name:
        return portal_name.group(1)
    return "Unknown"


def get_newsfrom_url(url):
    portal_name = extract_portal_name(url)
    news = "Couldn't find url"  # Default message
    try:
        match portal_name:
            case "onlinekhabar":
                scraper = OnlinekhabarScraper(url)
            case "ratopati":
                scraper = RatopatiScraper(url)
            case "setopati":
                scraper = SetopatiScraper(url)
            case "nayapatrikadaily":
                scraper = NayaPatrikaScraper(url)
            case "ekantipur":
                scraper = EkantipurkhabarScraper(url)
            case _:
                scraper = None
        
        if scraper:
            news_json = scraper.get_news_json()
            news = news_json.get("news_content", "News content not found")
    except Exception as e:
        news = f"Error fetching news: {e}"

    return news


def format_paragraph(text):
    #regular expression to match alphabetical characters,numbers,various symbols
    pattern = r'[a-zA-Z0-9!#@]'
    
    #Remove matched characters using the pattern
    text_without_chars = re.sub(pattern,'',text)
    # Split the text into lines, remove leading and trailing spaces from each line,  and filter out any empty lines.
    lines = [line.strip() for line in text_without_chars.splitlines() if line.strip()]
    # Join the lines with a space to ensure words are not concatenated without spacing.
    formatted_text = ' '.join(lines)
    return formatted_text

def split_text_by_sentence_end_in_range(text, min_chunk_size, max_chunk_size, delimiter='।'):
    words = text.split()
    chunks = []
    current_chunk = []
    current_word_count = 0

    for word in words:
        current_chunk.append(word)
        current_word_count += 1

        # When current chunk size is within the specified range
        if min_chunk_size <= current_word_count <= max_chunk_size and word.endswith(delimiter):
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        # If current chunk size exceeds max_chunk_size
        elif current_word_count > max_chunk_size:
            # Try to find the last delimiter within the chunk to split
            chunk_text = " ".join(current_chunk)
            last_delimiter_index = chunk_text.rfind(delimiter)
            if last_delimiter_index != -1:
                # Include the delimiter in the current chunk
                split_point = last_delimiter_index + len(delimiter)
                chunks.append(chunk_text[:split_point])
                # Start a new chunk with the remaining text
                remaining_text = chunk_text[split_point:].strip()
                current_chunk = remaining_text.split()
                current_word_count = len(current_chunk)
            else:
                # No delimiter found; forcefully split at max_chunk_size
                chunks.append(chunk_text)
                current_chunk = []
                current_word_count = 0

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summary(text, model, tokenizer, max_summary_length):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    input_ids = inputs.input_ids.to(model.device)
    summary_ids = model.generate(input_ids, max_length=max_summary_length, num_beams=4, length_penalty=0.1, early_stopping=True)
    # print(f'Summary IDS:{summary_ids}')
    generated_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return generated_summary

#long summary
def summary_nepali(text,model,tokenizer,max_summary_length=512):
    chunks = split_text_by_sentence_end_in_range(text,100,150)
    for i in range(len(chunks)):
        print(chunks[i])

    summaries = [summary(chunk,model,tokenizer,max_summary_length) for chunk in chunks]

    final_summary = ' '.join(summaries)

    return final_summary


# short summary
def mt5Summary(text,model,tokenizer,max_summary_length=512):
    input = tokenizer(text,return_tensors="pt",max_length=max_summary_length,truncation=True)
    summary_ids = model.generate(input.input_ids.to(model.device), 
                                  max_length=max_summary_length, 
                                  num_beams=5,
                                  length_penalty=0.1,
                                  early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

#short summary
def mbartSummary(text,model,tokenizer,max_summary_length=512):
    inputs = tokenizer(text,return_tensors="pt",max_length=max_summary_length,truncation=True)
    summary_ids = model.generate(inputs.input_ids.to(model.device), 
                                  max_length=max_summary_length, 
                                  num_beams=5,
                                  length_penalty=0.1,
                                  early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/', methods=['GET', 'POST'])
def summarize():
    request.method == 'POST'
    data = request.json  
    print(f"data: {data}")  
    text = data.get('text', '')  
    given_url = data.get('url', '')  
    selected_model = data.get('selectedModel')
    selected_length = data.get('selectedLength')

    if given_url:
        text = get_newsfrom_url(given_url)
       

    formatted_text = format_paragraph(text)

    if selected_model == 'model1' and selected_length== 'short':
        summarized_text = mt5Summary(formatted_text, model, tokenizer)
    elif selected_model == 'model1' and selected_length == 'long':
        summarized_text = summary_nepali(formatted_text,model,tokenizer)
    elif selected_model == 'model2' and selected_length == 'short':
        summarized_text = mbartSummary(formatted_text,model2,tokenizer2)
        print(summarized_text)
    elif selected_model == 'model2' and selected_length == 'long':
        summarized_text = summary_nepali(formatted_text,model2,tokenizer2)
    
    try:
        summary = jsonify({'summarized_text': summarized_text,'formatted_text':formatted_text})
    except:
        summary = jsonify({'summarized_text':'Loading..'})
    return summary
    

if __name__ == "__main__":
    app.run(debug=True)
