import sys
import py_entitymatching as em
import pandas as pd
import math

# Display the versions
print('python version: ' + sys.version)
print('pandas version: ' + pd.__version__)
print('magellan version: ' + em.__version__)

# Get the paths
path_A = './../data/A.csv'
path_B = './../data/B.csv'
path_Matched = './../data/PredictedMatchedTuples.csv'

# Load csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')
M = em.read_csv_metadata(path_Matched)

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in Matches table: ' + str(len(M)))

print(list(A))
print(list(B))
print(list(M))

# join A with M
A_M = pd.merge(A, M, left_on='ID', right_on='ltable_ID')
# join further with B
merged_df = pd.merge(A_M, B, left_on='rtable_ID', right_on='ID')
print(list(merged_df))


# data merging step
def average_cols(x, y):
    return math.floor((int(x) + int(y)) / 2)


def max_length(x, y):
    if len(str(x)) > len(str(y)):
        return x
    else:
        return y


def add_if_different(x, y):
    x = str(x)
    y = str(y)
    if x != y:
        return x + '; ' + y
    else:
        return x


def retain_if_not_na(x, y):
    x = str(x)
    y = str(y)
    if x != 'NOT RATED':
        return x
    elif y != 'NOT RATED':
        return y
    else:
        return x  # return NOT RATED


# generating the new columns from X(A) and Y(B).
merged_df['Score'] = merged_df.apply(lambda x: average_cols(x['Score_x'], x['Score_y']), axis=1)
merged_df['Directed By'] = merged_df.apply(lambda x: max_length(x['Directed By_x'], x['Directed By_y']), axis=1)
merged_df['Written By'] = merged_df.apply(lambda x: max_length(x['Written By_x'], x['Written By_y']), axis=1)
merged_df['Runtime'] = merged_df.apply(lambda x: min(x['Runtime_x'], x['Runtime_y']), axis=1)
merged_df['Box Office'] = merged_df.apply(lambda x: max(x['Box Office_x'], x['Box Office_y']), axis=1)
merged_df['Genre'] = merged_df.apply(lambda x: add_if_different(x['Genre_x'], x['Genre_y']), axis=1)
merged_df['Studio'] = merged_df.apply(lambda x: add_if_different(x['Studio_x'], x['Studio_y']), axis=1)
merged_df['Rating'] = merged_df.apply(lambda x: retain_if_not_na(x['Rating_x'], x['Rating_y']), axis=1)

# TODO: change ID_x to Ankit's Matches ID
# basic select operation - ID_y is the ID of the matches table
Z = merged_df[['ID_y', 'Title_x', 'Score', 'Rating', 'Genre', 'Directed By', \
               'Written By', 'Box Office', 'Release Date_x', 'Runtime', 'Studio']]
# rename to match the required schema
E = Z.rename(columns={'ID_y': 'ID', 'Title_x': 'Title', 'Release Date_x': 'Release Date'})
print(list(Z))
print(list(E))

print(E.head(3))

path_E = './../data/E.csv'
E.to_csv(path_E, index=False)
