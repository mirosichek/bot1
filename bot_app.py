from aiogram import Bot, Dispatcher
from registrtion import registration_router
from send_messeges import quiz_router

class BotApp:
    def __init__(self, token, db):  
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.db = db
        self.dp.include_router(registration_router)
        self.dp.include_router(quiz_router)

    async def run(self):
        print("Бот запущен!")
        await self.dp.start_polling(self.bot)