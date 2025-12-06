from supabase import create_client, Client

class Database:
    def __init__ (self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def add_user(self, name: str, surname: str, chat_id):
        try:
            data = {"name": name, "surname": surname, "chat_id": chat_id}  
            response = self.supabase.table("QuizDatabase").insert(data).execute()
            
            if response.data:
                print("Данные успешно добавлены:", response.data)
                return True
            else:
                print("Не удалось добавить данные")
                return False
                
        except Exception as e:
            print("Неизвестная ошибка:", e)
            return False
        
    def read_question(self, flag: str ): 
        response = self.supabase.table("Questions") \
            .select("id, Question") \
            .eq("Flag", "универ") \
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

