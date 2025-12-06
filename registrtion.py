from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import Database as db

registration_router = Router()
db = None

class RegistrationState(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()

@registration_router.message(Command("reg"))
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(RegistrationState.waiting_for_name)


@registration_router.message(RegistrationState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    await state.set_state(RegistrationState.waiting_for_surname)
    await message.answer("Отлично! Теперь введи фамилию")


@registration_router.message(RegistrationState.waiting_for_surname)
async def get_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()

    chat_id = message.chat.id

    existing_user = db.get_user_by_chat_id(chat_id)

    if existing_user:
        await message.answer("✅ Вы уже зарегистрированы")
        await state.clear()
        return

    db.add_user(
        name=data["name"],
        surname=data["surname"],
        chat_id=chat_id,
    )

    await message.answer(
        f"✅ Регистрация завершена!\n"
        f"Имя: {data['name']}\n"
        f"Фамилия: {data['surname']}"
    )

    await state.clear()
