from pprint import pprint
from Google import Create_Service


CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


servise = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

reqest_body = {
    'summary': 'Test Calendar'
}

a = servise.calendars().insert(body=reqest_body).execute()
print(a)