"""
📬 email_reader.py
Módulo responsável por:
- Autenticar na API Gmail
- Ler e-mails com ou sem filtros
- Extrair anexos PDF e salvar localmente
- Enviar anexos para API FastAPI (/verificar)
- Oferecer função genérica para uso do smart_core
"""

import os
import base64
import requests
from email import message_from_bytes
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==== Carrega variáveis de ambiente do .env ====
load_dotenv()
CAMINHO_CREDENCIAIS = os.getenv("CAMINHO_CREDENCIAIS", "smart-config/credentials.json")
CAMINHO_TOKEN = os.getenv("CAMINHO_TOKEN", "smart-config/token.json")
CAMINHO_TEMP = os.getenv("CAMINHO_TEMP", "smart_documentos/temp/")

# ==== Autenticação com a API do Gmail ====
def autenticar_gmail():
    """
    Autentica na API do Gmail usando OAuth2 e retorna o serviço autenticado.
    Necessário o arquivo token.json e as credenciais da conta.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists(CAMINHO_TOKEN):
        creds = Credentials.from_authorized_user_file(CAMINHO_TOKEN, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("❌ Token inválido ou ausente. Refaça a autenticação.")

    return build('gmail', 'v1', credentials=creds)

# ==== Leitura com filtros específicos (usada para testes isolados) ====
def ler_emails(service, remetente_filtro: str, assunto_filtro: str, max_emails: int = 5):
    """
    Lê os e-mails mais recentes do remetente com assunto especificado.
    Ideal para testes manuais com filtros bem definidos.
    """
    query = f'from:{remetente_filtro} subject:{assunto_filtro}'
    response = service.users().messages().list(userId='me', q=query, maxResults=max_emails).execute()
    mensagens = response.get('messages', [])

    emails = []

    for msg in mensagens:
        dados_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = dados_msg['payload']
        partes = payload.get('parts', [])
        anexos = []

        # Salva anexos PDF encontrados
        for parte in partes:
            filename = parte.get("filename")
            body = parte.get("body", {})
            if filename and 'data' in body:
                dados = base64.urlsafe_b64decode(body['data'])
                caminho = os.path.join(CAMINHO_TEMP, filename)
                with open(caminho, 'wb') as f:
                    f.write(dados)
                anexos.append(caminho)

        # Extrai texto do corpo do e-mail
        corpo_email = ""
        if 'parts' in payload:
            for parte in payload['parts']:
                if parte['mimeType'] == 'text/plain':
                    corpo_email = base64.urlsafe_b64decode(parte['body']['data']).decode('utf-8')
                    break

        emails.append({"assunto": assunto_filtro, "corpo": corpo_email, "anexos": anexos})

    return emails

# ==== Nova função: leitura genérica para smart_core ====
def ler_emails_com_anexos():
    """
    Versão compatível com smart_core:
    - Lê todos os e-mails da INBOX que contenham anexos PDF
    - Salva os arquivos em CAMINHO_TEMP
    - Retorna lista de dicionários com remetente, assunto, texto e anexos
    """
    print("📨 Lendo e-mails com anexos PDF...")
    service = autenticar_gmail()

    resultado = service.users().messages().list(
        userId="me", labelIds=["INBOX"], q="has:attachment filename:pdf"
    ).execute()
    mensagens = resultado.get("messages", [])

    saida = []

    for msg in mensagens:
        try:
            dados_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = dados_msg['payload']
            headers = payload.get('headers', [])

            # Extrai remetente e assunto
            remetente = next((h["value"] for h in headers if h["name"] == "From"), "[desconhecido]")
            assunto = next((h["value"] for h in headers if h["name"] == "Subject"), "[sem assunto]")
            mensagem_txt = dados_msg.get("snippet", "")
            anexos_salvos = []

            # Salva anexos PDF em CAMINHO_TEMP
            for parte in payload.get("parts", []):
                filename = parte.get("filename")
                body = parte.get("body", {})
                if filename and 'data' in body:
                    dados = base64.urlsafe_b64decode(body['data'])
                    caminho = os.path.join(CAMINHO_TEMP, f"{msg['id']}_{filename}")
                    with open(caminho, 'wb') as f:
                        f.write(dados)
                    anexos_salvos.append(caminho)

            if anexos_salvos:
                saida.append({
                    "remetente": remetente,
                    "assunto": assunto,
                    "mensagem": mensagem_txt,
                    "anexos_salvos": anexos_salvos
                })

        except Exception as e:
            print(f"⚠️ Erro ao processar e-mail: {e}")

    return saida

# ==== Integração externa: envia anexos para FastAPI ====
def enviar_para_fastapi(lista_verificacao: str, anexos: list[str]) -> None:
    """
    Envia a lista de verificação e os documentos em anexo para a API /verificar da FastAPI.
    Usado como cliente HTTP local.
    """
    url = "http://localhost:8000/verificar"

    # Prepara os arquivos como multipart/form-data
    files = [
        ('documentos', (os.path.basename(arquivo), open(arquivo, 'rb'), 'application/pdf'))
        for arquivo in anexos
    ]
    data = {'lista_verificacao': lista_verificacao}

    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        print("✅ Resposta da API:", response.json())
    except Exception as e:
        print("❌ Erro ao enviar para a API:", e)
    finally:
        for _, (nome, arquivo, _) in files:
            arquivo.close()
