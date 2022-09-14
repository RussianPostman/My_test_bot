from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_bt = KeyboardButton('/help')
schedule_bt = KeyboardButton('/Расписание')
my_booking_bt = KeyboardButton('/Мои_бронирования')

get_booking_bt = KeyboardButton('/Забронировать_время')
time_cansell_bt = KeyboardButton('/Отменить_бронирование')
back_bt = KeyboardButton('/Назад')

admin_agry_bt = KeyboardButton('Да')
stop_bt = KeyboardButton('/отмена')

kb_on_start = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kb_on_start.add(my_booking_bt)
kb_on_start.add(time_cansell_bt)
kb_on_start.row(schedule_bt, help_bt)

kb_empty_booking = ReplyKeyboardMarkup(resize_keyboard=True)
kb_empty_booking.add(get_booking_bt)
kb_empty_booking.add(back_bt)

kb_booking = ReplyKeyboardMarkup(resize_keyboard=True)
kb_booking.add(time_cansell_bt)
kb_booking.add(get_booking_bt)
kb_booking.add(back_bt)

kb_admin = ReplyKeyboardMarkup()
kb_admin.add(admin_agry_bt)
kb_admin.add(stop_bt)


def generate_bottoms(war_list: List[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for botton_text in war_list:
        keyboard.insert(KeyboardButton(botton_text))
    return keyboard.add(stop_bt)


if __name__ == 'main':
    pass