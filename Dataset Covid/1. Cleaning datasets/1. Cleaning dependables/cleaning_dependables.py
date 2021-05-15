# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np

# list of EU countries
eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 
                'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 
                'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania',
                'Slovakia', 'Slovenia', 'Spain', 'Sweden']

# function that checks if string in column is in eu_countries list
def country_checker(string):
    if string in eu_countries:
        return True


"""
DATA SOURCE: https://covid19.who.int/WHO-COVID-19-global-data.csv
Dataset from official WHO website that contains number of daily COVID cases and deaths.
"""

dataset = pd.read_csv("WHO-COVID-19-global-data.csv")
 
# Appying country_checker function 
dataset['is_eu']=dataset["Country"].apply(lambda x: country_checker(x))
dataset=dataset[dataset["is_eu"]==True]

# Removing unneccessary columns from dataset
dataset=dataset[["Date_reported","Country", "New_cases","New_deaths" ]]

# Renaming columns
dataset=dataset.rename(columns={"Date_reported":"date","Country":"country", "New_cases":"cases", "New_deaths":"deaths"   })

"""
------------------------------------DATASET DESCRIPTION -----------------------
"""
dataset.head()
dataset.info()

# We found negative values in cases and deaths columns     
# Negative values changed  please see additional source: ref:  https://www.google.com/search?client=firefox-b-d&q=covi+cases+italy+2020
dataset['cases'].describe()    # min      -1385.000000 
dataset['deaths'].describe()   # min        -31.000000


dataset["cases"] = np.where(dataset["cases"] < 0, 0, dataset["cases"])
dataset["deaths"] = np.where(dataset["deaths"] < 0, 0, dataset["deaths"])







# Daving cleaned dataset into csv file
dataset.to_csv("dataset_covid_cleaned.csv", index=False)













