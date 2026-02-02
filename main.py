import os
import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- 1. ОЖИВИТЕЛЬ ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "FPStore is Online"
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    Thread(target=run).start()

# --- 2. НАСТРОЙКИ ---
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
    for item in items: builder.button(text=item)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# --- 3. ЛОГИКА ОПРОСА ---

@dp.message(Command("start"))
async def start_survey(message: types.Message, state: FSMContext):
    policy_url = "ТВОЯ_ССЫЛКА_НА_ВК"  # <--- ВСТАВЬ СВОЮ ССЫЛКУ ТУТ
    text = (
        "🚀 <b>Заявка на сборку ПК в FPStore</b>\n\n"
        f"Нажимая «ДА», вы соглашаетесь с <a href='{policy_url}'>политикой конфиденциальности</a>.\n\n"
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
    await m.answer("<b>Вопрос 5:</b> Что входит в бюджет?", reply_markup=make_kb(["Только системный блок", "ПК + монитор + периферия"]))
    await state.set_state(Survey.q5_service)

@dp.message(Survey.q5_service)
async def p5(m: types.Message, state: FSMContext):
    await state.update_data(q5=m.text)
    await m.answer("<b>Вопрос 6:</b> Для каких задач ПК?", reply_markup=make_kb(["Игры", "Работа/Монтаж", "Учеба"]))
    await state.set_state(Survey.q6_tasks)

@dp.message(Survey.q6_tasks)
async def p6(m: types.Message, state: FSMContext):
    await state.update_data(q6=m.text)
    await m.answer("<b>Вопрос 7:</b> Желаемый цвет корпуса?", reply_markup=make_kb(["Черный", "Белый", "Другой"]))
    await state.set_state(Survey.q7_color)

@dp.message(Survey.q7_color)
async def p7(m: types.Message, state: FSMContext):
    await state.update_data(q7=m.text)
    await m.answer("<b>Вопрос 8:</b> Нужна ли подсветка?", reply_markup=make_kb(["Да, много RGB", "Минимум/Нет"]))
    await state.set_state(Survey.q8_light)

@dp.message(Survey.q8_light)
async def p8(m: types.Message, state: FSMContext):
    await state.update_data(q8=m.text)
    await m.answer("<b>Вопрос 9:</b> Предпочтения по платформе?", reply_markup=make_kb(["Intel", "AMD", "Без разницы"]))
    await state.set_state(Survey.q9_platform)

@dp.message(Survey.q9_platform)
async def p9(m: types.Message, state: FSMContext):
    await state.update_data(q9=m.text)
    await m.answer("<b>Вопрос 10:</b> Предпочтения по видеокарте?", reply_markup=make_kb(["NVIDIA GeForce", "AMD Radeon", "Без разницы"]))
    await state.set_state(Survey.q10_gpu)

@dp.message(Survey.q10_gpu)
async def p10(m: types.Message, state: FSMContext):
    await state.update_data(q10=m.text)
    await m.answer("<b>Вопрос 11:</b> Нужна ли предустановка Windows?", reply_markup=make_kb(["Да", "Нет"]))
    await state.set_state(Survey.q11_os)

@dp.message(Survey.q11_os)
async def p11(m: types.Message, state: FSMContext):
    await state.update_data(q11=m.text)
    await m.answer("<b>Вопрос 12:</b> Из какого Вы города?")
    await state.set_state(Survey.q12_city)

@dp.message(Survey.q12_city)
async def p12(m: types.Message, state: FSMContext):
    await state.update_data(q12=m.text)
    await m.answer("<b>Вопрос 13:</b> Способ доставки?", reply_markup=make_kb(["СДЭК", "Курьер", "Самовывоз"]))
    await state.set_state(Survey.q13_delivery)

@dp.message(Survey.q13_delivery)
async def p13(m: types.Message, state: FSMContext):
    await state.update_data(q13=m.text)
    if "СДЭК" in m.text.upper():
        await m.answer("<b>Вопрос 14:</b> Введите адрес отделения СДЭК или домашний адрес:")
        await state.set_state(Survey.q14_address)
    else:
        await finish(m, state)

@dp.message(Survey.q14_address)
async def p14(m: types.Message, state: FSMContext):
    await state.update_data(q14=m.text)
    await finish(m, state)

async def finish(m: types.Message, state: FSMContext):
    data = await state.get_data()
    user = f"@{m.from_user.username}" if m.from_user.username else "Нет ника"
    
    report = (
        f"📩 <b>НОВАЯ ЗАЯВКА</b>\n\n"
        f"👤 Имя: {data.get('q2')}\n"
        f"🔗 Связь: {user}\n"
        f"📞 Тел: {data.get('q3')}\n"
        f"💰 Бюджет: {data.get('q4')}\n"
        f"⚙️ Задачи: {data.get('q6')}\n"
        f"🎨 Цвет: {data.get('q7')}\n"
        f"🚚 Доставка: {data.get('q13')}\n"
        f"🏠 Адрес: {data.get('q14', 'Не требуется')}"
    )
    
    await bot.send_message(ADMIN_ID, report, parse_mode="HTML")
    await m.answer("✅ Заявка отправлена! Мы свяжемся с Вами в ближайшее время.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
    # 5. Обязательно закрываем состояние, чтобы клиент мог начать заново
    await state.clear()
