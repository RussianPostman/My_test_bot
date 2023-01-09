"""В этом файле хронятся """

import datetime
import os
from googleapiclient.errors import HttpError
from typing import List
from pprint import pprint
from dotenv import load_dotenv

# from create_bot import service
from Google import Oauth2_autentefication
from Google import Event


load_dotenv()

CALENDAR_ID = os.getenv('CALENDAR_ID')


def get_free_events() -> List[Event]:
    """Получает от гугл календаря список событий и отбирает все с пометкой 
    "+" """

    free_events = []
    all_event = get_events_list()

    if all_event is None:
        return None

    for simple_event in all_event:
        if simple_event.event.get('summary') == '+':
            free_events.append(simple_event)
    return free_events


def get_users_booking(username: str) -> List[Event]:
    """Отбирает все события забронированные пользователем."""

    event_list = []
    input_list = get_events_list()
    for simple_event in input_list:
        if simple_event.event.get('summary') == username:
            event_list.append(simple_event)
    return event_list


def get_events_list() -> List[Event]:
    """Получает словарь с событиями из гугл календаря и возвращает
    список объектов класса Event."""
    
    output_events = []
    service = Oauth2_autentefication()

    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId=CALENDAR_ID, timeMin=now,
            maxResults=100, singleEvents=True,
            orderBy='startTime'
        ).execute()
        dict_with_events = events_result.get('items', [])

    except AttributeError as error:
        print('An error occurred: %s' % error)
        return None
    
    for event in dict_with_events:
        event_obj = Event(event=event)
        output_events.append(event_obj)

    return output_events


def update_event(data: dict):
    service = Oauth2_autentefication()

    free_ivents = []
    month = data.get('month')
    day = data.get('day')
    time = data.get('time')
    user = data.get('user')
    free_ivents: List[Event] = get_events_list()

    for event in free_ivents:
        start = event.get_detatime_start()
        month_st = start.get('month')
        day_st = start.get('day')
        hour_st = start.get('hour')

        if day_st == day and month_st == month and time[0] == hour_st:
            filtered_event = event
    
    filtered_event.update_field('summary', user)
    
    event_id = filtered_event.event.get('id')
    service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=filtered_event.event
        ).execute()


def cencel_booking(data: str, username: str):
    service = Oauth2_autentefication()

    input_list = get_users_booking(username)

    data_split = data.split(' ')
    deta_input = data_split[0].split('.')
    day = deta_input[0]
    month = deta_input[1]
    time = data_split[2].split(':')

    
    for event in input_list:
        start = event.get_detatime_start()
        month_st = start.get('month')
        day_st = start.get('day')
        hour_st = start.get('hour')
        minutes_st = start.get('minutes')

        if day_st == day and month_st == month and time[0] == hour_st\
            and time[1] == minutes_st:

            filtered_event = event
    
    filtered_event.update_field('summary', '+')
    
    event_id = filtered_event.event.get('id')
    service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=filtered_event.event
        ).execute()
    

if __name__ == 'main':
    pass