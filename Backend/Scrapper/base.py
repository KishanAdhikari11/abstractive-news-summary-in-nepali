import requests
from bs4 import BeautifulSoup
import re
import json

class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.portal_name = self.extract_portal_name()

    def get_soup(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content, 'lxml')
        return soup

    def get_news(self):
        soup = self.get_soup()
        raise NotImplementedError("Subclasses should implement this method.")

    def extract_portal_name(self):
        portal_name = re.search(r"https?://(?:www\.)?(\w+)\.", self.url)
        if portal_name:
            return portal_name.group(1)
        return "Unknown"

    def get_news_json(self):
        news_content = self.get_news()
        return {
            "portal_name": self.portal_name,
            "news_content": news_content
        }