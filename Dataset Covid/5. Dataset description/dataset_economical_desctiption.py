# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
import matplotlib.cm as cm


dataset_economical_cleaned=pd.read_csv("dataset_economical_cleaned.csv")

# dataset characteristics
print(dataset_economical_cleaned.columns )
# Index(['country', 'population', 'gdp', 'density_per_sqr_km'], dtype='object')

# Dataset statistics
dataset_economical_cleaned.info()
dataset_economical_cleaned.describe()



# Converting float64 data into decimal an integer 
dataset_economical_cleaned['population'] = dataset_economical_cleaned['population'].apply(int)
dataset_economical_cleaned['gdp'] = dataset_economical_cleaned['gdp'].apply(lambda x: round(Decimal(x), 0))
dataset_economical_cleaned['density_per_sqr_km'] = dataset_economical_cleaned['density_per_sqr_km'].apply(lambda x: round(Decimal(x), 0))






# Feature Distribution and Correlations

sns.barplot(x='density_per_sqr_km', y='country', data=dataset_economical_cleaned, order=dataset_economical_cleaned.sort_values('density_per_sqr_km', ascending=False).country)

sns.barplot(x='gdp', y='country', data=dataset_economical_cleaned, order=dataset_economical_cleaned.sort_values('gdp', ascending=False).country)
# How many counties in T
sns.distplot(dataset_economical_cleaned['gdp'], kde=False, bins=5)


fig, ax= plt.subplots()
g = ax.hist(dataset_economical_cleaned['gdp'], label="women", bins=5, color='skyblue', )     
plt.title("GDP in EU countries ")
ax.set_xlabel('gdp (USD)', c='C4', )
ax.set_ylabel('number of EU countries')
plt.show()

middle = dataset_economical_cleaned[["country", "gdp"]]









