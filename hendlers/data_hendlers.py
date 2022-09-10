"""В этом файле хронятся обработчики информации, своего рода сериализаторы
для наладки взаимодействия пользователя и API."""

from typing import List

from hendlers.google_tools import get_free_events, Event, get_users_booking


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


def print_booking(booking: List[str]):
    result = 'У вас актуальные бронирования на:\n'
    for string in booking:
        result += f'{string}\n'
    return result



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


def event_hour_hendler(event_str: str) -> str:
    """Принимет текст ответа пользователя и возвращает список с часом и минутой
    начала забронированного времени."""

    first_split = event_str.split(' ')
    return first_split[1].split(':')


def events_list_hendler() -> str:
    """Получает список ивентов из гугл словаря,
    забирает оттуда дату провебения, время начала и окончания
    события и выдаёт эту информацию в виде строки."""

    actions = 'Свободное время есть:\n'
    event_list = get_free_events()

    if not event_list:
        return 'На данный момент, свободного времени нет.'

    for event in event_list:
        dt_start = event.get_detatime_start()
        dt_finish = event.get_detatime_finish()

        s_dey = dt_start.get('day')
        s_monh = dt_start.get('month')
        s_hour = dt_start.get('hour')
        s_minutes = dt_start.get('minutes')

        f_hour = dt_finish.get('hour')
        f_minutes = dt_finish.get('minutes')

        one_action = (
            f'{s_dey}.{s_monh} '
            + f'c {s_hour}:{s_minutes} '
            + f'до {f_hour}:{f_minutes}'
        )
        actions += one_action + '\n'

    return actions


def get_event_month() -> List[str]:
    """Просматривает расписаение и выдаёт список месяцев в которых есть
    свободное для бронирования время."""

    valid_events_list = get_free_events()
    output_list = []
    # записывает в словарь месяца в которых есть свободное время
    for event in valid_events_list:
        dt_start = event.get_detatime_start()

        month = MONTH_DICT.get(dt_start.get('month'))
        if month not in output_list:
            output_list.append(month)
    
    return output_list


def get_event_day(choosen_month: str) -> List[str]:
    """Принимает месяц, возвращает дни в которые есть свободное для
    бронирования время."""

    first_validation_events_list = get_free_events()
    second_validation_events_list: List[Event] = []
    output_list = []

    for event in first_validation_events_list:
        dt_start = event.get_detatime_start()
        
        if dt_start.get('month') == choosen_month:
            second_validation_events_list.append(event)
    # записывает в список дни в которых есть свободное время 
    for event in second_validation_events_list:
        dt_start = event.get_detatime_start()

        day = dt_start.get('day')
        if day not in output_list:
            output_list.append(day)
    
    return output_list


def get_event_hour(choosen_month: str, choosen_day: str) -> List[str]:
    """Принимает месяц и день, выдаёт все свободные "окна" в указанный день."""

    first_validation_events_list = get_free_events()
    second_validation_events_list: List[Event] = []
    output_list = []

    for event in first_validation_events_list:
        dt_start = event.get_detatime_start()
        day = dt_start.get('day')
        month = dt_start.get('month')
        
        if month == choosen_month and day == choosen_day:
            second_validation_events_list.append(event)
    # формирует список из свободных "окон" в расписании
    for event in second_validation_events_list:
        start = event.get_detatime_start()
        finish = event.get_detatime_finish()

        hour_st = start.get('hour')
        minutes_st = start.get('minutes')
        hour_fn = finish.get('hour')
        minutes_fn = finish.get('minutes')

        action = (
            f'c {hour_st}:{minutes_st} '
            + f'до {hour_fn}:{minutes_fn}'
        )
        if action not in output_list:
            output_list.append(action)
    
    return output_list


def user_booking(username: str) -> List[str]:
    """Выдаёт список с датами и временим которые этот юзер бронировал"""

    event_list = get_users_booking(username)
    outout_list = []

    for event in event_list:
        start = event.get_detatime_start()
        finish = event.get_detatime_finish()
        
        month_st = start.get('month')
        day_st = start.get('day')
        hour_st = start.get('hour')
        minutes_st = start.get('minutes')
        hour_fn = finish.get('hour')
        minutes_fn = finish.get('minutes')
        one_action = (
            f'{day_st}.{month_st} '
            + f'c {hour_st}:{minutes_st} '
            + f'до {hour_fn}:{minutes_fn}'
        )
        outout_list.append(one_action)

    return outout_list


if __name__ == 'main':
    pass