import os
import re
import json
import io
from pprint import pprint


def main():
    counter = 0
    for file in os.listdir('notes_files'):
        print(file)
        lines = readFile(file)
        dictObj = readIntoDict(lines)
        pprint(dictObj)
        createJsonFile(dictObj)
        counter += 1
    print('Successfully exported {} JSON files.'.format(counter))


def readFile(filename):
    lines = []
    filename = './notes_files/{}'.format(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as file:
            lines = [line.strip() for line in file.readlines()]
    lines = filter(None, lines) # remove empty strings from list
    return lines


def readIntoDict(lines):
    section_names = ('Metadata', 'TranscriptionInfo', 'Notes')
    dictObj = {}
    sections = splitIntoSections(lines)
    for i, section in enumerate(sections):
        if i == 2:
            # No "key: value" pairs in Notes section.
            dictObj[section_names[i]] = readNotesSection(section)
        else:
            dictObj[section_names[i]] = readSingleSection(section)
    return dictObj


def createJsonFile(dictObj):
    record_ID = int(dictObj['Metadata']['Record ID'])
    record_ID = str(record_ID).zfill(4)
    filename = './output/notes_{}.json'.format(record_ID)
    with io.open(filename, 'w', encoding='utf-8') as json_file:
        json_str = json.dumps(dictObj, ensure_ascii=False).encode('utf-8')
        print(json_str)
        json_file.write(str(json_str))
        #json.dump(dictObj, json_file, ensure_ascii=False)
    print('Created JSON file: {}'.format(filename))


#====================================================#
# Helper Functions
#====================================================#

def splitIntoSections(lines):
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


def readSingleSection(lines):
    dictObj = {}
    for line in lines:        
        key_value = [x.strip() for x in line.split(':')]
        if len(key_value) == 1:
            key = 'Problems or Queries'
            value = key_value[0]
        elif len(key_value) == 2:
            key, value = key_value
        else:
            key = key_value[0]
            value = ':'.join(key_value[1:])
        dictObj[key] = value
    return dictObj


def readNotesSection(lines):
    dictObj = {'OtherNotes': [], 'FootNotes': {}}
    for line in lines:
        footnote_num = re.findall(r'^\[(.*?)\]', line)
        if not footnote_num:
            dictObj['OtherNotes'].append(line)
        elif len(footnote_num) == 1:
            try:
                footnote_num = int(footnote_num[0])
            except ValueError:
                footnote_num = footnote_num[0]
            note = re.findall(r'^\[(?:.*?)\](.*)', line)[0].strip()
            dictObj['FootNotes'][footnote_num] = note
        else:
            raise(Exception('ERROR: Multiple footnotes in one line. Details: {}'.format(line)))
    return dictObj


if __name__ == '__main__':
    main()