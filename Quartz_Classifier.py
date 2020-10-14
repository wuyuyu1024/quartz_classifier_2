from joblib import load
import pandas as pd
from collections import Counter

print("""
A classifier to predict the type of quartz samples with full of ['Al','Ti','Li','Ge','Sr'] values,
PLease input or paste your the path of your data file as either .xlsx or .csv 
(for example: path\\to\\file\\example_data.xlsx )
The data are supposed to contain all the 5 features above to predict.
If either feature is missing in a sample, the sample will be dropped.

""")
try:
    clf = load(r'.\quartz_clf.joblib')
except:
    input("FileNotFoundError, press Enter to Exit.")
    raise SystemExit()

path = input('Please input the path of your data file:')
elements = ['Al', 'Ti', 'Li', 'Ge', 'Sr']
try:
    if 'xls' in path[-4:]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
except:
    raise Exception('Path does not exist')

for ele in elements:
    df[ele] = pd.to_numeric(df[ele], errors='coerce')

try:
    to_predict = df.loc[:, elements].dropna()
    print(f'{len(to_predict.Al)} samples available')
    predict_res = clf.predict(to_predict)
    c = Counter(predict_res)
    to_predict['predict_result'] = predict_res
    print(to_predict)
    print('The samples are predicted respectively to be: ')
    print(c.most_common(8), '\n')
    print(f'The most possible type of the group of samples are {c.most_common(1)[0][0] if c else None}.')
except:
    print('no sample with the 5 features detected!')
finally:
    print('\n promgram end')
    input('press any button to exit')

