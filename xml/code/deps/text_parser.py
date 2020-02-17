import re
from collections import defaultdict
from pprint import pprint

# text_parser.py (v1) Apr 09, 2018
# --------------------------------
# Parses sections from RWD's text files.
# This module uses Python 3.
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class TextParser:

    def __init__(self, input_dir, utils, metadata, normalize):
        self.utils = utils
        self.input_dir = input_dir
        self.input_file_names = self.utils.getInputFileNames(input_dir)
        self.metadata = metadata
        self.normalize = normalize

    def getTextSections(self):
        texts = {}
        for input_file_name in self.input_file_names:
            record_id = self.utils.getRecordID(input_file_name)
            if record_id not in self.metadata:
                continue
            lines = self.utils.readFile(self.input_dir, input_file_name)
            sections = self.readIntoDict(lines, input_file_name)
            # Performs Orthographic Systematization for Latin texts
            if self.normalize and self.metadata[record_id]['Language'] == 'Latin':
                sections = self.normalizeText(sections)
                #pprint(sections)
            texts[record_id] = sections
        return texts

    # Helper Functions

    def normalizeText(self, sections):
        for section_name in sections['section_names']:
            section = sections[section_name]
            new_section = section[:]
            for index, line in enumerate(section):

                # Remove section numbers inside parantheses e.g (1) (ii)
                inside_parentheses = re.findall(r'^(\(.*?\))', line)
                #print(inside_parentheses)
                new_line = line
                for word in inside_parentheses:
                    new_line = line.replace('{} '.format(word), '')
                    new_line = new_line.replace(word, '')

                new_line = new_line.replace('j', 'i')
                new_line = new_line.replace('J', 'I')

                new_line = new_line.replace('ae', 'e')
                new_line = new_line.replace('AE', 'E')

                new_line = new_line.replace('dioec', 'dioc')
                new_line = new_line.replace('DIOEC', 'DIOC')
                new_line = new_line.replace('Dioec', 'Dioc')

                word_list = new_line.split(' ')
                for i, word in enumerate(new_line.split(' ')):
                    y_to_i_blacklist = ['presby', 'synod', 'martyr', 'symb', 'chrys', 'hymn', 'kyri', 'camyn']
                    if not any(x in word.lower() for x in y_to_i_blacklist):
                        word_list[i] = word_list[i].replace('y', 'i')
                        word_list[i] = word_list[i].replace('Y', 'I')
                    if not any(x in word.lower() for x in ['coe']):
                        word_list[i] = word_list[i].replace('oe', 'e')
                        word_list[i] = word_list[i].replace('OE', 'E')
                    if not any(x in word.lower() for x in ['stio', 'xtio']):
                        word_list[i] = word_list[i].replace('tio', 'cio')
                        word_list[i] = word_list[i].replace('TIO', 'CIO')
                    if not any(x in word.lower() for x in ['stia']):
                        word_list[i] = word_list[i].replace('tia', 'cia')
                        word_list[i] = word_list[i].replace('TIA', 'CIA')
                    if self.replace_v_with_u(word_list[i]):
                        word_list[i] = word_list[i].replace('v', 'u')
                        word_list[i] = word_list[i].replace('V', 'U')
                new_line = ' '.join(word_list)
                new_section[index] = new_line
            # Update the section
            sections[section_name] = new_section

        return sections


    def replace_v_with_u(self, word):
        word = re.sub(r'[^a-zA-Z]+', '', word.lower())
        if set(word).issubset(set(['c', 'i', 'l', 'm', 'v', 'x'])):
            return False
        regex_list = [r'^[cilmvx]+a$', r'^[cilmvx]+us$', r'^[cilmvx]+o$', r'^[cilmvx]+um$']
        if any(re.match(regex, word) for regex in regex_list):
            return False
        else:
            return True

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
            line = line.strip()
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
