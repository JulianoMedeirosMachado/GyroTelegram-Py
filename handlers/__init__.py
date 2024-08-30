from .ia import register_handlers as register_ia_handlers
from .imgai import register_handlers as register_imgai_handlers
from .music import register_handlers as register_music_handlers
from .help import register_handlers as register_help_handlers
from .resumo import register_resumo_handler
from .sticker import register_handlers as register_sticker_handlers
from .createyourownbot import register_handlers as register_createyourownbot_handlers
from .twitchalert import register_handlers as register_twitchalert_handlers

__all__ = [
    'register_ia_handlers',
    'register_imgai_handlers',
    'register_music_handlers',
    'register_help_handlers',
    'register_resumo_handler',
    'register_sticker_handlers',
    'register_createyourownbot_handlers',
    'register_twitchalert_handlers'
]

def register_all_handlers(dp, message_store):
    register_ia_handlers(dp)
    register_imgai_handlers(dp)
    register_music_handlers(dp)
    register_help_handlers(dp)
    register_resumo_handler(dp, message_store)
    register_sticker_handlers(dp)
    register_createyourownbot_handlers(dp)
    register_twitchalert_handlers(dp)

print("Handlers package initialized")

