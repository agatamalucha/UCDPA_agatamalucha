# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:37:11 2021

@author: agata
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from decimal import Decimal
import matplotlib.cm as cm
from sklearn import preprocessing


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
dataset_policies_travel['count_2_days'] = dataset_policies_travel.groupby('country')['restrictions_internal_movements'].transform(lambda x: x[x.str.contains('2')].count())
dataset_policies_travel.columns
dataset_policies_travel = dataset_policies_travel[['country', 'level_0_days', 'level_1_days', 'level_2_days']]
dataset_policies_travel = dataset_policies_travel.drop_duplicates()





























