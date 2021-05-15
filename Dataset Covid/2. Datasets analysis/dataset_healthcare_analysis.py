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
from sklearn import preprocessing

# Allows saving plot to .png
matplotlib.use('Agg')

dataset_health=pd.read_csv("dataset_healthcare_cleaned.csv")

# dataset characteristics
print(dataset_health.columns)
# Index(['country', 'physicians', 'nurses', 'hospital_beds'], dtype='object')


# Dataset statistics
dataset_health.info()
dataset_health.describe()

# Top 3 countries with highest number of physicians, nurses and hospital beds.
dataset_health_top_physicians=dataset_health.sort_values(by=['physicians'], ascending=False)
print(dataset_health_top_physicians.head())

dataset_health_top_nurses=dataset_health.sort_values(by=['nurses'], ascending=False)
print(dataset_health_top_nurses.head())

dataset_health_top_beds=dataset_health.sort_values(by=['hospital_beds'], ascending=False)
print(dataset_health_top_beds.head())

# Top 3 countries with lowest number of physicians, nurses and hospital beds.
dataset_health_bottom_physicians=dataset_health.sort_values(by=['physicians'], ascending=True)
print(dataset_health_bottom_physicians.head())

dataset_health_bottom_nurses=dataset_health.sort_values(by=['nurses'], ascending=True)
print(dataset_health_bottom_nurses.head())

dataset_health_bottom_beds=dataset_health.sort_values(by=['hospital_beds'], ascending=True)
print(dataset_health_bottom_beds.head())


# Converting float64 data into decimal data
dataset_health['physicians'] = dataset_health['physicians'].apply(lambda x: round(Decimal(x), 4))
dataset_health['nurses'] = dataset_health['nurses'].apply(lambda x: round(Decimal(x), 4))
dataset_health['hospital_beds'] = dataset_health['hospital_beds'].apply(lambda x: round(Decimal(x), 4))


# Feature Distribution and visuals
sns.barplot(x='physicians', y='country', data=dataset_health, order=dataset_health.sort_values('physicians', ascending=False).country)
sns.barplot(x='nurses', y='country', data=dataset_health, order=dataset_health.sort_values('nurses', ascending=False).country)
sns.barplot(x='hospital_beds', y='country', data=dataset_health, order=dataset_health.sort_values('hospital_beds', ascending=False).country)

plt.savefig('dataset_healhcare_1.png') 
plt.close()


dataset_economical_cleaned=pd.read_csv("dataset_economical_cleaned.csv")
dataset_healthcare_outliers = dataset_health.merge(dataset_economical_cleaned, on="country", how="left")
dataset_healthcare_outliers.columns
dataset_healthcare_outliers = dataset_healthcare_outliers[['country', 'physicians', 'nurses', 'hospital_beds', 'gdp']]


# Feature Correlation  between Number of physicians and GDP per Capita

# Normalizing values in range 0-1

scaler = preprocessing.MinMaxScaler()
dataset_healthcare_outliers[[ 'physicians', 'nurses', 'hospital_beds', 'gdp']] = scaler.fit_transform(dataset_healthcare_outliers[['physicians', 'nurses', 'hospital_beds', 'gdp']].values)

# Avoid 0 division

dataset_healthcare_outliers['gdp'] = dataset_healthcare_outliers['gdp'] + 0.0001
dataset_healthcare_outliers['physicians'] = dataset_healthcare_outliers['physicians'] + 0.0001

dataset_healthcare_outliers['physicians_gdp_ratio'] = dataset_healthcare_outliers['physicians'] / dataset_healthcare_outliers['gdp']

"""
Producing scattered plot to find outliers (high GDP but low number of physicians and low GDP and high number of pysicians)
"""

g = sns.scatterplot( y=dataset_healthcare_outliers['physicians'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s = 50, hue=dataset_healthcare_outliers['country'],) 
g.legend(loc='center left', bbox_to_anchor=(1, 0.5))


for i in range(dataset_healthcare_outliers.shape[0]):
 g.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['physicians'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))
 
plt.savefig('dataset_healhcare_2.png') 
plt.close()
 
"""
Producing scattered plot to find outliers (high GDP but low number of nurses and low GDP and high number of nurses)
""" 

h = sns.scatterplot( y=dataset_healthcare_outliers['nurses'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s = 50, hue=dataset_healthcare_outliers['country'],) 
h.legend(loc='center left', bbox_to_anchor=(1, 0.5))


for i in range(dataset_healthcare_outliers.shape[0]):
 h.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['nurses'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))

plt.savefig('dataset_healhcare_3.png')
plt.close()

"""
Producing scattered plot to find outliers (high GDP but low number of hospital beds and low GDP and high number of hospital beds)
"""

b = sns.scatterplot( y=dataset_healthcare_outliers['hospital_beds'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s = 50, hue=dataset_healthcare_outliers['country'],) 
b.legend(loc='center left', bbox_to_anchor=(1, 0.5))


for i in range(dataset_healthcare_outliers.shape[0]):
 b.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['hospital_beds'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))

plt.savefig('dataset_healhcare_4.png')
plt.close()

