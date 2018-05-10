import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/E.csv')

# populate maps
genres_map_box_office = {}
genres_map_count = {}
directors_map_score = {}
directors_map_count = {}
rating_map_viewed = {}
rating_map_count = {}
writer_map_length = {}
writer_map_count = {}
studio_map_earnings = {}
studio_map_count = {}
for index, row in df.iterrows():
    current_genres = str(row['Genre']).split(';')
    for genre in current_genres:
        genres_map_box_office[genre] = 0
        genres_map_count[genre] = 0

    director = row['Directed By']
    directors_map_score[director] = 0
    directors_map_count[director] = 0

    rating = row['Rating']
    rating_map_viewed[rating] = 0
    rating_map_count[rating] = 0

    writer = row['Written By']
    writer_map_length[writer] = 0
    writer_map_count[writer] = 0

    current_studios = row['Studio']
    if type(current_studios) is not float:
        current_studios = current_studios.split(';')
        for studio in current_studios:
            studio_map_earnings[studio] = 0
            studio_map_count[studio] = 0


for index, row in df.iterrows():
    current_genres = str(row['Genre']).split(';')
    box_office = row['Box Office']
    for genre in current_genres:
        genres_map_box_office[genre] = genres_map_box_office[genre] + box_office
        genres_map_count[genre] = genres_map_count[genre] + 1

    director = row['Directed By']
    score = row['Score']
    directors_map_score[director] = directors_map_score[director] + score
    directors_map_count[director] = directors_map_count[director] + 1

    rating = row['Rating']
    rating_map_viewed[rating] = rating_map_viewed[rating] + box_office
    rating_map_count[rating] = rating_map_count[rating] + 1

    writer = row['Written By']
    runtime = row['Runtime']
    writer_map_length[writer] = writer_map_length[writer] + runtime
    writer_map_count[writer] = writer_map_count[writer] + 1

    current_studios = row['Studio']
    if type(current_studios) is not float:
        current_studios = current_studios.split(';')
        for studio in current_studios:
            studio_map_earnings[studio] = studio_map_earnings[studio] + box_office
            studio_map_count[studio] = studio_map_count[studio] + 1


# Popular genres with the average box office earnings above 70000000
removal_list_genre = []
for genre in genres_map_box_office:
    genres_map_box_office[genre] = genres_map_box_office[genre]/genres_map_count[genre]
    if genres_map_box_office[genre] < 70000000:
        removal_list_genre.append(genre)

for genre in removal_list_genre:
    del genres_map_box_office[genre]

print(genres_map_box_office)
plt.bar(genres_map_box_office.keys(), genres_map_box_office.values(), align='center')
plt.ylabel('Average Box Office Earnings')
plt.xlabel('Genres')
plt.show()

# which rating is most viewed
for rating in rating_map_viewed:
    rating_map_viewed[rating] = rating_map_viewed[rating]/rating_map_count[rating]

del rating_map_viewed['NOT RATED']

print(rating_map_viewed)

plt.bar(rating_map_viewed.keys(), rating_map_viewed.values(), align='center')
plt.ylabel('Average Box Office Earnings')
plt.xlabel('Ratings')
plt.show()

# which writer write long scripts ( 3 hour+ movies)
removal_list_writer = []
for writer in writer_map_length:
    writer_map_length[writer] = writer_map_length[writer]/writer_map_count[writer]
    if writer_map_length[writer] < 190:
        removal_list_writer.append(writer)

for writer in removal_list_writer:
    del writer_map_length[writer]

print(writer_map_length)

plt.bar(writer_map_length.keys(), writer_map_length.values(), align='center')
plt.ylabel('Average Run time')
plt.xlabel('Writers')
plt.show()

# most profitable studios per movie (> 33 million earnings)
removal_list_studio = []
for studio in studio_map_earnings:
    studio_map_earnings[studio] = studio_map_earnings[studio]/studio_map_count[studio]
    if studio_map_earnings[studio] < 330000000:
        removal_list_studio.append(studio)

for studio in removal_list_studio:
    del studio_map_earnings[studio]

print(studio_map_earnings)
plt.bar(studio_map_earnings.keys(), studio_map_earnings.values(), align='center')
plt.ylabel('Average Box Office Earnings per movie')
plt.xlabel('Studios')
plt.show()