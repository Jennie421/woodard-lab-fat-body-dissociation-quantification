
# Import Libraries 
import pandas as pd
import os
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import sys


metadata_loc = os.environ['metadata_loc']


def study_wide_analysis(study):
	# load metadata file 
	try:
		metadata_path = metadata_loc + "study_wide_metadata.csv"
		metadata = pd.read_csv(metadata_path)
	except:
		print("No metadata for current study, returning") # in case this function is called standalone, notify the user if no processed transcripts exist
		return
    
    


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    study_wide_analysis(sys.argv[1])
