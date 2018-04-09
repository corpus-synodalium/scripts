import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


class UtilityFunctions:
    def __init__(self):
        pass

    def getXMLStr(self, text, footnotes, metadata, filename):
        root = self.getXMLTemplate()
        self.populateTeiHeader(root, metadata, filename)
        self.populateText(root, text, footnotes, metadata, filename)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        return xmlstr

    def getXMLTemplate(self):
        root = ET.Element('root')

        # TEI Header
        teiHeader = ET.SubElement(root, 'teiHeader')
        fileDesc = ET.SubElement(teiHeader, 'fileDesc')

        # Title Statement
        titleStmt = ET.SubElement(fileDesc, 'titleStmt')
        title = ET.SubElement(titleStmt, 'title')
        recordID = ET.SubElement(titleStmt, 'recordID')
        transcription = ET.SubElement(titleStmt, 'transcription')
        respStmt = ET.SubElement(titleStmt, 'respStmt')
        resp = ET.SubElement(respStmt, 'resp')
        name = ET.SubElement(respStmt, 'name')
        note = ET.SubElement(respStmt, 'note')
        date = ET.SubElement(note, 'date')
        problems = ET.SubElement(note, 'problems')

        # Source Description
        sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
        baseText = ET.SubElement(sourceDesc, 'baseText')
        textNeeded = ET.SubElement(sourceDesc, 'textNeeded')
        noKnownText = ET.SubElement(sourceDesc, 'noKnownText')
        fragment = ET.SubElement(sourceDesc, 'fragment')
        ocrNote = ET.SubElement(sourceDesc, 'ocrNote')
        msDesc = ET.SubElement(sourceDesc, 'msDesc')
        bibl = ET.SubElement(sourceDesc, 'bibl')
        sourceNote = ET.SubElement(sourceDesc, 'sourceNote')

        # Profile Description
        profileDesc = ET.SubElement(teiHeader, 'profileDesc')
        langUsage = ET.SubElement(profileDesc, 'langUsage')
        languageNote = ET.SubElement(profileDesc, 'languageNote')
        langUsage = ET.SubElement(profileDesc, 'langUsage')
        creation = ET.SubElement(profileDesc, 'creation')
        textDesc = ET.SubElement(profileDesc, 'textDesc')
        domain = ET.SubElement(textDesc, 'domain')
        genNotes = ET.SubElement(profileDesc, 'genNotes')

        # child nodes of 'creation'
        origDate = ET.SubElement(creation, 'origDate')
        dateNotes = ET.SubElement(creation, 'dateNotes')
        origPlaces = ET.SubElement(creation, 'origPlaces')
        diocese = ET.SubElement(creation, 'diocese')
        province = ET.SubElement(creation, 'province')
        country = ET.SubElement(creation, 'country')
        geo = ET.SubElement(creation, 'geo')
        placeNotes = ET.SubElement(creation, 'placeNotes')
        orgName = ET.SubElement(creation, 'orgName')
        persName = ET.SubElement(creation, 'persName')
        altName = ET.SubElement(creation, 'altName')
        regnalYears = ET.SubElement(creation, 'regnalYears')
        delegated = ET.SubElement(creation, 'delegated')
        classNotes = ET.SubElement(creation, 'classNotes')

        # Text
        text = ET.SubElement(root, 'text')
        body = ET.SubElement(text, 'body')

        return root

    # ---------------------------------------------
    # Helper Functions
    # ---------------------------------------------
    
    def getTitleFromFileName(self, filename):
        record_id = re.findall(r'^(.*?)_', filename)[0]
        name = re.findall(r'^(?:.*?)_(.*?)_(?:.*?)\.txt$', filename)[0]
        year = re.findall(r'^(?:.*?)_(?:.*?)_(.*?)\.txt$', filename)[0]
        title = '{}. {} ({})'.format(record_id, name, year)
        return title



    def populateTeiHeader(self, root, metadata, filename):
        self.populateFileDesc(root, metadata, filename)
        self.populateProfileDesc(root, metadata, filename)

    def populateFileDesc(self, root, metadata, filename):
        title = root.find('teiHeader/fileDesc/titleStmt/title')
        title.text = self.getTitleFromFileName(filename)


        recordID = root.find('teiHeader/fileDesc/titleStmt/recordID')
        recordID.text = 'Record ID: {}'.format(str(int(metadata['RecordID'])).zfill(4))

        

    def populateProfileDesc(self, root, metadata, filename):
        diocese = root.find('teiHeader/profileDesc/creation/diocese')
        diocese.text = metadata['Diocese']

        province = root.find('teiHeader/profileDesc/creation/province')
        province.text = metadata['Province']


    def populateText(self, root, text, footnotes, metadata, filename):
        body = root.find('text/body')
        meta = ET.SubElement(body, 'div')
        head = ET.SubElement(meta, 'head')
        head.text = 'Metadata'

        for key in self.getColumnNames():
            p = ET.SubElement(meta, 'p')
            p.text = '{}: {}'.format(key, metadata[key])

        # Text
        section_names = text['section_names']
        all_text = ET.SubElement(body, 'div')
        head = ET.SubElement(all_text, 'head')
        head.text = 'Text'

        for section in section_names:
            div = ET.SubElement(all_text, 'div')
            head = ET.SubElement(div, 'head')
            head.text = section

            for line in text[section]:
                p = ET.SubElement(div, 'p')
                p.text = line

        # FootNotes
        div = ET.SubElement(all_text, 'div')
        head = ET.SubElement(div, 'head')
        head.text = 'Footnotes' 

        for line in footnotes:
            p = ET.SubElement(div, 'p')
            p.text = line 

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
