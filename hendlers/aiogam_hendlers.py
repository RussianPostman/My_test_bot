"""В этом файле находятся обработчики самого бота, а так же инициализируется диспетчер."""

import os
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text

from hendlers.data_hendlers import HELLO_TEXT, HELP_TEXT, events_list_hendler, \
    get_event_month, month_convert_to_digit, get_event_day, get_event_hour, \
    event_hour_hendler, admin_notification_hendler, user_booking, print_booking
from hendlers.google_tools import update_event, cencel_booking
from hendlers.keyboards import generate_bottoms, kb_on_start, kb_empty_booking, \
    kb_booking


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

async def comand_start(message: types.Message):
    await bot.send_message(message.from_user.id, HELLO_TEXT,
                           reply_markup=kb_on_start,)


async def comand_help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP_TEXT,
                           reply_markup=kb_on_start)


async def get_event_list(message: types.Message):
    await  bot.send_message(message.from_user.id, events_list_hendler())


async def my_booking(message: types.Message):
    booking = user_booking(message.from_user.full_name)
    if len(booking) == 0:
        await bot.send_message(
            message.from_user.id,
            text='У вас нет актуальных бронирований',
            reply_markup=kb_empty_booking,
            )
    else:
        await bot.send_message(
            message.from_user.id,
            text=print_booking(booking),
            reply_markup=kb_booking,
            )

# Тут начинается машина состояний для принятия данных пользователя и
# отправки UPDATE запроса гугл календарю.

class FSMEvent(StatesGroup):
    month = State()
    day = State()
    time = State()

# Первый шаг, начало диалога бронирования урока
# @dp.message_handler(commands='Забронировать_время', state=None)
async def update_start(message: types.Message):
    await FSMEvent.month.set()
    await message.reply(
        'Выберите месяц:',
        reply_markup=generate_bottoms(get_event_month())
        )


# Выбор месяца
# @dp.message_handler(state=FSMEvent.month)
async def chose_month(message: types.Message, state: FSMContext):
    validation_list = get_event_month()
    if message.text in validation_list:
        async with state.proxy() as data:
            data['month'] = month_convert_to_digit(message.text)
        await FSMEvent.next()
        await message.reply(
            'Выберите день:',
            reply_markup=generate_bottoms(get_event_day(data.get('month')))
            )
    else:
        await message.reply(
            'Пожалуйста, используйте кнопки для выбора',
            )

# выбор дня
# @dp.message_handler(state=FSMEvent.day)
async def chose_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        validation_list = get_event_day(data.get('month'))

        if message.text in validation_list:
            # async with state.proxy() as data:
            data['day'] = message.text
            await FSMEvent.next()
            await message.reply(
                'Выберите время:',
                reply_markup=generate_bottoms(
                    get_event_hour(
                        data.get('month'),
                        data.get('day')
                        )
                    )
                )
        else:
            await message.reply(
                'Пожалуйста, используйте кнопки для выбора',
                )

# выбор времени и бронирование времени в календаре
# @dp.message_handler(state=FSMEvent.time)
async def chose_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        validation_list = get_event_hour(data.get('month'), data.get('day'))
        if message.text in validation_list:    

            data['time'] = event_hour_hendler(message.text)
            data['user'] = message.from_user.full_name
        
            update_event(data)
            await bot.send_message(ADMIN_ID, admin_notification_hendler(data))
            await state.finish()
            await message.reply('Готово!', reply_markup=kb_on_start)
        else:
            await message.reply(
                'Пожалуйста, используйте кнопки для выбора',
                )

# функция выхода из машины состояний
async def censel_hendler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok', reply_markup=kb_on_start)


async def semple_censel_hendler(message: types.Message):
    await message.reply('Ok', reply_markup=kb_on_start)

# Тут начинается машина состояний для отмены бронирования
class FSMCencel(StatesGroup):
    chose = State()


# Первый шаг, начало диалога отмены бронирования урока
async def cencel_start(message: types.Message):

    await FSMCencel.chose.set()
    await message.reply(
        'Ваши бронирования:',
        reply_markup=generate_bottoms(user_booking(message.from_user.full_name))
        )


async def chose_detatime(message: types.Message, state: FSMContext):
    validation_list = user_booking(message.from_user.full_name)
    if message.text in validation_list:
        cencel_booking(message.text, message.from_user.full_name)
        await bot.send_message(
            ADMIN_ID,
            f'Пользователь {message.from_user.full_name} отменил бронирование на {message.text}'
            )
        await state.finish()
        await message.reply('Готово!', reply_markup=kb_on_start)
    else:
            await message.reply(
                'Пожалуйста, используйте кнопки для выбора',
                )


def register_hendlers(dp: Dispatcher):
    dp.register_message_handler(get_event_list, commands=['Расписание'])
    dp.register_message_handler(comand_start, commands=['start'])
    dp.register_message_handler(comand_help, commands=['help'])
    dp.register_message_handler(my_booking, commands=['Мои_бронирования'])
    dp.register_message_handler(semple_censel_hendler, commands=['отмена', 'назад'])
    # машина состояний на бронирование
    dp.register_message_handler(censel_hendler, state='*', commands='отмена')
    dp.register_message_handler(censel_hendler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(update_start, commands='Забронировать_время', state=None)
    dp.register_message_handler(chose_month, state=FSMEvent.month)
    dp.register_message_handler(chose_day, state=FSMEvent.day)
    dp.register_message_handler(chose_time, state=FSMEvent.time)
    # машина состояний на отмену бронирования
    dp.register_message_handler(cencel_start, commands='Отменить_бронирование', state=None)
    dp.register_message_handler(chose_detatime, state=FSMCencel.chose)
    
