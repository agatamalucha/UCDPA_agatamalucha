# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
from sklearn import preprocessing

dataset_health=pd.read_csv("dataset_healthcare_cleaned.csv")

# dataset characteristics
print(dataset_health.columns)
# Index(['country', 'physicians', 'nurses', 'hospital_beds'], dtype='object')


# Dataset statistics
dataset_health.info()
dataset_health.describe()

# Top 3 countries with highest number of physicians, nurses and hospital beds 
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


# Converting float64 data into decimal data with rounded to 4 places after coma
dataset_health['physicians'] = dataset_health['physicians'].apply(lambda x: round(Decimal(x), 4))
dataset_health['nurses'] = dataset_health['nurses'].apply(lambda x: round(Decimal(x), 4))
dataset_health['hospital_beds'] = dataset_health['hospital_beds'].apply(lambda x: round(Decimal(x), 4))

# Feature Distribution and visuals   physicians, beds, nurses  per 1000 population.
a =sns.barplot(x='physicians', y='country', data=dataset_health, order=dataset_health.sort_values('physicians', ascending=False).country)
a.set_title(" Number of physicians per 1000 population ", y=1.05)
plt.show(a)
b = sns.barplot(x='nurses', y='country', data=dataset_health, order=dataset_health.sort_values('nurses', ascending=False).country)
b.set_title(" Number of nurses per 1000 population ", y=1.05)
plt.show(b)
c = sns.barplot(x='hospital_beds', y='country', data=dataset_health, order=dataset_health.sort_values('hospital_beds', ascending=False).country)
c.set_title(" Number of hospital beds per 1000 population ", y=1.05)
plt.show(c)

# Merging healthcare data with economical data
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

g = sns.scatterplot( y=dataset_healthcare_outliers['physicians'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s = 55, hue=dataset_healthcare_outliers['country'], legend=False) 
g.legend(loc='center left', bbox_to_anchor=(1, 0.5))
sns.set_style("darkgrid")
for i in range(dataset_healthcare_outliers.shape[0]):
 g.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['physicians'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))
g.legend( loc=2, bbox_to_anchor=(1, 0.5))
g.set_title("Relation between GDP and Physicians (normalized)", y=1.05, fontweight="bold")
g.set(xlabel="GDP", ylabel = "Physicians")
plt.show(g)
"""
Producing scattered plot to find outliers (high GDP but low number of nurses and low GDP and high number of nurses)
""" 

h = sns.scatterplot( y=dataset_healthcare_outliers['nurses'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s = 55, hue=dataset_healthcare_outliers['country'],legend=False) 
h.legend(loc='center left', bbox_to_anchor=(1, 0.5))
sns.set_style("darkgrid")

for i in range(dataset_healthcare_outliers.shape[0]):
 h.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['nurses'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))
h.set_title("Relation between GDP per capita and Nurses (normalized)", y=1.05, fontweight="bold")
h.set(xlabel="GDP", ylabel = "Nurses")
plt.show(h)
"""
Producing scattered plot to find outliers (high GDP but low number of hospital beds and low GDP and high number of hospital beds)
"""

e = sns.scatterplot( y=dataset_healthcare_outliers['hospital_beds'], x=dataset_healthcare_outliers['gdp'], data=dataset_healthcare_outliers, s =55, hue=dataset_healthcare_outliers['country'],legend=False) 
e.legend(loc='center left', bbox_to_anchor=(1, 0.5))
sns.set_style("darkgrid")

for i in range(dataset_healthcare_outliers.shape[0]):
 e.text(x=dataset_healthcare_outliers['gdp'][i],y=dataset_healthcare_outliers['hospital_beds'][i],s=dataset_healthcare_outliers['country'][i], 
          fontdict=dict(color='black',size=8))
e.set_title("Relation between GDP per capita and number of hospital beds (normalized)", y=1.05, fontweight="bold")
e.set(xlabel="GDP", ylabel = "Hospital Beds")
plt.show(e)

