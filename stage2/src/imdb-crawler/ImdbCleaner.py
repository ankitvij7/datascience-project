import csv

#TODO: this must be changed to the correct one.
fieldnames = ['Url', 'Title', 'Score', 'Rating', 'Genre', 'Directed By', 'Written By', 'Box Office', 'Release Date', 'Runtime', 'Studio', 'Audience Score']

filename = "ImdbMovieDatabase"
input_file = open(filename + ".raw", "r", encoding='utf-8')
output_file = open("../../data/" + filename + ".csv", "a")
reader = csv.DictReader(input_file, fieldnames=fieldnames)
writer = csv.DictWriter(output_file, fieldnames=fieldnames)

readUrl = []
duplicate_count = 0
for row in reader:
    # print(row)
    url = row['Url']
    if url not in readUrl:
        readUrl.append(url)
        writer.writerow(row)
    else:
        duplicate_count = duplicate_count + 1
        print("duplicate row: ", duplicate_count)

    output_file.flush()

