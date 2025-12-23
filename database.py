from supabase import create_client, Client

class Database:
    def __init__ (self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def add_user(self, name: str, surname: str, chat_id: int, team_id: int):
        data = {
            "name": name,
            "surname": surname,
            "chat_id": chat_id,
            "group": team_id
        }

        self.supabase.table("QuizDatabase").insert(data).execute()        
        
    def read_question(self, flag: str ): 
        response = self.supabase.table("Questions") \
            .select("id, Question") \
            .eq("Flag", flag) \
            .execute()
        if response.data:
            return response.data
        return []
    
    def read_answers(self, question_id: int):
        response = self.supabase.table("QuestionAnswer") \
            .select("id, Answer, Right") \
            .eq("Question", question_id) \
            .execute()
        return response.data or []

    def read_users(self):
        response = self.supabase.table("QuizDatabase") \
            .select("chat_id") \
            .execute()
        return response.data or []

    def get_user_by_chat_id(self, chat_id: int):
        response = self.supabase.table("QuizDatabase") \
            .select("id") \
            .eq("chat_id", str(chat_id)) \
            .limit(1) \
            .execute()
            
        return response.data[0] if response.data else None