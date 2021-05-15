
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
import matplotlib.cm as cm


# Allows saving plot to .png
matplotlib.use('Agg')

dataset_economical_cleaned=pd.read_csv("dataset_economical_cleaned.csv")

# dataset characteristics
print(dataset_economical_cleaned.columns )
# Index(['country', 'population', 'gdp', 'density_per_sqr_km'], dtype='object')

# Dataset statistics
dataset_economical_cleaned.info()
dataset_economical_cleaned.describe()



# Saving GDP Bar chart as .png file
plt.figure(figsize=(12,18))
sns.barplot(x='gdp', y='country', data=dataset_economical_cleaned, order=dataset_economical_cleaned.sort_values('gdp', ascending=False).country)
#plt.show(sns)
plt.savefig('dataset_economical_1.png')
plt.close()

# Saving GDP Distribution histogram chart as .png file
fig, ax= plt.subplots()
g = ax.hist(dataset_economical_cleaned['gdp'], bins=5, color='skyblue', )     
plt.title("GDP in EU countries ")
ax.set_xlabel('gdp (USD)', c='C8', )
ax.set_ylabel('number of EU countries', c='C8')


plt.savefig('dataset_economical_2.png')
plt.close()







