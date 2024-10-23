import pandas as pd
import datetime as dt

df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)

# keep the necessary fields
dat = df[['cust_id','activated_date','last_payment_date','cash_advance','credit_limit']]
# Convert to datetime to get the year
dat['activated_date'] = pd.to_datetime(dat['activated_date'])
dat['last_payment_date'] = pd.to_datetime(dat['last_payment_date'])
dat['year_activation'] = dat['activated_date'].dt.year
dat['year_payment'] = dat['last_payment_date'].dt.year
dat = dat[(dat['year_activation']==2020) & (dat['year_payment']==2020)]
dat = dat.drop(['year_activation','year_payment'], axis=1)
dat['cust_id'] = dat['cust_id'].str[1:]
dat['activated_date'] = dat['activated_date'].dt.to_period('M')
dat['percentage_field'] = dat['cash_advance'] / dat['credit_limit']
dat