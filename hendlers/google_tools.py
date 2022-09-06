"""В этом файле хронятся """

import datetime
import os
from googleapiclient.errors import HttpError
from typing import List
from pprint import pprint
from dotenv import load_dotenv

from create_servise import service


load_dotenv()

CALENDAR_ID = os.getenv('CALENDAR_ID')

def get_events_list() -> List[dict]:
    """Получает словарь с событиями из гугл календаря."""

    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=100, singleEvents=True,
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
    service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=filtered_event
        ).execute()


def cencel_booking(data: str, username: str):
    input_list = get_events_list()
    event_list = []

    data_split = data.split(' ')
    deta_input = data_split[0].split('.')
    day = deta_input[0]
    month = deta_input[1]
    time = data_split[2].split(':')


    for simple_event in input_list:
        if simple_event.get('summary') == username:
            event_list.append(simple_event)
    
    for event in event_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date = start_list[0].split('-')
        time1 = start_list[1].split(':')

        if date[2] == day and date[1] == month and time[0] == time1[0]\
            and time[1] == time1[1]:

            filtered_event = event
    
    filtered_event['summary'] = 'свободно'
    
    event_id = filtered_event.get('id')
    service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=filtered_event
        ).execute()
    
