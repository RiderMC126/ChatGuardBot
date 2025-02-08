from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboards_users import index_keyboard
from config import *
from utils import create_database, create_log_folder, write_to_log
from db import accept_rules_db, add_user, get_user, increment_message_count
import asyncio
import logging
import sys
import sqlite3
import time
import datetime
import threading
import random
import string
import os
import json
import re


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher()
router = Router()
LOG_FOLDER = 'logs'
create_database()
create_log_folder('logs')



event_log = []
user_ranks = {}


class Form(StatesGroup):
    accept_rules = State()


# Команда /start
@dp.message(F.text)
async def cmd_start(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    user = get_user(user_id)  # Получаем данные пользователя из базы данных
    increment_message_count(user_id)
    # Если пользователь найден в базе данных
    if user is not None:
        # Проверяем, заблокирован ли пользователь
        if user[5] == "YES":
            await message.answer("Вы заблокированы")
            return  # Прекращаем выполнение функции

        # Проверяем, принял ли пользователь правила
        if user[4] == "NO":
            await message.answer(
                "Добро пожаловать! Для доступа к чату нажмите на кнопку ниже, чтобы принять правила.",
                reply_markup=index_keyboard()
            )
            return  # Прекращаем выполнение функции

    # Если пользователь не найден в базе данных
    if user is None:
        add_user(user_id, username)  # Добавляем пользователя в базу данных
        await message.answer(
            "Добро пожаловать! Для доступа к чату нажмите на кнопку ниже, чтобы принять правила.",
            reply_markup=index_keyboard()
        )


    if F.text.startswith == "/mute":
        # Извлекаем текст после команды /mute
        args = message.text.split(maxsplit=1)

        # Проверяем, передан ли аргумент (ник пользователя)
        if len(args) < 2:
            await message.answer("Использование: /mute <ник>")
            return

        # Извлекаем ник пользователя
        username = args[1]

        # Отправляем сообщение
        await message.answer(f"{username}, Вы получили мут!")
        logging.info(f"Администратор {message.from_user.username} выдал мут пользователю {username}.")
        write_to_log(message=f"Администратор @{message.from_user.username} выдал мут пользователю {username}.", folder=LOG_FOLDER)
    # await bot.send_message(message.chat.id, text=f'Привет!!!!!')


@dp.callback_query(F.data == "accept_rules")
async def accept_rules(call: types.CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username
    await call.answer("Подтверждено")  # Ответить пользователю
    accept_rules_db(user_id)
    await call.message.delete()
    write_to_log(message=f"Пользователь @{username} принял правила", folder=LOG_FOLDER)


# Команда /mute
@dp.message(F.text.startswith("/mute"))
async def cmd_mute(message: Message):
    await bot.send_message(message.chat.id, text=f"Йоу")



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())