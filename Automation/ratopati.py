from bs4 import BeautifulSoup
import requests
from lxml import html
import pandas as pd
import csv

def get_link(soup):
    root=html.fromstring(str(soup))
    links = root.xpath("//div[@class='columnnews mbl-col col3']//a/@href")
    return links

def extract_news(soup):
    root = html.fromstring(str(soup))
    title=root.xpath("//div[@class='news-detail-header']//h2/text()")
    article=root.xpath("//div[@class='news-contentarea']//p/text()")
    cleaned_title=' '.join(title)
    cleaned_title=cleaned_title.strip()
    news_article=' '.join(article)
    news_article=news_article.strip()
    cleaned_article=news_article.replace("\n","")
    return cleaned_title,cleaned_article


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

if __name__=="__main__":
    page_no=1
    page_limit=200

    
   
    # print(link)
    while page_no <= page_limit:
        base_url="https://www.ratopati.com/category/news?page="+str(page_no)
        soup=get_soup(base_url)
        link=get_link(soup)
        news_link=get_link(soup)
        
        for link in news_link:
            soup=get_soup(link)
            
            title,news=extract_news(soup)
                
            if title and news is not None:
                print(title,len(news))
                with open("news.txt",'a') as f:
                    f.write(str(news)+'\n')
                with open("title.txt",'a') as f:
                    f.write(str(title)+'\n')
        page_no+=1
        
    