# GyroTelegram-Py
 
**Gyro Bot** é um bot do Telegram desenvolvido em Python utilizando a biblioteca `aiogram`. Este bot oferece várias funcionalidades, como geração de resumos, busca de músicas, criação de figurinhas a partir de imagens, e muito mais.

## Funcionalidades

- **/ia [texto]**: Gera uma resposta baseada no texto fornecido após o comando utilizando a API da Google GEMINI.
- **/imgai [imagem]**: Processa uma imagem enviada como resposta e gera uma descrição da imagem.
- **/music [nome da música]**: Busca e envia uma música MP3 baseada no nome fornecido.
- **/resumo**: Gera um resumo das últimas 500 mensagens no chat atual.
- **/figurinha**: Processa uma imagem enviada como resposta e gera uma figurinha da imagem.
- **/ajuda**: Exibe a lista de comandos disponíveis.

## Requisitos

- Python 3.10
- Biblioteca `aiogram 2.25`
- Biblioteca `yt-dlp` para baixar músicas
- Conta de desenvolvedor Google com acesso à API GEMINI

## Configuração

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/usuario/gyro-bot.git
    cd gyro-bot
    ```

2. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configuração do arquivo `config.py`**:

    O arquivo `config.py` deve conter suas configurações pessoais, como o token do bot e a chave da API do Google GEMINI.

    ```python
    BOT_TOKEN = 'SEU_BOT_TOKEN_AQUI'
    GOOGLE_API_KEY = 'SUA_GOOGLE_API_KEY_AQUI'
    MAX_MESSAGES = 500  # Quantidade máxima de mensagens a serem armazenadas para o comando de resumo
    ```

4. **Inicie o bot**:

    ```bash
    python3 main.py
    ```

## Contribuição

Sinta-se à vontade para enviar pull requests ou abrir issues para discutir melhorias, bugs ou novas funcionalidades.
