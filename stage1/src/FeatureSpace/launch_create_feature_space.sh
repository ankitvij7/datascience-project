#!/bin/bash

python CreateFeatureSpace.py intermediatefeaturespace_train.csv featurespace_train.csv I
python CreateFeatureSpace.py intermediatefeaturespace_test.csv featurespace_test.csv J
python3 ../MLandMetrics/MLandMetrics.py ../../Output/featurespace-train.csv