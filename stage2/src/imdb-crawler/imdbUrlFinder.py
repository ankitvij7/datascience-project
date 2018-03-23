from bs4 import BeautifulSoup
import requests
from ImdbExtractor import extract_info
import csv

# ```http://www.imdb.com/search/title?at=0&genres=action&start=51```
# "http://www.imdb.com/search/title?genres=action&start=51```
# Maybe do top 300 from each genre ?


pre_base_uri = 'http://www.imdb.com/search/title'
# first_sort_type = '?sort=boxoffice_gross_us,desc'
first_sort_type = '?sort=moviemeter,asc'

base_uri = pre_base_uri + first_sort_type
genre_base = '&genres='
imdb_genres = ("action", "comedy", "mystery", "sci_fi", "adventure", "fantasy", "horror", "animation", "drama", "thriller")
page_load_base = '&start='
# 50 movies per page
pages_per_genre = 7

fieldnames = ['Movie Url', 'Title', 'Score', 'Rating', 'Genre', 'Genre1', 'Genre2', 'Director', 'Writer', 'Release Date', 'Runtime', 'Studio']
output_file = open("ImdbMovieDatabase.raw", "a")
output = csv.DictWriter(output_file, fieldnames=fieldnames)
# Comment this out when re-running
output.writeheader()
start_page = 0

for p in range(start_page, pages_per_genre):
    for g in imdb_genres:
        # build our URI
        uri = base_uri + genre_base + g + page_load_base + str(p * 50 + 1)
        # print(uri)
        page = requests.get(uri)
        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())

        list_movies = soup.find_all("h3", {"class": "lister-item-header"})
        # print(list_movies)

        for lm in list_movies:
            urlEndFull = lm.find('a', href=True)['href']
            # print(urlEndFull)
            urlEnd = urlEndFull[:urlEndFull.rfind("/") + 1]
            url = "https://www.imdb.com" + urlEnd;
            print("genre: ", g, ", page: ", p, " , movie: ", url)
            extract_info(url, output)
            #output_file.flush()
        #flush per page load, should speed it up.
        output_file.flush()
