from supabase import create_client, Client

class Database:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def add_user(self, name: str, surname: str):
        try:
            data = {"name": name, "surname": surname}  
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