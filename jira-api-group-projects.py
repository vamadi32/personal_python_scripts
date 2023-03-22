import requests
import json, os, sys

# A work in progress

api_token = os.getenv("JIRA_PERSO_TOKEN")


# Set up the Jira API endpoint and authentication details
jira_url =os.getenv("JIRA_PROD_URL")

# Set the API endpoint URLs
groups_endpoint = f'{jira_url}/rest/api/3/group/member'
projects_endpoint = f'{jira_url}/rest/api/3/group'

# Define the headers for the API requests
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_token}'
}

# Retrieve a list of groups
response = requests.get(groups_endpoint, headers=headers)
if response.status_code == 200:
    groups = json.loads(response.text)['values']
    print(f'Total groups: {len(groups)}')
    print('List of groups:')

    for group in groups:
        print(group['name'])

        # Retrieve a list of projects for each group
        response = requests.get(f'{projects_endpoint}?group={group["name"]}', headers=headers)
        if response.status_code == 200:
            projects = json.loads(response.text)['values']
            if len(projects) > 0:
                print('Projects:')
                for project in projects:
                    print(f'- {project["name"]}')
            else:
                print('No projects found for this group.')
        else:
            print('Failed to retrieve projects for this group.')

        print()
else:
    print('Failed to retrieve groups.')
