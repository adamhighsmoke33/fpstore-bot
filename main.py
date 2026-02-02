from flask import Flask
from threading import Thread
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    # Replit uses port 5000 for the web server
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- НАСТРОЙКИ ---
API_TOKEN = os.getenv("BOT_TOKEN")
admin_id_env = os.getenv("ADMIN_ID")
ADMIN_ID = int(admin_id_env) if admin_id_env else None

# Initialize bot only if token is provided and valid
bot = None
if API_TOKEN and API_TOKEN != "YOUR_BOT_TOKEN":
    try:
        bot = Bot(token=API_TOKEN)
    except Exception as e:
        print(f"Error initializing bot: {e}")

dp = Dispatcher()

# --- СОСТОЯНИЯ ОПРОСА ---
class OrderPC(StatesGroup):
    q1_time = State()
    q2_name = State()
    q3_phone = State()
    q4_budget = State()
    q5_service_inc = State()
    q6_tasks = State()
    q7_color = State()
    q8_rgb = State()
    q9_platform = State()
    q10_gpu = State()
    q11_os = State()
    q12_city = State()
    q13_delivery = State()
    q14_address = State()

# --- КЛАВИАТУРЫ ---
def get_kb(options):
    buttons = [[KeyboardButton(text=opt)] for opt in options]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- ЛОГИКА ---

@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    welcome_text = (
        "<b>Заявка на сборку ПК в FPStore</b>\n\n"
        "Пожалуйста, внимательно заполните форму. Внимание! Цены и наличие меняются каждый день. "
        "Конфигурация актуальна только в течение дня заказа."
    )
    await message.answer(welcome_text, parse_mode="HTML")
    await message.answer("Вопрос 1: ПЛАНИРУЕТЕ ЛИ ВЫ СБОРКУ ПК В БЛИЖАЙШЕЕ ВРЕМЯ?", 
                         reply_markup=get_kb(["ДА", "НЕТ"]))
    await state.set_state(OrderPC.q1_time)

@dp.message(OrderPC.q1_time)
async def q1(message: types.Message, state: FSMContext):
    await state.update_data(q1_time=message.text)
    await message.answer("Вопрос 2: Ваше Имя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderPC.q2_name)

@dp.message(OrderPC.q2_name)
async def q2(message: types.Message, state: FSMContext):
    await state.update_data(q2_name=message.text)
    await message.answer("Вопрос 3: Номер телефона")
    await state.set_state(OrderPC.q3_phone)

@dp.message(OrderPC.q3_phone)
async def q3(message: types.Message, state: FSMContext):
    await state.update_data(q3_phone=message.text)
    await message.answer("Вопрос 4: Каков Ваш бюджет на ПК?")
    await state.set_state(OrderPC.q4_budget)

@dp.message(OrderPC.q4_budget)
async def q4(message: types.Message, state: FSMContext):
    await state.update_data(q4_budget=message.text)
    text = ("Стоимость услуги по сборке составляет 6% (не менее 3500р). "
            "В нее входит сборка и кабель-менеджмент.\n\n"
            "Вопрос 5: Включена ли услуга в бюджет?")
    await message.answer(text, reply_markup=get_kb(["ДА", "НЕТ"]))
    await state.set_state(OrderPC.q5_service_inc)

@dp.message(OrderPC.q5_service_inc)
async def q5(message: types.Message, state: FSMContext):
    await state.update_data(q5_service_inc=message.text)
    await message.answer("Вопрос 6: Для каких задач ПК?", 
                         reply_markup=get_kb(["Работа с документами и серфинг", "Игры", "Свой вариант"]))
    await state.set_state(OrderPC.q6_tasks)

@dp.message(OrderPC.q6_tasks)
async def q6(message: types.Message, state: FSMContext):
    await state.update_data(q6_tasks=message.text)
    await message.answer("Цвет корпуса и комплектующих:", 
                         reply_markup=get_kb(["Белый", "Черный", "Не имеет значения", "Свой вариант"]))
    await state.set_state(OrderPC.q7_color)

@dp.message(OrderPC.q7_color)
async def q7(message: types.Message, state: FSMContext):
    await state.update_data(q7_color=message.text)
    await message.answer("Подсветка в корпусе:", 
                         reply_markup=get_kb(["ДА", "НЕТ", "Не имеет значения", "Свой вариант"]))
    await state.set_state(OrderPC.q8_rgb)

@dp.message(OrderPC.q8_rgb)
async def q8(message: types.Message, state: FSMContext):
    await state.update_data(q8_rgb=message.text)
    await message.answer("Платформа:", 
                         reply_markup=get_kb(["Intel", "AMD", "Я полагаюсь на выбор FPStore"]))
    await state.set_state(OrderPC.q9_platform)

@dp.message(OrderPC.q9_platform)
async def q9(message: types.Message, state: FSMContext):
    await state.update_data(q9_platform=message.text)
    await message.answer("Видеокарта:", 
                         reply_markup=get_kb(["Nvidia", "AMD", "Intel", "Я полагаюсь на выбор FPStore"]))
    await state.set_state(OrderPC.q10_gpu)

@dp.message(OrderPC.q10_gpu)
async def q10(message: types.Message, state: FSMContext):
    await state.update_data(q10_gpu=message.text)
    await message.answer("Установка и настройка Windows + тесты:", 
                         reply_markup=get_kb(["Windows 10", "Windows 11", "Не нуждаюсь в установке и тестах"]))
    await state.set_state(OrderPC.q11_os)

@dp.message(OrderPC.q11_os)
async def q11(message: types.Message, state: FSMContext):
    await state.update_data(q11_os=message.text)
    await message.answer("Ваш город:", reply_markup=get_kb(["Горячий Ключ", "Другой город(требуется доставка)"]))
    await state.set_state(OrderPC.q12_city)

@dp.message(OrderPC.q12_city)
async def q12(message: types.Message, state: FSMContext):
    await state.update_data(q12_city=message.text)
    await message.answer("Способ доставки:", 
                         reply_markup=get_kb(["Транспортной компанией СДЭК", "Курьером (Горячий Ключ)", "Самовывоз"]))
    await state.set_state(OrderPC.q13_delivery)

@dp.message(OrderPC.q13_delivery)
async def q13(message: types.Message, state: FSMContext):
    await state.update_data(q13_delivery=message.text)
    
    if "СДЭК" in message.text:
        await message.answer("Адрес доставки (индекс, страна, город, улица, дом, квартира):", 
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(OrderPC.q14_address)
    else:
        await state.update_data(q14_address="Не требуется")
        await finish_order(message, state)

@dp.message(OrderPC.q14_address)
async def q14(message: types.Message, state: FSMContext):
    await state.update_data(q14_address=message.text)
    await finish_order(message, state)

async def finish_order(message, state):
    data = await state.get_data()
    user = message.from_user
    
    # Текст для клиента
    finish_text = (
        "Доставка в другие города осуществляется СДЭК (упаковка, обрешетка, страховка). "
        "Стоимость рассчитывается индивидуально.\n\n"
        "Спасибо за заявку! В скором времени мы свяжемся с Вами!"
    )
    await message.answer(finish_text, reply_markup=ReplyKeyboardRemove())

    # Отчет для админа
    if ADMIN_ID and bot:
        report = (
            f"🚀 <b>НОВАЯ ЗАЯВКА FPStore</b>\n"
            f"Клиент: {data['q2_name']}\n"
            f"ТГ: @{user.username if user.username else 'нет'} (ID: {user.id})\n"
            f"Телефон: {data['q3_phone']}\n"
            f"🏙 Город: {data['q12_city']}\n"
            f"--------------------------\n"
            f"💰 Бюджет: {data['q4_budget']} (Сборка вкл: {data['q5_service_inc']})\n"
            f"🎯 Задачи: {data['q6_tasks']}\n"
            f"🎨 Цвет: {data['q7_color']} | RGB: {data['q8_rgb']}\n"
            f"💻 Железо: {data['q9_platform']} + {data['q10_gpu']}\n"
            f"💿 ОС: {data['q11_os']}\n"
            f"🚚 Доставка: {data['q13_delivery']}\n"
            f"📍 Адрес: {data['q14_address']}\n"
            f"⏳ Сборка в ближайшее время: {data['q1_time']}"
        )
        try:
            await bot.send_message(ADMIN_ID, report, parse_mode="HTML")
        except Exception as e:
            print(f"Error sending report to admin: {e}")
    await state.clear()

async def main():
    keep_alive()  # Запускаем веб-сервер
    if bot:
        print("Bot is starting...")
        await dp.start_polling(bot)
    else:
        print("Bot token is missing or invalid. Please set BOT_TOKEN in Secrets.")
        # Keep the thread alive if bot is not running
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
    except Exception as e:
        print(f"Critical error: {e}")
