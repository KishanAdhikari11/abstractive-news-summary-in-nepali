import requests
import logging
from csv_handler import CSVHandler

logging.basicConfig(
    filename='ok.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Summarizer:
    def __init__(self):
        self.csv_store = CSVHandler("summarized_news.csv")
        self.api_url = "http://127.0.0.1:11434/v1/llama"  # Local Ollama API URL

    def summarize(self, text, num_sentences=3):
        """Summarize the news article using Ollama LLM"""
        try:
            payload = {
                "input": text,
                "num_sentences": num_sentences  # You can pass any other custom parameters
            }
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                summary = response.json().get("summary", "")
                return summary
            else:
                logging.error(f"Error from Ollama API: {response.status_code}")
                return "Summary unavailable"
        except Exception as e:
            logging.error(f"Error using Ollama: {e}")
            return "Summary unavailable"

    def process_news(self, news_data):
        """Process and summarize the news data"""
        for article in news_data:
            headline = article['headline']
            news_content = article['news']
            
            # Summarize the news content using Ollama LLM
            summary = self.summarize(news_content)
            
            # Store the summary in CSV
            data = [{"headline": headline, "summary": summary}]
            self.csv_store.save_to_csv(data)
            logging.info(f"Summarized news for: {headline}")

# Example usage
if __name__ == "__main__":
    sample_news = [
        {"headline": "Politics in Nepal: Current State", "news": "Nepal’s political situation is complex with ongoing negotiations..."},
        {"headline": "Economy of Nepal: Challenges and Solutions", "news": "The economy of Nepal is facing numerous hurdles due to inflation..."}
    ]
    
    summarizer = Summarizer()
    summarizer.process_news(sample_news)
