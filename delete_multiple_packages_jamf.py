import argparse
import os
import requests
import logging
import json

# TO DO
# Consider using keychain 
# Configure command line arguments
parser = argparse.ArgumentParser(description='Delete packages from Jamf Pro')
parser.add_argument('environment', choices=['dev', 'prod'], help='Environment (dev or prod)')
parser.add_argument('search_string', help='Search string for package names')
parser.add_argument('package_name', help='Name of the package to delete')
args = parser.parse_args()

# Set up logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# Determine the environment and set credentials and URL accordingly
if args.environment == 'dev':
    api_username = os.getenv("JSS_DEV_USER")
    api_password = os.getenv("JSS_DEV_PASSWORD")
    jamfurl = os.getenv("JSS_DEV_URL")
else:
    api_username = os.getenv("JSS_USER")
    api_password = os.getenv("JSS_PASSWORD")
    jamfurl = os.getenv("JSS_URL")

# Jamf Pro API endpoint for package search
api_url = jamfurl + '/JSSResource/packages'
    
def getToken():
    urlendpoint = "/uapi/auth/tokens"
    payload=""
    headers={
        'Content-Type': "application/json",
        'Accept': "application/json"
    }
    response = requests.request("POST", jamfurl + urlendpoint, data=payload, headers=headers, auth=(api_username, api_password))
    return json.loads(response.text)

def invalidateToken(token):
    url = "/uapi/auth/invalidateToken"
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }
    response = requests.request("POST", jamfurl + url, data=payload, headers=headers)


def search_packages(token, api_url, api_username, api_password, search_string):
    # Set up the request headers with authentication
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }

    # Send the GET request to search for packages
    response = requests.get(api_url, headers=headers, auth=(api_username, api_password))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        packages = response.json().get('packages')
        matching_packages = []

        # Loop through the packages and find the ones that contain the search_string
        for package in packages:
            if search_string.lower() in package['name'].lower():
                matching_packages.append(package)
        
        return matching_packages

    return None

def delete_package(token, api_url, api_username, api_password, package_id):
    # Set up the request headers with authentication
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }

    # Construct the URL for deleting the package
    delete_url = '{}/{}/{}'.format(api_url, 'id', package_id)

    # Send the DELETE request to delete the package
    response = requests.delete(delete_url, headers=headers, auth=(api_username, api_password))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        logging.info(f"Package with ID: {package_id} deleted successfully!")
    else:
        print('Failed to delete the package with ID {}. Status code: {}'.format(package_id, response.status_code))

def main():
    logging.debug("Starting Program")
    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    # Search string to look for in package names
    search_string = args.search_string

    # Search for packages containing the search string
    packages_to_delete = search_packages(token, api_url, api_username, api_password, search_string)

    if packages_to_delete:
        print('Packages to delete:')
        for package in packages_to_delete:
            #print('- {}'.format(package['name']))
            # Example: Check if the package is not "AWS VPN Client-3.7.0.pkg" before deleting
            if package['name'] != args.package_name:
                # add line to delete package
                delete_package(token, api_url, api_username, api_password, package['id'])
    else:
        print('No packages containing "{}" found.'.format(search_string))

    invalidateToken(token)
if __name__ == '__main__':
    main()

