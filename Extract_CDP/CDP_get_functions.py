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
import pandas as pd
from CDP_xml import *
from collections import defaultdict 



def get_data(path):
    data = []
    metrics = []
    efficiency = []
    sector = path.split('/')[-2]
    
    # dict for dataframe
    dict_intensity = defaultdict(list) 
    dict_use_sold_product = defaultdict(list)
    dict_efficiency = defaultdict(list)
    
    # list for dataframe 
    list_df_elec = []


    for file in os.listdir(path):

        # go to file
        doc_path = path + file

        # read file
        XML_content = generating_XML(doc_path)
        questionnaire = questionnaire_vector(XML_content)

        # get section & subsection in file
        title, sections = section_questionnaire(questionnaire)
        all_subsections = defining_all_subsections(sections)
        subsections = text_subsections(sections, all_subsections)

        # get infos (generic)
        start_date, end_date = get_period(subsections)
        scope1 = get_scope1(subsections)
        scope2 = get_scope2(subsections)
        scope3_names, scope3 = get_scope3(subsections)

        _, currency = get_info_from_section(subsections, 
                      subsection_code = 'C0.4', 
                      subsection_tag = ['(C0.4) Select the currency used for all financial information disclosed throughout your response.'], 
                      prefix = 'currency')
        
        _, reporting_boundary = get_info_from_section(subsections, 
                      subsection_code = 'C0.5', 
                      subsection_tag = ['(C0.5) Select the option that describes the reporting boundary for which climate-related impacts on your business are being reported. Note that this option should align with your chosen approach for consolidating your GHG inventory.'], 
                      prefix = 'reporting_boundary')
        
        
        intensity_names, intensity = get_info_from_section(subsections, 'C6.10', S1_S2_intensity_tag, '')
        fill_dict_for_df(dict_intensity, intensity_names, intensity, title)

        # get infos (automotive)
        if sector == 'Automotive' :
            use_sold_products_names, use_sold_products = get_info_from_section(subsections, 'C-TO7.8', S3_Use_sold_products_from_transport_sections, '')
            fill_dict_for_df(dict_use_sold_product, use_sold_products_names, use_sold_products, title)
            try :
                efficiency_names, efficiency = get_info_from_section(subsections, 'C-TO8.4', efficiency_sections, '')
                fill_dict_for_df(dict_efficiency, efficiency_names, efficiency, title)
            except :
                efficiency_names, efficiency = get_info_from_section(subsections, 'C-TO8.5', efficiency_sections, '')
                fill_dict_for_df(dict_efficiency, efficiency_names, efficiency, title)
        
        # get infos (electricity)
        if sector == 'Electricity' :
            electric_capacity_names, electricity_capacity, electricity_capacity_sections = get_electric_capacity(subsections)
            # create dataframe from this file
            df_elec = pd.DataFrame(electricity_capacity, columns = electricity_capacity_sections)
            df_elec['Source'] = electric_capacity_names
            df_elec['Title'] = title
            df_elec = df_elec[['Title', 'Source'] + electricity_capacity_sections]
            
            list_df_elec.append(df_elec)

                
        data_file = [title, start_date, end_date, currency, reporting_boundary, scope1, scope2, scope3]
        data.append(data_file)

    return data, scope3_names, sector, dict_intensity, dict_use_sold_product, dict_efficiency, list_df_elec


def get_period(subsections):
    for i in range(len(subsections[0][1])):
        if subsections[0][1][i] == 'Row 1' or subsections[0][1][i] == 'Reporting year':
            start_date = subsections[0][1][i+1]
            end_date = subsections[0][1][i+2]

    return start_date, end_date


#########################################
## HARD CODED FUNCTIONS (to simplify)  #
#######################################


def get_scope1(subsections):
    scope1 = [s for s in subsections[6][0][1:] if isfloat(s)]
    if scope1:
        scope1 = scope1[0]
    else:
        scope1 = np.nan  # no answer
    return scope1


def get_scope2(subsections, scope2_sections=scope2_sections):
    """
    input: a vector with all subsections
    output:
        scope2[0] = location based
        scope2[1] = market based
    """

    scope2 = []

    for i in range(len(subsections[6][2][1:])):
        if subsections[6][2][i] in scope2_sections:
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

# C6.5


def get_scope3(subsections, scope3_sections=scope3_sections):
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

    scope3_data = np.reshape(scope3_data, (17, 4)).tolist()

    scope3_names, scope3 = [], []
    for s in scope3_data:
        scope3_names.append(s[0])
        scope3.append(s[2])

    return scope3_names, scope3


#### C-EU8.2d
def get_electric_capacity(subsections):
    
    electricity_by_source_sections = ['Nameplate capacity (MW)', 
                                 'Gross electricity generation (GWh)',
                                 'Net electricity generation (GWh)',
                                 'Absolute scope 1 emissions (metric tons CO2e)',
                                 'Scope 1 emissions intensity (metric tons CO2e per GWh)']
    
    try :
        text_of_interest = find_text_of_interest(subsections, 'C-EU8.2d')
        
    except :
        electric_capacity_names = ['Coal \\xe2\\x80\\x93 hard',
                                  'Lignite',
                                  'Oil',
                                  'Gas',
                                  'Biomass',
                                  'Waste (non-biomass)',
                                  'Nuclear',
                                  'Fossil-fuel plants fitted with CCS',
                                  'Geothermal',
                                  'Hydropower',
                                  'Wind',
                                  'Solar',
                                  'Marine',
                                  'Other renewable',
                                  'Other non-renewable',
                                  'Total']
        electricity_by_source = [[np.nan]*5]*16
        return electric_capacity_names, electricity_by_source, electricity_by_source_sections
    
    electricity_by_source_data = []
    for i in range(len(text_of_interest)):
        if text_of_interest[i] == 'Nameplate capacity (MW)' :
            electricity_by_source_data.append(text_of_interest[i-1])
        if text_of_interest[i] in electricity_by_source_sections:
            electricity_by_source_data.append(text_of_interest[i+1])
            
    electricity_by_source_data = np.reshape(electricity_by_source_data, (len(electricity_by_source_data)//6,6)).tolist()
        
    electricity_by_source_names, electricity_by_source = [], []
    for s in electricity_by_source_data:
        electricity_by_source_names.append(s[0])
        electricity_by_source.append(s[1:])

    
    return electricity_by_source_names, electricity_by_source, electricity_by_source_sections


############################
## CLEAN FUNCTIONS (tbc)  #
##########################

def find_text_of_interest(subsections, subsection_code):

    section_number = re.search(r'\d+', subsection_code).group()

    # find section of interest
    for subsection in subsections:
        # if section_number in subsection[0][0][:10] :
        if section_number == re.search(r'\d+', subsection[0][0][:10]).group():
            section_of_interest = subsection

    # delete old subsection_of_interest element to know if new is found
    try:
        del subsection_of_interest

    except NameError:
        pass

    # look for subsection_of_interest by subsection_code
    # should work for every basic section
    for subsection in section_of_interest:
        if subsection_code in subsection[0][:10]:
            subsection_of_interest = subsection
            break  # take the first matching subsection

    try:
        return subsection_of_interest

    # if no subsection_of_interest found look for by detailled reading
    # should only occure for sector specific sections
    except:

        for subsub in section_of_interest:
            i = 0
            for s in subsub:
                i += 1
                if s == subsection_code:
                    subsection_of_interest = subsub[i:]

        return subsection_of_interest


def get_info_from_section(subsections, subsection_code, subsection_tag, prefix) :
    
    text_of_interest = find_text_of_interest(subsections, subsection_code)
    
    # case for unique researched element
    if len(subsection_tag) == 1 :
        metrics = text_of_interest[1]
        return subsection_tag, metrics
    
    # select present tags among possible tags
    subsection_tag_copy = subsection_tag.copy()
    subsection_tag = [tag for tag in subsection_tag if tag in text_of_interest]
    
    # if nothing in section 
    if subsection_tag == [] :
                
        # specific case for section C6.10
        if 'Metric numerator (Gross global combined Scope 1 and 2 emissions, metric tons CO2e)' in subsection_tag_copy :
            subsection_tag_copy.remove('Metric numerator (Gross global combined Scope 1 and 2 emissions, metric tons CO2e)')
        
        metrics = [np.nan]*len(subsection_tag_copy)

        return subsection_tag_copy, metrics
    
    # organise text_of_interest (append nan and delete comment)
    j = 0
    for i,k in zip(text_of_interest[0::1], text_of_interest[1::1]):
        j += 1
        # insert NaN if no given answer
        if seq_in_seq([i,k], subsection_tag + [subsection_tag[0]] ) :
            text_of_interest.insert(j, np.nan)
            j += 1
        # keep only the first element after a name tag
        if not any(name in [i,k] for name in subsection_tag):
            text_of_interest.remove(k)
            j += -1
            
    if text_of_interest[-1] == subsection_tag[-1] :
        text_of_interest.append(np.nan)
    
    # get metrics
    metrics = [text_of_interest[i+1] for i in range(1, len(text_of_interest)-1, 2)]
    
    # create NaN list if no answer 
    if len(metrics) == 0 :
        metrics = [np.nan]*len(subsection_tag)
        
    # group information of same variable if several mentions
    if len(metrics) != len(subsection_tag) :
        metrics = np.reshape(metrics, 
                        (len(metrics)//len(subsection_tag), 
                                len(subsection_tag))).T.tolist()

    subsection_tag = [w.replace('Metric numerator (Gross global combined Scope 1 and 2 emissions, metric tons CO2e)', 'Metric numerator (Gross global combined Scope 1 and 2 emissions)') for w in subsection_tag]
    subsection_tag = [prefix + s for s in subsection_tag]
            
    return subsection_tag, metrics
