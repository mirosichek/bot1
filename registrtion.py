from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import Database
from quiz_service import QuizService

registration_router = Router()
db: Database | None = None
quiz: QuizService | None = None


class RegistrationState(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_command = State()


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
    chat_id = message.chat.id

    user_resp = db.supabase.table("QuizDatabase") \
        .select("id") \
        .eq("chat_id", chat_id) \
        .limit(1) \
        .execute()

    if user_resp.data:
        await message.answer("✅ Вы уже зарегистрированы")
        await state.clear()
        return

    teams_resp = db.supabase.table("Teams") \
        .select("id, team") \
        .execute()

    keyboard = quiz.build_team_keyboard(teams_resp.data or [])
    await state.set_state(RegistrationState.waiting_for_command)
    await message.answer("Выберите команду:", reply_markup=keyboard)

@registration_router.callback_query(
    RegistrationState.waiting_for_command,
    lambda c: c.data.startswith("team:")
)
async def choose_team(callback: types.CallbackQuery, state: FSMContext):
    team_id = int(callback.data.split(":")[1])
    data = await state.get_data()
    chat_id = callback.message.chat.id

    db.supabase.table("QuizDatabase").insert({
        "name": data["name"],
        "surname": data["surname"],
        "chat_id": chat_id,
        "group_id": team_id,
        "score": 0
    }).execute()

    await callback.message.answer("✅ Регистрация завершена!")
    await callback.answer()
    await state.clear()

