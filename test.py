import datetime
from pprint import pprint
from typing import List
from googleapiclient.errors import HttpError

from Google import Create_Service


CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']


servise = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def get_events_list() -> List[dict]:
    """Получает словарь с событиями из гугл календаря."""

    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = servise.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        # pprint(events_result)
        events = events_result.get('items', [])

    except HttpError as error:
        print('An error occurred: %s' % error)

    return events
