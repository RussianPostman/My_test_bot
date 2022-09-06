"""В этом файле хронятся обработчики информации, своего рода сериализаторы
для наладки взаимодействия пользователя и API."""

from typing import List

from hendlers.google_tools import get_events_list


HELLO_TEXT = (
    'Я -  бот помощник вашего преподавателя. Через меня вы можете '
    + 'узнать и выбрать свободное время в графике уроков.\n'
    + 'Чтобы получить быстрый обзор свободного времени, нажмите кнопку '
    + '"Расписание"\n'
    + 'Чтобы забронировать время, нажмите кнопку "Забронировать_время", '
    + 'после чего следуйте подсказкам в интерфейсе\n'
    + 'В любой момент вы можете отменить бронирование нажав '
    + '"Отменить_бронирование"\n'
    + 'Чтобы узнать подробности моей работы нажмите кнопку /help.\n'
    + 'Приятного использования.'
    )
HELP_TEXT = (
    'Принцип моей работы следующий:\n'
    + 'Преподаватель помечает в своём кадендаре время свободное для '
    + 'бронирования студентом, я же выдаю Вам список дат и времени '
    + 'доступных для брони.'
    + 'Чтобы получить быстрый обзор свободного времени, нажмите кнопку '
    + '"Расписание"\n'
    + 'Чтобы забронировать время, нажмите кнопку "Забронировать_время", '
    + 'после чего следуйте подсказкам в интерфейсе\n'
    + 'В любой момент вы можете отменить бронирование нажав '
    + '"Отменить_бронирование"\n'
    + 'Чтобы узнать подробности моей работы нажмите кнопку /help.\n'
    + 'Приятного использования.'
)
MONTH_DICT = {
    '01': 'Январь',
    '02': 'Фефраль',
    '03': 'Март',
    '04': 'Апрель',
    '05': 'Май',
    '06': 'Июнь',
    '07': 'Июль',
    '08': 'Август',
    '09': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь'
}

MONTH_PADESH_DICT = {
    '01': 'января',
    '02': 'фефраля',
    '03': 'марта',
    '04': 'апреля',
    '05': 'майа',
    '06': 'июня',
    '07': 'июля',
    '08': 'августа',
    '09': 'сентября',
    '10': 'октября',
    '11': 'ноября',
    '12': 'декабря'
}


# class Event:
#     def __init__(self, event) -> None:
#         self.event = event
    
#     def get_deta(self) -> List[str]:



def month_convert_to_digit(input_value: int) -> int:
    """Конвертирует название месяца в его числовое выражение."""

    for num, word in MONTH_DICT.items():
        if input_value == word:
            return num
    

def admin_notification_hendler(data: dict) -> str:
    """Обрабатывает информацию для отправки сообщения об успешном
     бронировании преподавателю."""

    user = data.get('user')
    month = MONTH_PADESH_DICT[data.get('month')]
    day = data.get('day')
    hour = data.get('time')

    output_str = (
        f'Пользователь {user} забронировал урок '
        + f'{day} {month} с {hour[0]}:{hour[1]}'
        )
    
    return output_str


def events_list_hendler() -> str:
    """Получает список ивентов из гугл словаря,
    забирает оттуда дату провебения, время начала и окончания
    события и выдаёт эту информацию в виде строки."""

    input_list = get_events_list()
    actions = 'Свободное время есть:\n'
    event_list = []

    if not input_list:
        return 'Уточните, настроен ли гугл календарь у преподавателя.'

    for simple_event in input_list:
        if simple_event.get('summary') == 'свободно':
            event_list.append(simple_event)

    if not event_list:
        return 'На данный момент, свободного времени нет.'

    for event in event_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        finish = event['end'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        finish_list = finish.split('T')
        date_start_split = start_list[0].split('-')
        time_start_split = start_list[1].split(':')
        finish_time_split = finish_list[1].split(':')
        one_action = (
            f'{date_start_split[2]}.{date_start_split[1]} '
            + f'c {time_start_split[0]}:{time_start_split[1]} '
            + f'до {finish_time_split[0]}:{finish_time_split[1]}'
        )
        actions += one_action + '\n'

    return actions


def get_event_month() -> List[str]:
    """Просматривает расписаение и выдаёт список месяцев в которых есть
    свободное для бронирования время."""

    input_list = get_events_list()
    valid_events_list = []
    output_list = []
    # выбираает ивенты с пометкой 'свободно'
    for simple_event in input_list:
        if simple_event.get('summary') == 'свободно':
            valid_events_list.append(simple_event)
    # записывает в словарь месяца в которых есть свободное время
    for event in valid_events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date_start_split = start_list[0].split('-')

        month = MONTH_DICT.get(date_start_split[1])
        if month not in output_list:
            output_list.append(month)
    
    return output_list


def get_event_day(choosen_month: str) -> List[str]:
    """Принимает месяц, возвращает дни в которые есть свободное для
    бронирования время."""

    input_list = get_events_list()
    first_validation_events_list = []
    second_validation_events_list = []
    output_list = []
    # выбираает ивенты с пометкой 'свободно'
    for simple_event in input_list:
        if simple_event.get('summary') == 'свободно':
            first_validation_events_list.append(simple_event)
    # из всего списка ивентов выбирает только евенты указанного месяца
    for event in first_validation_events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date_start_split = start_list[0].split('-')
        
        if date_start_split[1] == choosen_month:
            second_validation_events_list.append(event)
    # записывает в список дни в которых есть свободное время 
    for event in second_validation_events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date_start_split = start_list[0].split('-')

        day = date_start_split[2]
        if day not in output_list:
            output_list.append(day)
    
    return output_list


def get_event_hour(choosen_month: str, choosen_day: str) -> List[str]:
    """Принимает месяц идень, выдаёт все свободные "окна" в указанный день."""

    input_list = get_events_list()
    first_validation_events_list = []
    second_validation_events_list = []
    output_list = []
    # выбираает ивенты с пометкой 'свободно'
    for simple_event in input_list:
        if simple_event.get('summary') == 'свободно':
            first_validation_events_list.append(simple_event)
    # из всего списка ивентов выбирает только евенты указанного месяца и дня
    for event in first_validation_events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        date_start = start_list[0].split('-')
        
        if date_start[1] == choosen_month and date_start[2] == choosen_day:
            second_validation_events_list.append(event)
    # формирует список из свободных "окон" в расписании
    for event in second_validation_events_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        finish = event['end'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        finish_list = finish.split('T')
        time_start_split = start_list[1].split(':')
        finish_time_split = finish_list[1].split(':')
        action = (
            f'c {time_start_split[0]}:{time_start_split[1]} '
            + f'до {finish_time_split[0]}:{finish_time_split[1]}'
        )
        if action not in output_list:
            output_list.append(action)
    
    return output_list


def event_hour_hendler(event_str: str) -> str:
    """Принимет текст ответа пользователя и возвращает список с часом и минутой
    начала забронированного времени."""

    first_split = event_str.split(' ')
    return first_split[1].split(':')


def user_booking(username: str) -> List[str]:
    """Выдаёт список с датами и временим которые этот юзер бронировал"""

    input_list = get_events_list()
    event_list = []
    outout_list = []

    for simple_event in input_list:
        if simple_event.get('summary') == username:
            event_list.append(simple_event)

    if not event_list:
        event_list.append('На данный момент, свободного времени нет.')

    for event in event_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        finish = event['end'].get('dateTime', event['start'].get('date'))
        start_list = start.split('T')
        finish_list = finish.split('T')
        date_start_split = start_list[0].split('-')
        time_start_split = start_list[1].split(':')
        finish_time_split = finish_list[1].split(':')
        one_action = (
            f'{date_start_split[2]}.{date_start_split[1]} '
            + f'c {time_start_split[0]}:{time_start_split[1]} '
            + f'до {finish_time_split[0]}:{finish_time_split[1]}'
        )
        outout_list.append(one_action)

    return outout_list


