from aiogram import Router,F
from aiogram.types import Message
import aiogram.types as types
import sys
from datetime import date
import os
from aiogram.filters import Command
from aiogram.filters.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
# if imports from your dirs doesnt work use this(change my way for project directory to yours)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'D://PROJECT/telegram-bot'))
class States(StatesGroup):
    adding_amount = State()
    adding_currency = State()
    adding_description = State()
from databases.methods import DatabaseHolder
router = Router()
db = DatabaseHolder()
data_for_expenses = []
@router.message(Command('start'))
async def start(message: Message):
    kb = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='add-expense'),types.KeyboardButton(text='delete-expense')]],resize_keyboard=True)
    await db.add_user(message.from_user.id,message.from_user.username)
    return message.answer("Welcome to the tracker of expenses! You can add,delete your expenses and soon will be more functions!\nHope you enjoy it!",reply_markup=kb)
@router.message(F.text == 'add-expense')
async def add_expense_1(message:Message,state:FSMContext):
    await message.answer('Leave amount of your expense,then currency, and finally describe your expense')
    await state.set_state(States.adding_amount)
@router.message(States.adding_amount)
async def add_expense_2(message:Message,state:FSMContext):
    data_for_expenses.append(message.text)
    await state.set_state(States.adding_currency)
@router.message(States.adding_currency)
async def add_expense_3(message:Message,state:FSMContext): 
    data_for_expenses.append(message.text)
    await state.set_state(States.adding_description)
@router.message(States.adding_description)
async def add_expense_4(message:Message,state:FSMContext): 
    data_for_expenses.append(message.text)
    await db.add_expense(int(data_for_expenses[0]),message.from_user.id,data_for_expenses[1],date.today(),data_for_expenses[2])
    data_for_expenses.clear()
    await state.clear()
