import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
from csv_handler import CSVHandler

logging.basicConfig(
    filename='ok.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Scrapper:
    def __init__(self):
        self.url = 'https://nepalnews.com/s/'
        self.start = 1
        self.end = 200
        self.links = []
        self.category = ['politics', 'business', 'capital','sports','health','entertainment-lifestyle','science-technology', 'travel-tourism']
        self.csv_store = CSVHandler("news_data.csv")

    def get_soup(self, url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return BeautifulSoup(resp.content, 'lxml')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching the page {url}: {e}")
            return None

    def run(self):
        try:
            successful_id = []
            while self.start <= self.end:
                url = self.url + str(self.start)
                response = self.get_soup(url)
                if response:
                    successful_id.append(self.start)
                self.start += 1
            with open('successful.txt', 'w') as f:
                f.write(str(successful_id))
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching pages: {e}")

    def get_link(self):
        try:
            href_list = []
            temp_list=[]
            for cat in self.category[:1]:
                self.start=1
                while self.start<=self.end:
                    
                    link = self.url + cat+'/page/'+str(self.start)
                    soup = self.get_soup(link)
                    if soup:
                        link_divs = soup.find_all("div", class_='col')[:12]
                        for div in link_divs:
                            href = div.find('a')
                            if href:
                                href_tag = href.get('href')
                                temp_list.append(href_tag)
                                href_list.append(href_tag)
                                
                    logging.info(f"Number of links found: {len(temp_list)} on page {self.start}")
                    temp_list=[]
                    self.start+=1
            return href_list
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching category pages: {e}")
            return []

    def get_news(self):
        links = self.get_link()
        for link in links:
            try:
                soup = self.get_soup(link)
                if not soup:
                    continue

                # Extract headline
                headline = soup.find('h2', class_='title home-main-title').get_text(strip=True)
                # headline = headline_div.find('h2').get_text(strip=True) if headline_div else "No headline found"

                news = soup.find('div', class_='the-content')
                if news:
                    news_paragraphs = news.find_all('p')
                    news_content = ' '.join(p.get_text(strip=True) for p in news_paragraphs if p.get_text(strip=True))
                    
                else:
                    news_content = "No news content found"
                if len(news_content)>10 and len(news_content)<5000:

                    data = [{"headline": headline, "news": news_content}]
                    self.csv_store.save_to_csv(data)
            except Exception as e:
                logging.error(f"Error processing link {link}: {e}")

