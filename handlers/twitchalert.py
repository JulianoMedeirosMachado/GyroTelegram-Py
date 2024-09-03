import aiohttp
from aiogram import types
from aiogram.dispatcher import Dispatcher
import asyncio
from config import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN
from .persistence import save_watched_channels, load_watched_channels

TWITCH_API_URL = 'https://api.twitch.tv/helix/streams'
CHECK_INTERVAL = 30

watched_channels = load_watched_channels()
channel_states = {channel: False for channel in watched_channels}


async def check_twitch_streams(bot):
    while True:
        async with aiohttp.ClientSession() as session:
            for channel_name, chat_ids in watched_channels.items():
                params = {
                    'user_login': channel_name
                }
                headers = {
                    'Client-ID': TWITCH_CLIENT_ID,
                    'Authorization': f'Bearer {TWITCH_ACCESS_TOKEN}'
                }
                async with session.get(TWITCH_API_URL, headers=headers, params=params) as response:
                    data = await response.json()

                    print("Resposta da API do Twitch:", data)

                    if 'data' not in data:
                        print("A chave 'data' não está presente na resposta.")
                        continue

                    is_live = False
                    if data['data']:
                        stream = data['data'][0]
                        if stream['type'] == 'live':
                            is_live = True

                    if is_live and not channel_states[channel_name]:
                        message = f"Atenção!!! {channel_name} está ao vivo! {stream['title']} - https://www.twitch.tv/{channel_name}"
                        for chat_id in chat_ids:
                            print(f"Sending message to chat {chat_id}: {message}")
                            await bot.send_message(chat_id, message)
                            chat = await bot.get_chat(chat_id)
                            print(f"Chat type: {chat.type}")
                            if chat.type in ('group', 'supergroup'):
                                title = chat.title
                                if title.startswith("[OFF]"):
                                    title = title.replace("[OFF]", "[ON]")
                                elif not title.startswith("[ON]"):
                                    title = f"[ON] {title}"
                                await bot.set_chat_title(chat_id, title)
                            else:
                                print("Not a group chat, skipping title update")
                                await bot.send_message(chat_id,
                                                       "Erro: O bot não pode setar o título em chats privados.")
                        channel_states[channel_name] = True
                    elif not is_live and channel_states[channel_name]:
                        for chat_id in chat_ids:
                            chat = await bot.get_chat(chat_id)
                            print(f"Chat type: {chat.type}")
                            if chat.type in ('group', 'supergroup'):
                                title = chat.title
                                if title.startswith("[ON]"):
                                    title = title.replace("[ON]", "[OFF]")
                                elif not title.startswith("[OFF]"):
                                    title = f"[OFF] {title}"
                                await bot.set_chat_title(chat_id, title)
                            else:
                                print("Not a group chat, skipping title update")
                                await bot.send_message(chat_id,
                                                       "Erro: O bot não pode setar o título em chats privados.")
                        channel_states[channel_name] = False

        await asyncio.sleep(CHECK_INTERVAL)

async def is_user_admin(chat_id, user_id, bot):
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ('administrator', 'creator')
    except Exception as e:
        print(f"Erro ao verificar status do usuário: {e}")
        return False

async def twitchalert_handler(message: types.Message):
    if message.chat.type == 'private' or (message.chat.type in ('group', 'supergroup') and await is_user_admin(message.chat.id, message.from_user.id, message.bot)):
        args = message.get_args()
        if not args:
            await message.reply("Por favor, forneça o nome do canal.")
            return
        
        channel_name = args.strip()
        chat_id = message.chat.id
        if channel_name not in watched_channels:
            watched_channels[channel_name] = set()
            channel_states[channel_name] = False  
        watched_channels[channel_name].add(chat_id)
        save_watched_channels(watched_channels) 
        await message.reply(f"Você agora está monitorando o canal {channel_name}. Iremos avisar quando ele estiver ao vivo.")
    else:
        await message.reply("Desculpe, você precisa ser um administrador para usar este comando em grupos.")

async def remove_twitchalert_handler(message: types.Message):
    if message.chat.type == 'private' or (message.chat.type in ('group', 'supergroup') and await is_user_admin(message.chat.id, message.from_user.id, message.bot)):
        args = message.get_args()
        if not args:
            await message.reply("Por favor, forneça o nome do canal.")
            return
        
        channel_name = args.strip()
        chat_id = message.chat.id
        if channel_name in watched_channels:
            if chat_id in watched_channels[channel_name]:
                watched_channels[channel_name].remove(chat_id)
                if not watched_channels[channel_name]:
                    del watched_channels[channel_name]
                    del channel_states[channel_name] 
                save_watched_channels(watched_channels) 
                await message.reply(f"Você não está mais monitorando o canal {channel_name}.")
            else:
                await message.reply(f"Você não está monitorando o canal {channel_name}.")
        else:
            await message.reply(f"Canal {channel_name} não encontrado.")
    else:
        await message.reply("Desculpe, você precisa ser um administrador para usar este comando em grupos.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(twitchalert_handler, commands=['twitchalert'])
    dp.register_message_handler(remove_twitchalert_handler, commands=['removetwitchalert'])
    loop = asyncio.get_event_loop()
    loop.create_task(check_twitch_streams(dp.bot))

