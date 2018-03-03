import csv
import uuid
import re
from collections import Counter
import os

fieldnames = ['id', 'name', 'start_position', 'end_position', 'frequency',
              'file_name', 'label']

list_stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an",
                   "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below",
                   "between",
                   "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does",
                   "doesn't",
                   "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
                   "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
                   "hers",
                   "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
                   "into",
                   "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
                   "myself",
                   "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
                   "ourselves",
                   "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
                   "so",
                   "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
                   "there",
                   "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through",
                   "to",
                   "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
                   "were",
                   "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
                   "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
                   "you've",
                   "your", "yours", "yourself", "yourselves"]

output = csv.DictWriter(open("intermediatefeaturespace.csv", "w", newline=''), fieldnames=fieldnames)
output.writeheader()

total_words_read_all_files = 0
total_words_written_all_files = 0
total_words_written_with_labels_1_all_files = 0
file_counter = 0

dir1 = "C:\\Users\\user\\Desktop\\datascience-project\\stage1\\data\\J\\"
for fn in os.listdir(dir1):
    file_name = dir1 + fn
    file_counter += 1
    # print(file_name)
    counter = 0
    total_counter = 0
    written_to_csv = 0
    with open(file_name) as f:

        content = f.read()
        words = content.replace('<person>', ' <person> ').replace('</>', ' </> ').split()

        previous_end_location = -1
        cumulative_tag_counter = 0
        next_name_flag = 0
        counts = dict()
        # for line in content.splitlines():
        #     if len(line.strip()) == 0:
        #         print("hi")
        #         continue

        # a = 'abcdefg'
        # b = [a[i:i + 3] for i in xrange(len(a) - 2)]
        # print
        # b
        # ['abc', 'bcd', 'cde', 'def', 'efg']
        # first pass to get frequencies
        windowSize = 1
        while windowSize <= 7:
            for i in range(len(words) - windowSize):
                subsentence = (" ".join(map(str, words[i:i + windowSize])))
                subsentence = subsentence.strip()
                if subsentence in counts:
                    counts[subsentence] += 1
                else:
                    counts[subsentence] = 1
            windowSize += 1

        list_candidate_names = []
        windowSize = 1
        while windowSize <= 7:
            for i in range(len(words) - windowSize):
                # print(words[i:i + windowSize])
                subsentence = (" ".join(map(str, words[i:i + windowSize])))
                subsentence = subsentence.strip()
                dont_process_flag = 0
                for j in range(i + 1, i + windowSize):
                    if words[j] == "<person>" or words[j] == "</>":
                        dont_process_flag = 1
                if words[i] == "<person>" and words[i + windowSize] == "</>" and dont_process_flag == 0:
                    candidate_name = subsentence.replace('<person>', '').replace('</>', '').strip()
                    list_candidate_names.append(candidate_name)
                    # label = 1
            windowSize += 1
        print(file_name)
        print(list_candidate_names)

        windowSize = 1
        while windowSize <= 7:
            cumulative_tag_counter = 0
            previous_beg_location = -1
            m = 0
            n = 0
            for i in range(len(words) - windowSize):
                # print(words[i:i + windowSize])
                subsentence = (" ".join(map(str, words[i:i + windowSize])))
                subsentence = subsentence.strip()
                if words[i] == "<person>":
                    m += 1
                if words[i] == "</>":
                    n += 1
                beg_position = content.find(words[i], previous_beg_location + 1)
                true_beg_position = beg_position - (8 * m + 3 * n)
                # if the subsentence anywhere contains a <> in between it, it'll go off anyways
                # so don't care about it;s beg and end position
                true_end_position = true_beg_position + len(subsentence) - 1
                candidate_name = subsentence
                candidate_name = candidate_name.strip()
                label = 0
                identifier = uuid.uuid4()

                frequency = counts[subsentence]

                if candidate_name in list_candidate_names:
                    continue
                # label assignment
                # if the sentence contains <> , it'll go off, don't care about it's label
                # special case - do everything again

                dont_process_flag = 0
                for j in range(i+1, i+windowSize):
                    if words[j] == "<person>" or words[j] == "</>":
                        dont_process_flag = 1
                if words[i] == "<person>" and words[i + windowSize] == "</>" and dont_process_flag == 0:
                    true_beg_position = true_beg_position + 8  # this <person> tag length shouldn't be subtracted, so doing a refund
                    # subsentence_new = (" ".join(map(str, words[i+1:i + windowSize-1])))
                    # if subsentence_new.__contains__('<person>') or subsentence_new.__contains__('</>'):
                    #     dont_process_flag = 1
                    candidate_name = subsentence.replace('<person>', '').replace('</>', '').strip()
                    true_end_position = true_beg_position + len(candidate_name) - 1
                    label = 1
                    counter += 1

                flag_stop_word = 0  # doesn't contain a stop word
                for j in range(i, i + windowSize):
                    if words[j].lower() in list_stop_words:
                        flag_stop_word = 1
                        break

                total_counter += 1

                searchObj = re.search(r'[^a-z\sA-Z\.]', candidate_name, re.M)
                # [!@#\$%\^&\*\(\)\[\]:;\',-]
                # print(len(candidate_name.split()))
                # if dont_process_flag == 1:
                #     pass
                if searchObj:
                    pass
                elif flag_stop_word == 1:
                    pass
                elif len(candidate_name.split()) > 5:
                    pass
                else:
                    written_to_csv += 1
                    if file_name == "C:\\Users\\user\\Desktop\\datascience-project\\stage1\\data\\I\\NPR-02-20-2018-More.txt":
                        if label == 1:
                            print(candidate_name)
                    output.writerow({'id': identifier,
                                     'name': candidate_name,
                                     'start_position': true_beg_position,
                                     'end_position': true_end_position,
                                     'frequency': frequency,
                                     'file_name': fn,
                                     'label': label});

                previous_beg_location = beg_position
            windowSize += 1

    print(total_counter)
    print(written_to_csv)
    print(file_name , ":  contains: ", counter)
    total_words_read_all_files += total_counter
    total_words_written_all_files += written_to_csv
    total_words_written_with_labels_1_all_files += counter

print(total_words_read_all_files)
print(total_words_written_all_files)
print(total_words_written_with_labels_1_all_files)
print(file_counter)