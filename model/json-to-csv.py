import json
import csv

# read JSON data and create a list of dictionaries
data = []
with open('Kindle_Store_5_2018.json', 'r') as json_file:
    for line in json_file:
        entry = json.loads(line)
        if 'vote' not in entry:
            entry['vote'] = "0"  # set 'vote' to "0" if not present
        data.append(entry)

# modify the 'style' column
for entry in data:
    if 'style' in entry:
        style_value = entry['style'].get('Format:', '')
        entry['style'] = style_value

# determine the fieldnames dynamically based on the keys in the data
fieldnames = set()
for entry in data:
    fieldnames.update(entry.keys())

# write the json data to a CSV file
with open('Kindle_Store_5_2018.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(fieldnames))
    
    writer.writeheader()
    for entry in data:
        writer.writerow(entry)