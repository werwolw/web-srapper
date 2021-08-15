import requests

from bs4 import BeautifulSoup as BS

MOVIE = {}
url = input("Input your URL:").strip()

request = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

if "imdb" and "title" in url:
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')
        MOVIE = {'title': soup.find("h1").text,
                 'description': soup.select_one("[data-testid='plot-l']").text}
        print(MOVIE)
    else:
        print("Invalid movie page!")
else:
    print("Invalid movie page!")
