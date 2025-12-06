from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class QuizService:
    def __init__(self, db):
        self.db = db

    def get_question(self, flag: str):
        return self.db.read_question(flag)
        
    def get_answers(self, question_id: int):
        answer = self.db.read_answers(question_id)
        return answer or []

    def build_keyboard(self, question_id: int, answers: list):
        keyboard = []

        for ans in answers:
            callback = f"quiz:{question_id}:{ans['id']}"
            keyboard.append([
                InlineKeyboardButton(
                    text=ans["Answer"],
                    callback_data=callback
                )
            ])

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    

