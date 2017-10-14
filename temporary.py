import pandas as pd

KOSPI=pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_KOSPI.csv")
kosdaq=pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_kosdaq.csv")

KOSPI.columns=['KOSPI','CODE']
kosdaq.columns=['KOSDAQ','CODE']
KOSPI.index=KOSPI['KOSPI']
kosdaq.index=kosdaq['KOSDAQ']
KOSPI=KOSPI['CODE']
kosdaq=kosdaq['CODE']

print(kosdaq)
