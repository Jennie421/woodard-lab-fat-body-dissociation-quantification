# Woodard Lab
## fat body dissociation quantification
This repo contains the manuscripts and codes for quantitative assessment of Drosophila fat body dissociation. 

## Step 1: ImageJ 
### Set up 
1. Download ImageJ
2. Open the microscopy image in ImageJ 

### Set scale using the scale bar 
(important for determining the area)

### Thresholding 
1. change image type to 8-bit
2. Go to "tools" - "analyze" - "thresholding"
3. Adjust the threshold until the red area covers desired area. 
4. Click "OK" 
   
### Determine area 
1. now you get an image with only the particles you selected. 
2. Go to "analyze" - "analyze particles" 
3. Click "OK"
4. Rename in the following formate and save the result.csv file: genotype_temperature_starttime_endtime_date. E.g. WT_25c_0905_1755_20220207


## Step 2: Python Script
