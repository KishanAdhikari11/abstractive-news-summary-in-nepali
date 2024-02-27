from flask import Flask, render_template, request
from flask_cors import CORS
from flask import jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)

tokenizer = AutoTokenizer.from_pretrained("Kishan11/test")
model = AutoModelForSeq2SeqLM.from_pretrained("Kishan11/test")

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer2 = AutoTokenizer.from_pretrained("Adarsh203/mBART_SUM")
model2 = AutoModelForSeq2SeqLM.from_pretrained("Adarsh203/mBART_SUM")

# def split_text(text,chunk_size=200):
#     sentences = text.split('|')
#     chunks = []
#     current_chunk = []

#     def word_count(sentences_list):
#         return sum(len(sentence.split()) for sentence in sentences_list)
    
#     for sentence in sentences:
#         if word_count(current_chunk+[sentence]) <= chunk_size:
#             current_chunk.append(sentence)

#         else:
#             if current_chunk:
#                 chunks.append('|'.join(current_chunk))
#                 current_chunk = [sentence]

#             else:
#                 chunks.append(sentence)
    
#     if current_chunk:
#         chunks.append('|'.join(current_chunk))

#     return chunks

# def summary_nepali(text,model,tokenizer,max_summary_length=512):
#     chunks = split_text(text)

#     summaries = [summary(chunk,model,tokenizer,max_summary_length) for chunk in chunks]

#     final_summary = '|'.join(summaries)

#     return final_summary



# def summary(text, model, tokenizer, max_summary_length):
#     inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
#     input_ids = inputs.input_ids.to(model.device)
#     summary_ids = model.generate(input_ids, max_length=max_summary_length, num_beams=4, length_penalty=0.1, early_stopping=True)
#     generated_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return generated_summary


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
    generated_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return generated_summary

def summary_nepali(text,model,tokenizer,max_summary_length=512):
    chunks = split_text_by_sentence_end_in_range(text,50,125)
    for i in range(len(chunks)):
        print(chunks[i])

    summaries = [summary(chunk,model,tokenizer,max_summary_length) for chunk in chunks]

    final_summary = ' '.join(summaries)

    return final_summary



def mbartSummary(text,model,tokenizer,max_summary_length=512):
    input = tokenizer2(text,return_tensors="pt",max_length=max_summary_length,truncation=True)
    summary_ids = model.generate(input.input_ids.to(model.device), 
                                  max_length=max_summary_length, 
                                  num_beams=5,
                                  length_penalty=0.1,
                                  early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary



def format_paragraph(text):
    sentences = text.split('\n\n')
    formatted_text = '\n\n'.join(' '.join(sentence.split()) for sentence in sentences)
    return formatted_text

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/summarize', methods=['POST'])
# def summarize():
#     data = request.json
#     # text = request.form['text']
#     text = data['text']
#     summarized_text = summary(text, model, tokenizer)
#     # return render_template('summary.html', original_text=text, summarized_text=summarized_text)
#     return jsonify({'summarized_text':summarized_text})


# if __name__ == "__main__":
#     app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def summarize():
    # if request.method == 'POST':
    #     data = request.json
    #     text = data['text']
    #     summarized_text = summary_nepali(text, model, tokenizer)
    #     return jsonify({'summarized_text': summarized_text})

    request.method == 'POST'
    data = request.json
    text = data['text']
    selected_model = data['selectedModel']

    if selected_model == 'default':
        summarized_text = summary_nepali(text, model, tokenizer)
    elif selected_model == 'model2':
        summarized_text = mbartSummary(text,model2,tokenizer2)
    
    try:
        summary = jsonify({'summarized_text': summarized_text})
    except:
        summary = jsonify({'summarized_text':'Loading..'})
    return summary
    # else:
    #     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
