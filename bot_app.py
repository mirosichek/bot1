from aiogram import Bot, Dispatcher
from registrtion import registration_router
from inline_key import quiz_ruoter

class BotApp:
    def __init__(self, token, db):  # <- Этот конструктор должен быть!
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.db = db
        self.dp.include_router(registration_router)
        self.dp.include_router(quiz_ruoter)

    async def run(self):
        print("Бот запущен!")
        await self.dp.start_polling(self.bot)