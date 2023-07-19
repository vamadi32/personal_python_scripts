#!/usr/bin/env python3

'''
Edited by:
Victor Amadi
inspiration from Nathan Ahrens work
27/03/2022

Description:
Use this script to automatically download all the scripts from Jamf.
Requires "requests" to be installed (pip3 install requests)
Requires that the following values are in the user's environment variables:
JSS_USER=[jamf username]
JSS_PASSWORD=[jamf password] - encode it using base64.b64encode("password")
JSS_URL = "https://yourcompany.jamfcloud.com"

Jamf API Documentation:
UAPI (used for retrieving scripts):
https://yourcompany.jamfcloud.com/uapi/doc/
Classic API (used for retrieving extension attributes):
https://developer.jamf.com/apis/classic-api/index
'''

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

def getScripts(token, page):
   # url = "/uapi/settings/scripts?page=" + str(page) + "&page-size=100&sort=id"
    url = "/api/v1/scripts?page=" + str(page) + "&page-size=100&sort=id" + "%3Aasc"
    payload = ""
    headers = {
        'Accept': "application/json",
        'Authorization': "Bearer " + token
    }
    
    response = requests.request("GET", os.environ['JSS_URL'] + url, data=payload, headers=headers)
    if response.status_code == 200:
         return json.loads(response.text)
    else:
        logging.ERROR(response.status_code)
        sys.exit(0)

def main():
    logging.info(f"Starting Program")

    # Make directory for today's date
    dirName = 'scripts'
    try:
        os.mkdir(current_date)
        os.mkdir(current_date + '/' + dirName)
        print("Directory ", dirName, " created")
    except FileExistsError:
        print("Directory ", dirName, " already exists")
        exit()

    # Get the token
    tokenResponse = getToken()
    token = tokenResponse['token']
    expires = tokenResponse['expires']
    logging.info(f"Token Expiration: {expires}")

    scriptResponse = getScripts(token,0)
    scriptCount = scriptResponse['totalCount']
    scriptList = scriptResponse['results']

    pageCount = int(scriptCount/len(scriptList)) + 1
    page = 1

    for page in range(1, pageCount):
        # process current scriptList
        for script in scriptList:
            name = script['name']
            content = script['scriptContents']
            f = open(current_date + "/scripts/" + name, 'w')
            f.write(content)
            f.close()

        # get next page
        scriptList = getScripts(token, page)['results']

    # invalidate the token
    invalidateToken(token)

if __name__ == "__main__":
    main()