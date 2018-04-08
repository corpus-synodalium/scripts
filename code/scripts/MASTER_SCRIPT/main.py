#!/usr/bin/env python

import deps.text_parser
import deps.note_parser
import deps.csv_parser
import deps.utils
from pprint import pprint


class MasterParser():

    def __init__(self):
        self.text_input_dir = './input/text/'
        self.notes_input_dir = './input/notes/'
        self.csv_file_name = './input/metadata/data.csv'
        self.xml_output_dir = './output/'

        self.text_parser = deps.text_parser.TextParser(self.text_input_dir)
        self.note_parser = deps.note_parser.NoteParser(self.notes_input_dir)
        self.csv_parser = deps.csv_parser.CSVParser(self.csv_file_name)
        self.utils = deps.utils.UtilityFunctions()

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
        for filename in sorted(self.text_parser.input_file_names):
            record_id = self.text_parser.getRecordID(filename)
            xml_file_name = '{}{}.xml'.format(self.xml_output_dir, record_id)
            with open(xml_file_name, 'w') as xml_file:
                text = self.texts[record_id]
                footnotes = self.footnotes[record_id]
                metadata = self.metadata[record_id]
                xml_file.write(self.utils.getXMLStr(text, footnotes, metadata, filename))
            print('Created {}'.format(xml_file_name))

def main():
    master = MasterParser()
    master.checkInputFiles()
    master.writeXMLFiles()

if __name__ == '__main__':
    main()