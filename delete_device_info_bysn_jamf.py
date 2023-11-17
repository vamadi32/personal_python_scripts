import requests
import os, sys
import json
import logging
import argparse


"""
Usage:
python3 delete_device_info_bysn_jamf.py [enter serial number] --delete
if --delete is not entered, output information for the device
"""
# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description="Search for and optionally delete a device in Jamf Pro by serial number.")
parser.add_argument("serial_number", help="The serial number of the device to search for.")
parser.add_argument("--delete", action="store_true", help="Delete the device after finding it.")
args = parser.parse_args()

# Your Jamf Pro credentials
api_username = os.getenv("JSS_USER")
print(api_username)
#os._exit(0)
api_password = os.getenv("JSS_PASSWORD")
jamfurl = os.getenv("JSS_URL")

# Jamf Pro API endpoint for computer search
api_url = jamfurl + '/JSSResource/computers/match/'


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


def delete_device(token, device_id):
    api_delete_url = jamfurl + f'/JSSResource/computers/id/{device_id}'
    print(api_delete_url)
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }
    response = requests.delete(api_delete_url, headers=headers)

    if response.status_code != 200:
        print(f"Error deleting device: HTTP Status Code {response.status_code}, Response: {response.text}")
        return False

    return True



def search_device(token, api_url, serial_number):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }

    response = requests.get(api_url + serial_number, headers=headers)

    if response.status_code == 200:
        computers = response.json().get('computers')
        if computers:
            return computers[0]  # Return the first matching computer
        else:
            return None
    else:
        return None


def main():
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    device_info = search_device(token, api_url, args.serial_number)

    if device_info:
        print('Device found: {}'.format(device_info))
        if args.delete:
            confirm = input("Are you sure you want to delete this device? Type 'yes' to confirm: ")
            if confirm.lower() == 'yes':
                if delete_device(token, device_info['id']):
                    print("Device successfully deleted.")
                else:
                    print("Failed to delete the device.")
                    print(device_info['id'])
            else:
                print("Device deletion cancelled.")
    else:
        print('Device not found.')

    invalidateToken(token)


if __name__ == '__main__':
    main()
