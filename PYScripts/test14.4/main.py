import aiogram
import crud_func
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

global products
products = crud_func.get_all_prods()

class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()

api = ""
bot = Bot(token = api)
disp = Dispatcher(bot,storage=MemoryStorage())

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(KeyboardButton(text = "Информация"),KeyboardButton(text = "Рассчитать"))
keyboard.row(KeyboardButton(text = "Регистрация"),KeyboardButton(text = "Купить"))

sellkb = InlineKeyboardMarkup(resize_keyboard=True)
sellkb.row(InlineKeyboardButton(text="Продукт 1",callback_data='product_buying'),
           InlineKeyboardButton(text="Продукт 2",callback_data='product_buying'),
           InlineKeyboardButton(text="Продукт 3",callback_data='product_buying'),
           InlineKeyboardButton(text="Продукт 4",callback_data='product_buying'))

ikeyboard = InlineKeyboardMarkup(resize_keyboard=True)
ikeyboard.row(InlineKeyboardButton(text="Формулы расчетов",callback_data='formulas'),
             InlineKeyboardButton(text="Рассчитать норму калорий",callback_data='calories'))
@disp.message_handler(text = 'Рассчитать')
async def main_menu(msg):
    await msg.answer("Выберите опцию",reply_markup=ikeyboard)

@disp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    await call.message.answer("Формула вычисления: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

@disp.message_handler(text = "Купить")
async def get_buying_list(msg):
    for prod in products:
        with open(f"pics/{prod[0]}.jpg","rb") as pic:
            await msg.answer_photo(pic,f"{prod[1]} | Описание: {prod[2]} | Цена : {prod[3]}")
    await msg.answer("Выберите продукт для покупки:",reply_markup=sellkb)

@disp.callback_query_handler(text="product_buying")
async def send_confirm_msg(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@disp.message_handler(commands=['start'])
async def start(msg):
    await msg.answer('Привет! Я бот помогающий твоему здоровью.',reply_markup=keyboard )

@disp.message_handler(text = "Информация")
async def info(msg):
    await msg.answer("Этот бот используется для вычисления калорий. \n Нажмите или напишите \"Рассчитать\" для начала вычислений", reply_markup=keyboard )

@disp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите возраст",reply_markup=None)
    await call.answer()
    await UserState.age.set()

@disp.message_handler(state=UserState.age)
async def set_height(msg,state):
    await state.update_data(age = msg.text)
    await msg.answer('Введите рост')
    await UserState.height.set()

@disp.message_handler(state=UserState.height)
async def set_weight(msg,state):
    await state.update_data(height = msg.text)
    await msg.answer('Введите массу')
    await  UserState.weight.set()

@disp.message_handler(state=UserState.weight)
async def get_calories(msg,state):
    await state.update_data(weight = msg.text)
    data = await state.get_data()
    result =10 * float(data['weight']) + 6.25 * float(data['height']) - 5 * float(data['age']) + 5
    await msg.answer(f"Норма калорий: {result}")
    await state.finish()

@disp.message_handler()
async def all_messages(msg):
    if msg['text'].lower() == 'lorem':
        await msg.answer("ipsum")
        return 0
    await msg.answer("Введите команду /start, чтобы начать общение")

if __name__ == "__main__":
    executor.start_polling(disp,skip_updates=True)