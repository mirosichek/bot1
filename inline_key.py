from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

quiz_ruoter= Router()

class QuizState(StatesGroup):
    wait_for_question=State()
    wait_for_answers=State()


def ease_link_kb(taxt):
    inline_kb_list = [
        [InlineKeyboardButton(text=taxt, url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

@quiz_ruoter.message(Command("make"))
async def start_question(message: types.Message, state: FSMContext):
    await message.answer('Введите вопрос: ')
    await state.set_state(QuizState.wait_for_question)

@quiz_ruoter.message(QuizState.wait_for_question)
async def get_question(message: types.Message, state: FSMContext):
   await state.update_data(question=message.text)
   await state.set_state(QuizState.wait_for_answers)

@quiz_ruoter.message(QuizState.wait_for_answers)
async def get_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()

    await message.answer(data["question"], reply_markup=ease_link_kb(data["answer"]))
    
    await message.answer(f"Вопрост содан")
    await state.clear()
