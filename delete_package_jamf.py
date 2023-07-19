import requests
import os, json
import logging


logging.basicConfig(level=logging.DEBUG, 
format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)

 # Your Jamf Pro credentials
api_username = os.getenv("JSS_USER")
api_password = os.getenv("JSS_PASSWORD")
jamfurl = os.getenv("JSS_URL")

# Jamf Pro API endpoint for package search
api_url = jamfurl + '/JSSResource/packages'


# Get bearer token
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
    logging.info(response)

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
                return package
        
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
        print('Package deleted successfully.')
    else:
        print('Failed to delete the package. Status code: {}'.format(response.status_code))


def main():
    logging.info("Starting Programm")
    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    # Example Package name to search for
    package_name = '1Password8-8.10.6.pkg'

    # Search for the package
    package = search_package(token, api_url, api_username, api_password, package_name)

    # Print the result
    if package:
        logging.info(f'Package found: {package_name}')

        # Delete the package
        delete_package(token, api_url, api_username, api_password, package['id'])
    else:
        logging.ERROR('Package not found.')
    
    invalidateToken(token)

if __name__ == '__main__':
    main()

