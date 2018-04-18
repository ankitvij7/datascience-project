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

print(A.head(2))

print(B.head(2))

# Display the key attributes of table A and B.
em.get_key(A), em.get_key(B)

# Blocking plan

# A, B -- AttrEquivalence blocker [release date] -----------|
#                                                           |---> candidate set C--> Score proximity rule based blocker --> D
# A, B -- Overlap blocker [title]---------------------------|

# Create attribute equivalence blocker
ab = em.AttrEquivalenceBlocker()
# Block tables using 'year' attribute : same year include in candidate set
C1 = ab.block_tables(A, B, 'Release Date', 'Release Date',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating']
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
C2 = ob.block_tables(A, B, 'Title', 'Title', show_progress=False, overlap_size=2, rem_stop_words=True)
# C2 = ob.block_tables(A, B, 'Title')
#print(C2)
print("C2", len(C2))

# Combine the outputs from attr. equivalence blocker and overlap blocker
# union because if there is an error in the release date, at least the movies should have their names in common
C = em.combine_blocker_outputs_via_union([C1, C2])
print("C", len(C))

# debug 1
E = em.debug_blocker(C2, A, B, attr_corres=[('Title','Title')])
print(len(E))

# Rule based blocker on score after C
block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)
# print(block_f)
rb = em.RuleBasedBlocker()
rb.add_rule(['Score_Score_anm(ltuple, rtuple) > 0.90'], block_f)

D = rb.block_candset(C, show_progress=False)
D.head()
print(len(D))

S = em.sample_table(D, 300)
# S.to_csv('S.csv')

def f(row):
    if str(row['ltable_Title']).lower() == str(row['rtable_Title']).lower():
        val = 1
    else:
        val = 0
    return val

G = S.copy()
G['label'] = S.apply(f, axis=1)
G = G.drop(columns=['rtable_Release Date', 'ltable_Release Date'])
G.to_csv('G.csv')
# print(G.head(10))
print(G.loc[G['label'] == 1])
# A_title = A[['Title']]
# B_title = B[['Title']]
# i = 0
# for index, row in S.iterrows():
#     if row['ltable_Title'] == row2['rtable_Title']:
#
#             i += 1
# print(i)
#
# print(S.head(7))
# G = em.label_table(S, 'gold')

# debug 2
E = em.debug_blocker(D, A, B, attr_corres=[('Title','Title')])
# print(E.head(20))
print(len(E))

# exact matches
# print(block_f)
#
# A_title = A[['Title']]
# B_title = B[['Title']]
#


# i = 0
# for index, row in A_title.iterrows():
#     for index2, row2 in B_title.iterrows():
#         if row['Title'] == row2['Title']:
#             i += 1
# print(i)
#
# rb2 = em.RuleBasedBlocker()
# rb2.add_rule(['Title_Title_jac_qgm_3_qgm_3(ltuple, rtuple) > 0.90'], block_f)
# Exact_Matches = rb2.block_tables(A, B, l_output_attrs=['Title'], r_output_attrs=['Title'])
# print(Exact_Matches.head(2))
# print(len(Exact_Matches))

