import os
import asyncio
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
# Добавили этот импорт для работы с файлами
from aiogram.types import FSInputFile

# --- 1. ВЕБ-СЕРВЕР ДЛЯ RENDER ---
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

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Survey(StatesGroup):
    q1_time = State()
    q2_name = State()
    q3_phone = State()
    q4_budget = State()
    q5_tasks = State()
    q6_color = State()
    q7_light = State()
    q8_platform = State()
    q9_gpu = State()
    q10_os = State()
    q11_city = State()
    q12_delivery = State()
    q13_address = State()

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
    
    photo_path = "pc.jpg"
    link = "https://vk.ru/@fpstore23-politika-konfidencialnosti-fpstore"
    
    caption = (
        f"🚀 <b>FPStore</b>\n\n"
        f"Нажимая «ДА», вы принимаете <a href='{link}'>политику конфиденциальности</a>.\n\n"
        f"<b>Сборка планируется в ближайшее время?</b>"
    )

    try:
        if os.path.exists(photo_path):
            await message.answer_photo(
                photo=FSInputFile(photo_path),
                caption=caption,
                reply_markup=make_kb(["ДА", "НЕТ"]),
                parse_mode="HTML"
            )
        else:
            await message.answer(caption, reply_markup=make_kb(["ДА", "НЕТ"]), parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        await message.answer(caption, reply_markup=make_kb(["ДА", "НЕТ"]), parse_mode="HTML")
    
    await state.set_state(Survey.q1_time)

@dp.message(Survey.q1_time)
async def p1(m: types.Message, state: FSMContext):
    await state.update_data(q1=m.text)
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
    await m.answer("Для каких задач ПК?", reply_markup=make_kb(["Игры", "Офисные задачи", "Другое"]))
    await state.set_state(Survey.q5_tasks)

@dp.message(Survey.q5_tasks)
async def p5(m: types.Message, state: FSMContext):
    await state.update_data(q5=m.text)
    await m.answer("Цвет корпуса?", reply_markup=make_kb(["Черный", "Белый", "Другой"]))
    await state.set_state(Survey.q6_color)

@dp.message(Survey.q6_color)
async def p6(m: types.Message, state: FSMContext):
    await state.update_data(q6=m.text)
    await m.answer("Нужна ли подсветка?", reply_markup=make_kb(["ДА", "НЕТ"]))
    await state.set_state(Survey.q7_light)

@dp.message(Survey.q7_light)
async def p7(m: types.Message, state: FSMContext):
    await state.update_data(q7=m.text)
    await m.answer("Процессор?", reply_markup=make_kb(["Intel", "AMD", "Любой"]))
    await state.set_state(Survey.q8_platform)

@dp.message(Survey.q8_platform)
async def p8(m: types.Message, state: FSMContext):
    await state.update_data(q8=m.text)
    await m.answer("Видеокарта?", reply_markup=make_kb(["NVIDIA", "AMD", "Любая"]))
    await state.set_state(Survey.q9_gpu)

@dp.message(Survey.q9_gpu)
async def p9(m: types.Message, state: FSMContext):
    await state.update_data(q9=m.text)
    await m.answer("Нужна установка Windows c драйверами и тестами?", reply_markup=make_kb(["ДА", "НЕТ"]))
    await state.set_state(Survey.q10_os)

@dp.message(Survey.q10_os)
async def p10(m: types.Message, state: FSMContext):
    await state.update_data(q10=m.text)
    await m.answer("Из какого Вы города?")
    await state.set_state(Survey.q11_city)

@dp.message(Survey.q11_city)
async def p11(m: types.Message, state: FSMContext):
    await state.update_data(q11=m.text)
    await m.answer("Способ доставки?", reply_markup=make_kb(["СДЭК", "Самовывоз", "В черте города"]))
    await state.set_state(Survey.q12_delivery)

@dp.message(Survey.q12_delivery)
async def p12(m: types.Message, state: FSMContext):
    await state.update_data(q12=m.text)
    if "СДЭК" in m.text.upper():
        await m.answer("Введите адрес отделения СДЭК:")
        await state.set_state(Survey.q13_address)
    else:
        await finish_now(m, state)

@dp.message(Survey.q13_address)
async def p13(m: types.Message, state: FSMContext):
    await state.update_data(q13=m.text)
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
        f"⚙️ <b>Задачи:</b> {data.get('q5')}\n"
        f"🎨 <b>Цвет корпуса:</b> {data.get('q6')}\n"
        f"💡 <b>Подсветка:</b> {data.get('q7')}\n"
        f"🔌 <b>Платформа:</b> {data.get('q8')}\n"
        f"🎮 <b>Видеокарта:</b> {data.get('q9')}\n"
        f"🖥️ <b>Windows:</b> {data.get('q10')}\n"
        f"📍 <b>Город:</b> {data.get('q11')}\n"
        f"🚚 <b>Доставка:</b> {data.get('q12')}\n"
        f"🏠 <b>Адрес СДЭК:</b> {data.get('q13', 'Не указан')}\n"
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
