import aiohttp
from aiogram import types
from aiogram.dispatcher import Dispatcher
import asyncio
from config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

TWITCH_API_URL = 'https://api.twitch.tv/helix/streams'
CHECK_INTERVAL = 60  # Intervalo de verificação em segundos

# Armazena os canais a serem monitorados e seus respectivos chats
watched_channels = {}

async def check_twitch_streams(bot):
    while True:
        async with aiohttp.ClientSession() as session:
            for channel_name, chat_ids in watched_channels.items():
                params = {
                    'user_login': channel_name
                }
                headers = {
                    'Client-ID': TWITCH_CLIENT_ID,
                    'Authorization': f'Bearer {TWITCH_CLIENT_SECRET}'
                }
                async with session.get(TWITCH_API_URL, headers=headers, params=params) as response:
                    data = await response.json()
                    if data['data']:
                        stream = data['data'][0]
                        if stream['type'] == 'live':
                            message = f"Atenção!!! {channel_name} está ao vivo! {stream['title']} - https://www.twitch.tv/{channel_name}"
                            for chat_id in chat_ids:
                                await bot.send_message(chat_id, message)
        await asyncio.sleep(CHECK_INTERVAL)

async def twitchalert_handler(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Por favor, forneça o nome do canal.")
        return
    
    channel_name = args.strip()
    chat_id = message.chat.id
    if channel_name not in watched_channels:
        watched_channels[channel_name] = set()
    watched_channels[channel_name].add(chat_id)
    await message.reply(f"Você agora está monitorando o canal {channel_name}. Iremos avisar quando ele estiver ao vivo.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(twitchalert_handler, commands=['twitchalert'])
    loop = asyncio.get_event_loop()
    loop.create_task(check_twitch_streams(dp.bot))

