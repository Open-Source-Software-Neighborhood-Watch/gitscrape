"""Convert csv to json compliant with open source nutrition label format.

Thank you @Laxman on SO: https://stackoverflow.com/a/48131334
Thank you @jancod on SO: https://stackoverflow.com/a/29020644
"""

import csv
import json

file = "../processed_data/julia_combined_results_gitscrape_20211107.csv"
json_file = "output_file_name.json"

# Read CSV File
def read_CSV(file, json_file):
    # each field type must be specified, otherwise the csv reader converts
    # all fields to str. If the integer fields are treated as strings, the
    # open source nutrition label prototype will not sort properly.
    row_types = {
        "repo_name": str,
        "forks": float,
        "stars": int,
        "days_since_last_updated": int,
    }
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend(
                [
                    {
                        # row_types[field[i]] leads to a field-specific
                        # type conversion
                        field[i]: row_types[field[i]](row[field[i]])
                        for i in range(len(field))
                    }
                ]
            )
        convert_write_json(csv_rows, json_file)


# Convert csv data into json
def convert_write_json(data, json_file):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(",", ": ")))
        f.write(json.dumps(data))


read_CSV(file, json_file)
