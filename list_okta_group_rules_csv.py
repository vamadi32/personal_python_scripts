import csv, os, logging
from okta.client import Client as OktaClient
import asyncio

# Replace the following variables with your Okta API credentials and domain
okta_domain = os.getenv("OKTA_API_BASE_URL")
okta_api_key = os.getenv("OKTA_READONLY_PROD_TOKEN")

# Initialize the Okta client with logging. 
# Change logging.INFO to logging.DEBUG for DEV
config = { 
    'orgUrl': okta_domain,
    'token': okta_api_key,
    'login': {
    "enabled": True,
    'logLevel': logging.INFO
    }
    
}

async def main():
    async with OktaClient(config) as client:
        # Retrieve all groups and their associated group rules
        groups, okta_resp, err = await client.list_groups()
        # Initialize an empty list to store the group information
        group_info = []

        # Loop through the groups and retrieve their information
        for group in groups:
            # Retrieve the group's ID and name
            group_id = group.id
            group_name = group.profile.name
        

            # # Retrieve the group's assigned users
            users, okta_resp, err = await client.list_group_users(group_id)
            # Check if the group is empty
            if not users:
                user_present = 'No'
            else:
                user_present = 'Yes'

            #retrieve the groups's assigned apps
            group_apps, okta_resp, err = await client.list_assigned_applications_for_group(group.id)
            # Check if application is assigned group
            if not group_apps:
                app_present = 'No'
            else:
                app_present = 'Yes'
            
            
            # Add the group information to the list
            group_info.append([group_id, group_name, user_present, app_present])

            # Save the group information to a CSV file
            with open('okta_groups.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Group ID', 'Group Name', 'Users Present', 'Application Present' ])
                for group in group_info:
                    writer.writerow(group)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())