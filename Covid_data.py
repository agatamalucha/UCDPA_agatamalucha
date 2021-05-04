# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:30:32 2021

@author: agata
"""
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt  # imports necessery functions for charts
import seaborn as sb
from pandas import DataFrame
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


"""
error_bad_lines=False 
"""

# CASES AND DEATHS
url='https://covid19.who.int/WHO-COVID-19-global-data.csv'  # https://covid19.who.int/info/
urlretrieve(url,'file.csv')
df=pd.read_csv('file.csv', sep=';') 

dataset_daily_worldwide=pd.read_csv("WHO-COVID-19-global-data.csv")
dataset_europe=dataset_daily_worldwide[dataset_daily_worldwide["WHO_region"]=="EURO"]

dataset_europe.head()
dataset_europe.info()
dataset_europe.describe()

europe=[]










#TESTING
dataset_testing = pd.read_excel("Daily_testing.xlsx")         #https://www.ecdc.europa.eu/en/publications-data/covid-19-testing


# HOSPITAL BEDS     #  https://data.worldbank.org/indicator/SH.MED.PHYS.ZS
dataset_hopital_beds= pd.read_csv("API_SH.MED.BEDS.ZS_DS2_en_csv_v2_2253154.csv" )


# HEALTH CARE WORKERS ( PHYSICIANS + NURSES AND MIDWIVES)    
dataset_nurses_midwifes= pd.read_csv("API_SH.MED.NUMW.P3_DS2_en_csv_v2_2253161.csv" )  #https://data.worldbank.org/indicator/SH.MED.NUMW.P3?end=2018&start=1960
dataset_physicians=pd.read_csv("API_SH.MED.PHYS.ZS_DS2_en_csv_v2_2252675.csv")        #https://data.worldbank.org/indicator/SH.MED.PHYS.ZS?end=2018&start=1960

#POPULATION               #https://data.worldbank.org/indicator/SP.POP.TOTL?locations=EU
dataset_population=pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_2252106.csv")

#GDP per capita  https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?end=2019&locations=EU&start=1970&view=chart
dataset_per_capita=pd.read_csv("API_NY.GDP.PCAP.CD_DS2_en_csv_v2_2252129.csv")

#POPULATION DENSITY    https://data.worldbank.org/indicator/EN.POP.DNST     ( People per sqr. km)
dataset_population_density =pd.read_csv("API_EN.POP.DNST_DS2_en_csv_v2_2253141.csv")

# AGE MEDIAN

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

    
df = pd.DataFrame(lst)
df.columns=["Country", "Median age in years", "Population under 20 years old", "Life expectancy"]


#POLICY RESPONSES            #https://ourworldindata.org/policy-responses-covid
dataset_schools=pd.read_csv("school-closures-covid.csv")
dataset_internal_movement=pd.read_csv("internal-movement-covid.csv")
datset_change_retail_recreation=pd.read_csv("change-visitors-retail-recreation.csv")


#dataset_daily_cases_EU=pd.read_csv("data.csv")                               #https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country
#dataset_daily_cases_EU_till_Dec_14=pd.read_csv("data_till_2020_12_14.csv")    #https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide



#Vaccination
dataset_vaccination=pd.read_csv("daily-covid-vaccination-doses-per-capita.csv")