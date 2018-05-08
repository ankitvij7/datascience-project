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

################################## Blocker Portion ##################################
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

################################## Matcher Portion ##################################

path_G = '../data/G.csv'
G = em.read_csv_metadata(path_G, key='_id', ltable=A, rtable=B, fk_ltable='ltable_ID', fk_rtable='rtable_ID')
print('Number of tuples in G: ' + str(len(G)))

# prepare RF classifier
rf = em.RFMatcher(name='RF', random_state=0)

# need A and B csv files
feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=True)

print(feature_table.feature_name)

H_total = em.extract_feature_vecs(G, feature_table=feature_table, attrs_after='label', show_progress=False)
H_total.fillna(value=0, inplace=True)

# generate our Random forest classifier

rf.fit(table=H_total, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')

predictions = rf.predict(table=C, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'], append=True, target_attr='predicted', inplace=False)
print(predictions)

# eval_result = em.eval_matches(predictions, 'label', 'predicted')
# print('\n Random Forest Result-')
# em.print_eval_summary(eval_result)

# # create I and J sets
# IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
# I = IJ['train']
# J = IJ['test']
#
# # prepare RF classifier
# rf = em.RFMatcher(name='RF', random_state=0)
#
# # need A and B csv files
# feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=True)
#
# print(feature_table.feature_name)
#
# H = em.extract_feature_vecs(I,
#                             feature_table=feature_table,
#                             attrs_after='label',
#                             show_progress=False)
# H.fillna(value=0, inplace=True)
#
# L = em.extract_feature_vecs(J, feature_table=feature_table,
#                             attrs_after='label', show_progress=False)
# L.fillna(value=0, inplace=True)
#
# # generate our Random forest classifier
#
# rf.fit(table=H,
#        exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
#        target_attr='label')
#
# predictions = rf.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
#                          append=True, target_attr='predicted', inplace=False)
#
# eval_result = em.eval_matches(predictions, 'label', 'predicted')
# print('\n Random Forest Result-')
# em.print_eval_summary(eval_result)
