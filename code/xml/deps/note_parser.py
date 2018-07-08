import re

# note_parser.py (v1) Apr 09, 2018
# --------------------------------
# Parses metadata and footnotes from RWD's notes files.
# This module uses Python 3. 
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class NoteParser:

    def __init__(self, input_dir, utils, normalize, metadata):
        self.utils = utils
        self.input_dir = input_dir
        self.input_file_names = self.utils.getInputFileNames(input_dir)
        self.normalize = normalize
        self.metadata = metadata
        

    def getFootNotes(self):
        # Return a dictionary
        # Key: 4-digit recordID (string)
        # Value: a list of footnotes (a list of strings)
        footnotes = {}
        for input_file_name in self.input_file_names:
            lines = self.utils.readFile(self.input_dir, input_file_name)
            record_id = self.utils.getRecordID(input_file_name)
            notes_list = self.splitIntoSections(lines)[2]
            if self.normalize and self.metadata[record_id]['Language'] == 'Latin':
                notes_list = self.normalizeText(notes_list)
            footnotes[record_id] = notes_list
        return footnotes

    # Helper Functions (Don't call them directly outside the module)

    def normalizeText(self, notes_list):
        temp = notes_list[:]
        for index, line in enumerate(notes_list):
            new_line = line
            
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
            temp[index] = new_line

        return temp

    def replace_v_with_u(self, word):
        word = re.sub(r'[^a-zA-Z]+', '', word.lower())
        if set(word).issubset(set(['c', 'i', 'l', 'm', 'v', 'x'])):
            return False
        regex_list = [r'^[cilmvx]+a$', r'^[cilmvx]+us$', r'^[cilmvx]+o$', r'^[cilmvx]+um$']
        if any(re.match(regex, word) for regex in regex_list):
            return False
        else:
            return True

    def splitIntoSections(self, lines):
        metadata, transcription, notes = ([], [], [])
        section_breaks = ['--', '---']
        section_break_counts = 0
        for line in lines:
            if line in section_breaks:
                section_break_counts += 1
                continue
            if 'notes:' in line.lower():
                continue
            if section_break_counts == 0:
                metadata.append(line)
            elif section_break_counts == 1:
                transcription.append(line)
            elif section_break_counts == 2:
                notes.append(line)
            else:
                raise(Exception('ERROR: More than 3 section breaks found in {}'.format(str(metadata))))
        return (metadata, transcription, notes)
