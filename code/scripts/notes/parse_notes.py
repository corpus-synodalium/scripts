import os
import re
from pprint import pprint


def main():
    counter = 0
    for input_file_name in getInputFileNames('./input/'):
        #print(input_file_name)
        lines = readFile(input_file_name)
        notes = parseFootNotes(lines)
        writeOutputFile(notes, input_file_name)
        counter += 1
    print('Successfully exported {} JSON files.'.format(counter))


# Helper Functions

def writeOutputFile(notes, input_file_name):
    output_file_name = './output/{}_Footnotes.txt'.format(re.findall(r'(.*?)_Notes.txt', input_file_name)[0])
    with open(output_file_name, 'w', encoding='utf-8') as file:
        for line in notes:
            file.write('{}\n'.format(line))
    print('Created {}'.format(output_file_name))

def getInputFileNames(dir_str):
    input_file_names = [filename for filename in os.listdir(dir_str) if re.match(r'.*\.txt', filename)]
    print('Number of input txt files: {}'.format(len(input_file_names)))
    return input_file_names


def readFile(filename):
    lines = []
    filename = './input/{}'.format(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
    except UnicodeDecodeError:
        #print('UnicodeDecodeError for file: {}'.format(filename))
        with open(filename, 'r', encoding='latin-1') as file:
            lines = [line.strip() for line in file.readlines()]
    lines = list(filter(None, lines)) # remove empty strings from list
    return lines

def parseFootNotes(lines):
    metadata, transcription, notes = splitIntoSections(lines)
    return notes

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

if __name__ == '__main__':
    main()