from Scrapper.base import BaseScraper
from lxml import html

class GorkhapatraScraper(BaseScraper):
    def get_news(self):
        soup = self.get_soup()
        root=html.fromstring(str(soup))
        news = root.xpath("//div[@class='blog-details']/p//text()")
        if news:
            news_content = []
            for p in news:
                paragraph = p.strip()  # Strip to remove extra whitespace
                if paragraph:  # Exclude empty paragraphs
                    news_content.append(paragraph)
            return ' '.join(news_content)
        else:
            return "No news found on Gorkhapatra"
