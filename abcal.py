# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 22:37:23 2022

@author: LS Le Clercq
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import io
import folium
import scipy.stats as stats
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
from geopy.geocoders import Nominatim
from scipy.stats import shapiro
from folium.plugins import MarkerCluster
from PIL import Image

print('ABC: Author Bias Computation (1.0.2)')
print('Copyright (C) 2023 Le Clercq')
print('This is free software.  There is NO warranty; not even for',
      'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.')
print()

def menu_choice():
    """ Find out what the user wants to do next. """
    print("MAIN MENU:")
    print("----------------------------------------")
    print("Choose one of the following options?")
    print("   a) Calculate Author bias")
    print("   b) Calibrate Author bias")
    print("   c) Check normality of Author bias distribution")
    print("   d) Get upper/lower quartiles of Author bias")
    print("   e) Create plots")
    print("   q) Quit")
    print("----------------------------------------")
    choice = input("Choice: ")
    print()
    if choice.lower() in ['a','b','c','d','e','q']:
        return choice.lower()
    else:
        print(choice +"?")
        print("Invalid option")
        print()
        return None

def author_bias():
    ''''Calculates the abundance of contributions from the same author to
    test for possible bias'''
    infile = input("Authors file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Authors = pd.read_csv(infile)
    length = len(Authors)
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
    output_name = input("File name (.csv) for Author counts: ")
    if output_name.endswith('.csv') is True:
        pass
    elif output_name.endswith('.csv') is False:
        output_name = output_name + '.csv'
    AuthorDF.to_csv(output_name, index=False)
    Sum = AuthorDF['Pubs'].sum()
    Normlist = []
    for x in AuthorDF['Author']:
        PubsNorm = AuthorDF['Pubs']/Sum
        Normlist = list(PubsNorm)
    AuthorDF['Pubs.Norm'] = Normlist
    length_2 = len(AuthorDF.index)
    Names = []
    Values = []
    for i in range(0, length_2):
        old_value = AuthorDF.iloc[i]['Author']
        Names.append(old_value)
        new_value = AuthorDF.iloc[i]['Pubs.Norm']
        Values.append(new_value)
        Authors.replace(to_replace=old_value, value=new_value, inplace=True)
    Individual_bias = pd.DataFrame(list(zip(Names, Values)),
                                           columns = ['Author', 'Ind.Bias']) 
    output_name_2 = input("File name (.csv) for calculated values (Individual): ")
    if output_name_2.endswith('.csv') is True:
        pass
    elif output_name_2.endswith('.csv') is False:
        output_name_2 = output_name_2 + '.csv'
    Individual_bias.to_csv(output_name_2, index=False)
    Bias = Authors.sum(axis=1)
    Authors['Bias'] = Bias
    Authors_Out = pd.DataFrame(Authors, columns=['Paper', 'Bias'])
    output_name_3 = input("File name (.csv) for calculated values (Paper): ")
    if output_name_3.endswith('.csv') is True:
        pass
    elif output_name_3.endswith('.csv') is False:
        output_name_3 = output_name_3 + '.csv'
    Authors_Out.to_csv(output_name_3, index=False)
    print()
    print()

def calibrate():
    ''''Calibrate to Author number'''
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
    Authors['Cal.Bias'] = PubsNorm_2
    output_name = input("File name (.csv) for calibrated values: ")
    if output_name.endswith('.csv') is True:
        pass
    elif output_name.endswith('.csv') is False:
        output_name = output_name + '.csv'
    Authors.to_csv(output_name, index=False)
    print()
    print()

def normality_menu():
    """Brings up the menu options for testing normality"""
    print("NORMALITY MENU:")
    print("----------------------------------------")
    print("Choose one of the following options?")
    print("   a) Shapiro-Wilk")
    print("   b) QQ Plot")
    print("   c) Histogram")
    print("   q) Quit")
    print("----------------------------------------")
    choice = input("Choice: ")
    print()
    if choice.lower() in ['a','b','c','q']:
        return choice.lower()
    else:
        print(choice +"?")
        print("Invalid option")
        print()
        return None

def normality():
    '''Returns function to test normality'''
    choice = normality_menu()
    if choice == 'a':
        check_norm_shapiro()
    if choice == 'b':
        check_norm_QQ()
    if choice == 'c':
        check_norm_histo()

def check_norm_shapiro():
    '''Verify normal distribution by SW'''
    infile = input("Authors with computed bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Data = pd.read_csv(infile)
    Bias = Data['Cal.Bias']
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

def check_norm_QQ():
    '''Plots the QQ plot to check normality'''
    infile = input("Authors with computed bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Data = pd.read_csv(infile)
    Bias = Data['Cal.Bias']
    Bias = Bias.to_frame()
    Values = Bias["Cal.Bias"].values.tolist()
    Values = np.array(Values)
    fig, ax = plt.subplots(figsize =(10, 7))
    plt.rcParams['axes.facecolor'] = '#f2f2f5'
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
    ax.set_facecolor('#f2f2f5')
    ax.set_title("Quantile plot for bias values", fontdict=font, fontsize=20, pad=15)
    ax.set_xlabel("Theoretical quantile", fontdict=font, fontsize=15, labelpad=10)
    ax.set_ylabel("Sample quantile", fontdict=font, fontsize=15, labelpad=10)
    sm.qqplot(Values, line ='45', scale=2, ax=ax)
    fig.savefig('QQ Plot.png')
    
def check_norm_histo():
    '''Plots the histograms to check normality'''
    infile = input("Authors with computed bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Data = pd.read_csv(infile)
    Bias = Data['Cal.Bias']
    Bias = Bias.to_frame()
    Values = Bias["Cal.Bias"].values.tolist()
    Values = np.array(Values)
    fig, ax = plt.subplots(figsize =(10, 7))
    plt.rcParams['axes.facecolor'] = '#f2f2f5'
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
    ax.set_facecolor('#f2f2f5')
    ax.set_title("Histogram of distribution for bias values", fontdict=font, fontsize=20, pad=15)
    ax.set_xlabel("Bias value", fontdict=font, fontsize=15, labelpad=10)
    ax.set_ylabel("Count", fontdict=font, fontsize=15, labelpad=10)
    ax.hist(Values)
    plt.savefig("Histogram of bias values.png")
    print()
    print('Done!')
    print()

def get_quantiles():
    '''Get the quantiles and determine level of bias'''
    infile = input("Authors with bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Data = pd.read_csv(infile)
    Bias = Data['Cal.Bias']
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
    file.write('Low:     ' + "{:.4f}".format(Quantiles[0]) +
               ' to ' + "{:.4f}".format(Quantiles[1]) + '\n')
    file.write('Medium:  ' + "{:.4f}".format(Quantiles[1]) +
               ' to ' + "{:.4f}".format(Quantiles[3]) + '\n')
    file.write('High:    ' + "{:.4f}".format(Quantiles[3]) +
               ' to ' + "{:.4f}".format(Quantiles[4]))
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

def plots_menu():
    """Brings up the menu options for generating plots"""
    print("PLOTS MENU:")
    print("----------------------------------------")
    print("Choose one of the following options?")
    print("   a) Plot by Year")
    print("   b) Plot by Authors")
    print("   c) Plot by Location")
    print("   d) Plot z-values of Calibrated Bias")
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

def plots():
    '''Brings up funtion to call for plot'''
    choice = plots_menu()
    if choice == 'a':
        year_plot()
    if choice == 'b':
        author_plot()
    if choice == 'c':
        location_plot()
    if choice == 'd':
        bias_plot()

def year_plot():
    '''plots publications by year'''
    infile = input("Authors file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Authors = pd.read_csv(infile)
    Years = Authors['Year']
    Papers = Authors['Paper']
    df2 = pd.DataFrame(list(zip(Papers, Years)),
              columns=['Paper','Year'])
    df3 = df2.groupby(['Year']).size()
    YearsData = list(set(Years))
    YearsData = sorted(YearsData)
    fig, ax = plt.subplots(figsize =(16, 10))
    plt.rcParams['axes.facecolor'] = '#f2f2f5'
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
    ax.set_facecolor('#f2f2f5')
    ax.set_title("Publications by year", fontdict=font, fontsize=20, pad=15)
    ax.set_xlabel("Year", fontdict=font, fontsize=15, labelpad=10)
    ax.set_ylabel("Publications", fontdict=font, fontsize=15, labelpad=10)
    ax.bar(YearsData,df3)
    plt.savefig("Year Plot.png")
    plt.show()
    print()
    print("Done!")
    print()

def author_plot():
    """Plots the top Authors for a given analysis"""
    infile = input("Authors file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Authors = pd.read_csv(infile)
    Number = int(input("Number of Authors:  "))
    df4 = Authors[['Author','Pubs']].nlargest(n=Number, columns='Pubs')
    TopAuthors = df4['Author']
    Pubs = df4['Pubs']
    fig_2, ax = plt.subplots(figsize =(16, 9))
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
    colors = ["#e00202", "#de8602", "#49b849", "#4804cc", "#764fc2"]
    ax.barh(TopAuthors, Pubs, color=colors)
    ax.set_facecolor('#f2f2f5')
    ax.set_title("Publications by author", fontdict=font, fontsize=20, pad=15)
    ax.set_xlabel("Number of publications", fontdict=font, fontsize=15, labelpad=10)
    ax.set_ylabel("Authors", fontdict=font, fontsize=15, labelpad=10)
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.grid(b = True, color ='white', linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    plt.savefig("Author Plot.png")
    plt.show()
    print()
    print("Done!")
    print()

def location_plot():
    '''Plots the publications per location'''
    infile = input("Locations file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Locations = pd.read_csv(infile)
    Location = Locations['Location']
    Papers = Locations['Paper']
    df4 = pd.DataFrame(list(zip(Papers, Location)),
              columns=['Paper','Location'])
    df5 = df4.groupby(['Location']).size()
    df5 = pd.Series.to_frame(df5)
    df5 = df5.reset_index()
    df5.columns = ['Location', 'Publications']
    End = max(df5['Publications']) + 1
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
        )
    world_map = folium.Map(location=(30, 10), tiles="cartodbpositron",
                           control_scale=True, zoom_start=2)
    folium.Choropleth(
    geo_data=political_countries_url,
    data=df5,
    columns=["Location", "Publications"],
    key_on="feature.properties.name",
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Publications by Country",
    bins=list(range(0,End,1))
    ).add_to(world_map)
    world_map.save("Locations plot.html")
    img_data = world_map._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save('Location plot.png', dpi=(600,600))
    print()
    print('Done!')
    print()
    
def bias_plot():
    '''Plot of bias measure computed for authors'''
    infile = input("Computed bias file (.csv): ")
    if infile.endswith('.csv') is True:
        pass
    elif infile.endswith('.csv') is False:
        infile = infile + '.csv'
    Data = pd.read_csv(infile)
    Data = pd.DataFrame(Data)
    Bias = Data['Cal.Bias']
    ZBias = stats.zscore(Bias)
    fig, ax = plt.subplots(figsize =(10, 7))
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
    ax.boxplot(ZBias, patch_artist = True,
                notch ='True')
    ax.set_facecolor('#f2f2f5')
    ax.set_title("Publications bias", fontdict=font, fontsize=20, pad=15)
    ax.set_xlabel("Bias", fontdict=font, fontsize=15, labelpad=10)
    ax.set_ylabel("Z-values", fontdict=font, fontsize=15, labelpad=10)
    plt.savefig("Bias plot.png")

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
            author_bias()
        elif choice == 'b':
            calibrate()
        elif choice == 'c':
            normality()
        elif choice == 'd':
            get_quantiles()
        elif choice == 'e':
            plots()
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main_loop()
