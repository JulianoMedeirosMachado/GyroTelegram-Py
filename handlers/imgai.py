import logging
import io
import PIL.Image
from aiogram import Dispatcher, types
import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def generate_from_image(message: types.Message):
    if message.reply_to_message and message.reply_to_message.photo:
        image = message.reply_to_message.photo[-1]
        prompt = "Descreva esta imagem."

        processing_message = await message.answer("<b>Gerando resposta por favor aguarde...</b>", parse_mode='html')

        try:
            img_data = await message.bot.download_file_by_id(image.file_id)
            img = PIL.Image.open(io.BytesIO(img_data.getvalue()))

            response = model.generate_content([prompt, img])
            response_text = response.text

            await message.answer(response_text, parse_mode=None)
        except Exception as e:
            logging.error(f"Erro durante a análise da imagem: {e}")
            await message.answer("<b>Ocorreu um erro, por favor tente novamente</b>", parse_mode='html')
        finally:
            await message.bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
    else:
        await message.answer("<b>Use este comando em uma imagem por favor.</b>", parse_mode='html')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(generate_from_image, commands=['imgai'])
