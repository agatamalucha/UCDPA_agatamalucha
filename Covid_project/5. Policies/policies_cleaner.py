# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:25:51 2021

@author: agata
"""



import pandas as pd
import numpy as np


#POLICY RESPONSES            #https://ourworldindata.org/policy-responses-covid
dataset_schools=pd.read_csv("school-closures-covid.csv")
dataset_internal_movement=pd.read_csv("internal-movement-covid.csv")

dataset_covid = pd.read_csv("dataset_covid_cleaned.csv")

# dataset_policies = dataset_schools.merge(dataset_internal_movement, on=["Entity", "Code", "Day"]).merge( dataset_change_retail_recreation, on=["Entity", "Code", "Day"])

eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 
                'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 
                'Slovenia', 'Spain', 'Sweden']
len(eu_countries)   # There is 27 countries in the list


eu_countries = sorted(eu_countries)


def country_checker(string):
    if string in eu_countries:
        return True

"""
SCHOOL CLOSURES
"""
countries_unique= list(dataset_schools["Entity"].unique())

dataset_schools['is_eu'] = dataset_schools["Entity"].apply(lambda x: country_checker(x))
dataset_schools=dataset_schools[dataset_schools["is_eu"]==True]
dataset_schools=dataset_schools[["Entity","Day",  "school_closures"]]
countries_unique= list(dataset_schools["Entity"].unique())

dataset_schools=dataset_schools.rename(columns={"Entity":"country", "Day":"date"})

"""
 INTERNAL MOVEMENT
"""
countries_unique= list(dataset_internal_movement["Entity"].unique())

dataset_internal_movement['is_eu']=dataset_internal_movement["Entity"].apply(lambda x: country_checker(x))
dataset_internal_movement=dataset_internal_movement[dataset_internal_movement["is_eu"]==True]
dataset_internal_movement=dataset_internal_movement[["Entity","Day", "restrictions_internal_movements"]]
countries_unique= list(dataset_internal_movement["Entity"].unique())

dataset_internal_movement=dataset_internal_movement.rename(columns={"Entity":"country", "Day":"date"})



dataset = dataset_covid.merge(dataset_schools, how="left", on=["country", "date"])


dataset = dataset.merge(dataset_internal_movement, how="left", on=["country", "date"])
dataset =dataset.fillna(0)  

dataset.to_csv("dataset_policies_cleaned.csv", index=False)



































