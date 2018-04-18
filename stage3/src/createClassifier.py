import py_entitymatching as em
import os

# read A and B
path_A = '../data/A.csv'
path_B = '../data/B.csv'
A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')
# read G
path_G = '../data/G.csv'
G = em.read_csv_metadata(path_G,
                         key='_id',
                         ltable=A, rtable=B,
                         fk_ltable='ltable_ID', fk_rtable='rtable_ID')
print('Number of tuples in A: ' + str(len(A)))
print('Number of tuples in B: ' + str(len(B)))
print('Number of tuples in G: ' + str(len(G)))


# create I and J sets
IJ = em.split_train_test(G, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']

# prepare classifiers
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')

# need A and B csv files
feature_table = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)

H = em.extract_feature_vecs(I,
                            feature_table=feature_table,
                            attrs_after='label',
                            show_progress=False)

# select best matcher
# precision
result = em.select_matcher([dt, rf, svm, ln, lg], table=H,
                           exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
                           k=5,
                           target_attr='label', metric_to_select_matcher='precision', random_state=0)
print(result['cv_stats'])

# recall
result = em.select_matcher([dt, rf, svm, ln, lg], table=H,
                           exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
                           k=5,
                           target_attr='label', metric_to_select_matcher='recall', random_state=0)
print(result['cv_stats'])

L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='label', show_progress=False)

# select the best classifier using the above precision and recall results - for now choosing random forest
rf.fit(table=H,
       exclude_attrs=['_id', 'ltable_v', 'rtable_ID', 'label'],
       target_attr='label')

predictions = rf.predict(table=L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID', 'label'],
                         append=True, target_attr='predicted', inplace=False)

eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)

I.to_csv(os.fdopen(os.open("I.csv", os.O_RDWR | os.O_CREAT), 'w+'), index=False)
J.to_csv(os.fdopen(os.open("J.csv", os.O_RDWR | os.O_CREAT), 'w+'), index=False)
