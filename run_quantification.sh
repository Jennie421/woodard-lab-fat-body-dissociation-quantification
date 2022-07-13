#!/bin/bash

# start by getting the absolute path to the directory this script is in, which will be the top level of the repo
# this way script will work even if the repo is downloaded to a new location, rather than relying on hard coded paths to where I put the repo. 
repo_root=$PWD
export repo_root
echo "repo root is $repo_root"

# Take command line argument as study name variable 
study=$1
export study

# Default mmetadata path 
metadata_loc=$repo_root/"$study"/metadata/
export metadata_loc

func_root="$repo_root"/functions_called/

study_loc=$repo_root/"$study"

# Let user know script is starting
echo ""
echo "Beginning script - fat body quantification for:"
echo "$study"
echo ""

# Add current time for runtime tracking purposes
now=$(date +"%T")
echo "Current time: ${now}"
echo ""


# Make a folder for output if it doesn't already exist
if [[ ! -d $metadata_loc ]]; then
	mkdir $metadata_loc
fi

# Remove old metadata file if exists. Avoid concatonation error. 
if [[ -f $metadata_loc/study_wide_metadata.csv ]]; then
	rm $metadata_loc/study_wide_metadata.csv
	echo "removing old metadata"
fi


# Run the script
echo "******************* Generating scattered plots for each genotype *******************"
# switch to study folder
cd "$study"/area_data

for g in *; do
	cd "$g"
	# Make a subfolder to save individual results 
	if [[ ! -d results ]]; then
		mkdir results
	fi
	python /Users/test/woodard-lab-fat-body-dissociation-quantification/functions_called/quantification.py "$study" "$g"
	echo "Completed analysis for $g"
	
	cd ../  # back out of folder for next loop
done 

echo ""
cd $repo_root

echo "******************* Generating study-wide summary *******************"
# switch to output folder 
cd $metadata_loc
python "$func_root"/study_wide_analysis.py "$metadata_loc" 
echo ""


# Add current time for runtime tracking purposes
now=$(date +"%T")
echo "Current time: ${now}"
echo ""


# Script wrap up - unset environment variables so doesn't mess with future scripts
unset genotype
unset study
echo "=============Script Terminated============="
echo ""