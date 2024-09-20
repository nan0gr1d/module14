#  module_14_5

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions_145 as crud_functions

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


api = "6517651701:AAGRaBGr6aE29JvN345e7QX7Ept2_oXupZo"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup([
    [KeyboardButton(text='Купить'),KeyboardButton(text='Регистрация'), KeyboardButton(text='Рассчитать'),
     KeyboardButton(text='Информация')]
], resize_keyboard=True)
kbin = InlineKeyboardMarkup(3, [
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
     InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ], resize_keyboard=True)
kb_buy = InlineKeyboardMarkup(3, [
    [
        InlineKeyboardButton(text='Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')
     ]
], resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Привет, {message.from_user.username} !\nЯ бот, помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kbin)

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer("""Упрощенный вариант формулы Миффлина-Сан Жеора:
 - для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
 - для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
                            """)
    await call.answer()

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    products = crud_functions.get_all_products()
    i = 0
    for product in products:
        i += 1
        id, title, descr, price = product
        await message.answer(f"Название: {title} | Описание: {descr} | Цена: {price}")
        try:
            with open(f"files/img{i}.png", "rb") as img:
                await message.answer_photo(img)
        except:
            pass
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_buy)

@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

"""
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.

Файлы module_14_5.py, crud_functions.py, а также файл с базой данных и таблицей Users 
"""

@dp.message_handler(text=['Информация'])
async def info(message):
    await message.answer('Информация о настоящем Телеграм-боте.\nДля начала работы введите /start')

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age'])
    await message.answer(f"Рекомендуемая норма калорий:\n - для мужчин: {calories + 5}\n - для женщин: {calories -161}")
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    await message.answer(f'Привет {message.from_user.username} !\nВведите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
