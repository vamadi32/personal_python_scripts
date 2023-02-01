import okta.models as models
from okta.client import Client

# Replace these values with your own Okta domain and API token
okta_domain = "your_okta_domain"
api_token = "your_api_token"

# Create a client object
client = Client(token=api_token, org_url=okta_domain)

# Use the client to get a list of all groups in your Okta organization
all_groups = client.groups.list()

# Iterate through the list of groups and check if each group is empty
for group in all_groups:
    members = client.groups.list_users(group.id)
    if len(members) == 0:
        print(f"Group '{group.profile.name}' is empty")

