import os
import re

# note_parser.py (v1) Apr 09, 2018
# --------------------------------
# This module uses Python 3. Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class NoteParser:

    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.input_file_names = self.getInputFileNames(input_dir)

    def getFootNotes(self):
        # Return a dictionary
        # Key: 4-digit recordID (string)
        # Value: a list of footnotes (a list of strings)
        footnotes = {}
        for input_file_name in self.input_file_names:
            lines = self.readFile(input_file_name)
            record_id = self.getRecordID(input_file_name)
            notes_list = self.splitIntoSections(lines)[2]
            footnotes[record_id] = notes_list
        return footnotes

    # Helper Functions (Don't call them directly outside the module)

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
