import requests
import os, csv
import time
import json
from rich import print
from rich.logging import RichHandler
import logging
import concurrent.futures

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(RichHandler())

# Jamf Pro credentials and URL
api_username = os.getenv("JSS_USER")
api_password = os.getenv("JSS_PASSWORD")
jamfurl = os.getenv("JSS_URL")

def getToken():
    urlendpoint = "/uapi/auth/tokens"
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json"
    }
    response = requests.post(jamfurl + urlendpoint, headers=headers, auth=(api_username, api_password))
    return json.loads(response.text)

def invalidateToken(token):
    url = "/uapi/auth/invalidateToken"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }
    requests.post(jamfurl + url, headers=headers)

def get_user_ids(token):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }
    users_url = jamfurl + '/JSSResource/users'
    response = requests.get(users_url, headers=headers)

    if response.status_code == 200:
        return [user['id'] for user in response.json().get('users', [])]
    else:
        log.error(f"Error retrieving user IDs: HTTP Status Code {response.status_code}")
        return []

def get_user_details_parallel(token, user_ids):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }
    
    def fetch_user_details(user_id):
        user_url = jamfurl + f'/JSSResource/users/id/{user_id}'
        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving user details for ID {user_id}: HTTP Status Code {response.status_code}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(fetch_user_details, user_ids))
    
def get_computer_details(token, computer_id):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }
    computer_url = jamfurl + f'/JSSResource/computers/id/{computer_id}'
    response = requests.get(computer_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        log.error(f"Error retrieving computer details for ID {computer_id}: HTTP Status Code {response.status_code}")
        return None

def main():
    start_time = time.time()
    tokenResponse = getToken()
    token = tokenResponse['token']

    user_ids = get_user_ids(token)
    user_details_list = get_user_details_parallel(token, user_ids)

    users_with_multiple_devices = []

    for user_details in user_details_list:
        if user_details and len(user_details['user'].get('links', {}).get('computers', [])) > 1:
            user_name = user_details['user']['name']
            computer_ids = [computer['id'] for computer in user_details['user']['links']['computers']]
            computer_details = [get_computer_details(token, cid) for cid in computer_ids]
            device_serials = [cd['computer']['general']['serial_number'] for cd in computer_details if cd]
            users_with_multiple_devices.append((user_name, device_serials))

    # Write to CSV
    with open('users_with_multiple_devices.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User Name', 'Device Serial Numbers'])
        for user, devices in users_with_multiple_devices:
            writer.writerow([user, ', '.join(devices)])

    # Print the total number
    log.info(f"Total number of users with multiple devices: {len(users_with_multiple_devices)}")

    invalidateToken(token)
    end_time = time.time()
    print(f"Script executed in {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()