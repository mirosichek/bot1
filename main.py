import asyncio
from bot_app import BotApp
from database import Database
import os
import registrtion
from quiz_service import QuizService
import send_messeges

TOKEN = os.environ.get("BOT_TOKEN") or "8425256609:AAGQAseZO2ZlhV04H-cSDou_hDQ8uVj7ObI"
SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://zxdprwvrgzqpxyvxksud.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp4ZHByd3ZyZ3pxcHh5dnhrc3VkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1MDI5NjQsImV4cCI6MjA3OTA3ODk2NH0.Rd8UXhHz97ifIrSezDkcBNzBn18_wAVtY_mUVCf32FE"

def main():
    db = Database(SUPABASE_URL, SUPABASE_KEY)
    quiz = QuizService()

    registrtion.db = db
    registrtion.quiz = quiz

    send_messeges.db = db
    send_messeges.quiz = quiz

    app = BotApp(TOKEN, db)
    asyncio.run(app.run())

    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Бот остановлен вручную")