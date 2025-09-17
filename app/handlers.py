from aiogram import Router
from aiogram.types import Message
import sys
import os
from aiogram.filters import Command
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'D://PROJECT/telegram-bot'))
from databases.methods import DatabaseHolder
router = Router()
db = DatabaseHolder()
@router.message(Command('start'))
async def stast(message: Message):
    await db.add_user(message.from_user.id,message.from_user.username)
    return message.answer("Starting...")
