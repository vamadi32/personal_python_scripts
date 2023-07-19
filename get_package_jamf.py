import requests
import os, sys, json
import logging


 # Your Jamf Pro credentials
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

def search_package(token, api_url, api_username, api_password, package_name):
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
        # Loop through the packages and find the matching package
        for package in packages:
            if package['name'] == package_name:
                return package['name']
        
    return None


def main():
    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    # Package name to search for
    package_name = '1Password-7.9.pkg'

    # Search for the package
    package_full_name = search_package(token, api_url, api_username, api_password, package_name)

    # Print the result
    if package_full_name:
        print('Package found: {}'.format(package_name))
        print('Package full name: {}'.format(package_full_name))
    else:
        print('Package not found.')
    
    invalidateToken(token)

if __name__ == '__main__':
    main()

