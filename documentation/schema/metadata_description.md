## Metadata Field Descriptions 

## Main Database


For the “Title” field (which the TEI format requires, I think), can it just be the filename of the .txt file? (NB: the title consists of RecordID_Place_Year - and the year is followed by a “c” if the date is uncertain, e.g. 0300_Milan_1287 or 0540_Piacenza_1337c)


NB: Fields that are found in all records will be marked by a (*) next to it; other fields may be blank


- ***RecordID **: unique identifier, starting at 0001; expressed in four-digit form in filenames, but not in database

- **Date**: dates are expressed numerically; where a date is uncertain, an arbitrary intermediate year is given
   1. ***Year **
   2. **Month **
   3. **Day**
   4. **Circa** [=ca.]: field is marked ‘Yes’ if the issuing year is uncertain; it is not checked if the uncertainty concerns only the month/day
   5. **Dating Notes**: discursive field giving date ranges (for texts of uncertain dating) or other remarks concerning the dates of the text

- **Place**: the place where the council or synod associated with the text’s issuing occurred (which is usually, though not always, the diocesan or metropolitan see)
   1. ***Place**
   2. **Diocese** (often omitted in the case of provincial or legatine councils)
   3. **Province** (often omitted where a diocese is directly subject to the Holy See)
      1. Most records include entries for both diocese and province; some lack one or the other; no records lack both.
   1. ***Country_Modern** (the country in which the place of issue is currently located)
   2. ***Latitude** (for the place of issue; usually taken from GeoHack)
   3. ***Longitude** (for the place of issue usually taken from GeoHack)
   4. **PlaceNotes**: discursive field giving further information concerning place, diocese, or province

- **Classification**: The nature and jurisdictional scope of the text 
   1. ***Classification** (options include):
      1. Diocesan: legislation issued at or in association with a diocesan synod)
      2. Provincial: legislation issued at or in association with a provincial council (or a council bringing together several neighboring provinces)
      3. Legatine: legislation issued at or in association with a legatine or national council
      4. Liber Synodalis: normally, a systematic collection of diocesan legislation, often similar to (or even indistinguishable from) a diocesan compilation
      5. Compilation (Diocesan): a gathering of earlier diocesan legislation, sometimes with emendations or additions
      6. Compilation (Provincial): a gathering of earlier provincial legislation, sometimes with emendations or additions
      7. Abstract/Abbreviation: a summary or abbreviated version of an existing text
      8. Other: these include texts such as episcopal mandates or synodal ordines that do not fit neatly into the above categories but have nevertheless been included in the corpus for some reason
      9. Unclear
   1. **Issuing Authority**: The ecclesiastical authority in whose name the legislation is principally promulgated; in the case of provincial councils, the name of the metropolitan is given
   2. **Issuing Authority**: the name of the issuing bishop/archbishop/prelate 
   3. **Issuing Authority Alt**: common alternative spellings of the name of the issuing authority
   4. **Regnal Years**: the years in which the issuing authority served as bishop/archbishop of the jurisdiction concerned
      1. Start (Year)
      2. End (Year)
   1. **Delegated**: checked ‘Yes’ if the competent ecclesiastical authority delegated the task of promulgating the statutes to an official (usually a vicar general, though in cases of sede vacante this might be a neighbouring bishop or apostolic administrator)
   2. **Classification Notes**: discursive field giving information on the classification decision; in cases where the issuing of the text was delegated to someone other than the bishop/archbishop, their name and office is usually given here

- **Language**: the principal language in which the text is written
   1. **Language** (options include):
      1. Latin
      2. Italian
      3. Middle Dutch
      4. Middle English
      5. Middle High German
      6. Occitan
      7. Old Catalan
      8. Old French
      9. Old Norse
      10. Old Polish
      11. Old Portuguese
      12. Old Spanish
   1. **Language Notes**: these indicate if other languages are substantially present in the text

- **Text Needed**: marked yes if I have not yet managed to consult a manuscript/edition of the text or acquire a copy thereof

- **No Known Text**: marked yes if no known copies of the text are known to survive (or remain unidentified)

- **Fragment**: marked yes if a text is significantly incomplete (i.e. not just marred by occasional lacunae)

- **Source**: the manuscript or printed editions from which the text is taken[1]
   1. **Source**: a manuscript witness for a given text. This is usually left blank, where a printed edition is available; where it is listed, it is not necessarily the best manuscript witness – rather it is the best manuscript witness that has so far been consulted.
   2. **Source_Other**: one or more additional manuscript witnesses (or occasionally early modern transcriptions of the manuscript listed under “Source”); the list is rarely comprehensive
   3. **Edition**: the printed edition (where such exists) from which the transcription was derived
   4. **Edition_Other**: one or more additional printed editions; the list is rarely comprehensive
   5. **Source Notes**: discursive field giving information on manuscript sources or printed editions, including URL for digital copies or library shelfmarks for hard-to-find editions
   6. **Transcription Notes**: discursive field giving information concerning transcription difficulties or outstanding issues

- **Base Text**: The source from which the transcription was created, or against which transcription can be checked (note that multiple boxes can be checked yes)
   1. Hard Copy Scan: either a library hard copy or a personal copy was scanned to create a PDF
   2. WebDownload: an online PDF/image was downloaded (e.g. from Google Books)
   3. Data Capture: the text was manually inputted by a member of the project team or a transcription service (usually based on a hard copy scan or a web download)
   4. Digital MS: I possess a digital scan of the manuscript source, or of a microfilm image thereof
   5. Microfilm: I possess a microfilm of the manuscript source
   6. Other: the transcription was derived from some other text format, or (in the case of manuscripts/rare printed editions) was copied directly onsite without a digital copy being made

- **OCR**: marked yes if OCR technology was used to produce an initial transcription (note that this field was added late, and so many transcriptions that were initially generated from OCR technology are not marked accordingly) 

- ***Transcription** (only one can be checked yes)
   1. Not Started: Transcription has not yet begun
   2. In Process: Text is in queue for transcription
   3. Completed: Transcription has been created and corrected, but not reviewed by RWD
   4. Reviewed: Transcription has been reviewed by RWD (though that certainly does not mean that it is error-free!)

- **General Notes**: discursive field for miscellaneous information about the text

- **Biblio Refs**: Important Bibliographical References (note that this field is usually empty, but will hopefully be expanded over time as a digital bibliography is created)

   ​


## Notes `.txt` files

NB: the first four fields can all be completely ignored and need not be carried over into the XML-markup version of the text; they serve only to facilitate the transcription clean-up process

1. ***Record ID**: four digit numerical unique identifier, which should match the first four digits of the file name and the corresponding database entry
2. ***Date**: The year text was issued (arbitrary, where dating is uncertain - in which case date range is usually given here as well, in parentheses)
3. ***Location**: Generally equivalent to ‘Place’ field in database
4. ***Source**: Indicate the principal MS and/or printed edition from which transcription was derived
---
1. ***Transcribed by**: the name of the project member responsible for transcribing from the MS or printed edition, for correcting the initial OCR-generated transcription, and/or for formatting the transcription according to the project guidelines
2. ***Date Started**: the date the project member began transcribing/correcting/formatting the text
3. ***Date Finished**: the date the project member finished transcribing/correcting/formatting the text
4. **Reviewed RWD**: this field is added once the transcription has been reviewed by RWD, and gives the date at which the review took place
5. **Problems or Queries**: introduces a list of any issues or concerns arising from the transcription, as well as any important editorial decisions that affected the correction process
---
1. ***Notes**: any editorial notes or concerns will be noted here, with numbers in square brackets corresponding to numbered-and-square-bracketed entries in the corresponding text (not all texts will have notes, but some will have dozens or more)
________________

[1] I intend eventually to create a separate, properly organized database for all of these source/edition fields, such that each entry will simply be marked with an ID and the corresponding volume/page/folios numbers. But that’s a project for the summer or later.