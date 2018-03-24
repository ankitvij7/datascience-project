import csv

with open("RottenTomatoesMovieDatabase.raw", "r", encoding='utf-8') as rt_db_file:
    rotten_tomatoes_db = csv.DictReader(rt_db_file)
    fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre',
                  'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime',
                  'Studio', 'Audience Score']

    output = csv.DictWriter(open("RottenTomatoesMovieDatabase.csv", "w", encoding='utf-8'), fieldnames=fieldnames)
    output.writeheader()

    for row in rotten_tomatoes_db:
        movie_title_cleaned = row['Title'].replace("2018", "").replace("2017", ""). \
            replace("2016", "").replace("2015", "").replace("2014", "").replace("2013", "").replace("2012", "").\
            replace("()", "").strip(' \t\n\r')
        release_date = row['Release Date'].replace("\"", "")
        output.writerow({'Url': row['Url'],
                         'Title': movie_title_cleaned,
                         'Score': row['Score'],
                         'Rating': row['Rating'],
                         'Genre': row['Genre'],
                         'Directed By': row['Directed By'],
                         'Written By': row['Written By'],
                         'Box Office': row['Box Office'],
                         'Release Date': release_date,
                         'Runtime': row['Runtime'],
                         'Studio': row['Studio'],
                         'Audience Score': row['Audience Score']})
