# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 22:37:23 2022

@author: LS Le Clercq
"""
import pandas as pd
import numpy as np
from scipy.stats import shapiro 

print('ABC: Author Bias Computation (1.0.1)')
print('Copyright (C) 2022 Le Clercq')
print('This is free software.  There is NO warranty; not even for',
      'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.')
print()

def menu_choice():
    """ Find out what the user wants to do next. """
    print("MAIN MENU:")
    print("----------------------------------------")
    print("Choose one of the following options?")
    print("   a) Calculate Author bias")
    print("   b) Normalise Author bias")
    print("   c) Check normality of Author bias distribution")
    print("   d) Get upper/lower quartiles of Author bias")
    print("   q) Quit")
    print("----------------------------------------")
    choice = input("Choice: ")
    print()
    if choice.lower() in ['a','b','c','d','q']:
        return choice.lower()
    else:
        print(choice +"?")
        print("Invalid option")
        print()
        return None

def AuthorBias():
    ''''Calculates the abundance of contributions from the same author to
    test for possible bias'''
    infile = input("Authors file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Authors = pd.read_csv(infile)
    length = len(Authors)+1
    Author_list = list(Authors.iloc[0,1:length])
    rows = len(Authors.index)
    Num = 1
    for i in range(1,rows):
        AuthorAdd = Authors.iloc[i, 1:length]
        Add = list(AuthorAdd)
        Num = Num + 1
        Author_list = Author_list + Add
        Author_list = list(Author_list)
    Cleaned_Authors = [x for x in Author_list if str(x) != 'nan']
    Author_list_Unique = list(set(Cleaned_Authors))
    AuthorDF = pd.DataFrame(columns = ['Author','Pubs'])
    for x in Author_list_Unique:
        occurrence = Cleaned_Authors.count(x)
        AuthorDF = AuthorDF.append({'Author': x, 'Pubs':occurrence}, ignore_index=True)
    Sum = AuthorDF['Pubs'].sum()
    Normlist = []
    for x in AuthorDF['Author']:
        PubsNorm = AuthorDF['Pubs']/Sum
        Normlist = list(PubsNorm)
    AuthorDF['Pubs.Norm'] = Normlist
    length_2 = len(AuthorDF.index)
    for i in range(0, length_2):
        old_value = AuthorDF.iloc[i]['Author']
        new_value = AuthorDF.iloc[i]['Pubs.Norm']
        Authors.replace(to_replace=old_value, value=new_value, inplace=True)
    Bias = Authors.sum(axis=1)
    Authors['Bias'] = Bias
    output_name = input("File name (.csv) for calculated values: ")
    if output_name.endswith('.csv') is True:
        pass
    elif output_name.endswith('.csv') is False:
        output_name = output_name + '.csv'
    Authors.to_csv(output_name, index=False)
    print()
    print()
     
def normalize():
    ''''Normalize to Author number'''
    infile = input("Authors with bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv' 
    Authors = pd.read_csv(infile)
    length = len(Authors) + 1
    for i in range(1,len(Authors.index)):
        Author_list = list(Authors.iloc[i][1:length])
        Author_list = [x for x in Author_list if str(x) != 'nan']
        Auth_num = len(Author_list)
        for x in Authors['Paper']:
            PubsNorm_1 = Authors['Bias']/Auth_num
            PubsNorm_2 = list(PubsNorm_1)
    Authors['Norm.Bias'] = PubsNorm_2
    output_name = input("File name (.csv) for normalized values: ")
    if output_name.endswith('.csv') is True:
        pass
    elif output_name.endswith('.csv') is False:
        output_name = output_name + '.csv'
    Authors.to_csv(output_name, index=False)
    print()
    print()
        
def check_norm():
    '''Verify normal distribution'''
    infile = input("Authors with bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv' 
    Data = pd.read_csv(infile)
    Bias = Data['Bias.Norm']
    Normality = shapiro(Bias)
    Statistic = Normality.statistic
    PValue = Normality.pvalue
    file = open('Normality.txt','w')
    file.write('Test of Normality:\n')
    file.write('--------------------\n')
    file.write('Shapiro-Wilk: ' + "{:.3f}".format(Statistic) + '\n')
    if PValue <= 0.01:
        file.write('P-value: ' + str(PValue) + ' ***\n')
        file.write('Result: Not Normal')
    elif PValue <= 0.02:
        file.write('P-value: ' + str(PValue) + ' **\n')
        file.write('Result: Not Normal')
    elif PValue <= 0.05:
        file.write('P-value: ' + str(PValue) + ' *\n')
        file.write('Result: Not Normal')
    elif PValue > 0.05:
        file.write('P-value: ' + str(PValue) + '\n')
        file.write('Result: Normal')
    file.close()
    print()
    print()
    
def get_quantiles():
    '''Get the quantiles and determine level of bias'''
    infile = input("Authors with bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv' 
    Data = pd.read_csv(infile)
    Bias = Data['Norm.Bias']
    Quantiles = np.quantile(Bias, [0,0.33,0.5,0.66,1])
    Upper = Quantiles[3]
    Lower = Quantiles[1]
    #print('The quantiles are:', Quantiles)
    file = open('Quantiles.txt','w')
    file.write('The Quatiles are:\n')
    file.write('--------------------\n')
    file.write('\n')
    file.write('Min  ' + "{:.4f}".format(Quantiles[0]) + '\n')
    file.write('Max: ' + "{:.4f}".format(Quantiles[4]) + '\n')
    file.write('\n')
    file.write('Q33: ' + "{:.4f}".format(Quantiles[1]) + '\n')
    file.write('Q50: ' + "{:.4f}".format(Quantiles[2]) + '\n')
    file.write('Q66: ' + "{:.4f}".format(Quantiles[3]) + '\n')
    file.write('\n')
    file.write('The Levels are:\n')
    file.write('--------------------\n')
    file.write('\n')
    file.write('Low:     ' + "{:.4f}".format(Quantiles[0]) + ' to ' + "{:.4f}".format(Quantiles[1]) + '\n')
    file.write('Medium:  ' + "{:.4f}".format(Quantiles[1]) + ' to ' + "{:.4f}".format(Quantiles[3]) + '\n')
    file.write('High:    ' + "{:.4f}".format(Quantiles[3]) + ' to ' + "{:.4f}".format(Quantiles[4]))
    file.close()
    Level = []
    len(Bias)
    for items in Bias:
        value = items
        if value >= Upper:
            Add = 'High'
            Level.append(Add)
        elif value <= Lower:
            Add = 'Low'
            Level.append(Add)
        else:
            Add = 'Medium'
            Level.append(Add)             
    Data['Level'] = Level
    output_name = input("File name (.csv) for quantile leveled values: ")
    if output_name.endswith('.csv') is True:
        pass
    elif output_name.endswith('.csv') is False:
        output_name = output_name + '.csv'
    Data.to_csv(output_name, index=False)
    print()  
    print()
    
def main_loop():
    """The main loop of the script"""
    while True:
        choice = menu_choice()
        if choice is None:
            continue
        elif choice == 'q':
            print( "Exiting...")
            break     # jump out of while loop
        elif choice == 'a':
            AuthorBias()
        elif choice == 'b':
            normalize()
        elif choice == 'c':
            check_norm()
        elif choice == 'd':
            get_quantiles()
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main_loop()
    