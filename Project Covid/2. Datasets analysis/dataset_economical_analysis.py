
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
#import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Allows saving plot to .png
# matplotlib.use('Agg')

dataset_economical_cleaned=pd.read_csv("dataset_economical_cleaned.csv")

# dataset characteristics in order to know the name of columns for plot axis
print(dataset_economical_cleaned.columns )
# Index(['country', 'population', 'gdp', 'density_per_sqr_km'], dtype='object')

# Dataset statistics
dataset_economical_cleaned.describe()

"""
Plot Histogram - GDP per capita (USD) in  EU countries 
"""
s=sns.barplot(x='gdp', y='country', data=dataset_economical_cleaned, order=dataset_economical_cleaned.sort_values('gdp', ascending=False).country)
s.set_title(" GDP per capita (USD) in  EU countries ", y=1.05)
plt.show(s)

"""
Plot Histogram - GDP per capita vs How many EU countires in  each bracket -16 countires GDP below 30k  - 2 countries highter than 62k
"""

sns.set_style("darkgrid")
custom=["#7995c4"]
sns.set_palette(custom)
f, ax = plt.subplots(figsize=(7, 5))
sns.despine(f)
g=sns.histplot(
    dataset_economical_cleaned,
    x="gdp", bins=5, 
    edgecolor=".5",
    linewidth=.5)

g.set_title("Distribution of EU countries by GDP per capita  ", y=1.05, fontweight="bold")
ax.set_xticklabels(['<0K','< 30,000', '< 52,000','< 62000' ,'< 80,000 ', '< 115,000'])
g.set(xlabel="GDP (USD)", ylabel = "Number of EU countries")
plt.show(g)







