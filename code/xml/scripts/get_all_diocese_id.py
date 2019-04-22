import csv, json

# Get all jurisdiction IDs from the CSV sheet.
# Used in cosyn.app for making some regions semi-transparent if they are not in database.

def main():
    csv_file_name = '../_input/metadata/metadata.csv'
    column_id = 14 # Update as needed if CSV changes
    diocese_ids = set()
    with open(csv_file_name, newline='') as csvfile:
            database = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in database:
                diocese_id = row[column_id]
                diocese_ids.add(diocese_id)
    ids = sorted([id for id in list(diocese_ids) if id and id != 'Jurisdiction_ID'])
    print(len(ids))
    print(json.dumps(ids))


if __name__ == '__main__':
    main()
