# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:24:29 2021

@author: agata
"""

import pandas as pd
import matplotlib.pyplot as plt


dataset=pd.read_csv("dataset_covid_cleaned.csv")


country_count = len(dataset["country"].unique())

cases_max = dataset[dataset["cases"] == dataset["cases"].max()]
cases_min = dataset[dataset["cases"] == dataset["cases"].min()]

death_max = dataset[dataset["deaths"] == dataset["deaths"].max()]
deaths_min = dataset[dataset["deaths"] == dataset["deaths"].min()]


fig, ax= plt.subplots()
ax.hist(dataset['cases'], label='cases', bin= 5, histtype='step')

plt.show()



dataset.describe()








