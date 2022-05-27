# Fat Body Dissociation Quantification

By Jennie Li from Woodard Lab 

This repo contains the manuscripts and codes for quantitative assessment of _Drosophila_ fat body dissociation. 

## Step 1: ImageJ 
### Set up 
1. Download [ImageJ](https://imagej.nih.gov/ij/download.html).
2. Open the microscopy image in ImageJ.

### Calibrate using scale bar 
1. Select "Straight" tool from the tool bar (looks like a line). Draw a line on top of the scale bar (hold Shift to draw a perfect straight line). 
2. Go to "Analyze" - "Set Scale". "Distance in pixels" is the length of the scale bar regarding to the image. In "Known distance", enter the actual distance (E.g. 500). You can change the "Unit of length" to the unit of actual distance (E.g. um). Click "OK". 

### Thresholding 
1. In the tool bar, select "Rectangle". Then use mouse to select the portion of image for analysis, excluding the scale bar or any other labels. Go to "Image" - "Duplicate", and create a new image without any unwanted text. 
2. Go to "Image" - "Type“ - select "8-bit". 
3. Go to "Image" - "Adjust" - "Thresholding". 
4. Drag the first slide bar to adjust the threshold. The red color represents selected area. Make sure the red color nicely covers the particles. 
5. Click "Apply". 
   
### Determine area 
1. Now you get a black & white image with only the particles you selected. 
2. Go to "Analyze" - "Analyze particles". 
3. Click "OK". 
4. Save the output file. Rename it in the following formate and save as .csv file: 
   + genotype_temperature_starttime_endtime_date
   + E.g. WT_25c_0905_1755_20220207
5. These csv files, generated from your microscopy images, are the files used for the following quantification analysis. No need to save other files. 

### Resources for ImageJ
+ [This tutorial](https://www.youtube.com/watch?v=FiFwxoxOmNo&t=826s) is a good demonstration of some features of ImageJ, although it is not tailored to serve our purpose of area quantification. 
  + 1:46 - 4:56 Calibration 
  + 8:35 - 16:08 Thresholding and Measure Area 


## Step 2: Python Script
1. Download the zip file to your local computer. Click the green button "Code" on the upper right corner of this git hub page - "Download ZIP". 
2. Open **terminal**. Type following command: 
   ```
   pip install -r requirement.txt 
   ``` 
3. Put the csv files you want to analyze in a folder, inside the downloaded folder. 
4. Open quantification.py using [Visual Studio Code](https://code.visualstudio.com/?wt.mc_id=vscom_downloads). You only need to modify the section at the top. 
5. Set the **genotype variables** based on your design. For example, I have three csv files, 
   * WT_xx_xxxx_xxxx_xxxxxxxx
   * Dilp5-Shi_xx_xxxx_xxxx_xxxxxxxx
   * Dilp5-TrpA1_xx_xxxx_xxxx_xxxxxxxx
I should set variables genotype1, genotype2, and genotype3 equals to "WT", "Dilp5-Shi", and "Dilp5-TrpA1". **The quotation marks are necessary**. 
5. Set the **variable `directory`** to the relative location of the files you want to analyze. For example, set `directory` equals to "demo files" since my csv files are in the folder called "demo files". 
6. Save your changes. 
7. Go to **terminal**. To run the program, type 
   ```
   python quantification.py
   ``` 
   The program should run and output a "summary.csv" and linear regression plots. 
