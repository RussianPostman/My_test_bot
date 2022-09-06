from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_bt = KeyboardButton('/help')
schedule_bt = KeyboardButton('/Расписание')
time_chose_bt = KeyboardButton('/Забронировать_время')
time_cansell_bt = KeyboardButton('/Отменить_бронирование')

kb_on_start = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_on_start.add(time_chose_bt)
kb_on_start.add(time_cansell_bt)
kb_on_start.row(schedule_bt, help_bt)

def generate_bottoms(war_list: List[str]) -> ReplyKeyboardMarkup:
    stop_bt = KeyboardButton('/отмена')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for botton_text in war_list:
        keyboard.insert(KeyboardButton(botton_text))
    return keyboard.add(stop_bt)