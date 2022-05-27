#!/usr/bin/env python
# coding: utf-8

'''For Users'''
"""
Make sure the name of each csv file is in the below format: 
genotype_temperature_starttime_endtime_date
E.g. WT_30c_0905_1755_20220207
"""

'''Modify the below variables to match your setting'''
# Exactly as in the file name
genotype1 = "Dilp5-Shi"
genotype2 = "Dilp5-TrpA1"
genotype3 = "WT"
# The relative location where the csv files are 
directory = "demo files"



'''For Admin Only'''
# Import Libraries 
import sys
print(sys.executable)

import pandas as pd
import os
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


''' 
A function that performs area calculation. 
'''
def area_cal(name):
    df = pd.read_csv(name)
    total = sum(df['Area'])

    dissociated = sum(x for x in df["Area"] if x < 10000) 
    percent_dissociation = dissociated/total * 100
    result = round(percent_dissociation, 2) # round up  

    return result


''' 
A function that performs time calculation. 
'''
def time_cal(s):
    s = s.split('_')
    date = s[4]
    start = s[2]
    end = s[3]

    start_time = [int(o) for o in [date[:4], date[4:6], date[6:], start[:2], start[2:]]]
    start_date_obj = datetime.datetime(*start_time)
    
    end_time = [int(o) for o in [date[:4], date[4:6], date[6:], end[:2], end[2:]]]
    end_date_obj = datetime.datetime(*end_time) 

    if end_date_obj < start_date_obj: 
        end_date_obj += datetime.timedelta(days=1)

    duration = (end_date_obj - start_date_obj).total_seconds()/3600 # duration in hours 

    return duration


''' 
A function that perform regression analysis. 
It takes a data frame of a genotype and title
and returns a linear model plot. 
'''
def plot(df, title): 
    correlation = df["APF"].corr(df['Dissociation']).round(2)
    # get coeffs of linear fit
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['APF'],df['Dissociation'])
    lm_plot = sns.regplot( x="APF", y="Dissociation", data=df, line_kws={'label':"y={0:.1f}x+{1:.1f}".format(slope,intercept)} )
    lm_plot.legend(loc="upper left") # plot legend
    plt.axis([0,16,0,80])
    plt.text(x=10, y=3, s=f"r = {correlation}")
    plt.title(title)
    plt.savefig(f"Scatterplot_With_Regression_Fit_{title}.png")
    return lm_plot


'''Main Script'''

# Initialize a data set 
data = {'Genotype': [],
        'Temp': [],
        'APF': [],
        'Dissociation': [],
        'Original file': []}

# Extract genotype, temperature, APF from files
for file in os.listdir(directory):
    if file.endswith(".csv"):
        data['Dissociation'] += [area_cal(directory + '/' + file)]
        
        filename = file.split("_") # separate string into components 
        data['Genotype'] += [filename[0]]
        data['Temp'] += [filename[1]]
        data['APF'] += [time_cal(file.split('.')[0])] # calculate duration 

        data['Original file'] += [file] # add the original file name 

# Export a summary of results
df = pd.DataFrame(data).sort_values(by="APF")
df.to_csv('summary.csv')

# Establish df for each genotype 
df_genotype1 = df[df["Genotype"]==genotype1]
df_genotype2 = df[df["Genotype"]==genotype2]
df_genotype3 = df[df["Genotype"]==genotype3]

# Generate plots  
plot(df_genotype1, genotype1)
plot(df_genotype2, genotype2)
plot(df_genotype3, genotype3)

