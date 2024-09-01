from aiogram import Dispatcher, types
import google.generativeai as genai
from config import GOOGLE_API_KEY
from utils import MessageStore
import logging
import re

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def resumo_handler(message: types.Message, message_store: MessageStore):

    try:
        chat_id = message.chat.id
        logging.info(f"Comando /resumo recebido no chat {chat_id}")
        temp_message = await message.answer("📝 Gerando um resumo...")
        # Carregar mensagens do chat_id
        messages = message_store.get_messages(chat_id)
        if not messages:
            await message.answer("Não há mensagens para resumir.")
            await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)
            return

        messages.sort(key=lambda msg: msg['timestamp'])
        messages_text = ''.join(f"{msg['sender_name']}: {msg['text']}\n" for msg in messages)
        prompt = f"Resuma o seguinte texto citando o autor de cada tópico: {messages_text[:6000]}"
        response = model.generate_content(prompt)
        response_text = response.text
        escaped_response_text = re.sub(r'([\.!*-_~[\](){}])', r'\\\1', response_text)
        await message.answer(escaped_response_text, parse_mode='MarkdownV2')
        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

    except Exception as e:
        logging.error(f"Erro durante a obtenção do resumo: {e}")
        await message.answer("<b>Ocorreu um erro, por favor tente novamente</b>", parse_mode='html')
        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

def register_resumo_handler(dp: Dispatcher, message_store: MessageStore):
    dp.register_message_handler(lambda message: resumo_handler(message, message_store), commands=['resumo'])

