from aiogram import Dispatcher, types

async def help_handler(message: types.Message):
    help_text = (
        "<b>Comandos disponíveis:</b>\n\n"
        "<b>/ia</b> - Gera uma resposta baseada no texto fornecido após o comando.\n"
        "<b>/imgai</b> - Processa uma imagem enviada como resposta e gera uma descrição da imagem.\n"
        "<b>/resumo</b> - Gera um resumo das últimas 500 mensagens no chat atual.\n"
        "<b>/music [nome da música]</b> - Busca e envia uma música MP3 baseada no nome fornecido.\n"
        "<b>/figurinha</b> - Processa uma imagem enviada como resposta e gera uma figurinha da imagem.\n"
        "<b>/twitchalert [canal]</b> - Monitora o canal especificado e avisa quando o usuário fica online."
        "<b>/ajuda</b> - Exibe esta mensagem de ajuda.\n"

    )
    await message.answer(help_text, parse_mode='html')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(help_handler, commands=['ajuda'])

