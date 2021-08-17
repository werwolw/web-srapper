import requests
import re
import string
import sys

from bs4 import BeautifulSoup as BS

# URL = input("Input your URL:").strip()
URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"


def get_url():
    response = requests.get(URL, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response.status_code == 200:
        return response
    else:
        sys.exit(f"The URL returned {response.status_code}!")


def save_content(file_name, content, ext='txt', mode='wb'):
    try:
        file = open(f'{file_name}.{ext}', f'{mode}')
        file.write(content.encode())
        file.close()
        print(f"Content saved into {file_name}.{ext}")
    except SystemError as SE:
        print("Oops, something wrong:", SE)


def find_news_article(response):
    soup_main = BS(response.content, 'html.parser')
    all_articles = soup_main.find_all("article")
    for article in all_articles:
        type_of_article = article.find('span', class_="c-meta__type").text
        if type_of_article == "News":
            raw_title = article.find('a').text.strip()
            title = raw_title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            link_to_article = "https://www.nature.com" + article.a.get('href')
            get_news_article = requests.get(link_to_article)
            soup_news = BS(get_news_article.content, 'html.parser')
            body_article = soup_news.find(class_=re.compile(".*article-body.*")).text.strip()
            save_content(title, body_article)


if __name__ == '__main__':
    find_news_article(get_url())
