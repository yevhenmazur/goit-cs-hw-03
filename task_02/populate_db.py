'''
Скрипт додає до бази даних тестові дані про котів
'''
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

def populate_db():
    try:
        client = MongoClient(
            "mongodb://root:mongo_pass@localhost",
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000
        )
        # Перевірка підключення
        client.admin.command('ping')
        print("Підключення до MongoDB успішне")

        db = client.book

        cats = [
            {
                "name": "Farzoy",
                "age": 3,
                "features": ["грає з іграшками", "не любить дітей", "чорний"]
            },
            {
                "name": "Rapunzel",
                "age": 1,
                "features": ["ходить в лоток", "спокійна характер", "руда"]
            },
            {
                "name": "Matroskin",
                "age": 5,
                "features": ["не дає себе гладити", "любить бігати", "рудий"]
            },
            {
                "name": "Bella",
                "age": 2,
                "features": ["активний", "завжди голодний", "сіро-білий"]
            },
            {
                "name": "Charlie",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "коричневий"]
            },
            {
                "name": "Anfisa",
                "age": 3,
                "features": ["спокійна", "любить дітей", "чорний з білими плямами"]
            },
            {
                "name": "Leo",
                "age": 6,
                "features": ["любить ловити мишей", "не дає себе гладити", "тигровий"]
            },
            {
                "name": "Daisy",
                "age": 1,
                "features": ["дуже активна", "любитись гратись", "помаранчевий"]
            },
            {
                "name": "Vasian",
                "age": 5,
                "features": ["любить бути на руках", "спокійний", "білий з сірими плямами"]
            },
            {
                "name": "Max",
                "age": 2,
                "features": ["полюбляє їсти рибу", "грайливий", "чорний з білими лапками"]
            }
        ]

        db.cats.insert_many(cats)
        print("Дані успішно додано до бази")

    except errors.ServerSelectionTimeoutError:
        print("Не вдалося підключитися до MongoDB: сервер недоступний.")
    
    except errors.OperationFailure:
        print("Помилка авторизації: неправильні ім'я користувача або пароль.")
    
    except Exception as e:
        print(f"Сталася помилка: {e}")

if __name__ == "__main__":
    populate_db()