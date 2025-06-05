import os
import base64
import requests
from email import message_from_bytes
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path

# Escopo de acesso apenas à leitura do Gmail
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
    mensagens = resultados.get('messages', [])
    return mensagens

def extrair_corpo_e_anexos(gmail_service, mensagem_id):
    mensagem = gmail_service.users().messages().get(userId='me', id=mensagem_id, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(mensagem['raw'].encode('UTF-8'))
    mime_msg = message_from_bytes(msg_raw)
    lista_verificacao = mime_msg.get_payload()[0].get_payload(decode=True).decode('utf-8')
    anexos = []
    for parte in mime_msg.walk():
        if parte.get_content_maintype() == 'application' and parte.get_filename():
            filename = parte.get_filename()
            filepath = os.path.join('temp', filename)
            Path('temp').mkdir(exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(parte.get_payload(decode=True))
            anexos.append(filepath)
    return lista_verificacao, anexos

def enviar_para_fastapi(lista_verificacao, anexos):
    files = [('documentos', (Path(anexo).name, open(anexo, 'rb'), 'application/pdf')) for anexo in anexos]
    data = {'lista_verificacao': lista_verificacao}
    resposta = requests.post('http://127.0.0.1:8000/verificar', files=files, data=data)
    print("🧾 Relatório gerado:")
    print(resposta.json().get('relatorio'))

if __name__ == '__main__':
    service = autenticar_gmail()
    mensagens = buscar_emails(service)
    if not mensagens:
        print("❌ Nenhum e-mail com anexo encontrado.")
    else:
        mensagem_id = mensagens[0]['id']
        lista_verificacao, anexos = extrair_corpo_e_anexos(service, mensagem_id)
        enviar_para_fastapi(lista_verificacao, anexos)
