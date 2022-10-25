"""В этом файле находятся обработчики хбщих функций бота"""

import asyncio
import os
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from hendlers.keyboards import kb_admin, kb_on_start
from hendlers.google_tools import get_free_events
from create_bot import bot


load_dotenv()

MODERATOR_ID = os.getenv('MODERATOR_ID')
ADMIN_ID = os.getenv('ADMIN_ID')

# Тут начинается машина обновления токена доступа
class FSMСredentials(StatesGroup):
    agry = State()
    file = State()


# Первый шаг, подтверждение действия
async def mew_credentials(message: types.Message):

    await FSMСredentials.agry.set()
    await message.reply(
        'Введите пароль',
        )


async def send_file(message: types.Message, state: FSMContext):
    if message.text == os.getenv('PASSWORD'):
        await FSMСredentials.next()
        await message.reply(
            'Пришлите новый ключ доступа',
            reply_markup=types.ReplyKeyboardRemove()
            )
    else:
        await state.finish()
        await message.reply(
            'Получен ответ отличный от "Да", обновление остановленно',
            reply_markup=kb_on_start
            )

# 
async def update_credentials(message: types.Document, state: FSMContext):
    src = 'docs/token.json'
    if os.path.exists('docs/token.json'):
        os.remove('docs/token.json')
    await message.document.download(destination_file=src)

    await state.finish()
    await message.reply('Готово!', reply_markup=kb_on_start)


async def hendmade_folling(message: types.Message):
    count = 0
    while True:
        war = get_free_events()
        # await bot.send_message(MODERATOR_ID, f'war =  {war}')

        if war != None:
            day = count // 24
            hour = count % 24
            await bot.send_message(MODERATOR_ID, f'работает {day}д и {hour}ч')
            count += 1
            await asyncio.sleep(3600)
        else:
            await bot.send_message(MODERATOR_ID, f'сломалось')
            await asyncio.sleep(3600)



def register_admin_hendlers(dp: Dispatcher):
    # машина состояний обновление токена доступа
    dp.register_message_handler(hendmade_folling, commands='+')
    dp.register_message_handler(mew_credentials, commands='token', state=None)
    dp.register_message_handler(send_file, state=FSMСredentials.agry)
    dp.register_message_handler(update_credentials, state=FSMСredentials.file, content_types=['document'])
