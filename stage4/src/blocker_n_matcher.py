import sys
import py_entitymatching as em
import pandas as pd

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
print('Begin blocking stage')
# Display the key attributes of table A and B.
em.get_key(A), em.get_key(B)

# Create attribute equivalence blocker
ab = em.AttrEquivalenceBlocker()
# Block tables using 'year' attribute : same year include in candidate set
C1 = ab.block_tables(A, B, 'Release Date', 'Release Date',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By', 'Studio'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By', 'Studio']
                     )

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

# Attribute Equivalence Blocker for Title
C3 = ab.block_tables(A, B, 'Title', 'Title',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating', 'Directed By', 'Written By',
                                     'Studio']
                     )

# Combine the outputs from attr. equivalence blocker and overlap blocker
# union because if there is an error in the release date, at least the movies should have their names in common
D = em.combine_blocker_outputs_via_union([C1, C2, C3])

# Rule based blocker after D
block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)
rb = em.RuleBasedBlocker()
# print(block_f)
rb.add_rule(['Title_Title_lev_sim(ltuple, rtuple) < 0.4'], block_f)
C = rb.block_candset(D, show_progress=False)
print('Candidate Match set C Size: ', len(C))
print('Finish Blocking stage')

################################## Matcher Portion ##################################
# Open up out labeled data from the last Project.
path_G = '../data/G.csv'
G = em.read_csv_metadata(path_G, key='_id', ltable=A, rtable=B, fk_ltable='ltable_ID', fk_rtable='rtable_ID')
print('Number of tuples in Labeled Training Data G: ' + str(len(G)))

# prepare RF classifier
rf = em.RFMatcher(name='RF', random_state=0)

# need A and B csv files
feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

# generate our feature vectors for our labeled data.
H_total = em.extract_feature_vecs(G, feature_table=feature_table, attrs_after='label', show_progress=False)
H_total.fillna(value=0, inplace=True)

print("Train our Random Forest")
# generate our Random forest classifier
rf.fit(table=H_total, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'], target_attr='label')

# generate our Feature vectors for the full table.
C_FeatureVectors = em.extract_feature_vecs(C, feature_table=feature_table, show_progress=False)
C_FeatureVectors.fillna(value=0, inplace=True)

print("Make our Match using our Random Forest Model.")
# Use the trained random forest to find our ML matches.
predictions_entire = rf.predict(table=C_FeatureVectors, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID'],
                                append=True, target_attr='predicted', inplace=False)

################################## File Output Portion ##################################
print("Build and output our matches")
# Build up our matched set
Matched_Predictions = C[predictions_entire.predicted == 1]

entiredPredictedData = pd.concat(
    [Matched_Predictions.ltable_ID + Matched_Predictions.rtable_ID, Matched_Predictions.ltable_ID,
     Matched_Predictions.ltable_Title, Matched_Predictions.rtable_ID,
     Matched_Predictions.rtable_Title], names=['ID', 'ltable_ID', 'ltable_Title', 'rtable_ID', 'rtable_Title'], axis=1)

# Save out to disk in the intermediate format / Schema we want.
entiredPredictedData.to_csv('../data/PredictedMatchedTuples.csv', index=False)
df = pd.read_csv('../data/PredictedMatchedTuples.csv')
df = df.rename(columns=({'0': 'ID'}))
df.to_csv('../data/PredictedMatchedTuples.csv', index=False)
