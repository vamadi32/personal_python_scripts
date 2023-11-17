import requests
import os
import json
from rich import print
from rich.logging import RichHandler
import logging
import argparse

# Create a logger with RichHandler for rich, colorful log outputs
# Use log.info, log.debug, etc., for colored logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the log level
log.addHandler(RichHandler())

# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description="Search for a device in Jamf Pro by serial number.")
parser.add_argument("serial_number", help="The serial number of the device to search for.")
args = parser.parse_args()

# Your Jamf Pro credentials
api_username = os.getenv("JSS_USER")
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
    log.info("STARTING PROGRAM")
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    log.info(f"Token Expiration: {expires}")

    device_info = search_device(token, api_url, args.serial_number)

    if device_info:
        log.info('Device found: {}'.format(device_info))
    else:
        log.info('Device not found.')

    invalidateToken(token)


if __name__ == '__main__':
    main()
