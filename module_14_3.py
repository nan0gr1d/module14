#  module_14_3

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup([
    [KeyboardButton(text='Купить'), KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
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
    for i in range(1, 5):
        await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
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

@dp.message_handler(text=['Информация'])
async def set_age(message):
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
