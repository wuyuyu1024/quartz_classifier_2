# quartz_classifier_2

[![DOI](https://zenodo.org/badge/301276313.svg)](https://zenodo.org/badge/latestdoi/301276313)

dataset of quartz trace elements

code for build the svm classifier

pickled model

the code to predict new data:
  A classifier to predict the type of quartz samples with full of ['Al','Ti','Li','Ge','Sr'] values,
  PLease input or paste your the path of your data file as either .xlsx or .csv 
  (for example: path\to\file\example_data.xlsx )
  The data are supposed to contain all the 5 features above to predict.
  If either feature is missing in a sample, the sample will be dropped.
