import sys
# Let's bring in our parser!
import numpy
# We must implement CV with the following classifiers:  decision tree, random forest, support vector machine, linear regression, and logistic regression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
# When testing use the KFold to partition.
from sklearn.model_selection import KFold
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


# this was simplified from "calssification.py->classification_report" function.
def local_classification_report(p, r, f1, s, sample_weight=None, digits=2):
    labels = numpy.asarray([0, 1.0])

    last_line_heading = 'avg / total'
    target_names = [u'%s' % l for l in labels]
    name_width = max(len(cn) for cn in target_names)
    width = max(name_width, len(last_line_heading), digits)

    headers = ["precision", "recall", "f1-score", "support"]
    head_fmt = u'{:>{width}s} ' + u' {:>9}' * len(headers)
    report = head_fmt.format(u'', *headers, width=width)
    report += u'\n\n'

    row_fmt = u'{:>{width}s} ' + u' {:>9.{digits}f}' * 3 + u' {:>9}\n'
    rows = zip(target_names, p, r, f1, s)
    for row in rows:
        report += row_fmt.format(*row, width=width, digits=digits)

    report += u'\n'

    # compute averages
    report += row_fmt.format(last_line_heading,
                             numpy.average(p, weights=s),
                             numpy.average(r, weights=s),
                             numpy.average(f1, weights=s),
                             numpy.sum(s),
                             width=width, digits=digits)

    return report


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
classifiers_for_ensemble = [dt, rf, linr, logr]

# Primary portion of execution
# Tuning params.
# Example command line: python MLandMetrics.py ../../Output/Example_i.csv ../../Output/Example_j.csv
# Example command line: python MLandMetrics.py ../../Output/featurespace_train.csv ../../Output/featurespace_test.csv
# Example command line: python MLandMetrics.py ../../Output/featurespace-train.csv
#     where i = training, and j = test set
# training_set_filename = "../../Output/Example_i.csv"
# test_set_filename = "../../Output/Example_j.csv"
# training set is arg 1 and test set is arg 2
training_set_filename = sys.argv[1]
num_features = 8
id_index = 0
name_index = 1
first_feature_index = 2
last_feature_index = first_feature_index + num_features
label_index = last_feature_index + 1
num_k_folds = 10
ensemble_vote_percentage = 0.5

# File format & column address / indexes:
# has a header row.
#      0,            1,       2,...,      2+numFeatures,numFeatures+3<eol>
# "uuid","name_string",feature1,...,feature_numFeatures,Label(0,1)<eol>
#    str,          str,  Number,...,             Number,Number<eol>


if len(sys.argv) >= 4:
    print("Ensemble learning")
    # K fold on Training data and testing on test data.
    # We need to partition the "training_set_filename" into a training set and an test set
    # sets_instance_info = numpy.genfromtxt(training_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
    sets_instances = numpy.loadtxt(training_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
    sets_features = sets_instances[:, 0:-1]
    sets_labels = sets_instances[:, -1]
    # Let's load our Test set (j)
    test_set_filename = sys.argv[2]
    print("Loading Test Set from: " + test_set_filename)
    test_set = numpy.loadtxt(test_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
    test_set_features = test_set[:, 0:-1]
    test_set_labels = test_set[:, -1]

    test_set_final_prediction = numpy.zeros(len(test_set_labels))
    # Now lets actually do some work!
    kf = KFold(n_splits=num_k_folds, shuffle=True)
    for training_set_indexs, test_set_indexs in kf.split(sets_features):
        print("Staring Creation and Classification")
        for classifier_name in classifiers_for_ensemble:
            print(classifier_name + " Classifier:")
            # Create our Classifier and make the predictions on the actual test set.
            test_set_raw_predictions = classifier_functions[classifier_name](sets_features[training_set_indexs], sets_labels[training_set_indexs]).predict(test_set_features)
            # Modify the predictions, accumulate them to be normalized / voted on later.
            test_set_final_prediction = test_set_final_prediction + prediction_processing_function[classifier_name](test_set_raw_predictions)

    # Calculate our scaling and Normalized our predictions.
    ensemble_threshold = ensemble_vote_percentage * num_k_folds * len(classifiers_for_ensemble)
    test_set_normalized_prediction = [1 if prediction >= ensemble_threshold else 0 for prediction in test_set_final_prediction]
    # Print out the metrics for this run through.
    print(metrics.classification_report(test_set_labels, test_set_normalized_prediction, digits=4))
    print("FIN")


elif len(sys.argv) >= 3:
    # We have both the training and test set.
    print("Single training run")
    # Let's load our Training set (i)
    print("Loading Training Set from: " + training_set_filename)
    training_set_instance_info = numpy.genfromtxt(training_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
    training_set_ids = training_set_instance_info[:, 0]
    training_set_names = training_set_instance_info[:, 1]
    training_set = numpy.loadtxt(training_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
    training_set_features = training_set[:, :-1]
    training_set_labels = training_set[:, -1]

    # Let's load our Test set (j)
    test_set_filename = sys.argv[2]
    print("Loading Test Set from: " + test_set_filename)
    test_set_instance_info = numpy.genfromtxt(test_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
    test_set_ids = test_set_instance_info[:, 0]
    test_set_names = test_set_instance_info[:, 1]
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


else:
    # K fold on Training data only!
    # We need to partition the "training_set_filename" into a training set and an test set
    # sets_instance_info = numpy.genfromtxt(training_set_filename, delimiter=',', usecols=[id_index, name_index], dtype=str, skip_header=1)
    sets_instances = numpy.loadtxt(training_set_filename, delimiter=',', usecols=list(range(first_feature_index, label_index)), skiprows=1)
    sets_features = sets_instances[:, 0:-1]
    sets_labels = sets_instances[:, -1]
    # results = numpy.zeros((len(classifier_names), 4))
    results = {}
    for classifier_name in classifier_names:
        results[classifier_name] = []

    # Now lets actually do some work!
    kf = KFold(n_splits=num_k_folds, shuffle=True)
    for training_set_indexs, test_set_indexs in kf.split(sets_features):
        print("Staring Creation and Classification")
        for classifier_name in classifier_names:
            print(classifier_name + " Classifier:")
            # Create our Classifier and make the predictions
            test_set_raw_predictions = classifier_functions[classifier_name](sets_features[training_set_indexs], sets_labels[training_set_indexs]).predict(sets_features[test_set_indexs])
            # Modify the predictions
            test_set_final_prediction = prediction_processing_function[classifier_name](test_set_raw_predictions)
            # Save off the metrics.
            precision, recall, f1_score, true_sum = metrics.precision_recall_fscore_support(sets_labels[test_set_indexs], test_set_final_prediction)
            # print("Precision: ", precision, " Recall: ", recall, " F1: ", f_score, " TSum: ", true_sum)
            results[classifier_name].append([precision, recall, f1_score, true_sum])

    for classifier_name in classifier_names:
        print(classifier_name + " Classifier:")
        c_precision, c_recall, c_f1_score, c_true_sum = numpy.array(results[classifier_name]).mean(0)
        print(local_classification_report(c_precision, c_recall, c_f1_score, c_true_sum, digits=4))
    print("FIN")
