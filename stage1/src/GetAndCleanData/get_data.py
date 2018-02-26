import csv
import uuid
from collections import Counter


# function for extracting strings from text
def extract_strings(text):
    # getting the strings of length 1 and writing to csv file
    words = text.split()


    return text

file_name = 'CNN.txt' #should be input from command line

fieldnames = ['id', 'name', 'start_position', 'end_position', 'frequency',
                          'file_name', 'label']

counter = 0
with open(file_name) as f:
    output = csv.DictWriter(open("intermediatefeaturespace.csv", "w", newline=''), fieldnames=fieldnames)
    output.writeheader()
    content = f.read()
    words = content.replace('<person>','<person> ').replace('</>', ' </>').split()
    wordcount = Counter(words)

    previous_word_location = -1
    cumulative_tag_counter = 0
    next_name_flag = 0
    # for line in content.splitlines():
    #     if len(line.strip()) == 0:
    #         print("hi")
    #         continue

    for word in words:  # find each feature for each word
        if word.__contains__("<person>"):
            cumulative_tag_counter += 1
            next_name_flag = 1
            continue
        identifier = uuid.uuid4()
        beg_position = content.find(word, previous_word_location + 1)
        multiplier = cumulative_tag_counter
        if next_name_flag == 1:
            addition_term = cumulative_tag_counter * (8) + 3 * (cumulative_tag_counter - 1)
            label = 1
        else:
            addition_term = cumulative_tag_counter * 11
            label = 0

        true_beg_position = beg_position - addition_term
        true_end_position = true_beg_position + len(word) - 1
        candidate_name = word
        frequency = wordcount[word]
        counter = counter + 1
        output.writerow({'id': identifier,
                         'name': candidate_name,
                         'start_position': true_beg_position,
                         'end_position': true_end_position,
                         'frequency': frequency,
                         'file_name': file_name,
                         'label': label});

        # after writing
        previous_word_location = beg_position
        next_name_flag = 0

print(counter)
print(cumulative_tag_counter)