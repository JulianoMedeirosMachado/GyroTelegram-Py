import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from utils import MessageStore, store_message
from handlers import register_all_handlers  # Importa a função para registrar todos os handlers

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Initialize MessageStore
message_store = MessageStore()
logging.info("MessageStore inicializado.")

# Register handlers
register_all_handlers(dp, message_store)  # Passa message_store para a função de registro de handlers
dp.register_message_handler(lambda message: store_message(message, message_store), content_types=types.ContentTypes.TEXT)

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)

