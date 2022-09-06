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


def update_event(data: dict):
    free_ivents = []
    month = data.get('month')
    day = data.get('day')
    time = data.get('time')
    user = data.get('user')
    oll_events = get_events_list()

    for simple_event in oll_events:
        if simple_event.get('summary') == 'свободно':
            free_ivents.append(simple_event)

    for event in free_ivents:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date = start_list[0].split('-')
        time1 = start_list[1].split(':')

        if date[2] == day and date[1] == month and time[0] == time1[0]:
            filtered_event = event
    
    filtered_event['summary'] = user
    
    event_id = filtered_event.get('id')
    servise.events().update(
        calendarId='oleo555rambler.ru@gmail.com',
        eventId=event_id,
        body=filtered_event
        ).execute()

data = {'month': '09', 'day': '09', 'time': ['15', '45'], 'user': 'Mihail Usenko'}

update_event(data)