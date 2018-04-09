import os
import re
from collections import defaultdict

# text_parser.py (v1) Apr 09, 2018
# --------------------------------
# This module uses Python 3. Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class TextParser:

    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.input_file_names = self.getInputFileNames(input_dir)

    def getTextSections(self):
        texts = {}
        for input_file_name in self.input_file_names:
            lines = self.readFile(input_file_name)
            record_id = self.getRecordID(input_file_name)
            sections = self.readIntoDict(lines, input_file_name)
            texts[record_id] = sections
        return texts

    # Helper Functions
    
    def getInputFileNames(self, input_dir):
        return [filename for filename in os.listdir(input_dir) if re.match(r'.*\.txt', filename)]

    def getRecordID(self, input_file_name):
        return re.findall(r'^(.*?)_', input_file_name)[0]

    def readFile(self, input_file_name):
        lines = []
        input_file_name = '{}{}'.format(self.input_dir, input_file_name)
        try:
            with open(input_file_name, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines()]
        except UnicodeDecodeError:
            with open(input_file_name, 'r', encoding='latin-1') as file:
                lines = [line.strip() for line in file.readlines()]
        lines = list(filter(None, lines))  # remove empty strings from list
        return lines

    def readIntoDict(self, lines, input_file_name):
        d = defaultdict(list)
        section_found = False
        last_section_number = None
        section_names = []
        d['Incipit'] = []
        section_names.append('Incipit')
        for line in lines:
            if not (section_found or line.startswith('(')):
                d['Incipit'].append(line)
            elif line.startswith('('):
                # Match (X) at the beginning of a string where X is alpha-numeric string
                try:
                    last_section_number = re.findall(r'^\((.*?)\)', line)[0]
                except IndexError:
                    raise Exception('Improperly formatted section line in {}. \nDetails: "{}"'.format(input_file_name, line))
                if last_section_number.isdigit():
                    last_section_number = str(int(last_section_number))
                last_section_number = 'Capitulum {}'.format(last_section_number)
                section_found = True
                d[last_section_number].append(line)
                section_names.append(last_section_number)
            elif section_found:
                d[last_section_number].append(line)
                
        # inspect the last section for explicit (conclusion)
        d['Explicit'] = []
        section_names.append('Explicit')
        last_section = d[last_section_number]
        copy = last_section[:]
        is_explicit = False
        if len(last_section) > 1:
            for line in last_section[1:]:
                words_to_check = self.getExplicitIdentifiers()
                if is_explicit or any(word in line.lower() for word in words_to_check):
                    is_explicit = True
                    d['Explicit'].append(line)
                    copy.remove(line)
            d[last_section_number] = copy

        # Update the dict if the file has no numbered section
        if not section_found:
            #print('{}'.format(filename))
            new_dict = dict()
            new_dict['All Text'] = lines
            section_names = ['All Text']
            d = new_dict

        d['section_names'] = section_names
        assert(len(set(d['section_names'])) == len(d.keys()) - 1)
        return d

    def getExplicitIdentifiers(self):
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
