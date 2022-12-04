from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
import urllib.request
import json
import os
import time

bot = Bot(token="") #Тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
async def anti_flood(*args, **kwargs):
    pass
    
@dp.message_handler(commands="start")
@dp.throttled(anti_flood,rate=0.1)
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Добро пожаловать в бота BalaBoba\nЭто еще один проект от @CTOHKC\nСуть бота продолжать ваши истории.\nОтправь любой текст и бот попробует продолжить твое высказывание.")
    
@dp.message_handler(content_types=["text"])
@dp.throttled(anti_flood,rate=0.1)
async def get_text(message):
    chat_id = message.chat.id
    msg = await bot.send_message(chat_id, "Начинаю обработку...")
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://yandex.com',
    'Referer': 'https://yandex.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 05)',
    'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
        
    data = {'query': f'{message.text}', 'intro': 0, 'filter': 1}
    API_URL = 'https://yandex.ru/lab/api/yalm/text3'
    params = json.dumps(data).encode('utf8')
    await msg.edit_text("Ожидаем ответа...")
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    res = response.read().decode('utf8')
    result = json.loads(res)
    await msg.edit_text(f"<b>{message.text}</b> {result['text']}\n\nРазработчик: @CTOHKC", parse_mode='html')
    
while True:
    try:
        if __name__ == "__main__":
            executor.start_polling(dp, skip_updates=True)
    except:
        print("Ошибка.\nОжидаем перезапуск 20 сек...")
        time.sleep(20)