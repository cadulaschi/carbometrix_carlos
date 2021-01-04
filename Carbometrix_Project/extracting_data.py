"""
Extracting data from a CDP Questionnary in docx format

This script works for years: 2017, 2018, 2019

"""

import numpy as np
import pandas as pd

from CDP_get_functions import *

path = '../Carbometrix_Project/Questionnaires/Automotive/'

data, names = get_data(path)

scope3_names = names[0]

#Creating data frame
all_data = np.array(data, dtype=object).T.tolist()
dic = {}
dic['Title'] = all_data[0]
dic['Start Date'] = all_data[1]
dic['End Date'] = all_data[2]
dic['Scope 1'] = all_data[3]

all_data[4] = np.array(all_data[4], dtype=object).T
dic['Scope 2 (location based)'] = all_data[4][0]
dic['Scope 2 (market based)'] = all_data[4][1]

all_data[5] = np.array(all_data[5], dtype=object).T
for i in range(len(scope3_names)):
    dic[scope3_names[i]] = all_data[5][i]

df_data = pd.DataFrame.from_dict(dic, orient='index')
df_data = df_data.transpose()

#Saving table in a CSV file
df_data.to_csv('../Carbometrix_Project/automotive_data.csv')
