import os
import re
import string
import sys

import requests
from bs4 import BeautifulSoup as BS

URL = "https://www.nature.com/nature/articles"
COUNT_PAGES = int(input("Input count pages:"))
ARTICLE_TYPE = str(input("Input type of articles:")).title()


def get_url(page_number):
    response = requests.get(URL,
                            headers={'Accept-Language': 'en-US,en;q=0.5'},
                            params=f"page={page_number}")
    if response.status_code == 200:
        return response
    else:
        sys.exit(f"The URL returned {response.status_code}!")


def save_content(file_name, content, ext='txt', mode='wb', page_num=1):
    try:
        if not os.access(f"Page_{page_num}", os.F_OK):
            os.mkdir(f"Page_{page_num}")
        path_to_dir = os.path.join(os.getcwd(), f"Page_{page_num}")
        file = open(rf'{path_to_dir}\{file_name}.{ext}', f'{mode}')
        file.write(content.encode())
        file.close()
        print(f"Content saved into {file_name}.{ext}")
    except SystemError as SE:
        print("Oops, something wrong:", SE)


def find_news_article(response, page_number):
    soup_main = BS(response.content, 'html.parser')
    all_articles = soup_main.find_all("article")
    for article in all_articles:
        type_of_article = article.find('span', class_="c-meta__type").text
        if type_of_article == ARTICLE_TYPE:
            raw_title = article.find('a').text.strip()
            title = raw_title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')
            link_to_article = "https://www.nature.com" + article.a.get('href')
            get_news_article = requests.get(link_to_article)
            soup_news = BS(get_news_article.content, 'html.parser')
            body_article = soup_news.find(class_=re.compile(".*article-.*body.*")).text.strip()
            save_content(title, body_article, page_num=page_number)
        else:
            if not os.access(f"Page_{page_number}", os.F_OK):
                os.mkdir(f"Page_{page_number}")


if __name__ == '__main__':
    for num in range(1, COUNT_PAGES + 1):
        find_news_article(get_url(num), num)
