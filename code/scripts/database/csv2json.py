import csv
import json

"""
csv2json.py (v1) Mar 05, 2018
-----------------------------
- This python script parses the csv file (exported by the database) into json files.
- There is one json file created for each record ID.
- The number of json files created equals the number of rows in the csv file.
- Note: This script uses Python 2.7.14.
- Note: Create a new folder called json before running the script.
"""

# Config: change these values as needed
csv_file_name = 'data.csv'
json_file_format = lambda id: './json/database_{}.json'.format(id)

def main():
    with open(csv_file_name, 'rb') as csvfile:
        database = csv.reader(csvfile, delimiter=',', quotechar='"')
        num_rows = 0
        for row in database:
            dictObj = readIntoDict(row)
            createJsonFile(dictObj)
            num_rows += 1
        print('Number of JSON files created: {}'.format(num_rows))

def readIntoDict(row):
    column_names = getColumnNames()
    dictionary = dict()
    for i in range(len(row)):
        key = column_names[i]
        value = row[i] if row[i] else None # Convert '' to None
        key, value = processData(key, value)
        dictionary[key] = value
    return dictionary

def createJsonFile(dictionary):
    record_id = str(dictionary[getColumnNames()[0]]).zfill(4) # e.g: "0001"
    file_name = json_file_format(record_id)
    with io.open(file_name, 'w', encoding='utf-8') as json_file:
        #json_file.write(json.dumps(dictionary, ensure_ascii=False).encode('utf-8'))
        json.dump(dictionary, json_file, ensure_ascii=False)
    print('Created JSON file: {}'.format(file_name))

def processData(key, value):
    # deal with tab character in csv files exported by database
    # This tab character is known to appear in the following fields
    # BaseText, GeneralNotes, SourceNotes, PlaceNotes, DateNotes, Transcription Notes
    if value and '' in value:
        value_list = value.split('')
        value = filter(None, value_list) # filter empty strings
        if len(value) == 1:
            value = value[0] # ["lonely string"] => "lonely string"
    return (key, value)

def getColumnNames():
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

if __name__ == '__main__':
    main()