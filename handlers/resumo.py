import logging
from aiogram import Dispatcher, types
from collections import deque
import google.generativeai as genai
from config import MAX_MESSAGES, GOOGLE_API_KEY
from utils import MessageStore

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def resumo_handler(message: types.Message, message_store: MessageStore):
    try:
        chat_id = message.chat.id
        logging.info(f"Comando /resumo recebido no chat {chat_id}")

        temp_message = await message.answer("📝 Gerando um resumo...")

        messages = message_store.get_messages(chat_id)
        if not messages:
            await message.answer("Não há mensagens para resumir.")
            await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)
            return

        messages.sort(key=lambda msg: msg['timestamp'])
        messages_text = ''.join(msg['text'] for msg in messages)

        prompt = f"Resuma o seguinte texto: {messages_text[:2000]}"
        response = model.generate_content(prompt)
        response_text = response.text

        await message.answer(response_text, parse_mode='markdown')

        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

    except Exception as e:
        logging.error(f"Erro durante a obtenção do resumo: {e}")
        await message.answer("<b>Ocorreu um erro, por favor tente novamente</b>", parse_mode='html')

        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

def register_resumo_handler(dp: Dispatcher, message_store: MessageStore):
    dp.register_message_handler(lambda message: resumo_handler(message, message_store), commands=['resumo'])

