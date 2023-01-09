"""Файл в готором инициализируется бот и диспетчер бота."""

import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Google import Oauth2_autentefication


load_dotenv()

ADMIN_ID = os.getenv('ADMIN_ID')
storage = MemoryStorage()


TELEGRAM_TOKEN = os.getenv('TOKEN')
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
dir = os.path.abspath(os.curdir)

# try:
#     service = Oauth2_autentefication()
# except Exception as error:
#     service = None
#     print('Токен устарел, давайте новый')
