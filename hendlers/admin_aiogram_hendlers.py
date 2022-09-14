"""В этом файле находятся обработчики хбщих функций бота"""

import asyncio
import os
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from hendlers.keyboards import kb_admin, kb_on_start
from hendlers.google_tools import get_free_events


load_dotenv()

ADMIN_ID = os.getenv('MODERATOR_ID')

# Тут начинается машина обновления токена доступа
class FSMСredentials(StatesGroup):
    agry = State()
    file = State()


# Первый шаг, подтверждение действия
async def mew_credentials(message: types.Message):

    await FSMСredentials.agry.set()
    await message.reply(
        'Следующее действие удалит старый ключ доступа, Вы уверенны?',
        reply_markup=kb_admin
        )


async def send_file(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await FSMСredentials.next()
        await message.reply(
            'Пришлите новый ключ доступа',
            )
    else:
        await message.reply(
            'ПОлучен ответ отличный от "Да", обновление остановленно',
            )

# 
async def update_credentials(message: types.Document, state: FSMContext):
    src = 'docs/token.json'
    if os.path.exists('docs/token.json'):
        os.remove('docs/token.json')
    await message.document.download(destination_file=src )

    await state.finish()
    await message.reply('Готово!', reply_markup=kb_on_start)


async def hendmade_folling(message: types.Message):
    while True:
        war = get_free_events()
        print(war)
        await asyncio.sleep(3)


def register_admin_hendlers(dp: Dispatcher):
    # машина состояний обновление токена доступа
    dp.register_message_handler(hendmade_folling, commands='+')
    dp.register_message_handler(mew_credentials, commands='Токен', state=None)
    dp.register_message_handler(send_file, state=FSMСredentials.agry)
    dp.register_message_handler(update_credentials, state=FSMСredentials.file, content_types=['document'])
