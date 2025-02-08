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
from db import accept_rules_db, add_user, get_user, increment_message_count, muted_users, unmuted_users, banned_users, unbanned_users, warnned_users, unwarnned_users
import asyncio
import logging
import sys


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


# Обрабатываем команду /mute // Замутить
@dp.message(F.text.startswith("/mute"))
async def cmd_mute(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /mute ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, Вы получили мут!")
    muted_users(username)
    logging.info(f"Администратор @{message.from_user.username} выдал мут пользователю @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} выдал мут пользователю @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /unmute // Размутить
@dp.message(F.text.startswith("/unmute"))
async def cmd_mute(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /unmute ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, с Вас сняли мут.")
    unmuted_users(username)
    logging.info(f"Администратор @{message.from_user.username} снял мут пользователю @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} снял мут пользователю @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /ban // Забанить
@dp.message(F.text.startswith("/ban"))
async def cmd_ban(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /ban ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, Вы забанены!")
    banned_users(username)
    logging.info(f"Администратор @{message.from_user.username} забанил пользователя @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} забанил пользователя @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /unban // Разбанить
@dp.message(F.text.startswith("/unban"))
async def cmd_ban(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /unban ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, Вы разбанены.")
    unbanned_users(username)
    logging.info(f"Администратор @{message.from_user.username} разбанил пользователя @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} разбанил пользователя @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /warn // Выдать варн
@dp.message(F.text.startswith("/warn"))
async def cmd_ban(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /warn ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, Вам дали варн!")
    warnned_users(username)
    logging.info(f"Администратор @{message.from_user.username} выдал варн пользователю @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} выдал варн пользователю @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /unwarn // Снять варн
@dp.message(F.text.startswith("/unwarn"))
async def cmd_ban(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /unwarn ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, с вас сняли варн")
    unwarnned_users(username)
    logging.info(f"Администратор @{message.from_user.username} снял варн с пользователя @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} снял варн с пользователя @{username}.", folder=LOG_FOLDER)


# Обрабатываем все сообщения пользователей
@dp.message(F.text)
async def cmd_start(message: types.Message):
    username = message.from_user.username
    user_id = message.from_user.id
    user = get_user(user_id)  # Получаем данные пользователя из базы данных
    increment_message_count(user_id)
    # Если пользователь найден в базе данных
    if user is not None:
        # Проверяем, заблокирован ли пользователь
        if user[7] == "YES":
            await message.delete()
            await message.answer(f"@{username}, Вы заблокированы!")
            return  # Прекращаем выполнение функции
        if user[8] == "YES":
            await message.delete()
            await message.answer(f"@{username}, У вас мут!")
            return  # Прекращаем выполнение функции
        # Проверяем, принял ли пользователь правила
        if user[6] == "NO":
            await message.delete()
            await message.answer(
                "Добро пожаловать! Для доступа к чату нажмите на кнопку ниже, чтобы принять правила.",
                reply_markup=index_keyboard()
            )
            return  # Прекращаем выполнение функции
    # Если пользователь не найден в базе данных
    if user is None:
        add_user(user_id, username)  # Добавляем пользователя в базу данных
        await message.delete()
        await message.answer(
            "Добро пожаловать! Для доступа к чату нажмите на кнопку ниже, чтобы принять правила.",
            reply_markup=index_keyboard()
        )


# Обрабатываем принятие правил
@dp.callback_query(F.data == "accept_rules")
async def accept_rules(call: types.CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username
    await call.answer("Подтверждено")  # Ответить пользователю
    accept_rules_db(user_id)
    await call.message.delete()
    write_to_log(message=f"Пользователь @{username} принял правила", folder=LOG_FOLDER)




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())