import aiogram
import asyncio
import os

from app.handlers import router

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv()

bot = Bot(token=os.environ['TOKEN_OF_BOT'])
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
