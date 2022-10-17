# ABCal <img align="right" src="https://user-images.githubusercontent.com/85708751/176286890-15060001-79ba-4035-a815-e8cf821cec86.png"> 

#   
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
python ABCal.py
```
or
```
python setup.py install
python -m abcal
```
-> This option will install the relevant dependencies automatically

A pre-compiled stand-alone Windows executable is also available.
