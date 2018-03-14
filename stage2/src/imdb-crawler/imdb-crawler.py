from bs4 import BeautifulSoup
import requests

#page = requests.get('http://www.imdb.com/title/tt1365519/?ref_=inth_ov_tt')
page = requests.get('https://www.imdb.com/title/tt5164432/?ref_=inth_ov_tt')

soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())
title_wrapper = soup.find("div", {"class": "title_wrapper"})
print(title_wrapper)
print("***********************")

# Get Movie Title
title = soup.find("h1", {"class": ""}).text
# print(title)

# Get Play Time
playTime = title_wrapper.find("time").get("datetime")
# print(runTime)


itemProps = soup.find_all("span", {"class": "itemprop"})
genres = []
for i in itemProps:
    if i.get("itemprop") == "genre":
        genres.append(i.text)
# print(genres)

# get the Content Raiting &
meta = title_wrapper.find_all("meta")
# print(meta)
Rating = "none"
ReleaseDate = "none"
for m in meta:
    if m.get("itemprop") == "contentRating":
        Rating = m.get("content")
    elif m.get("itemprop") == "datePublished":
        ReleaseDate = m.get("content")

print(title)
print(playTime)
print(genres)
print(Rating)
print(ReleaseDate)

# Example code from internet.
# bs = BeautifulSoup(r.text)
# for movie in bs.findAll('td','title'):
#     title = movie.find('a').contents[0]
#     genres = movie.find('span','genre').findAll('a')
#     genres = [g.contents[0] for g in genres]
#     runtime = movie.find('span','runtime').contents[0]
#     rating = movie.find('span','value').contents[0]
#     year = movie.find('span','year_type').contents[0]
#     imdbID = movie.find('span','rating-cancel').a['href'].split('/')[2]
#     print title, genres,runtime, rating, year, imdbID
