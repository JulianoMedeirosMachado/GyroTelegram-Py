import json

FILE_PATH = 'watched_channels.json'

def save_watched_channels(watched_channels):
    # Converta o dicionário de sets para dicionário de listas para salvar
    watched_channels_serializable = {
        channel_name: list(chat_ids) for channel_name, chat_ids in watched_channels.items()
    }
    with open(FILE_PATH, 'w') as f:
        json.dump(watched_channels_serializable, f, indent=4)

def load_watched_channels():
    try:
        with open(FILE_PATH, 'r') as f:
            # Verifica se o arquivo está vazio
            if f.read(1):
                f.seek(0)  # Volta para o início do arquivo
                watched_channels = json.load(f)
                # Converte listas de volta para sets
                return {
                    channel_name: set(chat_ids) for channel_name, chat_ids in watched_channels.items()
                }
            else:
                # Retorna um dicionário vazio se o arquivo estiver vazio
                return {}
    except FileNotFoundError:
        # Retorna um dicionário vazio se o arquivo não for encontrado
        return {}
    except json.JSONDecodeError:
        # Retorna um dicionário vazio se houver um erro de decodificação JSON
        return {}

