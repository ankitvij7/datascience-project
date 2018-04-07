import csv

input_fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio', 'Audience Score']
output_fieldnames = ['ID', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio']
id_str = "ID"
url_str = "Url"
title_str = "Title"
score_str = "Score"
rating_str = "Rating"
genre_str = "Genre"
directed_str = "Directed By"
writen_str = "Written By"
box_office_str = "Box Office"
release_date_str = "Release Date"
runtime_str = "Runtime"
studio_str = "Studio"
aud_score_str = "Audience Score"


def prep_url(url):
    return url


def prep_title(title):
    return title


def prep_score(score):
    return score


def prep_rating(rating):
    return rating


def prep_genre(genre):
    return genre


def prep_directed(directed):
    return directed


def prep_writen(writen):
    return writen


def prep_box_office(box_office):
    return box_office


def prep_release_date(release_date):
    return release_date


def prep_runtime(runtime):
    return runtime


def prep_studio(studio):
    return studio


def clean_aud_score(aud_score):
    return aud_score


prep_field_fns = {url_str: prep_url,
                  title_str: prep_title,
                  score_str: prep_score,
                  rating_str: prep_rating,
                  genre_str: prep_genre,
                  directed_str: prep_directed,
                  writen_str: prep_writen,
                  box_office_str: prep_box_office,
                  release_date_str: prep_release_date,
                  runtime_str: prep_runtime,
                  studio_str: prep_studio,
                  aud_score_str: clean_aud_score}
remove_fields = {url_str, aud_score_str}


def prep_row(input_row, id_val):
    new_row = dict()
    new_row[id_str] = id_val
    # print("ID: ", id_val)
    for field in input_fieldnames:
        if field not in remove_fields:
            # print("field: ", field)
            new_row[field] = prep_field_fns[field](input_row[field])
            # print("row: ", new_row)
    return new_row


id_prepend = "B"
input_filename = "../data/RottenTomatoesMovieDatabase.csv"
output_filename = "../data/B.csv"
input_file = open(input_filename, "r", encoding='utf-8')
output_file = open(output_filename, "a", encoding='utf-8')
reader = csv.DictReader(input_file, fieldnames=input_fieldnames)
writer = csv.DictWriter(output_file, fieldnames=output_fieldnames)

i = 1
for row in reader:
    # print(row)
    # we only have ~3000 entries thus we only need 4 zero padded numbers
    writer.writerow(prep_row(row, (id_prepend + '{:04d}'.format(i))))
    i = i + 1

output_file.flush()
