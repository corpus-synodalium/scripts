import os
import re
import json
from pprint import pprint
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom

#from ElementTree_pretty import prettify

"""
create_xml.py (v1) Apr 04, 2018
--------------------------------
Parse sections from txt files.
"""

def main():
    input_file_names = [f for f in os.listdir('input')]
    counter = 0
    for f in input_file_names:
        #print(f)
        associated_json_file = './json/database_{}.json'.format(re.findall(r'^(.*?)_', f)[0])
        metadata = dict()
        with open(associated_json_file) as json_data:
            metadata = json.load(json_data)
        lines = readFile(f)
        dictObj = readIntoDict(lines, f)
        createXMLFile(dictObj, metadata, f)
        counter += 1
        

    print('Number of input txt files: {}'.format(len(input_file_names)))
    print('Number of output xml files: {}'.format(counter))

def createXMLFile(dictObj, metadata, filename):

    root = createXMLTemplate()
    xmlstr = populateXML(root, dictObj, metadata, filename)
    xml_filename = './xml_output/{}_output.xml'.format(re.findall(r'^(.*?)\.txt', filename)[0])
    with open(xml_filename, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xmlstr)
    print('Created {}'.format(xml_filename))

# ----------------
# Helper Functions
# ----------------

def populateXML(root, dictObj, metadata, filename):
    recordID = root.find('teiHeader/fileDesc/titleStmt/recordID')
    recordID.text = 'Record ID: {}'.format(str(int(metadata['RecordID'])).zfill(4))

    diocese = root.find('teiHeader/profileDesc/creation/diocese')
    diocese.text = metadata['Diocese']

    province = root.find('teiHeader/profileDesc/creation/province')
    province.text = metadata['Province']



    section_names = dictObj['section_names']
    body = root.find('text/body')
    for section in section_names:
        div = ET.SubElement(body, 'div')
        head = ET.SubElement(div, 'head')
        head.text = section

        for line in dictObj[section]:
            p = ET.SubElement(div, 'p')
            p.text = line

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    return xmlstr

def createXMLTemplate():
    root = ET.Element('root')

    # TEI Header
    teiHeader = ET.SubElement(root, 'teiHeader')
    fileDesc = ET.SubElement(teiHeader, 'fileDesc')

    # Title Statement
    titleStmt = ET.SubElement(fileDesc, 'titleStmt')
    recordID = ET.SubElement(titleStmt, 'recordID')
    transcription = ET.SubElement(titleStmt, 'transcription')
    respStmt = ET.SubElement(titleStmt, 'respStmt')
    resp = ET.SubElement(respStmt, 'resp')
    name = ET.SubElement(respStmt, 'name')
    note = ET.SubElement(respStmt, 'note')
    date = ET.SubElement(note, 'date')
    problems = ET.SubElement(note, 'problems')

    # Source Description
    sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
    baseText = ET.SubElement(sourceDesc, 'baseText')
    textNeeded = ET.SubElement(sourceDesc, 'textNeeded')
    noKnownText = ET.SubElement(sourceDesc, 'noKnownText')
    fragment = ET.SubElement(sourceDesc, 'fragment')
    ocrNote = ET.SubElement(sourceDesc, 'ocrNote')
    msDesc = ET.SubElement(sourceDesc, 'msDesc')
    bibl = ET.SubElement(sourceDesc, 'bibl')
    sourceNote = ET.SubElement(sourceDesc, 'sourceNote')

    # Profile Description
    profileDesc = ET.SubElement(teiHeader, 'profileDesc')
    langUsage = ET.SubElement(profileDesc, 'langUsage')
    languageNote = ET.SubElement(profileDesc, 'languageNote')
    langUsage = ET.SubElement(profileDesc, 'langUsage')
    creation = ET.SubElement(profileDesc, 'creation')
    textDesc = ET.SubElement(profileDesc, 'textDesc')
    domain = ET.SubElement(textDesc, 'domain')
    genNotes = ET.SubElement(profileDesc, 'genNotes')

    # child nodes of 'creation'
    origDate = ET.SubElement(creation, 'origDate')
    dateNotes = ET.SubElement(creation, 'dateNotes')
    origPlaces = ET.SubElement(creation, 'origPlaces')
    diocese = ET.SubElement(creation, 'diocese')
    province = ET.SubElement(creation, 'province')
    country = ET.SubElement(creation, 'country')
    geo = ET.SubElement(creation, 'geo')
    placeNotes = ET.SubElement(creation, 'placeNotes')
    orgName = ET.SubElement(creation, 'orgName')
    persName = ET.SubElement(creation, 'persName')
    altName = ET.SubElement(creation, 'altName')
    regnalYears = ET.SubElement(creation, 'regnalYears')
    delegated = ET.SubElement(creation, 'delegated')
    classNotes = ET.SubElement(creation, 'classNotes')

    # Text
    text = ET.SubElement(root, 'text')
    body = ET.SubElement(text, 'body')

    return root


def readFile(filename):
    lines = []
    filename = './input/{}'.format(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
        lines = list(filter(None, lines)) # remove empty strings from list
    except UnicodeDecodeError:
        print('UnicodeDecodeError for file: {}'.format(filename))
        with open(filename, 'r', encoding='latin-1') as file:
            lines = [line.strip() for line in file.readlines()]
        lines = list(filter(None, lines)) # remove empty strings from list
    return lines

def readIntoDict(lines, filename):
    d = defaultdict(list)
    section_found = False
    last_section_number = None
    section_names = []
    d['incipit'] = []
    section_names.append('incipit')
    for line in lines:
        if not (section_found or line.startswith('(')):
            d['incipit'].append(line)
        elif line.startswith('('):
            # Match (X) at the beginning of a string where X is alpha-numeric string
            last_section_number = re.findall(r'^\((.*?)\)', line)[0]
            if last_section_number.isdigit():
                last_section_number = str(int(last_section_number)).zfill(3)
            section_found = True
            d[last_section_number].append(line)
            section_names.append(last_section_number)
        elif section_found:
            d[last_section_number].append(line)
            
    # inspect the last section for explicit (conclusion)
    d['explicit'] = []
    section_names.append('explicit')
    last_section = d[last_section_number]
    copy = last_section[:]
    is_explicit = False
    if len(last_section) > 1:
        for line in last_section[1:]:
            words_to_check = getExplicitIdentifiers()
            if is_explicit or any(word in line.lower() for word in words_to_check):
                is_explicit = True
                d['explicit'].append(line)
                copy.remove(line)
        d[last_section_number] = copy

    # Update the dict if the file has no numbered section
    if not section_found:
        #print('{}'.format(filename))
        new_dict = dict()
        new_dict['text'] = lines
        section_names = ['text']
        d = new_dict

    d['section_names'] = section_names
    assert(len(set(d['section_names'])) == len(d.keys()) - 1)
    return d

def getExplicitIdentifiers():
    # if any of these identifiers appear in a line of the LAST numbered section,
    # then that line belong in "explicit" section.
    identifiers = ["actum", 
    "datum", 
    "explicit", 
    "expliciunt", 
    "in cuius rei", 
    "in cujus rei", 
    "conclusion", 
    "escatocolo",
    "se acaban",
    "fecho en",
    "leydas",
    "dada en",
    "diligencia notarial"]

    return identifiers

if __name__ == '__main__':
    main()