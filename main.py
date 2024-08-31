import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from utils import MessageStore
from handlers import register_all_handlers

logging.basicConfig(level=logging.INFO)

message_store = MessageStore(json_file='messages.json')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.info("Registrando handlers...")
register_all_handlers(dp, message_store)

async def handle_message(message: types.Message):
    message_store.store_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=message.text,
        timestamp=message.date.timestamp()
    )

dp.register_message_handler(handle_message, content_types=types.ContentTypes.TEXT)

def main():
    logging.info("Iniciando bot...")
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()

