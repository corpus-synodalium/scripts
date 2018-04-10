#!/usr/bin/env python

import deps.text_parser
import deps.note_parser
import deps.csv_parser
import deps.utils
import deps.xml_utils
from pprint import pprint

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
# ./input/text/*.txt
# ./input/notes/*.txt
# ./input/metadata/metadata.csv
# 
# For more info on how to use this script, see README.md


class MasterParser():

    def __init__(self):
        self.text_input_dir = './input/text/'
        self.notes_input_dir = './input/notes/'
        self.csv_file_name = './input/metadata/metadata.csv'
        self.xml_output_dir = './output/'

        self.utils = deps.utils.UtilityFunctions()
        self.xml_utils = deps.xml_utils.XMLUtils(self.utils)
        self.text_parser = deps.text_parser.TextParser(self.text_input_dir, self.utils)
        self.note_parser = deps.note_parser.NoteParser(self.notes_input_dir, self.utils)
        self.csv_parser = deps.csv_parser.CSVParser(self.csv_file_name, self.utils)
        

        self.texts = None
        self.footnotes = None
        self.metadata = None
        self.parseData()

    def parseData(self):
        print('Parsing text files ...')
        self.texts = self.text_parser.getTextSections()
        print('Success!')

        print('Parsing note files ...')
        self.footnotes = self.note_parser.getFootNotes()
        print('Success!')

        print('Parsing metadata ...')
        self.metadata = self.csv_parser.getMetadata()
        print('Success!')

    def checkInputFiles(self):
        print('Performing preliminary check of input files ...')
        print('Number of text files: {}'.format(len(self.text_parser.input_file_names)))
        print('Number of note files: {}'.format(len(self.note_parser.input_file_names)))
        print('Number of rows in csv file: {}'.format(len(self.metadata.keys())))

    def writeXMLFiles(self):
        #counter = 0 # added for testing purposes; remove later
        for filename in sorted(self.text_parser.input_file_names):
            record_id = self.utils.getRecordID(filename)
            xml_file_name = '{}{}.xml'.format(self.xml_output_dir, record_id)
            with open(xml_file_name, 'w') as xml_file:
                text = self.texts[record_id]
                footnotes = self.footnotes[record_id]
                metadata = self.metadata[record_id]
                xml_file.write(self.xml_utils.getXMLStr(text, footnotes, metadata, filename))
            print('Created {}'.format(xml_file_name))
            #counter += 1
            #if counter == 100:
            #    break

def main():
    master = MasterParser()
    master.checkInputFiles()
    master.writeXMLFiles()

if __name__ == '__main__':
    main()
