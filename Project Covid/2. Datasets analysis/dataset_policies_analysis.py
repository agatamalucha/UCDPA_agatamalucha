# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


#matplotlib.use('Agg')

dataset_policies=pd.read_csv("dataset_policies_cleaned.csv")

# dataset characteristics
print(dataset_policies.columns )
#Index(['country', 'date', 'school_closures','restrictions_internal_movements'],dtype='object')

# Dataset statistics
dataset_policies.info()

# Number of days in each level of school closure restrictions
dataset_policies_schools = dataset_policies
dataset_policies_schools['school_closures'] = dataset_policies_schools['school_closures'].apply(str)
dataset_policies_schools['level_0_days'] = dataset_policies_schools.groupby('country')['school_closures'].transform(lambda x: x[x.str.contains('0')].count())
dataset_policies_schools['level_1_days'] = dataset_policies_schools.groupby('country')['school_closures'].transform(lambda x: x[x.str.contains('1')].count())
dataset_policies_schools['level_2_days'] = dataset_policies_schools.groupby('country')['school_closures'].transform(lambda x: x[x.str.contains('2')].count())
dataset_policies_schools['level_3_days'] = dataset_policies_schools.groupby('country')['school_closures'].transform(lambda x: x[x.str.contains('3')].count())
dataset_policies_schools.columns
dataset_policies_schools = dataset_policies_schools[['country', 'level_0_days', 'level_1_days', 'level_2_days','level_3_days']]
dataset_policies_schools = dataset_policies_schools.drop_duplicates()




# Number of days in each level of internal movement restrictions
dataset_policies_travel = dataset_policies
dataset_policies_travel['restrictions_internal_movements'] = dataset_policies_travel['restrictions_internal_movements'].apply(str)
dataset_policies_travel['level_0_days'] = dataset_policies_travel.groupby('country')['restrictions_internal_movements'].transform(lambda x: x[x.str.contains('0')].count())
dataset_policies_travel['level_1_days'] = dataset_policies_travel.groupby('country')['restrictions_internal_movements'].transform(lambda x: x[x.str.contains('1')].count())
dataset_policies_travel['level_2_days'] = dataset_policies_travel.groupby('country')['restrictions_internal_movements'].transform(lambda x: x[x.str.contains('2')].count())
dataset_policies_travel.columns
dataset_policies_travel = dataset_policies_travel[['country', 'level_0_days', 'level_1_days', 'level_2_days']]
dataset_policies_travel = dataset_policies_travel.drop_duplicates()

dataset_policies_schools.to_csv("dataset_policies_schools_cleaned.csv", index=False)
dataset_policies_travel.to_csv("dataset_policies_travel_cleaned.csv", index=False)


# Creating heatmap  Number of Days of each country in  certain level of lockdown  (0,1,2,3) 0-no lockdown 3-highest restriction
data = dataset_policies.iloc[:,0:3]
dataset = data.groupby(["country", "school_closures", ]).agg({"date": "count"})

dataset["tuple"] = dataset.index
dataset["country"] = dataset["tuple"].str[0]
dataset["level"] = dataset["tuple"].str[1]
dataset["days_count"] = dataset["date"]
dataset = dataset[["country", "level", "days_count"]]
dataset = dataset.pivot(index="level", columns="country", values="days_count")

plt.rcParams['figure.figsize'] = (15.0, 7.0)
f = sns.heatmap(dataset, cmap="coolwarm", annot=False)
f.set_title("School closures - Total number of days in each level of restriction", y=1.05)
plt.show(f)













































