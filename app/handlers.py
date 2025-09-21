from aiogram import Router,F
from aiogram.types import Message,CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
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
    deleting_choose = State()
    confirmed_delete = State()
from databases.methods import DatabaseHolder
router = Router()
db = DatabaseHolder()
data_for_expenses = []
@router.message(Command('start'))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='add-expense'),KeyboardButton(text='delete-expense')]],resize_keyboard=True)
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
answer = ''
@router.message(F.text == 'delete-expense')
async def delete_expense(message:Message,state:FSMContext):
    expenses = await db.get_user_expenses(message.from_user.id)
    expenses = [str(expense[0])+' '+str(expense[1])+' '+str(expense[2])+ '\n' for expense in expenses]
    answer = 'description_of_expense date_when_you_created_it expense_number\n'
    for expense in expenses:
        answer += expense
    answer += 'all of your expenses are here. To delete choose number of your expense'
    await message.answer(answer)
    await state.set_state(States.deleting_choose)
@router.message(States.deleting_choose)
async def delete_confirm(message:Message,state:FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Yes',callback_data='confirmed_delete'),InlineKeyboardButton(text='No',callback_data='state_clear')]])
    await message.answer('are you sure you want to delete your expense? The information will be deleted permamently. Yes to confirm.',reply_markup=kb)
    expense_number = int(message.text)
    await state.update_data(expense_number=expense_number)
@router.callback_query(F.data == 'state_clear')
async def clear_state(query:CallbackQuery,state:FSMContext):
    await query.message.edit_text('cancelled delete')
    await state.clear()
@router.callback_query(F.data  == 'confirmed_delete')
async def delete_commit(query:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    await db.delete_expense(query.from_user.id,int(data.get('expense_number')))
    await query.message.edit_text('successfully deleted')
    await state.clear()