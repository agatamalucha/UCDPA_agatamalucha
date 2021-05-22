# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:33:44 2021

@author: agata
"""


import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.offline import plot
from sklearn import preprocessing



"""
---------- OPENING MAIN COVID DATASET (DEPENDABLE VARIABLE) -----------------
"""
dataset_covid_cleaned = pd.read_csv("dataset_covid_cleaned.csv", encoding="utf-8")

total_cases_by_date = dataset_covid_cleaned.groupby('date').agg(sum)
total_cases_countries = dataset_covid_cleaned.groupby('country').agg(sum)

"""
---------- OPENING ALL CLEANED SUB DATASETS -----------------
"""

dataset_economical = pd.read_csv("dataset_economical_cleaned.csv", encoding="utf-8")
dataset_healthcare_cleaned = pd.read_csv("dataset_healthcare_cleaned.csv", encoding="utf-8")
dataset_policies_schools_cleaned = pd.read_csv("dataset_policies_schools_cleaned.csv", encoding="utf-8")
dataset_policies = pd.read_csv("dataset_policies_cleaned.csv")
"""
----- VISUALISATION COUNTRY GDP per capita  vs. TOTAL COVID CASES PER 10000 population-------------
"""
dataset = total_cases_countries.merge(dataset_economical, how="left", on=[ "country",])
dataset['total cases per 10000']= (dataset['cases'] * 10000) /dataset['population']
dataset = dataset.sort_values('total cases per 10000', ascending=False)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
g = sns.barplot(y='total cases per 10000', x='country', data=dataset, order=dataset.sort_values('total cases per 10000', ascending=False).country, ax= ax1, alpha=0.5, color='#bb3f3f')
g.set_xticklabels( labels=dataset['country'], rotation=90)
g=ax1.yaxis.label.set_color("#bb3f3f")
h = sns.barplot(x="country", y="gdp", data=dataset, ax=ax2, color='#3399FF', alpha=0.7)
h=ax2.yaxis.label.set_color("#3399FF")
fig.suptitle("Total COVID cases in EU vs. GDP per capita")                        

"""
----- VISUALISATION COUNTRY Median age  vs.TOTAL COVID DEATHS PER 10000 population-------------
"""
dataset = total_cases_countries.merge(dataset_economical, how="left", on=[ "country",])
dataset['total deaths per 10000']= (dataset['deaths'] * 10000) /dataset['population']
dataset = dataset.sort_values('total deaths per 10000', ascending=False)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()   
g = sns.barplot(x="country", y="median age in years", data=dataset, order=dataset.sort_values('median age in years', ascending=False).country, ax= ax1, alpha=0.5, color='#bb3f3f')
g.set_xticklabels( labels=dataset['country'], rotation=90)
g=ax1.yaxis.label.set_color("#bb3f3f")
h = sns.barplot(y='total deaths per 10000', x='country', data=dataset, ax=ax2, color='#3399FF')
h=ax2.yaxis.label.set_color("#3399FF")
fig.suptitle("Total COVID deaths in EU counties vs. Median age EU country ")
plt.show()

"""
----- VISUALISATION SCHOOLS CLOSURE vs. TOTAL DAYS IN EACH LEVEL OF RESTRICTIONS-------------
"""
dataset = dataset_policies_schools_cleaned.merge(dataset_economical, how="left", on=[ "country",]).merge(total_cases_countries, how="left", on=[ "country",] )
dataset['total deaths per 10000']= (dataset['deaths'] * 10000) /dataset['population']
dataset = dataset.sort_values('total deaths per 10000', ascending=False)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()   
g = sns.barplot(y='total deaths per 10000', x='country', data=dataset, order=dataset.sort_values('total deaths per 10000', ascending=False).country, ax= ax1, alpha=0.5, color='#bb3f3f')
g.set_xticklabels( labels=dataset['country'], rotation=90)
g=ax1.yaxis.label.set_color("#bb3f3f")
h = sns.barplot(y='level_3_days', x='country', data=dataset, ax=ax2, color='#3399FF',alpha=0.7)
h=ax2.yaxis.label.set_color("#3399FF")
fig.suptitle('Total COVID deaths in EU counties vs. Total number of days in Level 3 restriction \n School closed requirement')
plt.show()



"""
----- VISUALISATION Time series in Plotly --  Inpact of school closures and movement restrictions vs. Covid cases (NORMALIZED DATA )-------------
"""

# Sum total number of Covid cases by day in whole EU
dataset_europe_cases = dataset_covid_cleaned.groupby("date").agg({"cases": "sum"})
fig_cases = go.Figure([go.Scatter(x=dataset_europe_cases.index, y=dataset_europe_cases["cases"])])

# For each day I sum the level of school closure and internal movement  in whole EU -
# higher number -more severe lockdown in EU , lower number- more open economy in EU
dataset_school_closures_sum = dataset_policies.groupby("date").agg({"school_closures": "sum"})
dataset_movement_restrictions_sum = dataset_policies.groupby("date").agg({"restrictions_internal_movements": "sum"})
dataset_policies_sum = dataset_school_closures_sum.merge(dataset_movement_restrictions_sum, left_index=True, right_index=True, how="left")
dataset_policies_sum["restrictions_sum"] = dataset_policies_sum["school_closures"] + dataset_policies_sum["restrictions_internal_movements"]

# Merging daily Covid cases with daily level of resttrictions in EU
dataset_cases_and_policies = dataset_europe_cases.merge(dataset_policies_sum, left_index=True, right_index=True, how="left")
dataset_cases_and_policies = dataset_cases_and_policies.fillna("0")

# Normalizing values in range 0-1 to display both lines on the same chart

scaler = preprocessing.MinMaxScaler()
dataset_cases_and_policies[[ 'restrictions_sum', 'cases']] = scaler.fit_transform(dataset_cases_and_policies[['restrictions_sum', 'cases']].values)

# Creating layout and parameters for the plot  
layout = go.Layout(
        title="Inpact of school closures and movement restrictions on flattening Covid cases ",
        shapes=[
            go.layout.Shape(
                type="rect",
                x0="2020-03-20",
                y0=0,
                x1="2020-05-01",
                y1=1.2,
                fillcolor="blue", 
                opacity=0.05, 
                line_width=0,
                
            ),
            go.layout.Shape(
                type="rect",
                x0="2020-10-30",
                y0=0,
                x1="2020-11-21",
                y1=1.2,
                fillcolor="red", 
                opacity=0.05, 
                line_width=0,
                
            )
        ],     
        
    )

fig_cases_and_policies = go.Figure([go.Scatter(x=dataset_cases_and_policies.index, y=dataset_cases_and_policies["restrictions_sum"], name="restrictions severity")], layout=layout)
fig_cases_and_policies.add_scatter(x=dataset_cases_and_policies.index, y=dataset_cases_and_policies["cases"], name="covid cases")
plot(fig_cases_and_policies) 

"""
----- VISUALISATION in Plotly NURSES vs. TOTAL DAYS IN EACH LEVEL OF RESTRICTIONS IN EU -------------
"""
# For each EU country  I sum the level of school closure and internal movement restrictions
dataset_school_closures_sum = dataset_policies.groupby("country").agg({"school_closures": "sum"})
dataset_movement_restrictions_sum = dataset_policies.groupby("country").agg({"restrictions_internal_movements": "sum"})
dataset_policies_sum = dataset_school_closures_sum.merge(dataset_movement_restrictions_sum, left_index=True, right_index=True, how="left")
dataset_policies_sum["restrictions_sum"] = dataset_policies_sum["school_closures"] + dataset_policies_sum["restrictions_internal_movements"]

dataset_policies_sum["country"] = dataset_policies_sum.index
dataset_policies_sum = dataset_policies_sum[["country", "restrictions_sum"]]
dataset_policies_sum = dataset_policies_sum.reset_index(drop=True)

# Merging helthcare dataset with restriction of movement.
dataset_restrictions_healthcare = dataset_healthcare_cleaned.merge(dataset_policies_sum, how="left", on="country")

# Normalizing values in range 0-1 to display both lines on the same chart

scaler = preprocessing.MinMaxScaler()
dataset_restrictions_healthcare[['physicians', 'nurses', 'hospital_beds', 'restrictions_sum']] = scaler.fit_transform(dataset_restrictions_healthcare[['physicians', 'nurses', 'hospital_beds', 'restrictions_sum']].values)

dataset_restrictions_healthcare["healthcare_state"] = (dataset_restrictions_healthcare['physicians'] + dataset_restrictions_healthcare['nurses'] + dataset_restrictions_healthcare['hospital_beds']) / 3
# Creating layout and parameters for the plot  
layout = go.Layout(
        xaxis={"title": "Low restrictions  <----- Medium Restrictions ------>   High restrictions",
               "ticks": "outside",
               "showline": True,
               "tickfont": {"size": 12, "color": "#000"},
               "titlefont": {"color": "#000", "size": 14},
               },
        yaxis={"title": " Lower number of staff <----- Nursing Staff ------->   Higher number of staff ",
               "ticks": "outside",
               "showline": True,
               "tickfont": {"size": 12, "color": "#000"},
               "titlefont": {"color": "#000", "size": 14},
               },
         title="Number of nursing staff vs. Severity in restrictions ",
         shapes=[
            go.layout.Shape(
                type="rect",
                x0=0,
                y0=0.5,
                x1=0.5,
                y1=1,
                fillcolor="green", 
                opacity=0.05, 
                line_width=0,
                
            ),
            go.layout.Shape(
                type="rect",
                x0=0.5,
                y0=0,
                x1=1,
                y1=0.5,
                fillcolor="red", 
                opacity=0.05, 
                line_width=0,
                
            )
        ],                        
        
    )

fig = go.Figure(data=go.Scatter(x=dataset_restrictions_healthcare["restrictions_sum"], 
                                y=dataset_restrictions_healthcare["nurses"], 
                                mode='markers+text',  
                                text=dataset_restrictions_healthcare['country'],
                                textposition='top right'), layout=layout)
plot(fig) 

"""
----- VISUALISATION IN PLOTLY --  SCHOOL CLOSURE AND RESTRICTION OF MOVEMENT vs. COVID DEATHS (NORMALIZED DATA )-------------
"""
# Total Covid deaths by country 
dataset_europe_cases = dataset_covid_cleaned.groupby("country").agg({"deaths": "sum"})
dataset_europe_cases["country"] = dataset_europe_cases.index
dataset_europe_cases = dataset_europe_cases[["country", "deaths"]]
dataset_europe_cases = dataset_europe_cases.reset_index(drop=True)

# Merging deaths cases with population column from economical dataset 
dataset_europe_cases = dataset_europe_cases.merge(dataset_economical, how="left", on="country")

# Calculating Covid deaths per capita  
dataset_europe_cases["total_cases_per_capita"] = dataset_europe_cases["deaths"] / dataset_europe_cases["population"]

# For each EU country  I sum the level of school closure and internal movement restrictions
dataset_school_closures_sum = dataset_policies.groupby("country").agg({"school_closures": "sum"})
dataset_movement_restrictions_sum = dataset_policies.groupby("country").agg({"restrictions_internal_movements": "sum"})
dataset_policies_sum = dataset_school_closures_sum.merge(dataset_movement_restrictions_sum, left_index=True, right_index=True, how="left")
dataset_policies_sum["restrictions_sum"] = dataset_policies_sum["school_closures"] + dataset_policies_sum["restrictions_internal_movements"]

dataset_policies_sum["country"] = dataset_policies_sum.index
dataset_policies_sum = dataset_policies_sum[["country", "restrictions_sum"]]
dataset_policies_sum = dataset_policies_sum.reset_index(drop=True)

dataset_restrictions_cases = dataset_europe_cases.merge(dataset_policies_sum, how="left", on="country")
dataset_restrictions_cases = dataset_restrictions_cases[["country", "total_cases_per_capita", "restrictions_sum"]]

# Normalizing values in range 0-1 to display both lines on the same chart

scaler = preprocessing.MinMaxScaler()
dataset_restrictions_cases[['total_cases_per_capita', 'restrictions_sum']] = scaler.fit_transform(dataset_restrictions_cases[['total_cases_per_capita', 'restrictions_sum']].values)

layout = go.Layout(
        xaxis={"title": "Low restrictions  <----- Medium Restrictions ------>   High restrictions",
               "ticks": "outside",
               "showline": True,
               "tickfont": {"size": 12, "color": "#000"},
               "titlefont": {"color": "#000", "size": 14},
               },
        yaxis={"title": " Low <----- Medium number of Covid deaths   -------> High ",
               "ticks": "outside",
               "showline": True,
               "tickfont": {"size": 12, "color": "#000"},
               "titlefont": {"color": "#000", "size": 14},
               },
          title="Covid deaths in each EU country vs. level of restrictions in each country  ",                   
         shapes=[
            go.layout.Shape(
                type="rect",
                x0=0,
                y0=0,
                x1=0.5,
                y1=0.5,
                fillcolor="green", 
                opacity=0.05, 
                line_width=0,
                
            ),
            go.layout.Shape(
                type="rect",
                x0=0.5,
                y0=0.5,
                x1=1,
                y1=1,
                fillcolor="red", 
                opacity=0.05, 
                line_width=0,
                
            )
        ],                        
        
    )

fig = go.Figure(data=go.Scatter(x=dataset_restrictions_cases["restrictions_sum"], 
                                y=dataset_restrictions_cases["total_cases_per_capita"], 
                                mode='markers+text',  
                                text=dataset_restrictions_cases['country'],
                                textposition='top right', marker={"color": "red", "symbol": 2, "size": 6}
                                ), layout=layout)

plot(fig) 

