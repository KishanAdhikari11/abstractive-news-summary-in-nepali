import os
import time
import pandas as pd
from typing import List, Dict
import csv
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

print(GEMINI_API_KEY)
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

def summarize_with_gemini(text: str, max_length: int = 400) -> str:
    """
    Summarize Nepali news text using Google's Gemini model.
    
    Args:
        text: The Nepali news text to summarize
        max_length: Maximum word count for the summary
    
    Returns:
        String containing the summary or error message
    """
    if not text or len(text) < 100:
        return "Text too short to summarize"
    
    try:
        prompt = (
            f"You are journalist woring in nepali news portal and your job is to give nepali summary of news article. Provide a concise summary of the following Nepali news article in approximately 2-4 sentence. 4 for longer article and 2 for shorter one and 3 for medium one"
            f"Focus on the main points, key events, and significant information while maintaining the Nepali context. "
            f"Give only summary and dont give unnecessary chat. Just give me summary, nothing more not even extra unwanted word. Just give me summary"
            f"summarize it in somewhat abstractive way by keeping the original context same by reducing long sentence into small one"
            f"Avoid unnecessary details and present the summary in clear and in give in Nepai:\n\n{text}"
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        return response.text.strip()
    except Exception as e:
        return f"Summarization failed: {str(e)}"

def process_articles_from_csv(input_csv: str, output_csv: str, article_column: str, max_length: int = 200, 
                             batch_size: int = 10, delay: float = 4.0) -> None:
    """
    Process articles from a CSV file, summarize each one, and save results to a new CSV.
    
    Args:
        input_csv: Path to the input CSV file containing articles
        output_csv: Path to save the output CSV with summaries
        article_column: Name of the column in input CSV that contains the article text
        max_length: Maximum word count for summaries
        batch_size: Number of articles to process before saving interim results
        delay: Delay in seconds between API calls to avoid rate limiting
    """
    try:
        df = pd.read_csv(input_csv, encoding='utf-8')
        print(f"Loaded {len(df)} articles from {input_csv}")
        
        if article_column not in df.columns:
            raise ValueError(f"Column '{article_column}' not found in the CSV file")
        
        results = []
        
        # Create output CSV file with headers
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['article', 'summary'])  # Write headers
        
        for i, row in enumerate(df.itertuples(), 1):
            article = getattr(row, article_column)
            if not isinstance(article, str):
                print(f"Skipping row {i}: Article is not a string")
                continue
            # if i<9660:
            #     continue
                
            print(f"Processing article {i}/{len(df)}...")
            
            # Skip overly long articles
            if len(article) > 9000:
                print(f"Skipping row {i}: Article too long (over 10,000 characters)")
                continue
            
            # Get summary
            summary = summarize_with_gemini(article, max_length)
            
            # Write directly to CSV in simple article, summary format
            with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([article, summary])
            
            print(f"Saved article {i} summary to {output_csv}")
            
            if i < len(df):  # Don't delay after the last item
                print(f"Waiting {delay} seconds before next request to respect rate limits...")
                time.sleep(delay)
                
            # if i == 10500:
            #     break
            
        print(f"Processing complete. Results saved to {output_csv}")
            
    except Exception as e:
        print(f"Error processing articles: {str(e)}")

if __name__ == "__main__":
    INPUT_CSV = "data/bizmandu/bizmandu_banking.csv"  # Update with your input CSV file path
    OUTPUT_CSV = "bizmandu_banking_sum.csv"  # Output file for summaries
    ARTICLE_COLUMN = "content"  # Update with your actual column name containing the article text
    MAX_SUMMARY_LENGTH = 400  # Maximum summary length in words
    
    process_articles_from_csv(
        input_csv=INPUT_CSV,
        output_csv=OUTPUT_CSV,
        article_column=ARTICLE_COLUMN,
        max_length=MAX_SUMMARY_LENGTH,
        batch_size=10,  # Save results after every 10 articles (note: in this version we save after each article)
        delay=4.0  # 5 second delay between API calls to respect rate limits
    )