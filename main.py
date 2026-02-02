import os
import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- 1. ВЕБ-СЕРВЕР ДЛЯ RENDER (PORT FIX) ---
app = Flask('')

@app.route('/')
def home():
    return "FPStore Bot is Online"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- 2. НАСТРОЙКИ БОТА ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Survey(StatesGroup):
    q1_time = State()
    q2_name = State()
    q3_phone = State()
    q4_budget = State()
    q5_service = State()
    q6_tasks = State()
    q7_color = State()
    q8_light = State()
    q9_platform = State()
    q10_gpu = State()
    q11_os = State()
    q12_city = State()
    q13_delivery = State()
    q14_address = State()

def make_kb(items: list):
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.button(text=item)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# --- 3. ОБРАБОТЧИКИ ОПРОСА ---

@dp.message(Command("start"))
async def start_survey(message: types.Message, state: FSMContext):
    policy_url = "https://vk.ru/@fpstore23-politika-konfidencialnosti-fpstore"
    text = (
        "🚀 <b>Заявка на сборку ПК в FPStore</b>\n\n"
        f"Нажимая кнопку «ДА», вы соглашаетесь с <a href='{policy_url}'>политикой конфиденциальности</a>.\n\n"
        "<b>Вопрос 1:</b> Планируете ли Вы сборку ПК в ближайшее время?"
    )
    await message.answer(text, reply_markup=make_kb(["ДА", "НЕТ"]), parse_mode="HTML")
    await state.set_state(Survey.q1_time)

@dp.message(Survey.q1_time)
async def p1(m: types.Message, state: FSMContext):
    await state.update_data(q1=m.text)
    await m.answer("<b>Вопрос 2:</b> Как к Вам обращаться?")
    await state.set_state(Survey.q2_name)

@dp.message(Survey.q2_name)
async def p2(m: types.Message, state: FSMContext):
    await state.update_data(q2=m.text)
    await m.answer("<b>Вопрос 3:</b> Ваш номер телефона?")
    await state.set_state(Survey.q3_phone)

@dp.message(Survey.q3_phone)
async def p3(m: types.Message, state: FSMContext):
    await state.update_data(q3=m.text)
    await m.answer("<b>Вопрос 4:</b> Ваш бюджет на сборку?")
    await state.set_state(Survey.q4_budget)

@dp.message(Survey.q4_budget)
async def p4(m: types.Message, state: FSMContext):
    await state.update_data(q4=m.text)
    await m.answer("<b>Вопрос 5:</b>
