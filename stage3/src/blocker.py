import sys
import py_entitymatching as em
import pandas as pd
import os

# Display the versions
print('python version: ' + sys.version )
print('pandas version: ' + pd.__version__ )
print('magellan version: ' + em.__version__ )

# Get the paths
path_A = '../data/A.csv'
path_B = '../data/B.csv'

# Load csv files as dataframes and set the key attribute in the dataframe
A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')

print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in A X B (i.e the cartesian product): ' + str(len(A)*len(B)))

print(A.head(2))

print(B.head(2))

# Display the key attributes of table A and B.
em.get_key(A), em.get_key(B)

# Blocking plan

# A, B -- AttrEquivalence blocker [release date] --------------------|
#                                                           |---> candidate set C--> Score proximity rule based blocker --> D
# A, B -- Overlap blocker [title]---------------------------|

# Create attribute equivalence blocker
ab = em.AttrEquivalenceBlocker()
# Block tables using 'year' attribute : same year include in candidate set
C1 = ab.block_tables(A, B, 'Release Date', 'Release Date',
                     l_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating'],
                     r_output_attrs=['Title', 'Genre', 'Score', 'Release Date', 'Rating']
                    )


# Initialize overlap blocker
ob = em.OverlapBlocker()
# Block over title attribute
C2 = ob.block_tables(A, B, 'Title', 'Title', show_progress=False, overlap_size=2)
print(len(C2))


# Combine the outputs from attr. equivalence blocker and overlap blocker
#union becuase if there is an error in the release date, at least the movies should have their names in common
C = em.combine_blocker_outputs_via_union([C1, C2])
print(len(C))

# Rule based blocker on score after C
block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)
print(block_f)
rb = em.RuleBasedBlocker()
rb.add_rule(['Score_Score_anm(ltuple, rtuple) > 0.90'], block_f)

D = rb.block_candset(C, show_progress=False)
D.head()
print(len(D))
