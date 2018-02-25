# Let's bring in our parser!
import numpy
# We must implement CV with the following classifiers:  decision tree, random forest, support vector machine, linear regression, and logistic regression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
# We must measure R/P/F1
from sklearn import metrics

dt = "Decision Tree"


# Fitted getClassifier Function for a Decision Tree Classifier
def getDecisionTreeClassifier(features, labels):
    # TODO: Found in an example, prune later.
    # return DecisionTreeClassifier(criterion="entropy", class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    return DecisionTreeClassifier().fit(features, labels)


rf = "Random Forest"


# Fitted getClassifier Function for a Random Forest Classifier
def getRandomForestClassifer(features, labels):
    # TODO: Found in an example, prune later.
    # return RandomForestClassifier(criterion="entropy", class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    return RandomForestClassifier().fit(features, labels)


svm = "Support Vector Machine"


# Fitted getClassifier Function for a Support Vector Machine Classifier
def getSupportVectorMachineClassifer(features, labels):
    # TODO: Found in an example, prune later.
    # return SVC(class_weight={1: 0.25, 0: 0.75}).fit(features, labels)
    # return SVC(C=100.0).fit(features, labels)
    # return SVC(kernel='linear').fit(features, labels)
    return SVC().fit(features, labels)


linr = "Linear Regression"
linrThreshold = 0.5


# Fitted getClassifier Function for a Linear Regression Classifier
def getLinearRegressionClassifier(features, labels):
    return LinearRegression().fit(features, labels)


logr = "Logistic Regression"


# Fitted getClassifier Function for a Logistic Regression Classifier
def getLogisticRegressionClassifier(features, labels):
    # TODO: Found in an example, prune later.
    # return LogisticRegression(C=100000).fit(features, labels)
    return LogisticRegression().fit(features, labels)


# Tools for looping through all the different Classifiers via Function pointers.
classifierNames = [dt, rf, svm, linr, logr]
classifierFns = {dt: getDecisionTreeClassifier,
                 rf: getRandomForestClassifer,
                 svm: getSupportVectorMachineClassifer,
                 linr: getLinearRegressionClassifier,
                 logr: getLogisticRegressionClassifier}

# Primary portion of execution
# Tuning params.
trainingSetFileName = "../../Data/Example_i.csv"
testSetFileName = "../../Data/Example_j.csv"
numFeatures = 8
idIndex = 0
nameIndex = 1
firstFeatureIndex = 2
lastFeatureIndex = firstFeatureIndex + numFeatures
labelIndex = lastFeatureIndex + 1
# File format & column address / indexes:
#      0,            1,       2,...,      2+numFeatures,numFeatures+3<eol>
# "uuid","name_string",feature1,...,feature_numFeatures,Label(0,1)<eol>
#    str,          str,  Number,...,             Number,Number<eol>

# Let's load our Training set (i)
print("Loading Training Set")
trainingSetInstanceInfo = numpy.genfromtxt(trainingSetFileName, delimiter=',', usecols=[idIndex, nameIndex],
                                           dtype=str)
trainingSetIds = trainingSetInstanceInfo[:, 0]
trainingSetNames = trainingSetInstanceInfo[:, 1]
trainingSet = numpy.loadtxt(trainingSetFileName, delimiter=',', usecols=list(range(firstFeatureIndex, labelIndex)))
trainingSetFeatures = trainingSet[:, :-1]
trainingSetLabels = trainingSet[:, -1]

# Let's load our Test set (j)
print("Loading Test Set")
testSetInstanceInfo = numpy.genfromtxt(testSetFileName, delimiter=',', usecols=[idIndex, nameIndex], dtype=str)
testSetIds = trainingSetInstanceInfo[:, 0]
testSetNames = trainingSetInstanceInfo[:, 1]
testSetSet = numpy.loadtxt(trainingSetFileName, delimiter=',', usecols=list(range(firstFeatureIndex, labelIndex)))
testSetFeatures = trainingSet[:, 0:-1]
testSetLabels = trainingSet[:, -1]

# print("Training Set Details:")
# print(trainingSetIds)
# print(trainingSetNames)
# print(trainingSetFeatures)
# print(trainingSetLabels)
# print("Test Set Details:")
# print(testSetIds)
# print(testSetNames)
# print(testSetFeatures)
# print(testSetLabels)

# Now lets actually do some work!
# TODO: add the k-folding
print("Staring Creation and Classification")
for classifierName in classifierNames:
    print(classifierName + "classifier")
    testSetPredictions = classifierFns[classifierName](trainingSetFeatures, trainingSetLabels).predict(testSetFeatures)
    # Linear Regression outputs are a bit different need to modify
    if classifierName == linr:
        tempPredictions = testSetPredictions[:]
        testSetPredictions = [1 if val > linrThreshold else 0 for val in tempPredictions]
    print(metrics.classification_report(testSetLabels, testSetPredictions, digits=3))
print("FIN")