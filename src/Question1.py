import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

df = pd.read_csv('./data/data.csv')
df = df.drop(['Unnamed: 0'], axis=1)

# A function that create a histogram for a numerical column
def histograma(columna: str, bins: int, title: str, xlabel: str, ylabel: str):
    """Plots a histogram for numerical column.
       Args:
        Labels (str): Labels of the plot.
        bins: Number of grouping intervals.
       Returns:
        Saved plot
    """
    plt.figure(figsize=(8, 6))
    sns.histplot(df[columna], bins=bins, kde=True, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('figures/balance_hist.png')
    plt.close()

# Question 1.1: histogram
histograma('balance', 15, 'Balance Amount', 'Categoría', 'Frequency')

# A function that calculates mean and median balance, grouped by year and month of 
# activated_date​
def mean_balance(column: str):
    """Table grouped by year and month of activated_date and aggregations of a numerical column.
       Args:
        column (str): Name of the column to calculate mean and median.
       Returns:
        Dataframe
    """
    dat = df[[column, 'activated_date']]
    dat['activated_date'] = pd.to_datetime(dat['activated_date'])
    dat['year'] = dat['activated_date'].dt.year
    dat['month'] = dat['activated_date'].dt.month
    dat = dat.drop(['activated_date'], axis=1)
    tabla = dat.groupby(['year', 'month']).agg(
        mean_balance = (column, 'mean'),
        median_balance = (column, 'median')).reset_index()
    return tabla

# Question 1.3: Mean, median balance table
mean_balance('balance')