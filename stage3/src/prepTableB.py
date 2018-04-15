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


# Genres in the file:
#   file_genres = [ Genre, NA, Action & Adventure, Drama, Science Fiction & Fantasy, Animation, Comedy, Kids & Family,
#                   Mystery & Suspense, Art House & International, Romance, Documentary, Horror, Special Interest, Western, Musical & Performing Arts, Anime & Manga,
#                   Sports & Fitness, Gay & Lesbian, Television, Classics, Cult Movies, Faith & Spirituality
# Ignore entries  = [Genre, NA]
# Valid set = [ Drama, Animation, Comedy, Horror, Documentary, Western, Romance, Television, Family, Film-Noir, Sport, Musical, Action, Adventure, Sci-Fi, Fantasy, Mystery, Thriller, Classics ]
# MAP for B->Valid
#   Anime & Manga -> Animation
#   Kids & Family -> Family
#   Art House & International -> Film-Noir
#   Sports & Fitness -> Sport
#   Musical & Performing Arts -> Musical
#   Action & Adventure -> Action;Adventure
#   Science Fiction & Fantasy -> Sci-Fi;Fantasy
#   Mystery & Suspense -> Mystery;Thriller
#   Special Interest -> ""
#   Gay & Lesbian -> ""
#   Cult Movies -> ""
#   Faith & Spirituality -> ""
genre_map_121 = {'Anime & Manga': 'Animation',
                 'Kids & Family': 'Family',
                 'Art House & International': 'Film-Noir',
                 'Sports & Fitness': 'Sport',
                 'Musical & Performing Arts': 'Musical'
                 }
genre_map_122 = {'Action & Adventure': {'Action', 'Adventure'},
                 'Science Fiction & Fantasy': {'Sci-Fi', 'Fantasy'},
                 'Mystery & Suspense': {'Mystery', 'Thriller'}
                 }
genre_map_to_EMPTY = ['Special Interest', 'Gay & Lesbian', 'Cult Movies', 'Faith & Spirituality']


def prep_genre(genre):
    if genre == 'NA' or genre == genre_str:
        return genre
    else:
        # Now Let's do some work.
        genres = genre.split(';')
        ret_genre = set()
        for g in genres:
            if g in genre_map_121:
                ret_genre.add(genre_map_121[g])
            elif g in genre_map_122:
                ret_genre = ret_genre | genre_map_122[g]
            elif g in genre_map_to_EMPTY:
                pass
            else:
                ret_genre.add(g)
        if len(ret_genre) == 0:
            return 'NA'
        else:
            return ';'.join(str(s) for s in ret_genre)


# String of ; separated authors.
def prep_directed(directed):
    return prep_sep_and_sort(directed, directed_str)


# String of ; separated authors.
def prep_written(written):
    return prep_sep_and_sort(written, written_str)


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


# Strings ; separated
def prep_studio(studio):
    return prep_sep_and_sort(studio, studio_str)


def clean_aud_score(aud_score):
    return aud_score


# Strings ; separated library.
def prep_sep_and_sort(sep_string, comp_str):
    if sep_string == 'NA' or sep_string == comp_str:
        return sep_string
    else:
        if not sep_string:
            return 'NA'
        else:
            sep_strings = sep_string.split(';')
            sep_strings.sort()
            return ';'.join(str(s) for s in sep_strings)


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

# # !!!DEBUG CODE!!!
# values = []

i = 0
for row in reader:
    # print(row)
    # we only have ~3000 entries thus we only need 4 zero padded numbers
    if i == 0:
        writer.writerow(prep_row(row, id_str))
    else:
        writer.writerow(prep_row(row, (id_prepend + '{:04d}'.format(i))))

    # # !!!DEBUG CODE!!!
    # preped_row = prep_row(row, (id_prepend + '{:04d}'.format(i)))
    # value = preped_row[directed_str]
    # # Single Value fields
    # # if value not in values:
    # #     values.append(value)
    #
    # # Multiple ";" separated fields
    # value_array = value.split(';')
    # for v in value_array:
    #     if v not in values:
    #         values.append(v)

    i = i + 1
    # end the lop.

# # !!!DEBUG CODE!!!
# print(*values)
output_file.flush()
