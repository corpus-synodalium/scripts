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

    def isTextFile(self, filename):
        """
        Return true if it is a text file, but not a Notes file.
        e.g. "2399_Gniezno_1298c.txt"
        """
        return re.match(r'.*\.txt', filename) and not self.isNotesFile(filename)

    def isNotesFile(self, filename):
        """
        Return true if it is a text file containing "_Notes"
        e.g. "2400_Gniezno_1309_Notes.txt"
        e.g. "2400_Gniezno_1309_Notes .txt" <-- also handle extra space at the end
        """
        return re.match(r'.*_Notes.*\.txt', filename)

    def getInputTextFileNames(self, input_dir):
        return [filename for filename in os.listdir(input_dir) if self.isTextFile(filename)]

    def getInputNotesFileNames(self, input_dir):
        return [filename for filename in os.listdir(input_dir) if self.isNotesFile(filename)]

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

    # Column Names from metadata.csv spreadsheet
    def getColumnNames(self):
        column_names = """RecordID,Year_Sort,Year,Month,Day,Circa,DatingNotes,Place,Diocese,Province,CountryModern,PlaceNotes,Latitude,Longitude,Jurisdiction_ID,Jurisdiction_ID2,Jurisdiction_ID3,Jurisdiction_ID4,Jurisdiction_ID5,Jurisdiction_ID6,Classification,IssuingAuthority,IssuingAuthorityAlt,RegnalStart,RegnalEnd,Delegated,ClassificationNotes,Language,LanguageNotes,Source,SourceOther,Edition,EditionOther,Source_URL,Source_URL2,SourceNotes,TranscriptionNotes,NoKnownText,TextNeeded,Fragment,BaseText,OCR,GeneralNotes,Transcription,BiblioRefs""".split(',')
        column_names = [str.strip() for str in column_names]
        return column_names

    # Ignored metadata columns that are not displayed in the database
    # but still processed by the script (jursidiction IDs for mapping)
    def getIgnoredMetadataFields(self):
        column_names = """Year_Sort,Jurisdiction_ID,Jurisdiction_ID2,Jurisdiction_ID3,
        Jurisdiction_ID4,Jurisdiction_ID5,Jurisdiction_ID6,TextNeeded,NoKnownText,
        Transcription,BaseText,OCR""".split(',')
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
