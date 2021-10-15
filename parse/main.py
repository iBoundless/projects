import logging
import asyncio
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.types.message import ParseMode
from config import TOKEN, URL
from db import process_search_model, init_db, find_id_search, find_all_cards
from parsermodul import ParseVideoCard


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='list')
async def send_list(message: types.Message):
    search_models = find_id_search(message.chat.id)
    cards=find_all_cards()
    for card in cards:
        card_title=card.title
        for search_model in search_models:
            search_title=search_model.title
            if card_title.find(search_title)>=0:
                message_text='Строка поиска {} \r\n Найдено {}'.format(search_title, utils.markdown.hlink(card_title, card.url))
    await message.answer(text=message_text, parse_mode=ParseMode.HTML)

@dp.message_handler(commands='search')
async def send_search(message: types.Message):
    search_models=find_id_search(message.chat.id)
    for search_model in search_models:
        await message.answer(text=search_model.title)

@dp.message_handler(commands='poslat')
async def send_search(message: types.Message):
    message_text='Иди на юг!'
    await message.answer(text=message_text)


@dp.message_handler()
async def echo(message: types.Message):
    await process_search_model(message)

async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        await parser.parse()

if __name__ =='__main__':
    init_db()
    parser = ParseVideoCard(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(100,parser))
    executor.start_polling(dp, skip_updates=True)