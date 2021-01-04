import zipfile
import re

def generating_XML(doc_path):
    """
    FUNCTION
    Input: doc_path
    Output: XML_content

    Example
    doc_path = '../Carbometrix/General Motor Company 2018.docx'
    """

    #Extract the xml file from a docx
    document = zipfile.ZipFile(doc_path)
    XML_content = document.read('word/document.xml')

    return XML_content

def questionnaire_vector(XML_content):
    """
    FUNCTION
    Input: XML_content
    Output: questionnaire

    This function creates a function of strings of all XML content
    """

    #Taking only w:t strings.
    questionnaire = re.findall('<w:t xml.*?><', str(XML_content))

    #Removing XML sintax from strings
    for i in range(len(questionnaire)):
        questionnaire[i] = re.sub('<w:t xml:space="preserve">', '', questionnaire[i])
        questionnaire[i] = re.sub('</w:t><','', questionnaire[i])

    return questionnaire

def section_questionnaire(questionnaire):
    """
    Organizing our questionary in sections

    The list 'sections' has the information about each section within the questionary.

    """

    sections_name = ['C0. Introduction','C1. Governance', 'C2. Risks and opportunities',
                    'C3. Business Strategy', 'C4. Targets and performance','C5. Emissions methodology',
                    'C6. Emissions data', 'C7. Emissions breakdowns', 'C8. Energy',
                    'C9. Additional metrics', 'C10. Verification', 'C11. Carbon pricing',
                    'C12. Engagement','C14. Signoff']

    str_quest, sections = [], []

    title = questionnaire[0]
    questionnaire = questionnaire[1:]
    sections_name = sections_name[1:] #Taking off 'C0: Introduction' to guarentee that the first section will be introduction

    for phrase in questionnaire:
        if phrase in sections_name:
            sections.append(str_quest)
            sections_name = sections_name[1:]
            str_quest = []
        str_quest.append(phrase)

    return title, sections

def defining_all_subsections(sections):
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

    return all_subsections

def get_text(text, list_name):
    text = text[1:]
    sub_text = []
    i = 0
    while text[i] not in list_name:
        sub_text.append(text[i])
        i += 1
        if i >= len(text):
            break

    return sub_text

def text_subsections(sections, all_subsections):
    sub_text = []
    subsections = []
    for i in range(len(sections)):
        for j in range(len(sections[i])):
            if sections[i][j] in all_subsections:
                text = sections[i][j:]
                sub_text.append(get_text(text, all_subsections))
                subsections_name = all_subsections[1:]
        subsections.append(sub_text)
        sub_text = []

    return subsections
