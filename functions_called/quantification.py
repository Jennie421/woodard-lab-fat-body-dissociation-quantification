#!/usr/bin/env python
# coding: utf-8

"""
Make sure the name of each csv file is in the below format: 
genotype_temperature_starttime_endtime_date
E.g. W1118_30c_0905_1755_20220207
"""

# Import Libraries 
import pandas as pd
import os
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import sys


metadata_loc = os.environ['metadata_loc']
output_path = "results"

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
def plot(df, title, save_path): 
	correlation = df["APF"].corr(df['Dissociation']).round(2)
	# get coeffs of linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(df['APF'],df['Dissociation'])
	lm_plot = sns.regplot( x="APF", y="Dissociation", data=df, line_kws={'label':"y={0:.1f}x+{1:.1f}".format(slope,intercept)} )
	lm_plot.legend(loc="upper left") # plot legend
	plt.axis([0,16,0,80])
	plt.text(x=10, y=3, s=f"r = {correlation}")
	plt.title(title)
	plt.savefig(save_path)
	return lm_plot


'''Main Script'''
def fat_body_quant(study, genotype): 

	# Initialize a data set 
	data = {'Genotype': [],
			'Temp': [],
			'APF': [],
			'Dissociation': [],
			'Original file': []}

	# Extract genotype, temperature, APF from files
	for file in os.listdir('.'):
		if file.endswith(".csv"):
			data['Dissociation'] += [area_cal(file)]
			filename = file.split("_") # separate string into components 
			data['Genotype'] += [filename[0]]
			data['Temp'] += [filename[1]]
			data['APF'] += [time_cal(file.split('.')[0])] # calculate duration 

			data['Original file'] += [file] # add the original file name 

	# Establish df for each genotype 
	cur_genotype = pd.DataFrame(data).sort_values(by="APF")

	# Export a summary of results
	cur_genotype.to_csv(f'{output_path}/{study}_{genotype}_summary.csv')

	# Generate plots  
	title = f"{genotype} ({cur_genotype.shape[0]} data points plotted)"
	save_path = f"{output_path}/{study}_{genotype}_regression.png"
	plot(cur_genotype, title, save_path)



	# build study-wide summary - add cur genotype to study-wide summary 
	try:
		study_wide_metadata = pd.read_csv(f'{metadata_loc}/study_wide_metadata.csv')
		study_wide_metadata = pd.concat([study_wide_metadata, cur_genotype], ignore_index=True)
	# 	study_wide_metadata.reset_index(drop=True, inplace=True)
	except:
		# if this is the first genotype ever being processed for this study then can just set to be cur_genotype
		# will also hit this exception if concat fails, which should only occur when there is a column mismatch - so if feature set changes
		study_wide_metadata = cur_genotype

	# finally save the new study-wide summary
	study_wide_metadata.to_csv(f'{metadata_loc}/study_wide_metadata.csv', index=False)



if __name__ == '__main__':
	# Map command line arguments to function arguments.
	fat_body_quant(sys.argv[1], sys.argv[2])