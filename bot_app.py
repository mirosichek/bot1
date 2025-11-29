import asyncio
from aiogram import Bot, Dispatcher
from registrtion import registration_router
from inline_key import quiz_ruoter

class BotApp:
    def _init_(self, token, db):
        self.bot = Bot(token)
        self.db = db
        self.dp = Dispatcher()
        self.dp.include_router(registration_router)
        self.dp.include_router(quiz_ruoter)

    async def run(self):
        print("Бот запущен!")
        await self.dp.start_polling(self.bot)