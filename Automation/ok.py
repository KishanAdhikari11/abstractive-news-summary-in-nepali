from bs4 import BeautifulSoup
import requests
from lxml import html
import pandas as pd
import csv


category = ['political', 'economy', 'lifestyle', 'travel', 'sports']

page_limit = 50

def get_link(soup):
    root = html.fromstring(str(soup))
    links = root.xpath("//div[@class='ok-news-post ltr-post']//a/@href")[::2]
    return links

def extract_news(soup):
    root = html.fromstring(str(soup))
    title = root.xpath("//div[@class='ok-post-header']/h1/text()")
    cleaned_title=' '.join(title)
    cleaned_title=cleaned_title.strip()
    news = root.xpath('//div[@class="post-content-wrap"]//p/text() | //div[@class="post-content-wrap"]//a/text() | //div[@class="post-content-wrap"]//h2/text()')
    news_article=' '.join(news)
    news_article=news_article.strip()
    return cleaned_title,news_article

def save_to_csv(title,article,category):
    data={'Title':[title],'Article':[article],'Category':[category]}
    df=pd.DataFrame(data)
    if not csv_exists():
        df.to_csv("ok.csv", index=False)
    else:
        df.to_csv("ok.csv", index=False, mode='a', header=False)
    
    
    
def csv_exists():
    try:
        with open("ok.csv") as file:
            return True
    except FileNotFoundError:
        return False

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

if __name__ == "__main__":
    page_no=1
    while page_no<=page_limit:
        base_url = "https://english.onlinekhabar.com/category/economy/page"+str(page_no)

        soup = get_soup(base_url)
        news_links = get_link(soup)
        
        for link in news_links:
            soup = get_soup(link)
            title,article=extract_news(soup)

            save_to_csv(title,article,'economy')
        page_no+=1

