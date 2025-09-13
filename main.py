import aiogram
import asyncio

import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token=os.environ["TOKEN_OF_BOT"])
dp = Dispatcher()

@dp.message(Command('start'))
async def stast(message: types.Message):
    return message.answer("Starting...")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
