import logging
from aiogram import Dispatcher, types
from collections import deque
import google.generativeai as genai
from config import MAX_MESSAGES, GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class MessageStore:
    def __init__(self):
        self.store = {}

    def add_message(self, chat_id, message_id, text, timestamp):
        if chat_id not in self.store:
            self.store[chat_id] = deque(maxlen=MAX_MESSAGES)
        self.store[chat_id].append({
            'id': message_id,
            'text': text,
            'timestamp': timestamp
        })
        logging.info(f"Mensagem adicionada ao chat {chat_id}: {text}")

    def get_messages(self, chat_id):
        messages = list(self.store.get(chat_id, []))
        logging.info(f"Mensagens recuperadas do chat {chat_id}: {messages}")
        return messages

async def store_message(message: types.Message, message_store: MessageStore):
    if message.text:
        message_store.add_message(
            message.chat.id,
            message.message_id,
            message.text,
            message.date
        )
        logging.info(f"Mensagem armazenada no chat {message.chat.id}: {message.text}")

