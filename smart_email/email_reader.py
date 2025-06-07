import os
import base64
from email import message_from_bytes, message_from_string, EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path
from typing import Tuple, List

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def buscar_emails(gmail_service, assunto_filtro="verificação"):
    resultados = gmail_service.users().messages().list(
        userId='me',
        q=f'subject:{assunto_filtro} has:attachment',
        maxResults=1
    ).execute()
    return resultados.get('messages', [])

def extrair_corpo_e_anexos(gmail_service, mensagem_id):
    mensagem = gmail_service.users().messages().get(userId='me', id=mensagem_id, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(mensagem['raw'].encode('UTF-8'))
    mime_msg = message_from_bytes(msg_raw)

    corpo = ""
    anexos = []

    for parte in mime_msg.walk():
        if parte.get_content_type() == 'text/plain':
            corpo += parte.get_payload(decode=True).decode(errors="ignore")
        elif parte.get_filename():
            filename = parte.get_filename()
            filepath = os.path.join('temp', filename)
            Path('temp').mkdir(exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(parte.get_payload(decode=True))
            anexos.append(filepath)

    return corpo.strip(), anexos

def ler_lista_verificacao_pdf(mensagem_id, gmail_service):
    lista_verificacao, _ = extrair_corpo_e_anexos(gmail_service, mensagem_id)
    return lista_verificacao

# Para testes com EmailMessage local
def extrair_corpo_e_anexos_de_email(mensagem: EmailMessage, pasta_destino: str) -> Tuple[str, List[str]]:
    corpo = ""
    anexos_salvos = []

    if mensagem.is_multipart():
        for parte in mensagem.walk():
            if parte.get_content_type() == "text/plain":
                corpo += parte.get_payload(decode=True).decode(errors="ignore")
            elif parte.get_filename():
                nome_arquivo = parte.get_filename()
                caminho = os.path.join(pasta_destino, nome_arquivo)
                with open(caminho, "wb") as f:
                    f.write(parte.get_payload(decode=True))
                anexos_salvos.append(caminho)
    else:
        corpo = mensagem.get_payload(decode=True).decode(errors="ignore")

    return corpo.strip(), anexos_salvos
