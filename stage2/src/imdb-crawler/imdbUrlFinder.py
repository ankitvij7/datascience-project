from bs4 import BeautifulSoup
import requests
from imdbExtractor import extract_info

# ```http://www.imdb.com/search/title?at=0&genres=action&start=51```
# "http://www.imdb.com/search/title?genres=action&start=51```
# Maybe do top 300 from each genre ?


pre_base_uri = 'http://www.imdb.com/search/title'
first_sort_type = '?sort=boxoffice_gross_us,desc'
# first_sort_type = '?sort=moviemeter,asc'
base_uri = pre_base_uri + first_sort_type
genre_base = '&genres='
imdb_genres = ("action", "comedy", "mystery", "sci_fi", "adventure", "fantasy", "horror", "animation", "drama", "thriller")
page_load_base = '&start='
# 50 movies per page
pages_per_genre = 7

for g in imdb_genres:
    for p in range(0, pages_per_genre):
        # build our URI
        uri = base_uri + genre_base + g + page_load_base + str(p * 50 + 1)
        print(uri)
        page = requests.get(uri)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(soup.prettify())

        list_movies = soup.find_all("h3", {"class": "lister-item-header"})
        print(list_movies)

        # urls = []
        for lm in list_movies:
            urlEndFull = lm.find('a', href=True)['href']
            print(urlEndFull)
            urlEnd = urlEndFull[:urlEndFull.rfind("/") + 1]
            print(urlEnd)
            # urls.append()
            url = "https://www.imdb.com" + urlEnd;
            print(url)
            extract_info(url)

        # print(urls)
