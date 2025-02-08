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
from db import accept_rules_db, add_user, get_user, increment_message_count, muted_users, unmuted_users, banned_users, unbanned_users, warnned_users, unwarnned_users, new_visitor, new_member, new_communicator, new_discussionleader, new_chatstar
from datetime import datetime
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
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /mute @username")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, Вы получили мут!")
    muted_users(username)
    logging.info(f"Администратор @{message.from_user.username} выдал мут пользователю @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} выдал мут пользователю @{username}.", folder=LOG_FOLDER)


# Обрабатываем команду /unmute // Размутить
@dp.message(F.text.startswith("/unmute"))
async def cmd_unmute(message: Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
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
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
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
async def cmd_unban(message: Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
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
async def cmd_warn(message: Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
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
async def cmd_unwarn(message: Message):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Вы не имеете права использовать эту команду.")
        return
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Использование: /unwarn ник")
        return

    username = args[1].lstrip('@')

    await message.answer(f"{username}, с вас сняли варн")
    unwarnned_users(username)
    logging.info(f"Администратор @{message.from_user.username} снял варн с пользователя @{username}.")
    write_to_log(message=f"Администратор @{message.from_user.username} снял варн с пользователя @{username}.", folder=LOG_FOLDER)


@dp.message(Command("me"))
async def cmd_me(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    user = get_user(user_id)
    # Преобразуем дату вступления в datetime объект
    join_date = datetime.strptime(user[3], "%Y-%m-%d")
    # Вычисляем текущую дату
    today = datetime.today()
    # Вычисляем разницу в днях
    days_since_join = (today - join_date).days
    if days_since_join == 0:
        days_since_join = 1
    # Склоняем слово "день"
    if days_since_join % 10 == 1 and days_since_join % 100 != 11:
        day_form = "день"
    elif 2 <= days_since_join % 10 <= 4 and (days_since_join % 100 < 10 or days_since_join % 100 >= 20):
        day_form = "дня"
    else:
        day_form = "дней"
    await bot.send_message(message.chat.id, text=f"@{username}, вот информация о Вас:\n\nС нами уже: {days_since_join} {day_form}\nСообщений написано: {user[5]}\nРанг: {user[4]}\nВарнов: {user[9]}")

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
        if user[7] == "YES" or user[9] == 3:
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
        if user[5] == 49:
            await message.answer(f'{username}, поздравляем Вас, вы достигли ранга: "Посетитель"!')
            new_visitor(user_id)
        if user[5] == 199:
            await message.answer(f'{username}, поздравляем Вас, вы достигли ранга: "Участник"!')
            new_member(user_id)
        if user[5] == 499:
            await message.answer(f'{username}, поздравляем Вас, вы достигли ранга: "Коммуникатор"!')
            new_communicator(user_id)
        if user[5] == 999:
            await message.answer(f'{username}, поздравляем Вас, вы достигли ранга: "Лидер Обсуждений"!')
            new_discussionleader(user_id)
        if user[5] == 1999:
            await message.answer(f'{username}, поздравляем Вас, вы достигли ранга: "Звезда Чата"!')
            new_chatstar(user_id)
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