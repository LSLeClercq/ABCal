![imgbin_scholarship-baresan-university-computer-icons-school-png_2_10](https://user-images.githubusercontent.com/85708751/196565804-57d05bd6-94ee-46ff-a910-879243040207.png) ![image](https://user-images.githubusercontent.com/85708751/196566604-f39ec73a-5074-475f-b763-56bc404a002a.png) <img align="right" src="https://user-images.githubusercontent.com/85708751/176286890-15060001-79ba-4035-a815-e8cf821cec86.png"> 
  
## Author Bias Computation and Scientometric Plotting
![Language](https://img.shields.io/badge/Language-Python-yellow)  ![Version](https://img.shields.io/badge/Version-1.0.2-purple) ![Windows](https://img.shields.io/badge/OS-Windows-green) ![License](https://img.shields.io/badge/License-Apache_2.0-red) 
### Introduction
ABCal is a menu-driven module used to calculate and quantify potential author bias in studies included in a review or meta-analysis. The menu guides you through the steps of creating a list of authors from a table of authors for each paper (see Examples) to calculating the number of total articles each author contributed to. The overall author contributions are then summed to determine the level of potential bias in the literature through an over-representation of specific authors. With the latest update some functionality has been added for plotting various aspects relevant to the scientometrics appraisal of included literature for reviews or meta-analyses, specifically the ability to visualise publications by year and location as well as the top contributing authors.

**Cite as:** Le Clercq, L.S. ABCal: a Python package for Author Bias Computation and Scientometric Plotting for Reviews and Meta-Analyses (2023). _Journal of Informetrics_. [Submitted]

**Dependencies:**
- Python >= 3.6
- Numpy >= 1.20.1
- Pandas >= 1.2.4
- SciPy >= 1.6.2
- Geopy >= 2.3.0
- MatPlotLib >= 3.3.4
- Statsmodels >= 0.12.2
- Folium >= 0.14.0

**Installation:**

After downloading and extracting the zip archive ABCal can be implemented in by navigating to the directory and using one of two methods:
```
python abcal.py
```
or
```
python setup.py install
python -m abcal
```
-> This option will install the relevant dependencies automatically

A pre-compiled stand-alone Windows executable is also available. [![DOI](https://img.shields.io/badge/doi-10.5281/zenodo.7224845-orange)](https://doi.org/10.5281/zenodo.7224845)

### Main menu
The following options are available through the main menu:
```
MAIN MENU:
----------------------------------------
Choose one of the following options?
   a) Calculate Author bias
   b) Calibrate Author bias
   c) Check normality of Author bias distribution
   d) Get upper/lower quartiles of Author bias
   e) Create plots
   f) Get descriptive/summary statistics
   q) Quit
----------------------------------------
```
input is given as lower case 'a', 'b', 'c', 'd', 'e', 'f', or 'q'
e.g.
```
Choice: a
```

#### a) Calculate Author bias (STEP 1)
- Takes table of authors as input e.g. ***Authors.csv***

e.g.

  |Paper|Author_1|Author_2|Author_3|Author_4|
  |---|---|---|---|---|
  |Paper 1|Author A|Author B|Author C|Author D|
  |Paper 2|Author E|Author B|Author D|NaN|
  |Paper 3|Author B|Author F|Author C|Author D|
  
- Asks for output file name for number of publications per author e.g. ***Author_Pubs.csv*** (useful for checking duplicates)
- Asks for output file name e.g. ***Auth_Bias.csv***
- Replaces authors with the proportions of the literature contributed by each author and writes a new column 'Bias' that refects the sum of proportions
  
#### b) Calibrate Author bias (STEP 2)
- Takes output from STEP 1 as input file and asks for the new output file name e.g. ***Auth_BiasNorm.csv***
- Writes a new column 'Bias.Norm' that reflects the paper author bias (sum) divided by the number of authors on the paper

#### c) Check normality of Author bias distribution (STEP 3)
- Takes output from STEP 2 as input file and checks normality in one of 3 ways based on menu choice.
```
NORMALITY MENU:
----------------------------------------
Choose one of the following options?
   a) Shapiro-Wilk
   b) QQ Plot
   c) Histogram
   q) Quit
----------------------------------------
```

##### Option a) Shapiro-Wilk:

- Tests for normality using the Shapiro-Wilk test and writes a new file 'Normality.txt' that contains estimates on if the author bias follows a normal distribution (typically it is not normally distributed in most cases)
```
Test of Normality:
--------------------
Shapiro-Wilk: 0.828
P-value: 7.557426579296589e-05 ***
Result: Not Normal
```
(* p-value<0.05, ** p-value<0.02, *** p-value<0.01)

##### Option b) QQ Plot:

- Plots the theoretical quantile distributions to the sample quantile distribution.

- If blue values fall on red line they follow a normal distribution, if blue values fall on a horizontal line they are evenly distributed.


##### Option c) Histogram:

- Plots the bias estimates by count as a histogram to verify clustering or a possible bell shaped distribution (normal distribution).

e.g.
![Histogram of bias values](https://github.com/LSLeClercq/ABCal/assets/85708751/883a5e07-0b2a-427d-8d2b-190a0e6d3980)

#### d) Get upper/lower quartiles of Author bias (STEP 4)
- Takes output from STEP 2 as input file and writes a new file 'Quantiles.txt' that contains the lower 3rd, middle, and upper 3rd of the normalised bias values
```
The Quatiles are:
--------------------

Min  0.0008
Max: 0.0521

Q33: 0.0081
Q50: 0.0267
Q66: 0.0425

The Levels are:
--------------------

Low:     0.0008 to 0.0081
Medium:  0.0081 to 0.0425
High:    0.0425 to 0.0521
```
- Asks for name of output file e.g. ***Auth_final.csv*** with an added column that indicates the 'Level' of a paricular paper as 'Low' for the lower 3rd, 'Medium' for the middle, and 'High' for the upper 3rd

#### e) Create plots

- Brings up the plots menu for scientometric analyses and visualisation of attributes of included studies.

```
PLOTS MENU:
----------------------------------------
Choose one of the following options?
   a) Plot by Year
   b) Plot by Authors
   c) Plot by Location
   d) Plot z-values of Calibrated Bias
   q) Quit
----------------------------------------
```

##### a) Plot by Year:

- Takes a table/csv ("Studies_Years.csv") as input with a column for the study name (Paper) and a column for the publication time (Year).

e.g.,
|Paper|Year|
|---|---|
|Paper 1|2014|
|Paper 30|2022|
  
- Generates a histogram with the number of publications per year.

e.g.,
![Year Plot](https://github.com/LSLeClercq/ABCal/assets/85708751/fb0700c5-c35a-4139-b932-38b90c9fa3b7)


##### b) Plot by Authors:

- Takes the first table given as output in STEP 1 and returns a plot of the top (N) authors and the number of publications/studies they contributed.

e.g.,
![Author Plot](https://github.com/LSLeClercq/ABCal/assets/85708751/280969ac-8edf-484f-b068-e4ab06be5b5c)

##### c) Plot by Location:

- Takes a table/csv ("Studies_Locations.csv") as input with a column for the study name (Paper) and a column for the study site (Location).

e.g.,
|Paper|Location|
|---|---|
|Paper 1|United States|
|Paper 30|France|
  
- Generates a chloropleth map with the number of publications per country indicated. The lowest is indicated in green and is scaled according to the data with the maximum indicated in red. 

e.g.,
![Location plot](https://github.com/LSLeClercq/ABCal/assets/85708751/f2d4784c-0bde-489d-912b-e921248a7fb5)

##### d) Plot z-values of Calibrated Bias:

- Takes output from calibration step (b) as input.
- Generates a boxplot of the z-score normalised bias estimates for the included publications.

e.g.

![Bias plot](https://github.com/LSLeClercq/ABCal/assets/85708751/e3478a9c-4a0c-417c-b830-8b603e80ae32)

#### f) Get descriptive/summary statistics

- Takes output from author bias calibration step and/or z-value plotting as input.
- Generates descriptive statistics for columns in files.

e.g.,

||Bias|Cal.Bias|Z-Score|
|---|---|---|---|
|count|67|67|67|
|mean|0.023613277|0.004086097|-2.10E-16|
|std|0.01601255|0.002039446|1.007547277|
|min|0.002487562|0.002487562|-0.789723972|
|25%|0.013681592|0.002487562|-0.789723972|
|50%|0.019900498|0.00331675|-0.380080644|
|75%|0.031094527|0.004975124|0.439206012|
|max|0.111940299|0.012437811|4.125995962|

#### q) Quit

- Exits ABCal.

## Publications:

Le Clercq, L.S., Kotzé, A., Grobler, J.P. and Dalton, D.L. Biological clocks as age estimation markers in animals: a systematic review and meta‐analysis (2023). _Biological Reviews_. DOI: [10.1111/brv.12992](https://doi.org/10.1111/brv.12992)

