
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np

eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 
                'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 
                'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
                'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 
                'Slovenia', 'Spain', 'Sweden']

eu_countries = sorted(eu_countries)


# HOSPITAL BEDS     #  https://data.worldbank.org/indicator/SH.MED.PHYS.ZS
dataset_hospital_beds= pd.read_csv("API_SH.MED.BEDS.ZS_DS2_en_csv_v2_2253154.csv" )


# HEALTH CARE WORKERS ( PHYSICIANS + NURSES AND MIDWIVES)    
dataset_nurses= pd.read_csv("API_SH.MED.NUMW.P3_DS2_en_csv_v2_2253161.csv" )  #https://data.worldbank.org/indicator/SH.MED.NUMW.P3?end=2018&start=1960
dataset_physicians=pd.read_csv("API_SH.MED.PHYS.ZS_DS2_en_csv_v2_2252675.csv")        #https://data.worldbank.org/indicator/SH.MED.PHYS.ZS?end=2018&start=1960


dataset_covid = pd.read_csv("dataset_covid_cleaned.csv")


def country_checker(string):
    if string in eu_countries:
        return True

"""
CLEANING HEALTHCARE DATASETS 
"""
countries_unique= list(dataset_hospital_beds["Country Name"].unique())

# Replace country names 
dataset_hospital_beds["Country Name"]=dataset_hospital_beds["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_hospital_beds["Country Name"]=dataset_hospital_beds["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_hospital_beds["Country Name"]=np.where(dataset_hospital_beds["Country Code"]=="ESP","Spain",dataset_hospital_beds["Country Name"] )


dataset_hospital_beds['is_eu']=dataset_hospital_beds["Country Name"].apply(lambda x: country_checker(x))
dataset_hospital_beds=dataset_hospital_beds[dataset_hospital_beds["is_eu"]==True]
countries_unique= list(dataset_hospital_beds["Country Name"].unique())
dataset_hospital_beds=dataset_hospital_beds[["Country Name", "2017"]]

dataset_hospital_beds=dataset_hospital_beds.rename(columns={"Country Name":"country", "2017": "hospital_beds"})

"""
CLEANING PHYSICIANS 
"""
countries_unique= list(dataset_physicians["Country Name"].unique())

# Replace country names 
dataset_physicians["Country Name"]=dataset_physicians["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_physicians["Country Name"]=dataset_physicians["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_physicians["Country Name"]=np.where(dataset_physicians["Country Code"]=="ESP","Spain",dataset_physicians["Country Name"] )


dataset_physicians['is_eu']=dataset_physicians["Country Name"].apply(lambda x: country_checker(x))
dataset_physicians=dataset_physicians[dataset_physicians["is_eu"]==True]
countries_unique= list(dataset_physicians["Country Name"].unique())
dataset_physicians=dataset_physicians[["Country Name","2014","2015", "2016"]]

dataset_physicians["2016"] = np.where(dataset_physicians["2016"].isnull(), dataset_physicians["2015"], dataset_physicians["2016"])

dataset_physicians=dataset_physicians[["Country Name","2016"]]

dataset_physicians=dataset_physicians.rename(columns={"Country Name":"country", "2016": "physicians"})

"""
CLEANING NURSES 
"""
countries_unique= list(dataset_nurses["Country Name"].unique())

# Replace country names 
dataset_nurses["Country Name"]=dataset_nurses["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_nurses["Country Name"]=dataset_nurses["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_nurses["Country Name"]=np.where(dataset_nurses["Country Code"]=="ESP","Spain",dataset_nurses["Country Name"] )


dataset_nurses['is_eu']=dataset_nurses["Country Name"].apply(lambda x: country_checker(x))
dataset_nurses=dataset_nurses[dataset_nurses["is_eu"]==True]
countries_unique= list(dataset_nurses["Country Name"].unique())
dataset_nurses=dataset_nurses[["Country Name","2014","2015", "2016"]]


dataset_nurses["2016"] = np.where(dataset_nurses["2016"].isnull(), dataset_nurses["2015"], dataset_nurses["2016"])

dataset_nurses=dataset_nurses[["Country Name", "2016"]]

dataset_nurses=dataset_nurses.rename(columns={"Country Name":"country", "2016": "nurses"})




dataset = dataset_covid.merge(dataset_physicians, how="left", on="country")


dataset = dataset.merge(dataset_nurses, how="left", on="country")


dataset = dataset.merge(dataset_hospital_beds, how="left", on="country")



dataset.to_csv("dataset_healthcare_cleaned.csv", index=False)









