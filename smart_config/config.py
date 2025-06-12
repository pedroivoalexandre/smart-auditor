# smart_config/config.py

import os

# --- Lógica Melhorada para Encontrar a Raiz do Projeto ---
# Isso garante que os caminhos sempre funcionem, não importa de onde o script é executado.
# __file__ é o caminho para este arquivo (config.py)
# os.path.dirname(__file__) é o caminho para a pasta /smart_config
# os.path.dirname(...) do resultado acima nos dá a raiz do projeto.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Escopos necessários para acessar o Gmail.
# Adicionei o escopo de envio para o futuro.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# --- Caminhos Corrigidos ---
# Agora os caminhos são construídos a partir da raiz do projeto.
PATH_CREDENTIALS = os.path.join(PROJECT_ROOT, "credentials.json")
PATH_TOKEN = os.path.join(PROJECT_ROOT, "token.json")