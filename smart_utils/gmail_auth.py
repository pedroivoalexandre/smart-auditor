# smart_utils/gmail_auth.py

import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Escopos exigidos para acessar Gmail e anexos
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Caminho para os arquivos de autenticação
CAMINHO_CREDENTIALS = os.getenv("CAMINHO_CREDENTIALS", "smart-config/credentials.json")
CAMINHO_TOKEN = os.getenv("CAMINHO_TOKEN", "smart-config/token.json")

def autenticar_gmail():
    """
    Autentica o acesso à API do Gmail usando OAuth2 e retorna um objeto de credenciais válido.
    O token de acesso é salvo em disco para reutilização futura.
    """
    creds = None

    # Verifica se já existe um token salvo
    if os.path.exists(CAMINHO_TOKEN):
        creds = Credentials.from_authorized_user_file(CAMINHO_TOKEN, SCOPES)

    # Se não houver token ou ele estiver inválido/expirado
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Inicia o fluxo de autenticação OAuth
            flow = InstalledAppFlow.from_client_secrets_file(CAMINHO_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva o token atualizado em disco
        with open(CAMINHO_TOKEN, "w") as token:
            token.write(creds.to_json())

    return creds
