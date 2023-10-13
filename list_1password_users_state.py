import csv

# Specify the input JSON file and output CSV file names
input_json_file = 'user_1pass.txt'
output_csv_file = 'output.csv'

# Create a CSV file and write the header
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'Name', 'Last Authentication', 'State'])

# Initialize variables to store data
current_item = {}
data = []

# Open the input JSON file and read line by line
with open(input_json_file, 'r') as json_file:
    for line in json_file:
        line = line.strip()

        # Check if the line is not empty
        if line:
            key, value = [item.strip() for item in line.split(':', 1)]

            # Store the key-value pairs in the current item
            if key == 'ID':
                current_item['ID'] = value
            elif key == 'Name':
                current_item['Name'] = value
            elif key == 'Last Authentication':
                current_item['Last Authentication'] = value
            elif key == 'State':
                current_item['State'] = value

        # If a complete item has been collected, add it to the data list and reset current_item
        if len(current_item) == 4:
            data.append(current_item)
            current_item = {}

# Write the data to the CSV file
with open(output_csv_file, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for item in data:
        csv_writer.writerow([item['ID'], item['Name'], item['Last Authentication'], item['State']])

print(f'Data has been successfully written to {output_csv_file}.')
