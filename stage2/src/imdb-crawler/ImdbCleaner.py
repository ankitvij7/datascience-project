import csv

#TODO: this must be changed to the correct one.
fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio', 'Audience Score']

filename = "ImdbMovieDatabase"
input_file = open(filename + ".raw", "r", encoding='utf-8')
output_file = open("../../data/" + filename + ".csv", "a")
reader = csv.DictReader(input_file, fieldnames=fieldnames)
writer = csv.DictWriter(output_file, fieldnames=fieldnames)

for row in reader:
    print(row)
    writer.writerow(row)
    output_file.flush()
