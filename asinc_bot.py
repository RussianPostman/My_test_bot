"""Главный файл проекта. Через него запускается бот."""

from aiogram.utils import executor

from create_bot import dp
from hendlers import aiogam_hendlers


async def on_startup(_):
    print('Бот вышел в онлайн.')

aiogam_hendlers.register_hendlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
