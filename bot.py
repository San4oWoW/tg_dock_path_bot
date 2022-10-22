import datetime
import logging
import sqlite3
from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import database as d
import blocks as b
import find as f
import config as c
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher.filters import Text

storage = MemoryStorage()

API_TOKEN = c.API_TOKEN
dirs_txt = c.DIRS_TXT


class FSM(StatesGroup):
    name = State()
    key = State()


class FSM1(StatesGroup):
    admin_request = State()


class FSM2(StatesGroup):
    admin_request_del = State()


class FSM3(StatesGroup):
    find1 = State()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if d.check_id_base(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup()
        for i in d.start_buttons_dict(dirs_txt).keys():
            keyboard.add(types.KeyboardButton(text=f"{i}"))
        await message.answer(f"Приветствую, {d.get_name(message.from_user.id)}! Выберете директорию.", reply_markup=keyboard)
    else:
        await message.bot.send_message(message.from_user.id, f"Ошибка авторизации, пожалуйста, зарегистрируйтесь /reg")


@dp.message_handler(commands="find")
async def find(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Введите ключевые слова для поиска: ")
    await FSM3.find1.set()


@dp.message_handler(state=FSM3.find1)
async def find(message: types.Message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, "Выполняется поиск...🔎")
    mas = d.read_file_in_mas(dirs_txt)
    async with state.proxy() as data:
        data['find1'] = message.text
        if len(f.find_dirs(mas, data['find1'])) > 0:
            for i in f.find_dirs(mas, data['find1']):
                try:
                    await message.bot.send_document(chat_id=message.from_user.id,  document=open(i, 'rb'))
                except:
                    await message.bot.send_message(message.from_user.id, "Файл слишком большой")
        else:
            await message.bot.send_message(message.from_user.id, "Поиск не дал результатов")
    await message.bot.send_message(message.from_user.id, "Поиск окончен")
    await state.finish()


@dp.message_handler(commands="admin_clear")
async def admin(message: types.Message):
    if message.from_user.id == 807761312 or 744224442:
        b.clear_users_from_base()
        await message.bot.send_message(message.from_user.id, "Успешно!")


@dp.message_handler(commands="admin_del")
async def admin(message: types.Message):
    if message.from_user.id == 807761312 or 744224442:
        await message.bot.send_message(message.from_user.id, "Введите имя клиента для удаления из базы: ")
        await FSM2.admin_request_del.set()


@dp.message_handler(state=FSM2.admin_request_del)
async def registration_next(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['admin_request_del'] = message.text
        db = sqlite3.connect('clients.db')
        sql = db.cursor()
        sql.execute(f"DELETE FROM clients WHERE name = '{data['admin_request_del']}'")
        db.commit()
        await message.bot.send_message(message.from_user.id, "Клиент удален")
    await state.finish()


@dp.message_handler(commands="admin_add")
async def admin(message: types.Message):
    if message.from_user.id == 807761312 or 744224442:
        await message.bot.send_message(message.from_user.id, "Введите имя клиента для получения доступа: ")
        await FSM1.admin_request.set()


@dp.message_handler(state=FSM1.admin_request)
async def registration_next(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['admin_request'] = message.text
        db = sqlite3.connect('clients.db')
        sql = db.cursor()
        sql.execute(f"INSERT INTO clients VALUES (?,?,?)", (f"{data['admin_request']}", '0', '0'))
        db.commit()
        await message.bot.send_message(message.from_user.id, "Клиент добавлен")
    await state.finish()


@dp.message_handler(commands="reg", state=None)
async def registration(message: types.Message):
    if b.check_user_in_block_base(message.from_user.id) == False or b.check_user_in_block_base(message.from_user.id) == None:
        await message.bot.send_message(message.from_user.id, "Введите данные для регистрации в формате: Фамилия Имя. По запросам/багам/предложениям просьба писать в группу https://t.me/Meridian_Help_Bot")
        await FSM.name.set()
    else:
        await message.bot.send_message(message.from_user.id, "Вы были заблокированы, обратитесь в чат поддержки! https://t.me/Meridian_Help_Bot")


@dp.message_handler(state=FSM.name)
async def registration_next(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        reg = d.registration(data['name'], message.from_user.id)
        if reg == "Ошибка регистрации":
            b.add_user_to_block_base(message.from_user.id)
            b.set_count(message.from_user.id)
            await message.bot.send_message(message.from_user.id, "Ошибка регистрации")
        else:
            await message.bot.send_message(message.from_user.id, "Успешно. Введите /start для начала")
    await state.finish()


@dp.message_handler(commands="myid")
async def get_id(message: types.Message):
    await message.bot.send_message(message.from_user.id, f"Ваш уникальный telegram id: {message.from_user.id}")


@dp.message_handler(Text(equals="🔙Назад"))
async def text_example(message: types.Message):
    if d.check_id_base(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup()
        if d.get_dir_from_db("'" + str(message.from_user.id) + "'") in d.start_buttons_dict(dirs_txt).values():
            for i in d.start_buttons_dict(dirs_txt).keys():
                keyboard.add(i)
            await message.answer(d.get_dir_from_db(message.from_user.id), reply_markup=keyboard)
        else:
            d.set_dir_in_db("'" + str(message.from_user.id) + "'",
                                         d.get_back_dir("'" + str(message.from_user.id) + "'"))
            keyboard.add("🔙Назад")
            for i in d.get_list_dir_from_db("'" + str(message.from_user.id) + "'"):
                keyboard.add(i)
            keyboard.add("🔙Назад")

            await message.answer(d.get_dir_from_db(message.from_user.id), reply_markup=keyboard)
    else:
        await message.bot.send_message(message.from_user.id, f"Ошибка автозации, пожалуйста, зарегистрируйтесь /reg")


@dp.message_handler()
async def main(message: types.Message):
    if d.check_id_base(message.from_user.id):
        try:
            keyboard = types.ReplyKeyboardMarkup()
            if message.text in d.start_buttons_dict(dirs_txt).keys():
                d.set_dir_in_db("'" + str(message.from_user.id) + "'", d.start_buttons_dict(dirs_txt)[message.text])
                keyboard.add("🔙Назад")
                for i in d.get_list_dir_from_db("'" + str(message.from_user.id) + "'"):
                    keyboard.add(i)
                keyboard.add("🔙Назад")

                await message.answer(d.get_dir_from_db(message.from_user.id), reply_markup=keyboard)
            else:
                try:
                    d.set_dir_in_db("'" + str(message.from_user.id) + "'", d.get_dir_from_db("'" + str(message.from_user.id) + "'") + "\\" + message.text)
                    await message.bot.send_document(chat_id=message.from_user.id,
                                                    document=open(d.get_dir_from_db("'" + str(message.from_user.id) + "'"),
                                                                  'rb'))
                    d.set_dir_in_db("'" + str(message.from_user.id) + "'", d.get_back_dir("'" + str(message.from_user.id) + "'"))
                    with open("log.log", 'a') as file:
                        file.write(f"{datetime.datetime.now()} downloading file: {message.text} id: {message.from_user.id} {d.get_name(message.from_user.id)}\n")
                        file.close()
                except:
                    keyboard.add("🔙Назад")
                    for i in d.get_list_dir_from_db("'" + str(message.from_user.id) + "'"):
                        keyboard.add(types.KeyboardButton(text=f"{i}"))
                    keyboard.add("🔙Назад")

                    await message.answer(d.get_dir_from_db(message.from_user.id), reply_markup=keyboard)
        except:
            d.set_dir_in_db("'" + str(message.from_user.id) + "'",
                            d.get_back_dir("'" + str(message.from_user.id) + "'"))
            await message.answer("Ошибка запроса. Файл содержит недопустимый размер или не существует. По вопросам/багам/предложениям просьба писать в группу https://t.me/Meridian_Help_Bot")
    else:
        await message.bot.send_message(message.from_user.id, f"Ошибка автозации, пожалуйста, зарегистрируйтесь /reg")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
