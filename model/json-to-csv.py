import json
import csv

data = []
with open('Kindle_Store_5_2018.json', 'r') as json_file:
    for line in json_file:
        entry = json.loads(line)
        if 'vote' not in entry:
            entry['vote'] = "0"  
        data.append(entry)

num_data_rows_json = len(data)

for entry in data:
    if 'style' in entry:
        style_value = entry['style'].get('Format:', '')
        entry['style'] = style_value

fieldnames = set()
for entry in data:
    fieldnames.update(entry.keys())

with open('Kindle_Store_5_2018.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(fieldnames))
    
    writer.writeheader()
    for entry in data:
        writer.writerow(entry)

num_data_rows_csv = len(data)

print(f"Number of data rows in JSON: {num_data_rows_json}")
print(f"Number of data rows in CSV output: {num_data_rows_csv}")
