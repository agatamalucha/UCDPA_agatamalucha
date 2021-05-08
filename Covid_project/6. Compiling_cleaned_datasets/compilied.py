# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:33:44 2021

@author: agata
"""


import pandas as pd
import numpy as np



dataset_covid_cleaned = pd.read_csv("dataset_covid_cleaned.csv", encoding="utf-8")
dataset_economical = pd.read_csv("dataset_economical_cleaned.csv", encoding="utf-8")
dataset_healthcare_cleaned = pd.read_csv("dataset_healthcare_cleaned.csv", encoding="utf-8")
dataset_policies_cleaned = pd.read_csv("dataset_policies_cleaned.csv", encoding="utf-8")



dataset = dataset_covid_cleaned.merge(dataset_economical, how="left", on=["date", "country", "cases", "deaths"])
dataset = dataset.merge(dataset_healthcare_cleaned, how="left", on=["date", "country", "cases", "deaths"])
dataset = dataset.merge(dataset_policies_cleaned, how="left", on=["date", "country", "cases", "deaths"])


dataset.head()
dataset.info()
dataset.describe()

#       Few negative valuse ref:  https://www.google.com/search?client=firefox-b-d&q=covi+cases+italy+2020   
# values negative changed to 0
dataset["cases"] = np.where(dataset["cases"] < 0, 0, dataset["cases"])
dataset["deaths"] = np.where(dataset["deaths"] < 0, 0, dataset["deaths"])














