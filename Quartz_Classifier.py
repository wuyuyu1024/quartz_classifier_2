import os
from typing import Counter
import numpy as np
import pandas as pd
from joblib import load

print(
    """
A classifier to predict the genetic type of quartz samples with 'Al','Ti','Li','Ge','Sr' values,
Please enter the path of the .xlsx or .csv data file.
(for example: /path/to/file/example_data.xlsx )
The data are supposed to contain all the 5 features above for prediction.
If any one of the features is missing in a sample, that sample will be discarded.
The columns' names of Al, Ti, Li, Ge, Sr should be exactly the two characters listed above without any prefix and suffix
and MAKE SURE this column name row is the FIRST row.
"""
)

try:
    classifier = load("quartz_clf.joblib")
except FileNotFoundError:
    print("Exception raised during loading of classifier.\n")
    raise

data_file_path = input("Please enter the path to the data file:")
# data_file_path = r"C:\Users\yuwan\Dropbox\Zotero\datapro\Qinglong.xlsx"  # DEBUG
# C:\Users\yuwan\Dropbox\Zotero\datapro\to_save\Rotier.xlsx
elements = ["Al", "Ti", "Li", "Ge", "Sr"]
# print(os.path.basename(data_file_path))
try:
    data_file_extension = os.path.splitext(data_file_path)[1]
    if data_file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(data_file_path)
    elif data_file_extension == ".csv":
        df = pd.read_csv(data_file_path)
except (FileNotFoundError, NameError):
    input("Exception raised during loading of data file.\n")
    # Debug

for element in elements:
    df[element] = pd.to_numeric(df[element], errors="coerce")

to_predict = df.loc[:, elements].dropna()
to_predict.reset_index(drop=True, inplace=True)
print(f"{to_predict.shape[0]} samples available")
print(to_predict.describe())
predict_res = classifier.predict(to_predict)
c: Counter[str] = Counter(predict_res)
if not c:
    input("no sample with the 5 features detected!")
    raise SystemExit()

proba = classifier.predict_proba(to_predict)
predict_res = predict_res.reshape((predict_res.shape[0], 1))
res = np.concatenate([predict_res, proba], axis=1)
res = pd.DataFrame(res, columns=['pred_quartz_type', 'IRG_proba', 'Carlin_proba', 'epithermal_proba',
                                 'granite_proba', 'greisen_proba', 'orogenic_proba', 'pegmatite_proba',
                                 'porphyry_proba', 'skarn_proba'])
pd.set_option('display.max_columns', 10)
print('Detailed report preview:\n', res)

print("The samples are predicted respectively to be: ")
print(c.most_common(), "\n")
print(
    f"The most possible type of the group of samples is: {c.most_common(1)[0][0]}.\n"
)

if input('Save report? (y/n): ').lower() == 'y':
    base_filename = os.path.basename(data_file_path)
    prefix, _ = os.path.splitext(base_filename)
    save_name = prefix + '_result.xlsx'
    res2 = pd.concat([to_predict['Al'], res], axis=1, )
    output = df.join(res2.set_index('Al'), on='Al')
    output.to_excel(save_name)
    print(f'{save_name} saved.')
input("Press any key to exit.")
