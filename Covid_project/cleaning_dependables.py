# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd

eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 
                'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 
                'Slovenia', 'Spain', 'Sweden']

eu_countries = sorted(eu_countries)


dataset = pd.read_csv("WHO-COVID-19-global-data.csv")
dataset=dataset[dataset["WHO_region"]=="EURO"]


def country_checker(string):
    if string in eu_countries:
        return True


dataset['is_eu']=dataset["Country"].apply(lambda x: country_checker(x))


dataset=dataset[dataset["is_eu"]==True]

dataset=dataset[["Date_reported","Country", "New_cases","New_deaths" ]]


dataset=dataset.rename(columns={"Date_reported":"date","Country":"country", "New_cases":"cases", "New_deaths":"deaths"   })


dataset.to_csv("dataset_covid_cleaned.csv", index=False)













