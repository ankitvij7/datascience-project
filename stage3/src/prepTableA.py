import csv

input_fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio']
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


# Not Used
def prep_url(url):
    return url


# String
def prep_title(title):
    return title


# Range Input = NA or [0.0, 10.0] map to NA or [0-100]
def prep_score(score):
    if score == 'NA' or score == score_str:
        return score
    else:
        return int(float(score) * 10)


# Ratings in the file:
#   file_ratings = [Rating, NO RATED, PG - 13, TV - MA, TV - 14, TV - PG, R, NOT RATED, PG, TV - Y7, G, TV - Y7 - FV, TV - G, NC - 17, TV - Y, APPROVED, UNRATED, PASSED]
# Invalid Ratings:
#   invalid_ratings = [NO RATED, APPROVED, UNRATED, PASSED]
# Valid Ratings
#   valid_ratings = [PG-13, TV-MA, TV-14, TV-PG, R, NOT RATED, PG, TV-Y7, G, TV-Y7-FV, TV-G, NC-17, TV-Y]
def prep_rating(rating):
    ret_rating = rating
    if rating == 'NO RATED' or rating == 'APPROVED' or rating == 'UNRATED' or rating == 'PASSED':
        ret_rating = 'NOT RATED'
    return ret_rating


# Genres in the file:
#   file_genres = [ Genre, Action, Adventure, Fantasy, Sci-Fi, Crime, Drama, Comedy, Mystery, Thriller, History, Music, Horror, Animation, Romance,
#                   Biography, Family, Musical, War, Short, Documentary, Western, Sport, Reality-TV, News, Talk-Show, Film-Noir, Game-Show ]
# Ignore entries  = [Genre, NA]
# Valid set = [ Drama, Animation, Comedy, Horror, Documentary, Western, Romance, Television, Family, Film-Noir, Sport, Musical, Action, Adventure, Sci-Fi, Fantasy, Mystery, Thriller, Classics ]
# MAP for A->Valid
#   Game-Show -> Television
#   Talk-Show -> Television
#   Reality-TV -> Television
#   News -> Television
#   History -> Documentary
#   Biography -> Documentary
#   War -> Documentary
#   Music -> Musical
#   Short -> ""
#   Crime -> ""
genre_map_to_TV = ['Game-Show', 'Talk-Show', 'Reality-TV', 'News']
genre_map_to_DOC = ['History', 'Biography', 'War']
genre_map_to_EMPTY = ['Short', 'Crime']


def prep_genre(genre):
    if genre == 'NA' or genre == genre_str:
        return genre
    else:
        # Now Let's do some work.
        genres = genre.split(';')
        ret_genre = set()
        for g in genres:
            if g in genre_map_to_TV:
                ret_genre.add('Television')
            elif g in genre_map_to_DOC:
                ret_genre.add('Documentary')
            elif g == 'Music':
                ret_genre.add('Musical')
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

# Input $num,ber; output integer
def prep_box_office(box_office):
    if box_office == 'NA' or box_office == box_office_str:
        return box_office
    else:
        return int(box_office.replace('$', '').replace(',', ''))


# Input Year-Month-Year
def prep_release_date(release_date):
    return release_date


# Input NA or PT156M;  output number of minutes
def prep_runtime(runtime):
    if runtime == 'NA' or runtime == runtime_str:
        return runtime
    else:
        return int(runtime[2:].split('M', 1)[0])


# Strings ; separated
def prep_studio(studio):
    return prep_sep_and_sort(studio, studio_str)


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
                  studio_str: prep_studio}
remove_fields = {url_str}


def prep_row(input_row, id_val):
    new_row = dict()
    new_row[id_str] = id_val
    #print("ID: ", id_val)
    for field in input_fieldnames:
        if field not in remove_fields:
            # print("field: ", field)
            new_row[field] = prep_field_fns[field](input_row[field])
            # print("row: ", new_row)
    return new_row


id_prepend = "A_"
input_filename = "../data/ImdbMovieDatabase.csv"
output_filename = "../data/A.csv"
input_file = open(input_filename, "r", encoding='ansi')
output_file = open(output_filename, "a")
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
