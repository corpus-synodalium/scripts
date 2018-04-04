import os
import re
import json
import codecs
import pprint
from collections import defaultdict

"""
parse_text_sections.py (v1) Apr 03, 2018
----------------------------------------
Parse sections from txt files.
"""

def main():
    input_file_names = [f for f in os.listdir('input')]
    counter = 0
    for f in input_file_names:
        lines = readFile(f)
        dictObj = readIntoDict(lines, f)
        createOutputFile(dictObj, f)
        counter += 1

    print('Number of input txt files: {}'.format(len(input_file_names)))
    print('Number of output txt files: {}'.format(counter))

# ----------------
# Helper Functions
# ----------------

def createOutputFile(dictObj, filename):
    json_file_name = './output/{}_output.txt'.format(re.findall(r'^(.*?)\.txt', filename)[0])
    with open(json_file_name, 'w') as file:
        section_names = dictObj['section_names']

        for section in section_names:
            file.write('Section: {}\n'.format(section))
            file.write('====================\n')
            values = dictObj[section]
            for v in values:
                file.write('{}\n'.format(v))
            file.write('\n')

    print('Created {}'.format(json_file_name))

def readFile(filename):
    lines = []
    filename = './input/{}'.format(filename)
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    lines = filter(None, lines) # remove empty strings from list
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