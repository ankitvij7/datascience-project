from bs4 import BeautifulSoup
import requests
import csv

fieldnames = ['Movie Url', 'Title', 'Score', 'Rating', 'Genre', 'Director', 'Writer', 'Release Date', 'Runtime', 'Studio']
# movie_url_str = "Movie Url"
title_str = "Title"
score_str = "Score"
rating_str = "Rating"
genre_str = "Genre"
# genre1_str = "Genre1"
# genre2_str = "Genre2"
director_str = "Director"
writer_str = "Writer"
release_date_str = "Release Date"
runtime_str = "Runtime"
studio_str = "Studio"


def extract_info(movie_url, output):
    # open out our dictionary.
    page = requests.get(movie_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.prettify())
    title_wrapper = soup.find("div", {"class": "title_wrapper"})
    #print(title_wrapper)

    movie_info = dict()
    # print("***********************")

    # Get Movie Title
    movie_info[title_str] = soup.find("h1", {"class": ["", "long"]}).text
    # print(movie_info[title_str])

    # Get Run Time
    #print(title_wrapper.find("time"))
    time_entry = title_wrapper.find("time")
    if time_entry:
        movie_info[runtime_str] = time_entry.get("datetime")
    # print(movie_info[runtime_str])

    itemProps = soup.find_all("span", {"class": "itemprop"})
    genres = []
    for i in itemProps:
        if i.get("itemprop") == "genre":
            genres.append(i.text)

    movie_info[genre_str] = ";".join(genres)
    # print(genres)
    # ignore any genres over 3
    # if 2 < len(genres):
    #     movie_info[genre2_str] = genres[2]
    # if 1 < len(genres):
    #     movie_info[genre1_str] = genres[1]
    # if 0 < len(genres):
    #     movie_info[genre_str] = genres[0]

    # get the Content Rating & release date.
    meta = title_wrapper.find_all("meta")
    # print(meta)
    for m in meta:
        if m.get("itemprop") == "contentRating":
            movie_info[rating_str] = m.get("content")
        elif m.get("itemprop") == "datePublished":
            movie_info[release_date_str] = m.get("content")

    # Left to extract
    # get the movie score aka ratingsValue

    # Try to get ratings wrapper
    ratings_wrapper = soup.find("div", {"class": "ratings_wrapper"})
    if ratings_wrapper is not None:
        span = ratings_wrapper.find_all("span")
        for s in span:
            if s.get("itemprop") == "ratingValue":
                movie_info[score_str] = s.text


    #finding directors and writers and possibly stars if we want
    credit_summary_item_s = soup.find_all("div", {"class": "credit_summary_item"})
    directors = []
    writers = []
    for item in credit_summary_item_s:
        span = item.find_all("span")
        flag_writer = 0
        flag_director = 0
        for s in span:
            if s.get("itemprop") == "director":
                flag_director = 1
                break
            elif s.get("itemprop") == "creator":
                flag_writer = 1
                break
        for s in span:
            if s.get("itemprop") == "name":
                if flag_director == 1:
                    directors.append(s.text)
                elif flag_writer == 1:
                    writers.append(s.text)
                # elif flag_actor == 1:
                #     stars.append...
    print(";".join(directors ))
    print(";".join(writers ))
    #TODO: change this - to something else, or only record limited number of directors and writers.
    if len(directors) > 0:
        movie_info[director_str] = ";".join(directors ) #concatenating all directors by - and adding them to the director column
    if len(writers) > 0:
        movie_info[writer_str] = ";".join(writers )

    # fieldnames = ['Movie Url', 'Title', 'Score', 'Rating', 'Genre', 'Genre1', 'Genre2', 'Director', 'Writer', 'Release Date', 'Runtime', 'Studio']
    output.writerow({'Movie Url': movie_url,
                     'Title': 'NA' if title_str not in movie_info else movie_info[title_str],
                     'Score': 'NA' if score_str not in movie_info else movie_info[score_str],
                     'Rating': 'NO RATED' if rating_str not in movie_info else movie_info[rating_str],
                     'Genre': 'NA' if genre_str not in movie_info else movie_info[genre_str],
                     # 'Genre1': 'NA' if genre1_str not in movie_info else movie_info[genre1_str],
                     # 'Genre2': 'NA' if genre2_str not in movie_info else movie_info[genre2_str],
                     'Director': 'NA' if director_str not in movie_info else movie_info[director_str],
                     'Writer': 'NA' if writer_str not in movie_info else movie_info[writer_str],
                     'Release Date': 'NA' if release_date_str not in movie_info else movie_info[release_date_str],
                     'Runtime': 'NA' if runtime_str not in movie_info else movie_info[runtime_str],
                     'Studio': 'NA' if studio_str not in movie_info else movie_info[studio_str]})

# Standalone execution examples.
# extract_info('http://www.imdb.com/title/tt1365519/')
# extract_info('https://www.imdb.com/title/tt5164432/')
# extract_info('https://www.imdb.com/title/tt0120737/', csv.DictWriter(open("LocalTest.csv", "a"), fieldnames=fieldnames))
# extract_info('https://www.imdb.com/title/tt4154756/', csv.DictWriter(open("LocalTest.csv", "a"), fieldnames=fieldnames))