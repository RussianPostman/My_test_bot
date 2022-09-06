"""Файл в готором инициализируется бот и диспетчер бота."""

import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()
storage = MemoryStorage()

TELEGRAM_TOKEN = os.getenv('TOKEN')
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)