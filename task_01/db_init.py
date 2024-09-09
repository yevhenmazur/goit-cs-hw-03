import psycopg2

db_config = {
    "database": "postgres_db",
    "host": "localhost",
    "user": "postgres_user",
    "password": "postgres_password",
    "port": "5433"
}

# SQL-запити для створення таблиць
create_tables_commands = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (status_id) REFERENCES status(id)
    )
    """
]

def create_tables():
    conn = None
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Створення таблиць
        for command in create_tables_commands:
            cur.execute(command)

        # Завершення транзакції
        conn.commit()

        # Закриття курсору і підключення
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

    # if cursor:
    #     cursor.close()
    
if __name__ == '__main__':

    # Виконання функції створення таблиць
    create_tables()