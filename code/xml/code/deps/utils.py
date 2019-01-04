import re
import os

# utils.py (v1) Apr 09, 2018
# --------------------------
# Utility (helper) functions that are shared across multiple scripts.
# This module uses Python 3.
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu)


class UtilityFunctions:

    def __init__(self):
        pass

    def getInputFileNames(self, input_dir):
        return [filename for filename in os.listdir(input_dir) if re.match(r'.*\.txt', filename)]

    def getRecordID(self, input_file_name):
        return re.findall(r'^(.*?)_', input_file_name)[0]

    def readFile(self, input_dir, input_file_name):
        lines = []
        input_file_name = '{}{}'.format(input_dir, input_file_name)
        try:
            with open(input_file_name, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines()]
        except UnicodeDecodeError:
            with open(input_file_name, 'r', encoding='latin-1') as file:
                lines = [line.strip() for line in file.readlines()]
        lines = list(filter(None, lines))  # remove empty strings from list
        return lines

    def color_print(self, text, color="yellow"):
        if color.lower() == "red":
            print("\033[91m{}\033[00m".format(text))

        if color.lower() == "green":
            print("\033[92m{}\033[00m".format(text))

        if color.lower() == "cyan":
            print("\033[96m{}\033[00m".format(text))

        if color.lower() == "purple":
            print("\033[95m{}\033[00m".format(text))

        if color.lower() == "yellow":
            print("\033[93m{}\033[00m".format(text))

        if color.lower() == "lightgray":
            print("\033[97m{}\033[00m".format(text))

        if color.lower() == "lightpurple":
            print("\033[94m{}\033[00m".format(text))


    def getColumnNames(self):
        column_names = """RecordID,Year_Sort,Year,Month,Day,Circa,DatingNotes,Place,Diocese,
        Province,CountryModern,Jurisdiction_ID,Jurisdiction_ID2,Jurisdiction_ID3,
        Latitude,Longitude,PlaceNotes,Classification,IssuingAuthority,IssuingAuthorityAlt,
        RegnalStart,RegnalEnd,Delegated,ClassificationNotes,Language,LanguageNotes,
        TextNeeded,NoKnownText,Fragment,Source,SourceOther,Edition,EditionOther,
        SourceNotes,Transcription,BaseText,OCR,TranscriptionNotes,BiblioRefs""".split(',')
        column_names = [str.strip() for str in column_names]
        return column_names

    def getExplicitIdentifiers(self):
        # if any of these identifiers appear in a line of the LAST numbered section,
        # then that line belong in "explicit" section.
        identifiers = ["actum",
        "datum",
        "explicit",
        "expliciunt",
        "in cuius rei",
        "in cujus rei",
        "conclusion",
        "escatocolo",
        "se acaban",
        "fecho en",
        "leydas",
        "dada en",
        "diligencia notarial"]

        return identifiers
