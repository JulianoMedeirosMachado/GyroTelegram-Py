import json
import os
from typing import List, Dict
from aiogram import types
from config import MAX_MESSAGES

class MessageStore:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.max_messages = MAX_MESSAGES
        self.messages = {}
        self.load()

    def load(self):
        """Carrega mensagens do arquivo JSON."""
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as file:
                self.messages = json.load(file)
        else:
            self.messages = {}

    def save(self):
        """Salva mensagens no arquivo JSON."""
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=4)

    def get_messages(self, chat_id: int) -> List[Dict]:
        """Retorna a lista de mensagens para um chat_id específico."""
        return self.messages.get(str(chat_id), [])

    def store_message(self, chat_id: int, message_id: int, text: str, timestamp: int, sender_name: str):
        """Armazena uma nova mensagem."""
        if str(chat_id) not in self.messages:
            self.messages[str(chat_id)] = []
        self.messages[str(chat_id)].append({
            'message_id': message_id,
            'text': text,
            'timestamp': timestamp,
            'sender_name': sender_name
        })
        self.save()

        if len(self.messages[str(chat_id)]) > self.max_messages:
            self.messages[str(chat_id)] = self.messages[str(chat_id)][-self.max_messages:]
        self.save()

    def delete_message(self, chat_id: int, message_id: int):
        """Remove uma mensagem específica."""
        if str(chat_id) in self.messages:
            self.messages[str(chat_id)] = [
                msg for msg in self.messages[str(chat_id)]
                if msg['message_id'] != message_id
            ]
            self.save()

