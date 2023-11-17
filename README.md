
## 🚀 AUTOPKG TOGGLER!
1. [autopkg_toggler.py](autopkg_toggler.py)
  
  **This is a personal script to help me Toggle between Autopkg dev and prod environments.**


# Setup the environment variables before running.


-  Using your favaourite text editor, save the following in your default shell mine is ~/.zshrc:
```
    export JSS_USER=<enter prod user here>

    export JSS_PASSWORD=<enter prod pw here>

    export JSS_URL=<enter prod url here>

    export JSS_DEV_USER=<enter dev user here>

    export JSS_DEV_PASSWORD=<enter dev password here>

    export JSS_DEV_URL=<enter url password here>
```

# restart terminal/IDE or do:
    

    source ~/.zshrc 
    This is assuming you stored the environmental variables in ~/.zshrc

# sample command to swap to dev:
    
    python3 autopkg_toggler.py dev

2. [getgitInfo.py](getgitInfo.py)


 - **This python script will get current git directory sha, url
 and concatenate them to form the current commit url.
 I am trying to convert this into an autopkg processor for audit purpose**


3. [jira-api-group-projects.py](jira-api-group-projects.py)

   PLEASE NOTE >>> This is incomplete and still being composed.

 - **This is a python script to get all jira groups and project they have access to**
 
4. [list_okta_group_rules_csv.py](list_okta_group_rules_csv.py)


 - **This is a python script that will get all Okta groups from your okta instance,
 check if group is empty and assigned an app, and save the info into a csv**

 5. [delete_all_user_no_device_fast_jamf.py](delete_all_user_no_device_fast_jamf.py)
 # Jamf Pro User Cleanup Script

## Overview
This Python script is designed to interact with a Jamf Pro server to identify users without assigned devices and optionally delete a specified number of these users. It's particularly useful in environments where user accounts need to be regularly audited and cleaned up for efficient resource management.

## Features
- Retrieve a list of all users from Jamf Pro.
- Identify users who do not have any devices assigned to them.
- Delete a specified number of users who do not have devices (up to 10 by default).

## Requirements
- Python 3.x
- `requests` library (install with `pip install requests`)
- Access to a Jamf Pro server with appropriate API permissions.

## Setup
1. Clone the repository or download the script to your local machine.
2. Ensure Python 3 is installed on your system.
3. Install the `requests` library if not already installed.
4. Set up environment variables for your Jamf Pro credentials:
   - `JSS_USER`: Your Jamf Pro username.
   - `JSS_PASSWORD`: Your Jamf Pro password.
   - `JSS_URL`: The URL of your Jamf Pro server.

## Usage
Run the script from the command line:

```bash
python3 delete_all_user_no_device_fast_jamf.py
```


## 🚀 Have Fun!

