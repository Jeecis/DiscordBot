import requests
from bs4 import BeautifulSoup

class Scraper:
        def __init__(self, web_link):
            self.web_link=web_link


        def scrape(self):

            if ("www." in self.web_link) == False:
                self.web_link = "www." + self.web_link

            if ("https://" in self.web_link) == False:
                self.web_link = "https://" + self.web_link

            html_text = requests.get(self.web_link).text
            soup = BeautifulSoup(html_text, 'lxml')

            articles = soup.find_all("article")

            link = "Couldn't get a link"
            # print(articles)
            for article in articles:
                href = article.find(href=True)
                if href:
                    link = href['href']
                    # h_tag = article.find(compile("^h"))
                    # print(self.web_link in link)
                    # print(h_tag)
                    if (self.web_link in link) == False:
                        link = self.web_link+href['href']
                    break


            return link




