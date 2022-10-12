import datetime
import os
from pprint import pprint
from typing import List
from googleapiclient.errors import HttpError

from create_bot import service
from Google import Event

def get_events_list() -> List[Event]:
    """Получает словарь с событиями из гугл календаря и возвращает
    список объектов класса Event."""
    
    output_events = []

    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='hindiguru.edu@gmail.com', timeMin=now,
            maxResults=100, singleEvents=True,
            orderBy='startTime'
        ).execute()
        dict_with_events = events_result.get('items', [])

    except HttpError as error:
        print('An error occurred: %s' % error)
    
    for event in dict_with_events:
        event_obj = Event(event=event)
        output_events.append(event_obj)

    return output_events


print(get_events_list())