![imgbin_scholarship-baresan-university-computer-icons-school-png_2_10](https://user-images.githubusercontent.com/85708751/196565804-57d05bd6-94ee-46ff-a910-879243040207.png) ![image](https://user-images.githubusercontent.com/85708751/196566604-f39ec73a-5074-475f-b763-56bc404a002a.png) <img align="right" src="https://user-images.githubusercontent.com/85708751/176286890-15060001-79ba-4035-a815-e8cf821cec86.png"> 
  
## Author Bias Computation
![Language](https://img.shields.io/badge/Language-Python-yellow)  ![Version](https://img.shields.io/badge/Version-1.0.1-purple) ![Windows](https://img.shields.io/badge/OS-Windows-green) ![License](https://img.shields.io/badge/License-Apache_2.0-red) 
### Introduction
ABCal is a menu-driven module used to calculate and quantify potential author bias in studies included in a review or meta-analysis. The menu guides you through the steps of creating a list of authors from a table of authors for each paper (see Examples) to calculating the number of total articles each author contributed to. The overall author contributions are then summed to determine the level of potential bias in the literature through an over-representation of specific authors.

**Dependencies:**
- Python >= 3.6
- Numpy >= 1.20.1
- Pandas >= 1.2.4
- SciPy >= 1.6.2

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
   b) Normalise Author bias
   c) Check normality of Author bias distribution
   d) Get upper/lower quartiles of Author bias
   q) Quit
----------------------------------------
```
input is given as lower case 'a', 'b', 'c', 'd', or 'q'
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
  
#### b) Normalise Author bias (STEP 2)
- Takes output from STEP 1 as input file and asks for the new output file name e.g. ***Auth_BiasNorm.csv***
- Writes a new column 'Bias.Norm' that reflects the paper author bias (sum) divided by the number of authors on the paper

#### c) Check normality of Author bias distribution (STEP 3)
- Takes output from STEP 2 as input file and writes a new file 'Normality.txt' that contains estimates on if the author bias follows a normal distribution (typically it is not normally distributed in most cases)
```
Test of Normality:
--------------------
Shapiro-Wilk: 0.828
P-value: 7.557426579296589e-05 ***
Result: Not Normal
```
(* p-value<0.05, ** p-value<0.02, *** p-value<0.01)

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
