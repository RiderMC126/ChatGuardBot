import sqlite3
import datetime


conn = sqlite3.connect("db.db")
cur = conn.cursor()


# Создание "users"
def create_table_users():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            date DATE NOT NULL DEFAULT CURRENT_DATE,
            rank TEXT NOT NULL DEFAULT 'Новичок',
            message_count INTEGER NOT NULL DEFAULT 0,
            verification TEXT NOT NULL DEFAULT 'NO',
            blocked TEXT NOT NULL DEFAULT 'NO',
            muted TEXT NOT NULL DEFAULT 'NO',
            warns INTEGER NOT NULL DEFAULT 0
        );
    ''')


def accept_rules_db(user_id):
    try:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET verification = "YES" WHERE user_id = ? """, (user_id,))
        if cursor.rowcount == 0:
            # Если пользователь не найден, можно добавить его или вывести ошибку
            print(f"Пользователь {user_id} не найден в базе данных.")
        conn.commit()
        conn.close()  # Закрытие соединения
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении базы данных: {e}")


# Добавление пользователя в базу данных
def add_user(user_id, username):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()


# Получение информации о пользователе
def get_user(user_id):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Функция обновления счётчика сообщений
def increment_message_count(user_id):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET message_count = message_count + 1 WHERE user_id = ?', (user_id,))
    conn.commit()


def muted_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET muted = "YES" WHERE username = ?""", (username,))
    conn.commit()

def unmuted_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET muted = "NO" WHERE username = ?""", (username,))
    conn.commit()

def banned_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET blocked = "YES" WHERE username = ?""", (username,))
    conn.commit()

def unbanned_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET blocked = "NO" WHERE username = ?""", (username,))
    conn.commit()

def warnned_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET warns = warns + 1 WHERE username = ?""", (username,))
    conn.commit()

def unwarnned_users(username):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET warns = warns - 1 WHERE username = ?""", (username,))
    conn.commit()