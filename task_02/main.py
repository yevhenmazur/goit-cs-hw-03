'''
Cкрипт, який використовує бібліотеку PyMongo для реалізації
основних CRUD (Create, Read, Update, Delete) операцій у MongoDB,
на прикладі бази даних з котами

Запустіть скрипт із опцією --help щоб зрозуміти як із ним працювати
'''
import argparse
import sys
from functools import wraps
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from populate_db import populate_db

try:
    client = MongoClient(
        "mongodb://root:mongo_pass@localhost",
        server_api=ServerApi('1'),
        serverSelectionTimeoutMS=5000
    )

    client.admin.command('ping')
    # print("Підключення до MongoDB успішне")

    db = client.book

except errors.ServerSelectionTimeoutError:
    print("Не вдалося підключитися до MongoDB: сервер недоступний.")
    sys.exit(1)

except errors.OperationFailure:
    print("Помилка авторизації: неправильні ім'я користувача або пароль.")
    sys.exit(1)

except Exception as e:
    print(f"Сталася помилка: {e}")
    sys.exit(1)


def parse_args():
    '''Describing the command line arguments'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--showall",
                        action='store_true',
                        help="Показати інформацію про всіх котів")
    parser.add_argument("-s", "--show",
                        type=str,
                        help="Показати інформацію про кота. Введіть ім'я кота")
    parser.add_argument("-u", "--updateage",
                        nargs=2,
                        metavar=("name", "age"),
                        help="Оновити вік кота. Введіть ім'я та новий вік")
    parser.add_argument("-af", "--addfeature",
                        nargs=2,
                        metavar=("name", "feature"),
                        help="Додає нову особливість кота. Введіть ім'я кота та особливість у лапках")
    parser.add_argument("-d", "--delete",
                        type=str,
                        help="Видалити кота. Введіть ім'я кота")
    parser.add_argument("-d!", "--deleteall", action='store_true',
                        help="Видалити всіх котів")
    parser.add_argument("-p", "--populate", action='store_true',
                        help="Наповнити базу зразками котів")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def check_cat_exists(func):
    ''' Декоратор для перевірки існування кота за ім'ям '''
    @wraps(func)
    def wrapper(name, *args, **kwargs):
        cat = db.cats.find_one({"name": name})
        if not cat:
            print(f"Кіт з ім'ям {name} не знайдений у базі")
            return None
        return func(name, *args, **kwargs)
    return wrapper


def show_all():
    ''' Вертає список всіх котів '''
    res = db.cats.find({})
    return res


@check_cat_exists
def show(name: str) -> list:
    ''' Знаходить кота за іменем '''
    res = []
    cat = db.cats.find_one({"name": name})
    res.append(cat)
    return res


@check_cat_exists
def update_age(name: str, new_age: int) -> str:
    ''' Оновлює вік кота за його ім'ям '''
    cat = db.cats.find_one({"name": name})
    old_age = cat.get('age')
    db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    msg = f"Вік кота {name} змінено із {old_age} на {new_age}"
    return msg


@check_cat_exists
def add_feature(name: str, feature: str) -> str:
    ''' Додає нову фічу кота у поле features '''
    cat = db.cats.find_one({"name": name})
    features = cat.get('features')
    features.append(feature)
    db.cats.update_one({"name": name}, {"$set": {"features": features}})
    msg = f"Для кота {name} додано особливість {feature}"
    return msg


@check_cat_exists
def delete_cat(name: str) -> str:
    ''' Видаляє кота за іменем '''
    db.cats.delete_one({"name": name})
    msg = f"Кота на ім'я {name} видалено з бази"
    return msg


def delete_all_cats() -> str:
    ''' Видаляє всіх котів з бази '''
    result = db.cats.delete_many({})
    msg = f"Видалено {result.deleted_count} котів"
    return msg


def print_table(cats: list):
    ''' Формує і виводить список котів у вигляді таблиці з заголовками. '''
    if not cats:
        # print("Котів, що задовільняють параметрам пошуку, не знайдено.")
        return None
    else:
        headers = ["Name", "Age", "Features"]
        print(f"{headers[0]:<15} | {headers[1]:<5} | {headers[2]}")
        print("-" * 70)  # Лінія для розділення заголовків і даних

        for cat in cats:
            name = cat.get('name', 'N/A')
            age = cat.get('age', 'N/A')
            features = ", ".join(cat.get('features', []))
            print(f"{name:<15} | {age:<5} | {features}")


def main():
    ''' Викликає всі інші функції, в залежності від аргументів командного рядка '''

    args = parse_args()

    if args.showall:
        print_table(show_all())
    if args.show:
        res = show(args.show)
        print_table(res)
    if args.updateage:
        name, age = args.updateage
        res = update_age(name, age)
        print(res)
    if args.addfeature:
        name, feature = args.addfeature
        res = add_feature(name, feature)
        print(res)
    if args.delete:
        res = delete_cat(args.delete)
        if res:
            print(res)
    if args.deleteall:
        res = delete_all_cats()
        print(res)
    if args.populate:
        populate_db()
        # print("База наповнена зразками котів")


if __name__ == "__main__":
    main()
