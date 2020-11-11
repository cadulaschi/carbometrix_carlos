"""
Extracting data from a CDP Questionnary in docx format

The format is for years: 2017, 2018, 2019

"""
#specific to extracting information from word documents
import os
import zipfile
#other tools useful in extracting the information from our document
import re
#to pretty print our xml:
import xml.dom.minidom
import xml.etree.ElementTree as ET
import PyPDF2

#print(os.listdir('.'))

#Extract the xml file from a docx
document = zipfile.ZipFile('../Carbometrix_Project/Renault 2019.docx')
xml_content = document.read('word/document.xml')
#print(document.namelist())

"""
This part is necessary to visualize the questionnary content
In other words, it is to help me to find pattern and have a global idea about thq questionnary
"""
xml_content = document.read('word/document.xml')
uglyXml = xml.dom.minidom.parseString(xml_content).toprettyxml(indent='  ')

text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
prettyXml = text_re.sub('>\g<1></', uglyXml)

#print(prettyXml)

#Taking only w:t strings.
questionary = re.findall('<w:t xml.*?><', str(xml_content))

#Removing XML sintax from strings
for i in range(len(questionary)):
    questionary[i] = re.sub('<w:t xml:space="preserve">', '', questionary[i])
    questionary[i] = re.sub('</w:t><','', questionary[i])

#print(questionary)

###############################################################################
"""
Defining the title of the questionary
"""
title = questionary[0]
print(title)
questionary = questionary[1:]

###############################################################################
"""
Organizing our questionary in sections

The list 'sections' has the information about each section within the questionary.

"""

sections_name = ['C0. Introduction', 'C1. Governance', 'C2. Risks and opportunities',
                'C3. Business Strategy', 'C4. Targets and performance', 'C5. Emissions methodology',
                'C6. Emissions data', 'C7. Emissions breakdowns', 'C8. Energy',
                'C9. Additional metrics', 'C10. Verification', 'C11. Carbon pricing',
                'C12. Engagement', 'C14. Signoff'
                ]

str_quest, sections = [], []

sections_name = sections_name[1:] #I need to take of 'C0: Introduction' to guarentee that the first section will be introduction

for phrase in questionary:
    if phrase in sections_name:
        sections.append(str_quest)
        sections_name = sections_name[1:]
        str_quest = []
    str_quest.append(phrase)

#print(sections[0])

################################################################################
"""
Defining all subsections within a questionnary
"""
subsection_name = []
subsection = "C"

for i in range(len(sections)):
    subsection += str(i) + "."
    for j in range(20):
        subsection_name.append(subsection + str(j+1))
    subsection = "C"

all_subsections = []
for i in range(len(sections)):
    for j in range(len(sections[i])):
        if sections[i][j] in subsection_name:
            all_subsections.append(sections[i][j])


###############################################################################

"""
In order to increase our data specification, in this cell has the list subsections, where is possible to access
each subsection of a section (Introduction, Governance, etc.).

"""

def taking_text(text, list_name):
    text = text[1:]
    sub_text = []
    i = 0
    while text[i] not in list_name:
        sub_text.append(text[i])
        i += 1
        if i >= len(text):
            break
    return sub_text

sub_text = []
subsections = []
for i in range(len(sections)):
    for j in range(len(sections[i])):
        if sections[i][j] in all_subsections:
            text = sections[i][j:]
            sub_text.append(taking_text(text, all_subsections))
            all_subsections = all_subsections[1:]
    subsections.append(sub_text)
    sub_text = []

################################################################################
#Scope1 Emissions
scope1 = [s for s in subsections[6][0][1:] if s.isdigit()]
scope1 = int(scope1[0])

################################################################################
#Scope2 Emissions (location-based and market-based)
scope2 = [s for s in subsections[6][2][1:] if s.isdigit()]
scope2_location_based = int(scope2[0])
scope2_market_based = int(scope2[1])

################################################################################
#Show results

print("\nQuestionnary: {}".format(title))
print("Scope 1 emissions: {} [metric tons C02e]".format(scope1))
print("Scope 2 (location-based) emissions: {} [metric tons C02e]".format(scope2_location_based))
print("Scope 2 (market-based) emissions: {} [metric tons C02e]\n".format(scope2_market_based))
