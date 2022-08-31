from email import message
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from google_logic import (Oauth2_autentefication, get_api_reqest)
from bot_logic import HELLO_TEXT, HELP_TEXT, reqest_data_hendler

load_dotenv()


async def on_startup(_):
    print('Бот вышел в онлайн.')

TELEGRAM_TOKEN = os.getenv('TOKEN')
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def comand_start(message: types.Message):
    await bot.send_message(message.from_user.id, HELLO_TEXT)


@dp.message_handler()
async def message_answer(message: types.Message):
    if message.text == 'Привет':
        await bot.send_message(message.from_user.id, 'И тебе привет!')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
