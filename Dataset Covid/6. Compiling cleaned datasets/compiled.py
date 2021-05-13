# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:33:44 2021

@author: agata
"""


import pandas as pd
import numpy as np

"""
---------- OPENING MAIN COVID DATASET (INDEPENDABLE VARIABLE) -----------------
"""
dataset_covid_cleaned = pd.read_csv("dataset_covid_cleaned.csv", encoding="utf-8")


"""
---------- OPENING ALL CLEANED SUB DATASETS -----------------
"""

dataset_economical = pd.read_csv("dataset_economical_cleaned.csv", encoding="utf-8")
dataset_healthcare_cleaned = pd.read_csv("dataset_healthcare_cleaned.csv", encoding="utf-8")
dataset_policies_cleaned = pd.read_csv("dataset_policies_cleaned.csv", encoding="utf-8")

"""
----- MERGING ALL CLEANED DATASETS INTO ONE DATASET-------------------------------
"""

dataset = dataset_covid_cleaned.merge(dataset_economical, how="left", on=["date", "country", "cases", "deaths"])
dataset = dataset.merge(dataset_healthcare_cleaned, how="left", on=["date", "country", "cases", "deaths"])
dataset = dataset.merge(dataset_policies_cleaned, how="left", on=["date", "country", "cases", "deaths"])





dataset.to_csv("dataset_covid_compiled.csv", index = False)
