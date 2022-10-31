#!/usr/bin/env python

import sys
from time import time
import deps.text_parser
import deps.note_parser
import deps.csv_parser
import deps.utils
import deps.xml_utils

# main.py (v1) Apr 09, 2018
# -------------------------
# Creates XML files required for PhiloLogic4 web app.
# This script uses Python 3.
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu)
#
# REQUIRED DEPENDENCY FILES:
# ./deps/utils.py
# ./deps/xml_utils.py
# ./deps/note_parser.py
# ./deps/text_parser.py
# ./deps/csv_parser.py
#
# REQUIRED INPUT FILES:
# ../_input/*.txt
# ../_input/metadata.csv
#
# For more info on how to use this script, see README.md

INPUT_FOLDER_PATH = '../_input/'
INPUT_CSV_PATH = '../_input/metadata.csv'
OUTPUT = '../_output/'

#==============#
# MasterParser #
#==============#

class MasterParser():
    """ Parse data from three sources (text, footnotes, csv)
    and write xml files.
    """
    def __init__(self, normalize):
        self.num_files = None
        self.texts = None
        self.footnotes = None
        self.normalize = normalize
        self.utils = deps.utils.UtilityFunctions()
        self.xml_utils = deps.xml_utils.XMLUtils(self.utils)
        self.metadata = deps.csv_parser.CSVParser(INPUT_CSV_PATH, self.utils).getMetadata()
        self.text_parser = deps.text_parser.TextParser(INPUT_FOLDER_PATH, self.utils, self.metadata, self.normalize)
        self.note_parser = deps.note_parser.NoteParser(INPUT_FOLDER_PATH, self.utils, self.metadata)

    def parse_data(self):
        self.utils.color_print('Step (2/3) - Parsing data. Please be patient ... \n')
        self.texts = self.text_parser.getTextSections()
        self.footnotes = self.note_parser.getFootNotes()
        print('Success! All data parsed.\n')

    def inspect_file_count(self):
        self.utils.color_print('Step (1/3) - Inspecting input files ... \n')
        num_text = len(self.text_parser.input_file_names)
        num_note = len(self.note_parser.input_file_names)
        num_csv = len(self.metadata.keys())
        self.num_files = num_text
        print('Number of text files: {}'.format(num_text))
        print('Number of note files: {}'.format(num_note))
        print('Number of csv rows  : {}\n'.format(num_csv))
        if (num_text != num_note): #or (num_text != num_csv):
            print('The number of files in all input sources must be the same.')
            print('Please check your input sources. If you want to continue,')
            print('you can comment out "inspect_file_count()" in main.py\n')
            raise Exception('The number of input files must match.')

    def write_xml_output(self):
        self.utils.color_print('Step (3/3) - Writing XML Files ...\n')
        for i, filename in enumerate(sorted(self.text_parser.input_file_names)):
            record_id = self.utils.getRecordID(filename)
            xml_file_name = '{}{}.xml'.format(OUTPUT, record_id)
            if self.normalize:
                xml_file_name = '{}{}_normalized.xml'.format(OUTPUT, record_id)
            with open(xml_file_name, 'w') as xml_file:
                if record_id not in self.metadata:
                    print('No metadata found. Skipped {}.'.format(record_id))
                    continue
                text = self.texts[record_id]
                footnotes = self.footnotes[record_id]
                metadata = self.metadata[record_id]
                try:
                    xml_str = self.xml_utils.getXMLStr(text, footnotes, metadata, filename)
                    xml_file.write(xml_str)
                except:
                    print('Error in {}\n'.format(filename))
            print_progress_bar(i+1, self.num_files, status=xml_file_name)

#==================#
# Helper Functions #
#==================#

def print_progress_bar(count, total, status=''):
    progress_bar_len = 40
    filled_len = int(round(progress_bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    progress_bar = '=' * filled_len + '-' * (progress_bar_len - filled_len)

    sys.stdout.write('[{}] {}{} {}\r'.format(progress_bar, percents, '%', status))
    sys.stdout.flush()
    if count == total:
        print('[{}] {}{} {}\r'.format(progress_bar, percents, '%', status))

def print_intro():
    intro = ('\nWelcome! This script will create XML files required for PhiloLogic4 web app.\n')
    print(intro)

def main():
    print_intro()
    start_time = time()
    normalize = '-n' in sys.argv
    master = MasterParser(normalize)
    master.inspect_file_count()
    master.parse_data()
    master.write_xml_output()
    print('\n--- All tasks complete! Time taken: {} seconds ---\n'.format(time() - start_time))

if __name__ == '__main__':
    main()
