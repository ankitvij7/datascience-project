import csv


fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre',
              'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime',
              'Studio', 'Audience Score']

filename = "RottenTomatoesMovieDatabase"
input = csv.DictReader(open(filename+".raw", "a"), fieldnames=fieldnames)
output = csv.DictReader(open("../../data"+filename+".cvs", "a"), fieldnames=fieldnames)

for row in input:
    output.writerow(row)

output.flush
