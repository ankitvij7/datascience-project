import csv
from datetime import datetime

input_fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio', 'Audience Score']
output_fieldnames = ['ID', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio']
id_str = "ID"
url_str = "Url"
title_str = "Title"
score_str = "Score"
rating_str = "Rating"
genre_str = "Genre"
directed_str = "Directed By"
written_str = "Written By"
box_office_str = "Box Office"
release_date_str = "Release Date"
runtime_str = "Runtime"
studio_str = "Studio"
aud_score_str = "Audience Score"


# Not Used
def prep_url(url):
    return url


# String
def prep_title(title):
    return title


# String Input: NA , 0-100
def prep_score(score):
    return score


# Comes in the form of: String with Rating(description)
# Ratings in the file:
#   file_ratings = [ Rating, PG-13, PG, NR, R, G, NC17, NA ]
# Invalid Ratings:
#   invalid_ratings = [NR, NC17, NA]
# Valid Ratings
#   valid_ratings = [Rating, PG-13, PG, NOT RATED, R, G, NC-17]
def prep_rating(rating):
    if rating != rating_str:
        ret_rating = rating.split('(', 1)[0].strip()
        if ret_rating == 'NA' or ret_rating == 'NR':
            return 'NOT RATED'
        elif ret_rating == 'NC17':
            return 'NC-17'
        else:
            return ret_rating
    else:
        return rating


def prep_genre(genre):
    return genre


def prep_directed(directed):
    return directed


def prep_written(written):
    return written


def prep_box_office(box_office):
    if box_office == 'NA' or box_office == box_office_str:
        return box_office
    else:
        return int(box_office.replace('$', '').replace(',', ''))


# Input Mon day, year, output year-month-day
def prep_release_date(release_date):
    if release_date == 'NA' or release_date == release_date_str:
        return release_date
    else:
        return f"{datetime.strptime(release_date, '%b %d, %Y'):%Y-%m-%d}"


# input NA, integer minutes, output integer number of minutes
def prep_runtime(runtime):
    if runtime == 'NA' or runtime == runtime_str:
        return runtime
    else:
        return int(runtime.split(' ', 1)[0].strip())


# String
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
                  written_str: prep_written,
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


id_prepend = "B_"
input_filename = "../data/RottenTomatoesMovieDatabase.csv"
output_filename = "../data/B.csv"
input_file = open(input_filename, "r", encoding='utf-8')
output_file = open(output_filename, "a", encoding='utf-8')
reader = csv.DictReader(input_file, fieldnames=input_fieldnames)
writer = csv.DictWriter(output_file, fieldnames=output_fieldnames)

values = []
i = 1
for row in reader:
    preped_row = prep_row(row, (id_prepend + '{:04d}'.format(i)))
    value = preped_row[box_office_str]
    if value not in values:
        values.append(value)

    # print(row)
    # we only have ~3000 entries thus we only need 4 zero padded numbers
    # writer.writerow(prep_row(row, (id_prepend + '{:04d}'.format(i))))
    i = i + 1

print(*values)
output_file.flush()
