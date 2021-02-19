# Extract CDP 

This git will be used to store the code to extract data from CDP reports, annual questionnaires evaluated by major companies.

### Process

The code extract data for every CDP reports in a given folder.

Requirements :
- CDP reports should be copy-paste in Google Doc-like program and export in .docx
- One unique activity sector by folder because sector specific sections occure

### Structure

Folders
- CDP_Report : folders of .docx report 
- Extracted_CSV : extracted .csv
- Test : 
    - Report_to_test : stable .docx report to compare
    - old_extract.csv : reference
    - test.py : compare .csv extracted from new extracting_data.py with old_extract.csv

Code
- parameters.py : hard coded parameters
- toolbox.py : basic functions (i.e. not specific to this task)
- CDP_xml.py : functions to read .docx
- CDP_get_functions.py : functions to extract each data
- extracting_data.py : code to run for extraction
    - argument : -p --path CDP_Report/wanted_sector (e.g. CDP_Report/Automotive)

### Main data from a questionary
- Title
- Start and end date
- Currency
- Reporting boundary
- Scope 1 Emissions
- Scope 2 Emissions (2 categories)
- Scope 3 Emissions (15 + 2 categories)
- Scope 1 + 2 intensity figures (8 categories)

### Sector specific data

##### Automotive
- Scope 3 use of sold products (10 categories)
- Efficiency figure (7 categories)

##### Electricity
- Capacity, generation, emission & intensity by source (15 categories + Total) 

### Processed Sections

##### Generic

C.4.5a

C.6.10

##### Sector specific

###### Automotive

C-TO8.4 & C-TO8.5

C-TO7.8

##### Electricity

C-EU8.2d


### Next Sections to process