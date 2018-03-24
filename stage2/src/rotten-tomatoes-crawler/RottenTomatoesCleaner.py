import csv

fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre',
              'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime',
              'Studio', 'Audience Score']
url = "Url"
title = "Title"
score = "Score"
rating = "Rating"
genre = "Genre"
directed = "Directed By"
writen = "Written By"
box_office = "Box Office"
release_date = "Release Date"
runtime = "Runtime"
studio = "Studio"
aud_score = "Audience Score"


def clean_url(url):
    return url


def clean_title(title):
    return title.replace("2018", "").replace("2017", "").replace("2016", "").replace("2015", "").replace("2014", "").replace("2013", "").replace("2012", "").replace("()", "").strip(' \t\n\r')


def clean_score(score):
    return score


def clean_rating(rating):
    return rating


def clean_genre(genre):
    return genre


def clean_directed(directed):
    return directed


def clean_writen(writen):
    return writen


def clean_box_office(box_office):
    return box_office


def clean_release_date(release_date):
    return release_date.replace("\"", "")


def clean_runtime(runtime):
    return runtime


def clean_studio(studio):
    return studio


def clean_aud_score(aud_score):
    return aud_score


clean_field_fns = {url: clean_url,
                   title: clean_title,
                   score: clean_score,
                   rating: clean_rating,
                   genre: clean_genre,
                   directed: clean_directed,
                   writen: clean_writen,
                   box_office: clean_box_office,
                   release_date: clean_release_date,
                   runtime: clean_runtime,
                   studio: clean_studio,
                   aud_score: clean_aud_score}


def clean_row(row):
    new_row = dict()
    for field in fieldnames:
        # print("field: ", field)
        new_row[field] = clean_field_fns[field](row[field])
        # print("row: ", new_row)
    return new_row


filename = "RottenTomatoesMovieDatabase"
input_file = open(filename + ".raw", "r", encoding='utf-8')
output_file = open("../../data/" + filename + ".csv", "a", encoding='utf-8')
reader = csv.DictReader(input_file, fieldnames=fieldnames)
writer = csv.DictWriter(output_file, fieldnames=fieldnames)

readUrl = []
duplicate_count = 0
for row in reader:
    # print(row)
    url = row['Url']
    if url not in readUrl:
        readUrl.append(url)
        writer.writerow(clean_row(row))
    else:
        duplicate_count = duplicate_count + 1
        print("duplicate row: ", duplicate_count)

    output_file.flush()
