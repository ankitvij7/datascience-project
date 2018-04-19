import sys
import py_entitymatching as em
import pandas as pd
import os

# Display the versions
print('python version: ' + sys.version)
print('pandas version: ' + pd.__version__)
print('magellan version: ' + em.__version__)

# Get the paths
path_A = '../data/A.csv'
path_B = '../data/B.csv'

# Load csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A) * len(B)))

# Display the key attributes of table A and B.
em.get_key(A), em.get_key(B)

# Create attribute equivalence blocker
ab = em.AttrEquivalenceBlocker()
# Block tables using 'year' attribute : same year include in candidate set
C1 = ab.block_tables(A, B, 'Release Date', 'Release Date',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By', 'Studio'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By', 'Studio']
                     )
print("C1", len(C1))

#  Initializeoverlap blocker
ob = em.OverlapBlocker()
# Block over title attribute
# overlap_size |rem_stop_words | ! rem_stop_words
# -------------|---------------|-----------------
#       1      |    103202     |    865894
#       2      |      1826     |     42140
#       3      |       260     |      1235
C2 = ob.block_tables(A, B, 'Title', 'Title', show_progress=False, overlap_size=2, rem_stop_words=True,
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio']
                     )
print("C2", len(C2))

# Attribute Equivalence Blocker for Title
C3 = ab.block_tables(A, B, 'Title', 'Title',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio']
                     )
print("C3", len(C3))

# Combine the outputs from attr. equivalence blocker and overlap blocker
# union because if there is an error in the release date, at least the movies should have their names in common
D = em.combine_blocker_outputs_via_union([C1, C2, C3])
print("D Set Size: ", len(D))

# Rule based blocker after D
block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)
rb = em.RuleBasedBlocker()
# print(block_f)
rb.add_rule(['Title_Title_lev_sim(ltuple, rtuple) < 0.4'], block_f)
C = rb.block_candset(D, show_progress=False)
print("C Set Size: ", len(C))


# debug blocker
E = em.debug_blocker(C, A, B, output_size=200)
E.head()
# print(len(E))
S = em.sample_table(C, 300)
# S.to_csv('S.csv')

# G = em.label_table(S, 'label')

def f(row):
    if str(row['ltable_Title']).lower() == str(row['rtable_Title']).lower():
        val = 1
    else:
        val = 0
    return val

G = S.copy()
G['label'] = S.apply(f, axis=1)

G.to_csv('../data/G.csv')
# print(G.loc[G['label'] == 1])




