# csv2json.py (v1)

This script reads in `data.csv` (which is the csv file exported by Prof. Dorin's database) and exports one JSON file per record ID. (As of Mar 05, 2018, it exports 923 JSON files.)

## Notes

- In the csv file, a unicode character () is known to occur in the following fields.
    - BaseText
    - GeneralNotes
    - SourceNotes
    - PlaceNotes
    - DateNotes
    - Transcription Notes

- Basically, it is a tab character which separates multiple values. For example, in the `BaseText` field, it appears like this `"GoogleBooksDigital MSData Capture"`.

- I have parsed it into a list of values as follows.
```
Input: "GoogleBooksDigital MSData Capture"
Output: ["GoogleBooks", "Digital MS", "Data Capture"]
```

- There are other **unicode** characters that appear in the database, such as foreign characters or cross sign. I have left them untouched.

- For an example of the JSON file, see the prettified version here: https://codebeautify.org/jsonviewer/cbdc2338

