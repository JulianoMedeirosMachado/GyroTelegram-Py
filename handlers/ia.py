import logging
from aiogram import Dispatcher, types
import google.generativeai as genai
from ..config import GOOGLE_API_KEY
import re

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def gemi_handler(message: types.Message):
    loading_message = None
    try:
        loading_message = await message.answer("<b>Gerando resposta por favor aguarde...</b>", parse_mode='html')

        if len(message.text.strip()) <= 5:
            await message.answer("<b>Nenhum texto ou pergunta muito pequena.</b>", parse_mode='html')
            return

        prompt = 'Você é um bot do telegram, por favor responda a seguinte mensagem: ' + ' '.join(message.text.split(maxsplit=1)[1:])
        response = model.generate_content(prompt)
        response_text = response.text

        # Escape special Markdown characters
        escaped_response_text = re.sub(r'([\.!*\-_~[\](){}])', r'\\\1', response_text)

        if len(escaped_response_text) > 4000:
            parts = [escaped_response_text[i:i+4000] for i in range(0, len(escaped_response_text), 4000)]
            for part in parts:
                await message.answer(part, parse_mode='markdown')
        else:
            await message.answer(escaped_response_text, parse_mode='markdown')

    except Exception as e:
        await message.answer(f"Ocorrreu um erro: {str(e)}")
    finally:
        if loading_message:
            await message.bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(gemi_handler, commands=['ia'])