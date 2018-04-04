import os
import re
import json
import codecs
import pprint
from collections import defaultdict

"""
parse_text_sections.py (v1) Apr 03, 2018
------------------------------
Parse sections from txt files.
"""

def main():
    input_file_names = [f for f in os.listdir('input')]
    counter = 0
    for f in input_file_names:
        lines = readFile(f)
        dictObj = readIntoDict(lines)
        createJsonFile(dictObj, f)
        counter += 1

    print('Number of input txt files: {}'.format(len(input_file_names)))
    print('Number of output txt files: {}'.format(counter))

# ----------------
# Helper Functions
# ----------------

def createJsonFile(dictObj, filename):
    json_file_name = './output/{}_output.txt'.format(re.findall(r'^(.*?)\.txt', filename)[0])
    with open(json_file_name, 'w') as file:
        # Incipit
        file.write('Section: {}\n'.format('incipit'))
        file.write('====================\n')
        values = dictObj['incipit']
        for v in values:
            file.write('{}\n'.format(v))
        file.write('\n')

        # Numbered Sections
        for k in sorted(dictObj.keys()):
            if k in ['incipit', 'explicit']:
                continue
            file.write('Section: {}\n'.format(k))
            file.write('====================\n')
            values = dictObj[k]
            for v in values:
                file.write('{}\n'.format(v))
            file.write('\n')

        # Explicit
        file.write('Section: {}\n'.format('explicit'))
        file.write('====================\n')
        values = dictObj['explicit']
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

def readIntoDict(lines):
    d = defaultdict(list)
    section_found = False
    last_section_number = None
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
        elif section_found:
            d[last_section_number].append(line)
            
    # inspect the last section for explicit (conclusion)
    d['explicit'] = []
    last_section = d[last_section_number]
    copy = last_section[:]
    is_explicit = False
    if len(last_section) > 1:
        for line in last_section[1:]:
            words_to_check = ["actum", "datum", "explicit", "expliciunt", "in cuius rei", "in cujus rei"]
            if is_explicit or any(word in line.lower() for word in words_to_check):
                is_explicit = True
                d['explicit'].append(line)
                copy.remove(line)
        d[last_section_number] = copy
    return d 

if __name__ == '__main__':
    main()