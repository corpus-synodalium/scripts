import re
from collections import defaultdict

# text_parser.py (v1) Apr 09, 2018
# --------------------------------
# Parses sections from RWD's text files.
# This module uses Python 3. 
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class TextParser:

    def __init__(self, input_dir, utils):
        self.utils = utils
        self.input_dir = input_dir
        self.input_file_names = self.utils.getInputFileNames(input_dir)
        
    def getTextSections(self):
        texts = {}
        for input_file_name in self.input_file_names:
            lines = self.utils.readFile(self.input_dir, input_file_name)
            record_id = self.utils.getRecordID(input_file_name)
            sections = self.readIntoDict(lines, input_file_name)
            texts[record_id] = sections
        return texts

    # Helper Functions

    def readIntoDict(self, lines, input_file_name):
        d = defaultdict(list)
        section_found = False
        last_section_number = '1'
        section_names = []
        d['Incipit'] = []
        section_names.append('Incipit')
        for line in lines:
            # Remove \ufeff (a zero-width character that is known to appear at the beginning of some files)
            line = line.replace('\ufeff', '')
            if line.startswith('('):
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
            else:
                d['Incipit'].append(line)
                            
        # inspect the last section for explicit (conclusion)
        d['Explicit'] = []
        section_names.append('Explicit')
        last_section = d[last_section_number]
        copy = last_section[:]
        is_explicit = False
        if len(last_section) > 1:
            for line in last_section[1:]:
                words_to_check = self.utils.getExplicitIdentifiers()
                if is_explicit or any(word in line.lower() for word in words_to_check):
                    is_explicit = True
                    d['Explicit'].append(line)
                    copy.remove(line)
            d[last_section_number] = copy

        # Remove incipit and explicit if empty
        if not d['Incipit']:
            d.pop('Incipit')
            section_names.remove('Incipit')

        if not d['Explicit']:
            d.pop('Explicit')
            section_names.remove('Explicit')

        # Update the dict if the file has no numbered section
        if not section_found:
            new_dict = dict()
            new_dict['All Text'] = lines
            section_names = ['All Text']
            d = new_dict

        d['section_names'] = section_names
        assert(len(set(d['section_names'])) == len(d.keys()) - 1)
        return d
