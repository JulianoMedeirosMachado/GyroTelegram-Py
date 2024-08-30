from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode

async def create_yourown_bot_handler(message: types.Message):
    await message.reply("Create your own bot")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(create_yourown_bot_handler, commands=['createyourownbot'])

