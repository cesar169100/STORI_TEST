import pandas as pd

df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)