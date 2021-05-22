# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

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
DATA SOURCE:                https://data.worldbank.org/indicator/SP.POP.TOTL?locations=EU
Dataset that contains population of each country  
"""
# Please note that csv files downloaded from worldbank website had a non relevant header in first  4 rows and  I have removed them manually from the files.
# I haven't  used  skiprows=4 parameter in pd.read_csv method , but I am aware of this .
dataset_population=pd.read_csv("dataset_population.csv")

"""
DATA SOURCE:                https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?end=2019&locations=EU&start=1970&view=chart
Dataset that contains GDP per capita of each country  
"""
dataset_gdp=pd.read_csv("dataset_gdp.csv")

"""
DATA SOURCE: SCRAPED DATA- MEDIAN AGE   https://www.worlddata.info/average-age.php
"""

# Extracting website data and saving it to Dataframe
url = "https://www.worlddata.info/average-age.php"
r=requests.get(url)
text=r.text
soup = BeautifulSoup(text, 'lxml')


lst = []
for row in soup.find_all('tr'):  
    cells = row.find_all('td')
    cell_lst = []
    for element in cells:
        txt = element.text
        cell_lst.append(txt)
    lst.append(cell_lst)    

    
dataset_median_age = pd.DataFrame(lst)
dataset_median_age.columns=["Country", "Median age in years", "Population under 20 years old", "Life expectancy"]

"""
---------------------------- CLEANINIG DATASETS -------------------------------
"""

"""
CLEANING POPULATION DATASET
"""

# Replace country names to match country names in main Covid  dataset      file: dataset_covid_cleaned.csv
dataset_population["Country Name"]=dataset_population["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_population["Country Name"]=dataset_population["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_population["Country Name"]=np.where(dataset_population["Country Code"]=="ESP","Spain",dataset_population["Country Name"] )
dataset_population['is_eu']=dataset_population["Country Name"].apply(lambda x: country_checker(x))
dataset_population=dataset_population[dataset_population["is_eu"]==True]
dataset_population=dataset_population[["Country Name", "2019"]]
dataset_population=dataset_population.rename(columns={"Country Name":"country", "2019":"population"})


"""
CLEANING GDP DATASET
"""
# Replace country names to match country names in main Covid  dataset      file: dataset_covid_cleaned.csv 
dataset_gdp["Country Name"]=dataset_gdp["Country Name"].str.replace("Czech Republic", "Czechia")
dataset_gdp["Country Name"]=dataset_gdp["Country Name"].str.replace("Slovak Republic", "Slovakia")
dataset_gdp["Country Name"]=np.where(dataset_gdp["Country Code"]=="ESP","Spain",dataset_gdp["Country Name"] )
dataset_gdp['is_eu']=dataset_gdp["Country Name"].apply(lambda x: country_checker(x))
dataset_gdp=dataset_gdp[dataset_gdp["is_eu"]==True]
dataset_gdp=dataset_gdp[["Country Name", "2019"]]
dataset_gdp=dataset_gdp.rename(columns={"Country Name":"country", "2019":"gdp"})

"""
CLEANING MEDIAN AGE DATASET
"""

# Checking if there is data for all 27 countries by comparing lists eu_countries and countries in dataset_median_age
countries=list(dataset_median_age["Country"])      # Cyprus Lithuania Slovakia

for element in eu_countries:
    if element in countries:
        print ("In list")
    else:
        print (element)
        
# Data is missing for 3 EU countries, missing values filled manually with accual data from websites.
# Cyprus 2015=34.9 closes median age to our median dataset (2013)   https://www.worldometers.info/world-population/cyprus-population/ 
# Slovakia   2015= 39.2                                             https://www.worldometers.info/world-population/slovakia-population/
# Lithuania  2018=43.7                                              https://en.wikipedia.org/wiki/List_of_countries_by_median_age
 
# Creating list of missing countries data
missing_countries_data=[["Cyprus", "34.9"],["Slovakia","39.2" ] , ["Lithuania","43.7"]]
# Converting Dataframe from list of lists
missing_countries_data=pd.DataFrame.from_records(missing_countries_data, columns=["Country", "Median age in years"])
#  Using iloc function to slice dataset by column , as we only need Country and Median age columns
dataset_median_age=dataset_median_age.iloc[:,0:2]
dataset_full_countries = pd.concat([missing_countries_data, dataset_median_age])
dataset_full_countries =dataset_full_countries.rename(columns={"Country":"country","Median age in years":"median age in years" })

"""
---------------------------- MERGING INDEPENDABLE VARIABLES DATASETS POPULATION, GDP, MEDIAN AGE------------------------------
"""

dataset=dataset_population.merge(dataset_gdp, on="country").merge(dataset_full_countries, on="country")   

dataset.to_csv("dataset_economical_cleaned.csv", index=False)


























