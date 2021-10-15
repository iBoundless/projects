from aiogram.types import ParseMode
from aiogram import utils
from peewee import *

db = SqliteDatabase('videodb.db')

class BaseModel(Model):
    class Meta:
        database = db


class VideoCard(BaseModel):
    title = CharField()
    url = TextField()

class SearchModel(BaseModel):
    title = CharField()
    chatid = TextField()

def find_all_cards():
    return VideoCard.select()

def find_id_search(chat_id):
    return SearchModel.select().where(chat_id == SearchModel.chatid)

def find_all_search():
    return SearchModel.select()


async def process_search_model(message):
    search_exist = True
    try:
        search=SearchModel.select().where(SearchModel.title == message.text).get()
        search.delete_instance()
        await message.answer('Строка поиска {} удалена'.format(message.text))
        return search_exist
    except DoesNotExist as de:
        search_exist = False

    if not search_exist:
        rec=SearchModel(title=message.text, chatid=message.chat.id)
        rec.save()
        await message.answer('Строка поиска {} добавлена'.format(message.text))
    else:
        await message.answer('Строка поиска {} уже есть'.format(message.text))
    return search_exist

async def process_video_card(title, url, chat_id, bot):
    card_exist = True
    try:
        card = VideoCard.select().where(VideoCard.title == title).get()
    except DoesNotExist as de:
        card_exist = False

    if not card_exist:
        rec = VideoCard(title=title,url=url)
        rec.save()
        message_text=utils.markdown.hlink(title, url)
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)
    return card_exist

def init_db():
    db.create_tables([VideoCard, SearchModel])
