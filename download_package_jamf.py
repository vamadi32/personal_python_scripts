import requests
import os, sys, json
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
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + token
    }

    response = requests.get(api_url, headers=headers, auth=(api_username, api_password))

    if response.status_code == 200:
        packages = response.json().get('packages')
        matching_packages = []

        for package in packages:
            if search_string.lower() in package['name'].lower():
                matching_packages.append(package)

        return matching_packages

    return None

def download_package(token, api_url, api_username, api_password, package_id, save_path):
    # Construct the URL for downloading the package
    download_url = '{}/{}/{}'.format(api_url, 'id', package_id)
    

    # Set up the request headers with authentication
    headers = {
        'Accept': 'application/octet-stream',
        'Authorization': "Bearer " + token
    }

    # Send the GET request to download the package
    response = requests.get(download_url, headers=headers, auth=(api_username, api_password), stream=True)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the binary response content to a file
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.info('Package downloaded and saved to: {}'.format(save_path))
    else:
        print('Failed to download the package with ID {}. Status code: {}'.format(package_id, response.status_code))


def main():
    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    # Eample Package name to search for
    package_name = 'depnotify-installersDEV'

    # Search for the package
    package_full_name = search_packages(token, api_url, api_username, api_password, package_name)
    

    # Print the result
    if package_full_name:
        logging.info('Package found: {}'.format(package_name))
        logging.info('Package full name: {}'.format(package_full_name))
    else:
        logging.info('Package not found.')
    
    if package_full_name:
        for package in package_full_name:
            save_path = '/tmp/{}'.format(package['name'])
            logging.info('Downloading package: {}'.format(package['name']))
            download_package(token, api_url, api_username, api_password, package['id'], save_path)
    else:
        logging.info('No packages containing "{}" found.'.format(package_name))
    
    invalidateToken(token)

if __name__ == '__main__':
    main()




