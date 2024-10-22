import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# A function

