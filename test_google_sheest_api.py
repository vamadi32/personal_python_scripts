from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

## Please place script in the same folder as the file containing 
# private and pub key. Rename the credential file  to credentials.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet
#eg #https://docs.google.com/spreadsheets/d/1cFYJ1YXiCoI6Cx_Mud_hVcB9TFozbJoCZa3N2nq_b0Y/edit#gid=0
#from example above is in between the d/ and /edit
SPREADSHEET_ID = ''
#so long as you do not change sheet name, default should be Sheet1. 
RANGE_NAME = 'Sheet1!A1:B'

# Get credentials from the token file
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])
print(values)
