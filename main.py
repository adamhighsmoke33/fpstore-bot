import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from flask import Flask
from threading import Thread

# --- БЛОК ОЖИВИТЕЛЯ (ДЛЯ RENDER) ---
app = Flask('')
@app.route('/')
def home(): return "FPStore Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- НАСТРОЙКИ ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- СОСТОЯНИЯ ОПРОСА ---
class Survey(StatesGroup):
    q1_time = State()
    q2_name = State()
    q3_phone = State()
    q4_budget = State()
    q5_service = State()
    q6_tasks = State()
    q6_color = State()
    q7_light = State()
    q8_platform = State()
    q9_gpu = State()
    q10_os = State()
    q11_city = State()
    q12_delivery = State()
    q13_address = State()

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ КНОПОК ---
def make_row_keyboard(items: list):
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.button(text=item)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# --- ЛОГИКА БОТА ---

@dp.message(Command("start"))
async def start_survey(message: types.Message, state: FSMContext):
    await message.answer(
        "🚀 **Заявка на сборку ПК в FPStore**\n\n"
        "Пожалуйста, внимательно заполните форму. Цены актуальны в течение дня.\n\n"
        "**Вопрос 1:** Планируете ли Вы сборку ПК в ближайшее время?",
        reply_markup=make_row_keyboard(["ДА", "НЕТ"])
    )
    await state.set_state(Survey.q1_time)

@dp.message(Survey.q1_time)
async def process_q1(message: types.Message, state: FSMContext):
    await state.update_data(q1_time=message.text)
    await message.answer("**Вопрос 2:** Ваше Имя?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Survey.q2_name)

@dp.message(Survey.q2_name)
async def process_q2(message: types.Message, state: FSMContext):
    await state.update_data(q2_name=message.text)
    await message.answer("**Вопрос 3:** Ваш номер телефона?")
    await state.set_state(Survey.q3_phone)

@dp.message(Survey.q3_phone)
async def process_q3(message: types.Message, state: FSMContext):
    await state.update_data(q3_phone=message.text)
    await message.answer("**Вопрос 4:** Каков Ваш бюджет на ПК?")
    await state.set_state(Survey.q4_budget)

@dp.message(Survey.q4_budget)
async def process_q4(message: types.Message, state: FSMContext):
    await state.update_data(q4_budget=message.text)
    await message.answer(
        "Стоимость услуги по сборке составляет 6% от комплектующих (минимум 3500р).\n"
        "**Вопрос 5:** Включена ли услуга по сборке в бюджет?",
        reply_markup=make_row_keyboard(["ДА", "НЕТ"])
    )
    await state.set_state(Survey.q5_service)

@dp.message(Survey.q5_service)
async def process_q5(message: types.Message, state: FSMContext):
    await state.update_data(q5_service=message.text)
    await message.answer(
        "**Вопрос 6:** Для каких задач будущий ПК?",
        reply_markup=make_row_keyboard(["Игры", "Работа с документами", "Свой вариант"])
    )
    await state.set_state(Survey.q6_tasks)

@dp.message(Survey.q6_tasks)
async def process_q6_tasks(message: types.Message, state: FSMContext):
    await state.update_data(q6_tasks=message.text)
    await message.answer(
        "**Вопрос 6 (доп):** Цвет корпуса и комплектующих?",
        reply_markup=make_row_keyboard(["Белый", "Черный", "Не имеет значения", "Свой вариант"])
    )
    await state.set_state(Survey.q6_color)

@dp.message(Survey.q6_color)
async def process_q6_color(message: types.Message, state: FSMContext):
    await state.update_data(q6_color=message.text)
    await message.answer(
        "**Вопрос 7:** Нужна ли подсветка?",
        reply_markup=make_row_keyboard(["ДА", "НЕТ", "Не имеет значения", "Свой вариант"])
    )
    await state.set_state(Survey.q7_light)

@dp.message(Survey.q7_light)
async def process_q7(message: types.Message, state: FSMContext):
    await state.update_data(q7_light=message.text)
    await message.answer(
        "**Вопрос 8:** Платформа?",
        reply_markup=make_row_keyboard(["Intel", "AMD", "Я полагаюсь на выбор FPStore"])
    )
    await state.set_state(Survey.q8_platform)

@dp.message(Survey.q8_platform)
async def process_q8(message: types.Message, state: FSMContext):
    await state.update_data(q8_platform=message.text)
    await message.answer(
        "**Вопрос 9:** Видеокарта?",
        reply_markup=make_row_keyboard(["Nvidia", "AMD", "Intel", "Я полагаюсь на выбор FPStore"])
    )
    await state.set_state(Survey.q9_gpu)

@dp.message(Survey.q9_gpu)
async def process_q9(message: types.Message, state: FSMContext):
    await state.update_data(q9_gpu=message.text)
    await message.answer(
        "**Вопрос 10:** Установка Windows и тесты?",
        reply_markup=make_row_keyboard(["Windows 10", "Windows 11", "Не нуждаюсь в установке"])
    )
    await state.set_state(Survey.q10_os)

@dp.message(Survey.q10_os)
async def process_q10(message: types.Message, state: FSMContext):
    await state.update_data(q10_os=message.text)
    await message.answer(
        "**Вопрос 11:** Ваш город?",
        reply_markup=make_row_keyboard(["Горячий Ключ", "Другой город"])
    )
    await state.set_state(Survey.q11_city)

@dp.message(Survey.q11_city)
async def process_q11(message: types.Message, state: FSMContext):
    await state.update_data(q11_city=message.text)
    await message.answer(
        "**Вопрос 12:** Способ доставки?",
        reply_markup=make_row_keyboard(["Транспортной компанией СДЭК", "Курьером (ГК)", "Самовывоз"])
    )
    await state.set_state(Survey.q12_delivery)

@dp.message(Survey.q12_delivery)
async def process_q12(message: types.Message, state: FSMContext):
    # Сохраняем ответ, убирая лишние пробелы по краям
    delivery_choice = message.text.strip()
    await state.update_data(q12_delivery=delivery_choice)
    
    # Проверяем выбор (используем "in", чтобы поиск был гибче)
    if "СДЭК" in delivery_choice:
        await message.answer("🏠 **Вопрос 13:** Введите адрес доставки (индекс, город, улица, дом):")
        await state.set_state(Survey.q13_address)
    else:
        # Если это самовывоз или курьер — завершаем опрос
        await finish_survey(message, state)

@dp.message(Survey.q13_address)
async def process_q13(message: types.Message, state: FSMContext):
    await state.update_data(q13_address=message.text)
    await finish_survey(message, state)

async def finish_survey(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "Нет ника"
    user_link = f"tg://user?id={message.from_user.id}"
    
    # Формируем отчет для админа
    report = (
        f"📩 **НОВАЯ ЗАЯВКА FPStore**\n"
        f"👤 Клиент: {user_data.get('q2_name')} ({username})\n"
        f"🔗 Ссылка: [Профиль клиента]({user_link})\n"
        f"📞 Тел: {user_data.get('q3_phone')}\n"
        f"💰 Бюджет: {user_data.get('q4_budget')}\n"
        f"⚙️ Сборка в бюджет: {user_data.get('q5_service')}\n"
        f"🎮 Задачи: {user_data.get('q6_tasks')}\n"
        f"🎨 Цвет: {user_data.get('q6_color')}\n"
        f"💡 Подсветка: {user_data.get('q7_light')}\n"
        f"📟 Платформа: {user_data.get('q8_platform')} / {user_data.get('q9_gpu')}\n"
        f"💿 ОС: {user_data.get('q10_os')}\n"
        f"📍 Город: {user_data.get('q11_city')}\n"
        f"🚚 Доставка: {user_data.get('q12_delivery')}\n"
    )
    if user_data.get('q13_address'):
        report += f"🏠 Адрес: {user_data.get('q13_address')}\n"

    try:
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        await message.answer(
            "Спасибо за заявку! В скором времени мы свяжемся с Вами!\n\n"
            "Доставка СДЭК включает страховку и обрешетку. Стоимость рассчитаем при отправке.",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
