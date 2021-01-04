"""
### Taking all data we need

- Title
- Start and end date
- Scope 1 emissions
- Scope 2 emissions (location-based and market-based
- Scope 3 data (15 + 2 categories)

"""

import os
import numpy as np
from CDP_xml import *


def get_data(path):
    data = []
    metrics = []
    efficiency = []

    for file in os.listdir(path):
        doc_path = path + file

        XML_content = generating_XML(doc_path)
        questionnaire = questionnaire_vector(XML_content)

        title, sections = section_questionnaire(questionnaire)
        all_subsections = defining_all_subsections(sections)

        subsections = text_subsections(sections, all_subsections)

        #get functions
        start_date, end_date = get_period(subsections)
        scope1 = get_scope1(subsections)
        scope2 = get_scope2(subsections)
        scope3_names, scope3 = get_scope3(subsections)

        ###testing
    #    metrics_name, intensity_metrics = taking_intensity_metrics(subsections)
    #    metrics.append([title, intensity_metrics])
    #
    #    efficiency_name, efficiency_metrics = taking_efficiency_metrics(subsections)
    #    efficiency.append([title, efficiency_metrics])


        #metrics_names, metrics = taking_intensity_metrics(subsections)
        #metrics.append([title,intensity_metrics])
        #metrics.append(intensity_metrics)
        #metrics = correcting_size(metrics)

        #new = metrics_names.copy()
        #for s in metrics_names:
        #    new.append(s)
        #metrics_names = new.copy()

        #efficiency_name, efficiency_metrics = taking_efficiency_metrics(subsections)
        #efficiency.append(efficiency_metrics)
        #efficiecy = correcting_size(efficiency)
        ############
        #data_file = [title, start_date, end_date, scope1, scope2_location_based, scope2_market_based, scope3, metrics]
        data_file = [title, start_date, end_date, scope1, scope2, scope3]
        data.append(data_file)

        names = [scope3_names]

    return data, names

def get_period(subsections):
    for i in range(len(subsections[0][1])):
        if subsections[0][1][i] == 'Row 1' or subsections[0][1][i] == 'Reporting year':
            start_date = subsections[0][1][i+1]
            end_date = subsections[0][1][i+2]

    return start_date, end_date

def get_scope1(subsections):
    scope1 = [s for s in subsections[6][0][1:] if isfloat(s)]
    if scope1:
        scope1 = scope1[0]
    else:
        scope1 = np.nan #no answer
    return scope1

def get_scope2(subsections):
    """
    input: a vector with all subsections
    output:
        scope2[0] = location based
        scope2[1] = market based
    """

    scope2 = []

    for i in range(len(subsections[6][2][1:])):
        if subsections[6][2][i] in ['Scope 2, location-based', 'Scope 2, market-based (if applicable)']:
            if isfloat(subsections[6][2][i+1]):
                scope2.append(subsections[6][2][i+1])
            elif subsections[6][2][i+1] in ['&lt;Not Applicable&gt;']:
                scope2.append(subsections[6][2][i+1])
            else:
                scope2.append(np.nan)

            if len(scope2) == 2:
                break


    scope2 = [s.replace('&lt;', '<') for s in scope2]
    scope2 = [s.replace('&gt;', '>') for s in scope2]

    return scope2

#### C6.5
def get_scope3(subsections):
    """
    ***Sources of Scope 3 emissions***

    0 - Purchased goods and services
    1 - Capital goods
    2 - Fuel-and-energy-related activities (not included in Scope 1 or 2)
    3 - Upstream transportation and distribution
    4 - Waste generated in operations
    5 - Business travel
    6 - Employee commuting
    7 - Upstream leased assets
    8 - Downstream transportation and distribution
    9 - Processing of sold products
    10 - Use of sold products
    11 - End of life treatment of sold products
    12 - Downstream leased assets
    13 - Franchises
    14 - Investments
    15 - Other (upstream)
    16 - Other (downstream)
    """

    scope3_sections = ['Evaluation status', 'Metric tonnes CO2e', 'Percentage of emissions calculated using data obtained from suppliers or value chain partners']

    scope3_data = []
    for i in range(len(subsections[6][4])):
        if subsections[6][4][i] in scope3_sections:
            if subsections[6][4][i] == 'Evaluation status':
                scope3_data.append(subsections[6][4][i-1])
            elif (subsections[6][4][i] == 'Metric tonnes CO2e' or subsections[6][4][i] == 'Percentage of emissions calculated using data obtained from suppliers or value chain partners'):
                if not(isfloat(subsections[6][4][i+1])):
                    scope3_data.append(np.nan)
                    continue
            scope3_data.append(subsections[6][4][i+1])

    for s in scope3_data:
        if not isfloat(s):
            s.replace('&lt;', '<')
            s.replace('&gt;', '>')

    scope3_data = np.reshape(scope3_data, (17,4)).tolist()

    scope3_names, scope3 = [], []
    for s in scope3_data:
        scope3_names.append(s[0])
        scope3.append(s[2])

    return scope3_names, scope3


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
