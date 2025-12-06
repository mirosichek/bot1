from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

quiz_router = Router()
quiz = None

class sendQuestionState(StatesGroup):
    wait_fot_flag=State()

@quiz_router.message(Command("quiz"))
async def start_quiz(message: types.Message, state: FSMContext):
    await message.answer("Введите индикатор вопроса")
    await state.set_state(sendQuestionState.wait_fot_flag)

@quiz_router.message(sendQuestionState.wait_fot_flag)
async def get_questionFlag(message: types.Message, state: FSMContext):
    flag = message.text

    questions = quiz.get_question(flag)
    if not questions: 
        await message.answer("Вопросов нет")
        await state.clear()
        return
    
    users=quiz.get_users()
    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user["chat_id"],
                text="Новый вопрос уже доступен!"
            )
        except Exception as e:
            print(f"Не удалось отправить {user['chat_id']}: {e}")

        for question in questions:
            answers = quiz.get_answers(question["id"])
            keyboard = quiz.build_keyboard(question["id"], answers)

            await message.bot.send_message(
                chat_id=user["chat_id"],
                text=question["Question"],
                reply_markup=keyboard
)


    await state.clear()

@quiz_router.callback_query(lambda c: c.data.startswith("quiz:"))
async def check_answer(callback: types.CallbackQuery):
    _, question_id, answer_id = callback.data.split(":")

    response = quiz.db.supabase.table("QuestionAnswer") \
        .select("Right") \
        .eq("id", int(answer_id)) \
        .single() \
        .execute()

    await callback.answer()

    if response.data and response.data["Right"]:
        await callback.message.answer("✅ Правильно!")
    else:
        await callback.message.answer("❌ Неправильно")


