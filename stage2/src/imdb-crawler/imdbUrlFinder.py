from bs4 import BeautifulSoup
import requests
from imdbExtractor import extract_info

page = requests.get('https://www.imdb.com/chart/top?ref_=nv_mv_250_6')
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())

top_movies = soup.find_all("td", {"class": "titleColumn"})
# print(top_movies)

# urls = []
for tm in top_movies:
    urlEndFull = tm.find('a', href=True)['href']
    # print(urlEndFull)
    urlEnd = urlEndFull[:urlEndFull.rfind("/") + 1]
    # print(urlEnd)
    # urls.append()
    url = "https://www.imdb.com" + urlEnd;
    print(url)
    extract_info(url)

# print(urls)
