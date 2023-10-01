import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db_bot
from keyboards.inline.my_keyboard import y_or_n_kb

@dp.message_handler(commands=['start'])
async def get_user_info(msg: types.Message):
    await msg.reply(f"Привіт {msg.from_user.first_name}! Щоб переглянути весь список команд — /help")

@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await msg.answer('''Список команд:
/start — Запустити бота
/help — Отримати список команд
/get_user_by_id — Знайти користувача по ID
/get_user_by_name — Знайти користувача по імені
/add_me — Додати мене у список користувачів
/remove_me — Видалити мене зі списку користувачів
/update_user — Оновити дані про користувача''')

def update_user_data():

    @dp.message_handler(commands=['update_user'])
    async def update_user(msg: types.Message, state: FSMContext):
        try:
            user_id = int(msg.text.split()[1])
            user_info = db_bot.get_user_by_id(user_id)
            print(user_info)
            user_name = str(user_info).split(': ')[2][:-10]
            user_id = str(user_info).split(': ')[1][:-11]
            await msg.reply(f'Ось поточна інформація про користувача {user_name}:\n{user_info}')
            await msg.reply('Хочете оновити дані?', reply_markup=y_or_n_kb)
            async with state.proxy() as data:
                data['user_id'] = user_id
            await state.set_state('Conf')
        except (IndexError, ValueError):
            await msg.reply("Введіть команду у такому форматі:\n/get_user_by_id user_id")


    @dp.callback_query_handler(lambda call: 'yes' in call.data, state='Conf')
    async def enter_first_name(call: types.CallbackQuery, state: FSMContext):
        await call.message.answer('Добре, будь ласка введіть нове ім\'я користувача')
        await state.set_state('First_name')

    @dp.message_handler(state='First_name')
    async def first_name(msg: types.Message, state: FSMContext):
        new_first_name = msg.text
        async with state.proxy() as data:
            db_bot.update('first_name', new_first_name, data['user_id'])
        await msg.answer('Чудово! Ім\'я користувача змінено. Хочете змінити прізвище користувача?', reply_markup=y_or_n_kb)
        await state.set_state('Conf2')

    @dp.callback_query_handler(lambda call: 'yes' in call.data, state='Conf2')
    async def enter_last_name(call: types.CallbackQuery, state: FSMContext):
        await call.message.answer('Добре, будь ласка введіть нове прізвище користувача')
        await state.set_state('Last_name')

    @dp.message_handler(state='Last_name')
    async def last_name(msg: types.Message, state: FSMContext):
        new_last_name = msg.text
        async with state.proxy() as data:
            db_bot.update('last_name', new_last_name, data['user_id'])
        await msg.answer('Чудово! Прізвище користувача змінено. Хочете змінити ім\'я користувача(username)?', reply_markup=y_or_n_kb)
        await state.set_state('Conf3')

    @dp.callback_query_handler(lambda call: 'yes' in call.data, state='Conf3')
    async def enter_username(call: types.CallbackQuery, state: FSMContext):
        await call.message.answer('Добре, будь ласка введіть нове ім\'я користувача(username)')
        await state.set_state('Username')
    
    @dp.message_handler(state='Username')
    async def last_name(msg: types.Message, state: FSMContext):
        new_username = msg.text
        async with state.proxy() as data:
            db_bot.update('user_name', new_username, data['user_id'])
        await msg.answer('Чудово! Ім\'я користувача(username) змінено.')
        await msg.answer('Щоб переглянути поточну інформацію про користувача — /get_user_by_id або /get_user_by_name')
        await state.finish()
    
    @dp.callback_query_handler(lambda call: 'no' in call.data, state=['Conf','Conf2','Conf3'])
    async def finish(call, state: FSMContext):
        await call.message.answer('Добре! Завершуємо оновлення даних про користувача')
        await call.message.answer('Щоб переглянути поточну інформацію про користувача — /get_user_by_id або /get_user_by_name')
        await state.finish()
update_user_data()

@dp.message_handler(commands=['get_user_by_id'])
async def get_user_info(msg: types.Message):
    try:
        user_id = int(msg.text.split()[1])
        user_info = db_bot.get_user_by_id(user_id)
        await msg.reply(user_info)
    except (IndexError, ValueError):
        await msg.reply("Введіит команду у такому форматі:\n/get_user_by_id user_id")

@dp.message_handler(commands=['get_user_by_name'])
async def get_user_info(msg: types.Message):
    user_name = msg.get_args()
    if user_name:
        user_info = db_bot.get_user_by_name(user_name)
        await msg.reply(user_info)
    else:
        await msg.reply("Введіит команду у такому форматі:\n/get_user_by_name user_name")

@dp.message_handler(commands=['add_me'])
async def add_user(msg: types.Message):
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    user_name = msg.from_user.username

    if not db_bot.user_exists(user_id):
        db_bot.add_user_to_db(user_id, first_name, last_name, user_name)
        await msg.reply("Користувача було успішно додано")
    else:
        await msg.reply("Такий користувач вже існує")

@dp.message_handler(commands=['remove_me'])
async def remove_user(msg: types.Message):
    user_id = msg.from_user.id

    if db_bot.user_exists(user_id):
        db_bot.remove_user_from_db(user_id)
        await msg.reply("Користувача успішно видалено")
    else:
        await msg.reply("Такого користувача не існує")