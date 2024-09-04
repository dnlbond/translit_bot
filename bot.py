import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def transliterate_name(text: str):
    translit_dict = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 
        'Ы': 'Y', 'Ъ': 'IE', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA'
    }
    
    result = ''
    for char in text:
        result += translit_dict.get(char.upper(), char)
    
    result = ' '.join([i.capitalize() for i in result.split()])

    return result

@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id = user_id, text = text)
    
@dp.message()
async def transliterate(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    original_text = message.text
    translit_text = transliterate_name(original_text)
    logging.info(f'{user_name} {user_id}: {original_text} -> {translit_text}')
    await message.answer(text=translit_text)
    
if __name__ == '__main__':
    dp.run_polling(bot)