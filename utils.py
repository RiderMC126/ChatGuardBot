import sqlite3
import datetime
from datetime import datetime
from db import create_table_users
import os


def create_database():
    try:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users"')
        if cursor.fetchone() is None:
            create_table_users()
            print("База данных создана")
        else:
            print("База данных уже существует")
    except sqlite3.Error as e:
        print(f"Ошибка создания базы данных: {e}")


def create_log_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f'Папка "LOG_FOLDER" создана')
    else:
        print(f'Папка "LOG_FOLDER" уже существует')


def write_to_log(message, folder):
    # Генерируем имя файла с текущей датой
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"log.{current_date}.txt"

    # Путь к файлу
    filepath = os.path.join(folder, filename)

    # Записываем сообщение в файл
    with open(filepath, 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")