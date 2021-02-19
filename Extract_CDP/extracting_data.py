"""
Extracting data from a CDP Questionnary in docx format

This script works for years: 2017, 2018, 2019

"""

import numpy as np
import pandas as pd
import argparse 

from CDP_get_functions import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a csv from the CDP report located in given path (name of folder should be sector name"
    )
    parser.add_argument("-p", "--path", help="The path to your folder.", required=True)

    args = parser.parse_args()
    path = args.path
    
    if path[-1] != '/' :
        path = path + '/'

    data, scope3_names, sector, dict_intensity, dict_use_sold_product, dict_efficiency, list_df_elec = get_data(path)


    #Creating major dataframe
    all_data = np.array(data, dtype=object).T.tolist()

    dic = {}
    dic['Title'] = all_data[0]
    dic['Start Date'] = all_data[1]
    dic['End Date'] = all_data[2]
    dic['Currency'] = all_data[3]
    dic['Reporting_boundary'] = all_data[4]
    dic['Scope 1'] = all_data[5]  

    all_data[6] = np.array(all_data[6], dtype=object).T.tolist()
    dic['Scope 2 (location based)'] = all_data[6][0]
    dic['Scope 2 (market based)'] = all_data[6][1]

    # Scope 3
    all_data[7] = np.array(all_data[7], dtype=object).T.tolist()
    for i in range(len(scope3_names)):
        dic[scope3_names[i]] = all_data[7][i]

    df_data = pd.DataFrame.from_dict(dic, orient='index')
    df_data = df_data.transpose()

    #Saving table in a CSV file
    df_data.to_csv('../Extract_CDP/Extracted_CSV/' + sector + '_CDP.csv')
    
    
    #Creating & saving sub dataframe
    df_intensity = pd.DataFrame(dict_intensity)
    df_intensity.to_csv('../Extract_CDP/Extracted_CSV/' + sector + '_intensity_CDP.csv')
    
    if sector == 'Automotive' :
        df_use_sold_product = pd.DataFrame(dict_use_sold_product)
        df_use_sold_product.to_csv('../Extract_CDP/Extracted_CSV/' + sector + '_use_sold_product_CDP.csv')
        
        df_efficiency = pd.DataFrame(dict_efficiency)
        df_efficiency.to_csv('../Extract_CDP/Extracted_CSV/' + sector + '_efficiency_CDP.csv')

    if sector == 'Electricity' :
        df_electricity = pd.concat(list_df_elec, ignore_index=True)
        df_electricity.to_csv('../Extract_CDP/Extracted_CSV/' + sector + '_capacity_CDP.csv')

