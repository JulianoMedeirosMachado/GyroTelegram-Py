import logging
from aiogram import Dispatcher, types
from aiogram.types import InputFile
import os

async def sticker_handler(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.answer("Por favor, responda a uma imagem com o comando /figurinha.")
        return
    
    try:
        temp_message = await message.answer("Gerando figurinha...")

        photo = message.reply_to_message.photo[-1]
        photo_file = await photo.download()

        await message.bot.send_sticker(chat_id=message.chat.id, sticker=InputFile(photo_file.name))
        
        os.remove(photo_file.name)

        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

    except Exception as e:
        logging.error(f"Erro ao criar figurinha: {e}")
        await message.answer("Ocorreu um erro ao criar a figurinha. Por favor, tente novamente.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(sticker_handler, commands=['figurinha'])

