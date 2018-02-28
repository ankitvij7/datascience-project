import sys
# Let's bring in our parser!
import numpy
# We must implement CV with the following classifiers:  decision tree, random forest, support vector machine, linear regression, and logistic regression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
# We must measure Recall, Precision & F1
from sklearn import metrics

dt = "Decision Tree"


# Fitted getClassifier Function for a Decision Tree Classifier
def get_decision_tree_classifier(features, labels):
    # TODO: Found in an example, prune later.
    # return DecisionTreeClassifier(criterion="entropy", class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    return DecisionTreeClassifier().fit(features, labels)


# Decision Tree Classifier doesn't do any post processing
def get_decision_tree_prediction_processing(predictions):
    return predictions


rf = "Random Forest"


# Fitted getClassifier Function for a Random Forest Classifier
def get_random_rorest_classifer(features, labels):
    # TODO: Found in an example, prune later.
    # return RandomForestClassifier(criterion="entropy", class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    return RandomForestClassifier().fit(features, labels)


# Random Forest Classifier doesn't do any post processing
def get_random_rorest_prediction_processing(predictions):
    return predictions


svm = "Support Vector Machine"


# Fitted getClassifier Function for a Support Vector Machine Classifier
def get_support_vector_machine_classifer(features, labels):
    # TODO: Found in an example, prune later.
    # return SVC(class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    # return SVC(C=100.0).fit(features, labels)
    # return SVC(kernel='linear').fit(features, labels)
    return SVC().fit(features, labels)


# Support Vector Machine Classifier doesn't do any post processing
def get_support_vector_machine_prediction_processing(predictions):
    return predictions


linr = "Linear Regression"
linrThreshold = 0.5


# Fitted getClassifier Function for a Linear Regression Classifier
def get_linear_regression_classifier(features, labels):
    return LinearRegression().fit(features, labels)


# Linear Regression Classifier outputs are a bit different need to be modified
def get_linear_regression_prediction_processing(predictions):
    return [1 if prediction > linrThreshold else 0 for prediction in predictions]


logr = "Logistic Regression"


# Fitted getClassifier Function for a Logistic Regression Classifier
def get_logistic_regression_classifier(features, labels):
    # TODO: Found in an example, prune later.
    # return LogisticRegression(C=100000).fit(features, labels)
    return LogisticRegression().fit(features, labels)


# Logistic Regression Classifier doesn't do any post processing
def get_logistic_regression_prediction_processing(predictions):
    return predictions


# Tools for looping through all the different Classifiers via Function pointers.
classifier_names = [dt, rf, svm, linr, logr]
classifier_functions = {dt: get_decision_tree_classifier,
                        rf: get_random_rorest_classifer,
                        svm: get_support_vector_machine_classifer,
                        linr: get_linear_regression_classifier,
                        logr: get_logistic_regression_classifier}
prediction_processing_function = {dt: get_decision_tree_prediction_processing,
                                  rf: get_random_rorest_prediction_processing,
                                  svm: get_support_vector_machine_prediction_processing,
                                  linr: get_linear_regression_prediction_processing,
                                  logr: get_logistic_regression_prediction_processing}

# Primary portion of execution
# Tuning params.
# Example command line: python MLandMetrics.py ../../Output/Example_i.csv ../../Output/Example_j.csv
#     where i = training, and j = test set
# training_set_filename = "../../Output/Example_i.csv"
# test_set_filename = "../../Output/Example_j.csv"
# training set is arg 1 and test set is arg 2
training_set_filename = sys.argv[1]
test_set_filename = sys.argv[2]
num_features = 8
id_index = 0
name_index = 1
first_feature_index = 2
last_feature_index = first_feature_index + num_features
label_index = last_feature_index + 1
# File format & column address / indexes:
# has a header row.
#      0,            1,       2,...,      2+numFeatures,numFeatures+3<eol>
# "uuid","name_string",feature1,...,feature_numFeatures,Label(0,1)<eol>
#    str,          str,  Number,...,             Number,Number<eol>

# Let's load our Training set (i)
print("Loading Training Set")
training_set_instance_info = numpy.genfromtxt(training_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
training_set_ids = training_set_instance_info[:, 0]
training_set_names = training_set_instance_info[:, 1]
training_set = numpy.loadtxt(training_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
training_set_features = training_set[:, :-1]
training_set_labels = training_set[:, -1]

# Let's load our Test set (j)
print("Loading Test Set")
test_set_instance_info = numpy.genfromtxt(test_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
test_set_ids = training_set_instance_info[:, 0]
test_set_names = training_set_instance_info[:, 1]
test_set = numpy.loadtxt(test_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
test_set_features = test_set[:, 0:-1]
test_set_labels = test_set[:, -1]

# print("Training Set Details:")
# print(training_set_ids)
# print(training_set_names)
# print(training_set_features)
# print(training_set_labels)
# print("Test Set Details:")
# print(test_set_ids)
# print(test_set_names)
# print(test_set_features)
# print(test_set_labels)

# Now lets actually do some work!
# TODO: add the k-folding
print("Staring Creation and Classification")
for classifier_name in classifier_names:
    print(classifier_name + " Classifier:")
    # Create our Classifier and make the predictions
    test_set_raw_predictions = classifier_functions[classifier_name](training_set_features, training_set_labels).predict(test_set_features)
    # Modify the predictions
    test_set_final_prediction = prediction_processing_function[classifier_name](test_set_raw_predictions)
    # Print out the metrics for this run through.
    print(metrics.classification_report(test_set_labels, test_set_final_prediction, digits=4))
print("FIN")
