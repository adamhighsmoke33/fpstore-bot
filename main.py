import os
import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- 1. ВЕБ-СЕРВЕР ---
app = Flask('')

@app.route('/')
def home():
    return "FPStore Online"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- 2. НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Убрали DefaultBotProperties, чтобы не было конфликтов с тегами
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

# --- 3. ЛОГИКА ---

@dp.message(Command("start"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.clear()
    link = "https://vk.ru/@fpstore23-politika-konfidencialnosti-fpstore"
    text = (
        f"🚀 <b>FPStore</b>\n\n"
        f"Нажимая «ДА», вы принимаете <a href='{link}'>политику конфиденциальности</a>.\n\n"
        f"<b>Сборка планируется в ближайшее время?</b>"
    )
    # Здесь явно указываем HTML
    await message.answer(text, reply_markup=make_kb(["ДА", "НЕТ"]), parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(Survey.q1_time)

@dp.message(Survey.q1_time)
async def p1(m: types.Message, state: FSMContext):
    await state.update_data(q1=m.text)
    # Обычный текст без тегов — никаких скобок не будет
    await m.answer("Как к Вам обращаться?")
    await state.set_state(Survey.q2_name)

@dp.message(Survey.q2_name)
async def p2(m: types.Message, state: FSMContext):
    await state.update_data(q2=m.text)
    await m.answer("Ваш номер телефона?")
    await state.set_state(Survey.q3_phone)

@dp.message(Survey.q3_phone)
async def p3(m: types.Message, state: FSMContext):
    await state.update_data(q3=m.text)
    await m.answer("Ваш бюджет на сборку?", reply_markup=make_kb(["35-50", "50-75", "75-100", "100+"]))
    await state.set_state(Survey.q4_budget)

@dp.message(Survey.q4_budget)
async def p4(m: types.Message, state: FSMContext):
    await state.update_data(q4=m.text)
    await m.answer("Сборка и настройка входит в бюджет?", reply_markup=make_kb(["ДА", "НЕТ"]))
    await state.set_state(Survey.q5_service)

@dp.message(Survey.q5_service)
async def p5(m: types.Message, state: FSMContext):
    await state.update_data(q5=m.text)
    await m.answer("Для каких задач ПК?", reply_markup=make_kb(["Игры", "Офисные задачи", "Другое"]))
    await state.set_state(Survey.q6_tasks)

@dp.message(Survey.q6_tasks)
async def p6(m: types.Message, state: FSMContext):
    await state.update_data(q6=m.text)
    await m.answer("Цвет корпуса?", reply_markup=make_kb(["Черный", "Белый", "Другой"]))
    await state.set_state(Survey.q7_color)

@dp.message(Survey.q7_color)
async def p7(m: types.Message, state: FSMContext):
    await state.update_data(q7=m.text)
    await m.answer("Нужна ли подсветка?", reply_markup=make_kb(["ДА", "НЕТ"]))
    await state.set_state(Survey.q8_light)

@dp.message(Survey.q8_light)
async def p8(m: types.Message, state: FSMContext):
    await state.update_data(q8=m.text)
    await m.answer("Процессор?", reply_markup=make_kb(["Intel", "AMD", "Любой"]))
    await state.set_state(Survey.q9_platform)

@dp.message(Survey.q9_platform)
async def p9(m: types.Message, state: FSMContext):
    await state.update_data(q9=m.text)
    await m.answer("Видеокарта?", reply_markup=make_kb(["NVIDIA", "AMD", "Любая"]))
    await state.set_state(Survey.q10_gpu)

@dp.message(Survey.q10_gpu)
async def p10(m: types.Message, state: FSMContext):
    await state.update_data(q10=m.text)
    await m.answer("Нужна установка Windows?", reply_markup=make_kb(["ДА", "НЕТ"]))
    await state.set_state(Survey.q11_os)

@dp.message(Survey.q11_os)
async def p11(m: types.Message, state: FSMContext):
    await state.update_data(q11=m.text)
    await m.answer("Из какого Вы города?")
    await state.set_state(Survey.q12_city)

@dp.message(Survey.q12_city)
async def p12(m: types.Message, state: FSMContext):
    await state.update_data(q12=m.text)
    await m.answer("Способ доставки?", reply_markup=make_kb(["СДЭК", "Самовывоз", "В черте города"]))
    await state.set_state(Survey.q13_delivery)

@dp.message(Survey.q13_delivery)
async def p13(m: types.Message, state: FSMContext):
    await state.update_data(q13=m.text)
    if "СДЭК" in m.text.upper():
        await m.answer("Введите адрес отделения СДЭК:")
        await state.set_state(Survey.q14_address)
    else:
        await finish_now(m, state)

@dp.message(Survey.q14_address)
async def p14(m: types.Message, state: FSMContext):
    await state.update_data(q14=m.text)
    await finish_now(m, state)

async def finish_now(m: types.Message, state: FSMContext):
    data = await state.get_data()
    user = f"@{m.from_user.username}" if m.from_user.username else "Ник скрыт"
    rep = (
        f"📩 <b>НОВАЯ ЗАЯВКА FPStore</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Имя:</b> {data.get('q2')}\n"
        f"🔗 <b>Связь:</b> {user}\n"
        f"📞 <b>Тел:</b> {data.get('q3')}\n"
        f"💰 <b>Бюджет:</b> {data.get('q4')}\n"
        f"📦 <b>Сборка в бюджете?:</b> {data.get('q5')}\n"
        f"⚙️ <b>Задачи:</b> {data.get('q6')}\n"
        f"🎨 <b>Цвет корпуса:</b> {data.get('q7')}\n"
        f"💡 <b>Подсветка:</b> {data.get('q8')}\n"
        f"🔌 <b>Процессор:</b> {data.get('q9')}\n"
        f"🎮 <b>Видеокарта:</b> {data.get('q10')}\n"
        f"🖥️ <b>Windows:</b> {data.get('q11')}\n"
        f"📍 <b>Город:</b> {data.get('q12')}\n"
        f"🚚 <b>Доставка:</b> {data.get('q13')}\n"
        f"🏠 <b>Адрес СДЭК:</b> {data.get('q14', 'Не указан')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏰ <b>Срочность:</b> {data.get('q1')}"
    )
    await bot.send_message(ADMIN_ID, rep, parse_mode="HTML")
    await m.answer("✅ Заявка принята! Скоро свяжемся.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
