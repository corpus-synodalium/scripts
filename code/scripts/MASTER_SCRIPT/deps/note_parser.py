import os
import re

# note_parser.py (v1) Apr 09, 2018
# --------------------------------
# Parses metadata and footnotes from RWD's notes files.
# This module uses Python 3. 
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class NoteParser:

    def __init__(self, input_dir, utils):
        self.utils = utils
        self.input_dir = input_dir
        self.input_file_names = self.utils.getInputFileNames(input_dir)
        

    def getFootNotes(self):
        # Return a dictionary
        # Key: 4-digit recordID (string)
        # Value: a list of footnotes (a list of strings)
        footnotes = {}
        for input_file_name in self.input_file_names:
            lines = self.utils.readFile(self.input_dir, input_file_name)
            record_id = self.utils.getRecordID(input_file_name)
            notes_list = self.splitIntoSections(lines)[2]
            footnotes[record_id] = notes_list
        return footnotes

    # Helper Functions (Don't call them directly outside the module)

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
