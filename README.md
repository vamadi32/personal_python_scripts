
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

## 🚀 Have Fun!

