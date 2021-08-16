import requests
import sys

from bs4 import BeautifulSoup as BS

MOVIE = {}
URL = input("Input your URL:").strip()


def get_url():
    response = requests.get(URL, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response.status_code == 200:
        return response
    else:
        # sys.exit(f"The URL returned {request.status_code}!")
        print(f"The URL returned {response.status_code}!")
        sys.exit()


def save_content(response):
    try:
        file = open('source.html', 'wb')
        file.write(response.content)
        file.close()
        print("Content saved.")
    except SystemError:
        print("Oops, something wrong")


def find_movie(response):
    save_content(response)
    if "imdb" and "title" in URL:
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            MOVIE = {'title': soup.find("h1").text,
                     'description': soup.select_one("[data-testid='plot-l']").text}
            print(MOVIE)
        else:
            print("Invalid movie page!")
    else:
        print("Invalid movie page!")


if __name__ == '__main__':
    find_movie(get_url())
