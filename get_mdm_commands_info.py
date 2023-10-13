import requests
import json
import base64
import os, sys
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, 
format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)

requests.packages.urllib3.disable_warnings()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Jamf API credentials
username = os.getenv("JSS_USER")
password = os.getenv("JSS_PASSWORD")
jamfurl = os.getenv("JSS_URL")


def getToken():
    urlendpoint = "/uapi/auth/tokens"
    payload=""
    headers={
        'Content-Type': "application/json",
        'Accept': "application/json"
    }
    response = requests.request("POST", jamfurl + urlendpoint, data=payload, headers=headers, auth=(username, password))
    # token = parsed_response['token']
    # expires = parsed_response['expires']
    return json.loads(response.text)

def invalidateToken(token):
    url = "/uapi/auth/invalidateToken"
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + token
    }
    response = requests.request("POST", os.environ['JSS_URL'] + url, data=payload, headers=headers)

def get_mdm_commands(token, page):
    url = "/api/v1/mdm/commands?page=" + str(page) + "&page-size=100&sort=dateSent" + "%3Aasc"
    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': "Bearer " + token
    }
    
    response = requests.request("GET", os.environ['JSS_URL'] + url, data=payload, headers=headers)
    if response.status_code == 200:
         return json.loads(response.text)
    else:
        logging.error(response.status_code)
        sys.exit(0)

def main():
    logging.info(f"Date: {current_date}")
    logging.info(f"Starting Program")

    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")
    scriptResponse = get_mdm_commands(token,0)
    

     # invalidate the token
    invalidateToken(token)

if __name__ == "__main__":
    main()