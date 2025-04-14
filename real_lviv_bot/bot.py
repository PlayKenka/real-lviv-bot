
import logging
from aiogram import Bot, Dispatcher, types, executor
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ADMIN_ID = "your_telegram_user_id"  # заміни на свій Telegram user ID

CATEGORY_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True)
CATEGORY_KEYBOARD.add("Заклад", "Лікар", "Фільм")
CATEGORY_KEYBOARD.add("Доставка", "Спортзал", "СТО")
CATEGORY_KEYBOARD.add("Товари", "Відпочинок", "Анонімно")

user_states = {}

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привіт! Обери категорію, про що хочеш залишити відгук:",
        reply_markup=CATEGORY_KEYBOARD,
    )

@dp.message_handler(lambda message: message.text in ["Заклад", "Лікар", "Фільм", "Доставка", "Спортзал", "СТО", "Товари", "Відпочинок", "Анонімно"])
async def category_chosen(message: types.Message):
    user_states[message.from_user.id] = message.text
    await message.reply("Напиши свій відгук або надішли фото:")

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def forward_feedback(message: types.Message):
    category = user_states.get(message.from_user.id, "Без категорії")
    user = message.from_user

    if message.content_type == "text":
        text = f"Надійшов відгук у категорії *{category}*:

{message.text}"
        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")
    elif message.photo:
        caption = f"Фото з відгуком у категорії *{category}*"
        await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=caption, parse_mode="Markdown")

    await message.reply("Дякуємо за твій відгук!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
