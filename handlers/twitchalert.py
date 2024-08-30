import aiohttp
from aiogram import types
from aiogram.dispatcher import Dispatcher
import asyncio
from config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
from persistence import save_watched_channels, load_watched_channels

TWITCH_API_URL = 'https://api.twitch.tv/helix/streams'
CHECK_INTERVAL = 60 

watched_channels = load_watched_channels()  # Carrega os dados ao iniciar

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

async def is_user_admin(chat_id, user_id, bot):
    chat_member = await bot.get_chat_member(chat_id, user_id)
    return chat_member.status in ('administrator', 'creator')

async def twitchalert_handler(message: types.Message):
    if not await is_user_admin(message.chat.id, message.from_user.id, message.bot):
        await message.reply("Desculpe, você precisa ser um administrador para usar este comando.")
        return

    args = message.get_args()
    if not args:
        await message.reply("Por favor, forneça o nome do canal.")
        return
    
    channel_name = args.strip()
    chat_id = message.chat.id
    if channel_name not in watched_channels:
        watched_channels[channel_name] = set()
    watched_channels[channel_name].add(chat_id)
    save_watched_channels(watched_channels)  # Salva os dados
    await message.reply(f"Você agora está monitorando o canal {channel_name}. Iremos avisar quando ele estiver ao vivo.")

async def remove_twitchalert_handler(message: types.Message):
    if not await is_user_admin(message.chat.id, message.from_user.id, message.bot):
        await message.reply("Desculpe, você precisa ser um administrador para usar este comando.")
        return

    args = message.get_args()
    if not args:
        await message.reply("Por favor, forneça o nome do canal.")
        return
    
    channel_name = args.strip()
    chat_id = message.chat.id
    if channel_name in watched_channels and chat_id in watched_channels[channel_name]:
        watched_channels[channel_name].remove(chat_id)
        if not watched_channels[channel_name]:
            del watched_channels[channel_name]
        save_watched_channels(watched_channels)  # Salva os dados
        await message.reply(f"Você não está mais monitorando o canal {channel_name}.")
    else:
        await message.reply(f"Você não está monitorando o canal {channel_name}.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(twitchalert_handler, commands=['twitchalert'])
    dp.register_message_handler(remove_twitchalert_handler, commands=['removetwitchalert'])
    loop = asyncio.get_event_loop()
    loop.create_task(check_twitch_streams(dp.bot))

