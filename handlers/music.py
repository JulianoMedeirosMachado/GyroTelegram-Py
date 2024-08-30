import os
import logging
import asyncio
import yt_dlp
from aiogram import Dispatcher, types
from aiogram.types import InputFile

def fetch_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        if 'entries' in info:
            video = info['entries'][0]
            for ext in ['mp3', 'webm', 'm4a']:
                possible_file_path = f"downloads/{video['title']}.{ext}"
                if os.path.exists(possible_file_path):
                    return possible_file_path
            raise Exception("O arquivo MP3 não foi encontrado.")
        else:
            raise Exception("Não foi possível encontrar a música.")

async def delete_file_after_delay(file_path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Arquivo {file_path} excluído após {delay} segundos.")

async def music_handler(message: types.Message):
    try:
        query = ' '.join(message.text.split(maxsplit=1)[1:])
        if not query:
            await message.answer("<b>Por favor, forneça o nome da música.</b>", parse_mode='html')
            return

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        temp_message = await message.answer("🎵 Procurando e baixando sua música...")

        mp3_path = fetch_music(query)

        if os.path.exists(mp3_path):
            with open(mp3_path, 'rb') as mp3_file:
                await message.bot.send_audio(chat_id=message.chat.id, audio=InputFile(mp3_file, filename='music.mp3'))

            asyncio.create_task(delete_file_after_delay(mp3_path, 60))
        else:
            await message.answer("<b>Arquivo MP3 não encontrado.</b>", parse_mode='html')

        await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_message.message_id)

    except Exception as e:
        logging.error(f"Erro durante a busca ou envio da música: {e}")
        await message.answer("<b>Ocorreu um erro, por favor tente novamente</b>", parse_mode='html')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(music_handler, commands=['music'])

