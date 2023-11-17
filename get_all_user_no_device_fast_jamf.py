import requests
import os, sys, time
import json
from rich import print
from rich.logging import RichHandler
import logging
import concurrent.futures

"""
Using Parallel processing to significantly speed up the script, especially as I am 
dealing with large data sets. However, I have to be cautious with the number of concurrent threads, 
as too many can overwhelm jamf pro server or hit rate limits on the API. 10 seem to be a safe number
Without parrallel proc: 337.27 secs
with parrallel proc: 33.84 secs!
"""

# Create a logger with RichHandler for rich, colorful log outputs
# Use log.info, log.debug, etc., for colored logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the log level
log.addHandler(RichHandler())


# Your Jamf Pro credentials and URL
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

def main():
    start_time = time.time()
    tokenResponse = getToken()
    token = tokenResponse['token']

    user_ids = get_user_ids(token)
    user_details_list = get_user_details_parallel(token, user_ids)

    users_without_devices = [
        user_details['user']['name'] for user_details in user_details_list 
        if user_details and not user_details['user'].get('links', {}).get('computers')
    ]

    print("Users without devices:")
    for user_name in users_without_devices:
        log.info(user_name)
    
    # print the total number
    log.info(f"Total number of users without devices: {len(users_without_devices)}")

    invalidateToken(token)
    end_time = time.time()  # End timing
    print(f"Script executed in {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()