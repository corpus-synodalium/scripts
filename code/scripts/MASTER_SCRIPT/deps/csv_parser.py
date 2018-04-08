import csv

# csv_parser.py (v1) Apr 09, 2018
# -------------------------------
# This module uses Python 3. Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class CSVParser():

    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def getMetadata(self):
        # Return a dictionary
        # Key: 4-digit recordID (string)
        # Value: a dictionary (metadata (key, value) pairs)
        metadata = dict()
        with open(self.csv_file_name, newline='') as csvfile:
            database = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in database:
                dictionary = self.readIntoDict(row)
                record_id = str(dictionary[self.getColumnNames()[0]]).zfill(4)  # e.g: "0001"
                metadata[record_id] = dictionary
        return metadata

    # Helper Functions

    def readIntoDict(self, row):
        column_names = self.getColumnNames()
        dictionary = dict()
        for i in range(len(row)):
            key = column_names[i]
            value = row[i] if row[i] else None  # Convert '' to None
            key, value = self.processData(key, value)
            dictionary[key] = value
        return dictionary

    def processData(self, key, value):
        # deal with tab character in csv files exported by database
        # This tab character is known to appear in the following fields
        # BaseText, GeneralNotes, SourceNotes, PlaceNotes, DateNotes, Transcription Notes
        if value and ('' in value):
            value_list = value.split('')
            value = list(filter(None, value_list))  # filter empty strings
            if len(value) == 1:
                value = value[0]  # ["lonely string"] => "lonely string"
        return (key, value)

    def getColumnNames(self):
        column_names = ['RecordID',
        'Year',
        'Month',
        'Day',
        'Circa',
        'DatingNotes',
        'Place',
        'Diocese',
        'Province',
        'CountryModern',
        'Latitude',
        'Longitude',
        'PlaceNotes',
        'Classification',
        'IssuingAuthority',
        'IssuingAuthorityAlt',
        'RegnalStart',
        'RegnalEnd',
        'Delegated',
        'ClassificationNotes',
        'Language',
        'LanguageNotes',
        'TextNeeded',
        'NoKnownText',
        'Fragment',
        'Source',
        'SourceOther',
        'Edition',
        'EditionOther',
        'SourceNotes',
        'TranscriptionNotes',
        'BaseText',
        'OCR',
        'Transcription',
        'GeneralNotes',
        'BiblioRefs']
        return column_names
