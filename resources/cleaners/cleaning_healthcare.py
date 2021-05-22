# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np

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
# Please note that csv files downloaded from worldbank website had a non-relevant header in first  4 rows and  I have removed them manually from the files.
# I haven't  used  skiprows=4 parameter in pd.read_csv method , but I am aware of this .

"""
DATA SOURCE:                https://data.worldbank.org/indicator/SH.MED.BEDS.ZS
Dataset that contains number of hospital beds of each country   (per 1,000 people)
"""
dataset_hospital_beds= pd.read_csv("dataset_beds.csv" )

"""
DATA SOURCE:                https://data.worldbank.org/indicator/SH.MED.NUMW.P3?end=2018&start=1960
Dataset that contains number of nurses of each country (per 1,000 people) 
"""   
dataset_nurses= pd.read_csv("dataset_nurses.csv" ) 

"""
DATA SOURCE:                https://data.worldbank.org/indicator/SH.MED.PHYS.ZS?end=2018&start=1960
Dataset that contains number of physicians of each country (per 1,000 people) 
"""   
dataset_physicians=pd.read_csv("dataset_physicians.csv")

"""
---------------------------- CLEANINIG DATASETS -------------------------------
"""

"""
CLEANING HOSPITAL BEDS DATASET
""" 
dataset_hospital_beds["Country Name"]=dataset_hospital_beds["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_hospital_beds["Country Name"]=dataset_hospital_beds["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_hospital_beds["Country Name"]=np.where(dataset_hospital_beds["Country Code"]=="ESP","Spain",dataset_hospital_beds["Country Name"] )
dataset_hospital_beds['is_eu']=dataset_hospital_beds["Country Name"].apply(lambda x: country_checker(x))
dataset_hospital_beds=dataset_hospital_beds[dataset_hospital_beds["is_eu"]==True]
dataset_hospital_beds=dataset_hospital_beds[["Country Name", "2017"]]
dataset_hospital_beds=dataset_hospital_beds.rename(columns={"Country Name":"country", "2017": "hospital_beds"})

"""
CLEANING NURSES DATASET
"""
dataset_nurses["Country Name"]=dataset_nurses["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_nurses["Country Name"]=dataset_nurses["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_nurses["Country Name"]=np.where(dataset_nurses["Country Code"]=="ESP","Spain",dataset_nurses["Country Name"] )
dataset_nurses['is_eu']=dataset_nurses["Country Name"].apply(lambda x: country_checker(x))
dataset_nurses=dataset_nurses[dataset_nurses["is_eu"]==True]
countries_unique= list(dataset_nurses["Country Name"].unique())
dataset_nurses=dataset_nurses[["Country Name","2014","2015", "2016"]]

# By looking at description of dataset you find if there are any null values
dataset_nurses.describe()
# Filling up missing values (NULL) with value from the previous year
dataset_nurses["2016"] = np.where(dataset_nurses["2016"].isnull(), dataset_nurses["2015"], dataset_nurses["2016"])
dataset_nurses=dataset_nurses[["Country Name", "2016"]]
dataset_nurses=dataset_nurses.rename(columns={"Country Name":"country", "2016": "nurses"})

"""CLEANING PHYSICIANS DATASET
"""
dataset_physicians["Country Name"]=dataset_physicians["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_physicians["Country Name"]=dataset_physicians["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_physicians["Country Name"]=np.where(dataset_physicians["Country Code"]=="ESP","Spain",dataset_physicians["Country Name"] )
dataset_physicians['is_eu']=dataset_physicians["Country Name"].apply(lambda x: country_checker(x))
dataset_physicians=dataset_physicians[dataset_physicians["is_eu"]==True]
countries_unique= list(dataset_physicians["Country Name"].unique())
dataset_physicians=dataset_physicians[["Country Name","2014","2015", "2016"]]

# By looking at description of dataset you find if there are any null values
dataset_physicians.describe()   
# Filling up missing values (NULL) with value from the previous year
dataset_physicians["2016"] = np.where(dataset_physicians["2016"].isnull(), dataset_physicians["2015"], dataset_physicians["2016"])
dataset_physicians=dataset_physicians[["Country Name","2016"]]
dataset_physicians=dataset_physicians.rename(columns={"Country Name":"country", "2016": "physicians"})

"""
---------------------------- MERGING INDEPENDABLE VARIABLES DATASETS HOSPITAL BEDS, NURSES, PHYSICIANS------------------------------
"""

dataset = dataset_physicians.merge(dataset_nurses, how="left", on="country")
dataset = dataset.merge(dataset_hospital_beds, how="left", on="country")
dataset.to_csv("dataset_healthcare_cleaned.csv", index=False)



