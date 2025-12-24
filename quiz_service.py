from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class QuizService:
    def build_question_keyboard(self, question_id: int, answers: list):
        keyboard = []

        for ans in answers:
            keyboard.append([
                InlineKeyboardButton(
                    text=ans["Answer"],
                    callback_data=f"quiz:{question_id}:{ans['id']}"
                )
            ])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def build_team_keyboard(self, teams: list):
        keyboard = []

        for team in teams:
            keyboard.append([
                InlineKeyboardButton(
                    text=team["team"],
                    callback_data=f"team:{team['id']}"
                )
            ])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
