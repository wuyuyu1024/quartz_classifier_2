import os
from typing import Counter

import pandas as pd
from joblib import load

print(
    """
A classifier to predict the type of quartz samples with full of ['Al','Ti','Li','Ge','Sr'] values,
Please enter the path of the .xlsx or .csv data file.
(for example: /path/to/file/example_data.xlsx )
The data are supposed to contain all the 5 features above for prediction.
If any one of the features is missing in a sample, that sample will be discarded.

"""
)

try:
    classifier = load(r"./quartz_clf.joblib")
except FileNotFoundError:
    print("Exception raised during loading of classifier.\n")
    raise

# data_file_path = input("Please enter the path to the data file:")
data_file_path = "data_for_svm.csv"  # DEBUG

elements = ["Al", "Ti", "Li", "Ge", "Sr"]

try:
    data_file_extension = os.path.splitext(data_file_path)[1]
    if data_file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(data_file_path)
    elif data_file_extension == ".csv":
        df = pd.read_csv(data_file_path)
except FileNotFoundError:
    print("Exception raised during loading of data file.\n")
    raise

for element in elements:
    df[element] = pd.to_numeric(df[element], errors="coerce")

to_predict = df.loc[:, elements].dropna()
print(f"{len(to_predict.Al)} samples available")
predict_res = classifier.predict(to_predict)
c: Counter[str] = Counter(predict_res)
if not c:
    print("no sample with the 5 features detected!")
    raise SystemExit()
to_predict["predict_result"] = predict_res
print(to_predict)
print("The samples are predicted respectively to be: ")
print(c.most_common(), "\n")
print(
    f"The most possible type of the group of samples is: {c.most_common(1)[0][0]}.\n"
)
input("Press any key to exit.")
