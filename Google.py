"""Этот файл взят из интернета. Он помогает получением и обновлением токена,
а так же с инициализацией гугл снрвисов."""

import os
from typing import Dict
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def Oauth2_autentefication():
    """Создаёт объект сервиса."""

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('docs/token.json'):
        creds = Credentials.from_authorized_user_file('docs/token.json', SCOPES)
    else:
        return None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                return None
        # Save the credentials for the next run
            with open('docs/token.json', 'w') as token:
                token.write(creds.to_json()) 

    service = build('calendar', 'v3', credentials=creds)
    return service


class Event:
    """Клас для распарсивания информации об ивентах."""

    def __init__(self, event) -> None:
        self.event = event

    def get_detatime_start(self) -> Dict[str, str]:
        """Возвращает словарь в котором по ключам: 'month', 'day',
        'hour', 'minutes' можно получить месяц, день , час и минуту начала события"""
    
        output_dict = {}

        start = self.event['start'].get('dateTime', self.event['start'].get('date'))
        start_list = start.split('T')
        date_start_list = start_list[0].split('-')
        time_start_list = start_list[1].split(':')
        
        output_dict['month'] = date_start_list[1]
        output_dict['day'] = date_start_list[2]
        output_dict['hour'] = time_start_list[0]
        output_dict['minutes'] = time_start_list[1]

        return output_dict

    def get_detatime_finish(self) -> Dict[str, str]:
        """Возвращает словарь в котором по ключам: 'month', 'day',
        'hour', 'minutes' можно получить месяц, день , час и минуту окончания события"""

        output_dict = {}

        finish = self.event['end'].get('dateTime', self.event['start'].get('date'))
        finish_list = finish.split('T')
        date_finish_list = finish_list[0].split('-')
        time_finish_list = finish_list[1].split(':')
        
        output_dict['month'] = date_finish_list[1]
        output_dict['day'] = date_finish_list[2]
        output_dict['hour'] = time_finish_list[0]
        output_dict['minutes'] = time_finish_list[1]

        return output_dict
    
    def update_field(self, field: str, value: str):
        self.event[field] = value


class GoogleCalendarHelper:
	...

class GoogleDriverHelper:
	...


if __name__ == '__main__':
	pass