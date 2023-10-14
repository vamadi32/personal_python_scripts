import csv
import re, os
import requests

# Specify the input text file, output CSV file, and Okta API endpoint
input_text_file = os.getenv('HOME')+'/Desktop/user_1pass.txt'
output_csv_file = 'output2.csv'
okta_api_url = os.getenv('OKTA_PROD_URL')+'users'  # Replace with the actual Okta API endpoint
okta_api_token = os.getenv('OKTA_API_RO')  # Replace with your actual Okta API token

# Function to check if the user exists in Okta and get their status
def check_user_status(email):
    headers = {
        'Authorization': f'SSWS {okta_api_token}',
    }
    response = requests.get(okta_api_url, headers=headers, params={'q': email})
    if response.status_code == 200:
        users = response.json()
        if users:
            user = users[0]
            return user['status']  # Assuming 'status' field indicates user status in Okta
    return 'Not Found'

# Initialize lists to store extracted data
data = []

# Regular expressions to match the ID, Name, Last Authentication, and Email patterns
id_pattern = r'ID:\s*(\d+)'
name_pattern = r'Name:\s*([^\\n]+)'
last_auth_pattern = r'Last Authentication:\s*([^\\n]+)'
email_pattern = r'Email:\s*([^\\n]+)'

# Read the input text file
with open(input_text_file, 'r') as text_file:
    text = text_file.read()

    # Find all matches using regular expressions
    id_matches = re.findall(id_pattern, text)
    name_matches = re.findall(name_pattern, text)
    last_auth_matches = re.findall(last_auth_pattern, text)
    email_matches = re.findall(email_pattern, text)

    # Combine the matches into a list of dictionaries
    for i in range(len(id_matches)):
        item = {
            'ID': id_matches[i],
            'Name': name_matches[i],
            'Last Authentication': last_auth_matches[i],
            'Email': email_matches[i],
        }

        # Check Okta for user status
        okta_status = check_user_status(item['Email'])
        item['Okta Status'] = okta_status
        data.append(item)

# Write the data to a CSV file
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'Name', 'Last Authentication', 'Email', 'Okta Status'])

    for item in data:
        csv_writer.writerow([item['ID'], item['Name'], item['Last Authentication'], item['Email'], item['Okta Status']])

print(f'Data has been successfully written to {output_csv_file}.')
