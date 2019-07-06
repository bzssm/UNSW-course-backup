# Uses data available at http://data.worldbank.org/indicator
# on Forest area (sq. km) and Agricultural land area (sq. km).
# Prompts the user for two distinct years between 1990 and 2004
# as well as for a strictly positive integer N,
# and outputs the top N countries where:
# - agricultural land area has increased from oldest input year to most recent input year;
# - forest area has increased from oldest input year to most recent input year;
# - the ratio of increase in agricultural land area to increase in forest area determines
#   output order.
# Countries are output from those whose ratio is largest to those whose ratio is smallest.
# In the unlikely case where many countries share the same ratio, countries are output in
# lexicographic order.
# In case fewer than N countries are found, only that number of countries is output.


# Written by *** and Eric Martin for COMP9021


import csv
import os
import sys
from collections import defaultdict

agricultural_land_filename = 'API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv'
if not os.path.exists(agricultural_land_filename):
    print(f'No file named {agricultural_land_filename} in working directory, giving up...')
    sys.exit()
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'
if not os.path.exists(forest_filename):
    print(f'No file named {forest_filename} in working directory, giving up...')
    sys.exit()
try:
    years = {int(year) for year in
             input('Input two distinct years in the range 1990 -- 2014: ').split('--')
             }
    if len(years) != 2 or any(year < 1990 or year > 2014 for year in years):
        raise ValueError
except ValueError:
    print('Not a valid range of years, giving up...')
    sys.exit()
try:
    top_n = int(input('Input a strictly positive integer: '))
    if top_n < 0:
        raise ValueError
except ValueError:
    print('Not a valid number, giving up...')
    sys.exit()

countries = []
year_1, year_2 = None, None

# Insert your code here
agricultural_land_dic = defaultdict(lambda: defaultdict(int))
year_1, year_2 = sorted(list(years))[0], sorted(list(years))[1]
agricultural_land_dif = dict()
forest_dic = defaultdict(lambda: defaultdict(int))
forest_dif = dict()


with open(agricultural_land_filename, 'r', encoding='utf-8') as f:
    lines = list(csv.reader(f))
    # print(lines[4])
    for i in range(5,len(lines)) :
        for j in range(4,len(lines[4])):
            agricultural_land_dic[lines[i][0]][lines[4][j]] = lines[i][j]
    # print(agricultural_land_dic)
    for e in agricultural_land_dic:
        if agricultural_land_dic[e][str(year_2)]!='' and agricultural_land_dic[e][str(year_1)]!='':
            agricultural_land_dif[e] = float(agricultural_land_dic[e][str(year_2)])-float(agricultural_land_dic[e][str(year_1)])


with open(forest_filename, 'r', encoding='utf-8') as f:
    lines = list(csv.reader(f))
    # print(lines[4])
    for i in range(5,len(lines)) :
        for j in range(4,len(lines[4])):
            forest_dic[lines[i][0]][lines[4][j]] = lines[i][j]
    # print(agricultural_land_dic)
    for e in forest_dic:
        if forest_dic[e][str(year_2)]!='' and forest_dic[e][str(year_1)]!='':
            forest_dif[e] = float(forest_dic[e][str(year_2)])-float(forest_dic[e][str(year_1)])
result = dict()
for e in agricultural_land_dif:
    if e in forest_dif:
        if agricultural_land_dif[e]>0 and forest_dif[e]>0:
            result[e]=agricultural_land_dif[e]/forest_dif[e]
result_list = sorted(list(result.items()),key=lambda x:(-x[1],x[0]))
result_list = result_list[:top_n]
# print(result_list)
for e in result_list:
    a,b = e
    b = f'{b:.2f}'

    countries.append(a+' ('+b+')')



print(f'Here are the top {top_n} countries or categories where, between {year_1} and {year_2},\n'
      '  agricultural land and forest land areas have both strictly increased,\n'
      '  listed from the countries where the ratio of agricultural land area increase\n'
      '  to forest area increase is largest, to those where that ratio is smallest:')
print('\n'.join(country for country in countries))
