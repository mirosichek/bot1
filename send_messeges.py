from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import Database
from quiz_service import QuizService

quiz_router = Router()
db: Database | None = None
quiz: QuizService | None = None

class sendQuestionState(StatesGroup):
    wait_fot_flag=State()

@quiz_router.message(Command("quiz"))
async def start_quiz(message: types.Message, state: FSMContext):
    await message.answer("Введите индикатор вопроса")
    await state.set_state(sendQuestionState.wait_fot_flag)

@quiz_router.message(sendQuestionState.wait_fot_flag)
async def get_questionFlag(message: types.Message, state: FSMContext):
    flag = message.text

    questions_resp = db.supabase.table("Questions") \
        .select("id, Question") \
        .eq("Flag", flag) \
        .execute()

    if not questions_resp.data:
        await message.answer("Вопросов нет")
        await state.clear()
        return

    users_resp = db.supabase.table("QuizDatabase") \
        .select("chat_id") \
        .execute()

    for user in users_resp.data:
        for question in questions_resp.data:
            answers_resp = db.supabase.table("QuestionAnswer") \
                .select("id, Answer, Right") \
                .eq("Question", question["id"]) \
                .execute()

            keyboard = quiz.build_question_keyboard(
                question["id"],
                answers_resp.data or []
            )

            await message.bot.send_message(
                chat_id=user["chat_id"],
                text=question["Question"],
                reply_markup=keyboard
            )

    await state.clear()


@quiz_router.callback_query(lambda c: c.data.startswith("quiz:"))
async def check_answer(callback: types.CallbackQuery):
    try:
        _, question_id, answer_id = callback.data.split(":")
        question_id = int(question_id)
        answer_id = int(answer_id)
        chat_id = callback.from_user.id

        await callback.answer()

        answered_resp = db.supabase.table("UserAnswers") \
            .select("id") \
            .eq("chat_id", chat_id) \
            .eq("question_id", question_id) \
            .execute()

        if answered_resp.data:
            await callback.message.answer("⚠️ Вы уже отвечали на этот вопрос")
            return

        answer_resp = db.supabase.table("QuestionAnswer") \
            .select("Right") \
            .eq("id", answer_id) \
            .execute()

        if not answer_resp.data:
            await callback.message.answer("Ответ не найден")
            return

        is_right = answer_resp.data[0]["Right"]

        db.supabase.table("UserAnswers").insert({
            "chat_id": chat_id,
            "question_id": question_id
        }).execute()

        if is_right:
            user_resp = db.supabase.table("QuizDatabase") \
                .select("score") \
                .eq("chat_id", chat_id) \
                .execute()

            current_score = user_resp.data[0]["score"] if user_resp.data else 0

            db.supabase.table("QuizDatabase") \
                .update({"score": current_score + 1}) \
                .eq("chat_id", chat_id) \
                .execute()

    except Exception as e:
        print("🔥 ERROR IN check_answer:", e)
        await callback.message.answer("❌ Внутренняя ошибка. Сообщите администратору.")

@quiz_router.message(Command("teamscore"))
async def team_score(message: types.Message):
    try:
        teams_resp = db.supabase.table("Teams") \
            .select("id, team, number_of_people") \
            .execute()

        if not teams_resp.data:
            await message.answer("Команд нет")
            return

        text = "🏆 Счет команд:\n\n"

        for team in teams_resp.data:
            users_resp = db.supabase.table("QuizDatabase") \
                .select("score") \
                .eq("group_id", team["id"]) \
                .execute()

            total_score = sum(u.get("score", 0) for u in users_resp.data)
            people_count = team.get("number_of_people") or 1

            team_score_value = round(total_score / people_count, 2)

            db.supabase.table("Teams") \
                .update({"score": team_score_value}) \
                .eq("id", team["id"]) \
                .execute()

            text += (
                f"👥 {team['team']}\n"
                f"Очки: {team_score_value}\n\n"
            )

        await message.answer(text)

    except Exception as e:
        print("TEAM SCORE ERROR:", e)
        await message.answer("❌ Ошибка подсчёта команд")