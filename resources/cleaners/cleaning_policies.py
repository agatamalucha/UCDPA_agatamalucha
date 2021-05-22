# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np


"""
---------- OPENING MAIN COVID DATASET (INDEPENDABLE VARIABLE) -----------------
"""

dataset_covid =  pd.read_csv("dataset_covid_cleaned.csv")

"""
---------------------------- COMMON FUNCTIONS  --------------------------------
"""

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
---------------------------- DATA SOURCES  ------------------------------------
"""

"""
DATA SOURCE:                #https://ourworldindata.org/policy-responses-covid
Dataset that contains restrictions on society during pandemic period  
"""
dataset_schools=pd.read_csv("school-closures-covid.csv")
dataset_internal_movement=pd.read_csv("internal-movement-covid.csv")

"""
---------------------------- CLEANINIG DATASETS -------------------------------
"""

"""CLEANING SCHOOL CLOSURES DATASET
"""
dataset_schools['is_eu'] = dataset_schools["Entity"].apply(lambda x: country_checker(x))
dataset_schools=dataset_schools[dataset_schools["is_eu"]==True]
dataset_schools=dataset_schools[["Entity","Day",  "school_closures"]]
dataset_schools=dataset_schools.rename(columns={"Entity":"country", "Day":"date"})

"""CLEANING  INTERNAL MOVEMENT DATASET
"""
dataset_internal_movement['is_eu']=dataset_internal_movement["Entity"].apply(lambda x: country_checker(x))
dataset_internal_movement=dataset_internal_movement[dataset_internal_movement["is_eu"]==True]
dataset_internal_movement=dataset_internal_movement[["Entity","Day", "restrictions_internal_movements"]]
dataset_internal_movement=dataset_internal_movement.rename(columns={"Entity":"country", "Day":"date"})



"""
----- MERGING DEPENDABLE VARIABLES DATASETS (SCHOOL CLOSURES, INTERNAL MOVEMENT) WITH MAIN COVID DATASET-------------------------------
"""

dataset = dataset_schools.merge(dataset_internal_movement, how="left", on=["country", "date"])
# Filing missing data with 0 value , we undestand that country as it's unknown we can assume that that country didn't apply restriction 
dataset =dataset.fillna(0)  
dataset.to_csv("dataset_policies_cleaned.csv", index=False)





