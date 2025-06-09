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

# ==== Função para autenticar e retornar o serviço do Gmail ====
def autenticar_gmail():
    """Autentica na API do Gmail usando OAuth2 e retorna o serviço autenticado."""
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    # Tenta carregar o token salvo
    if os.path.exists(CAMINHO_TOKEN):
        creds = Credentials.from_authorized_user_file(CAMINHO_TOKEN, SCOPES)

    # Caso não esteja válido, tenta renovar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError("❌ Token inválido ou ausente. Refaça a autenticação.")

    return build('gmail', 'v1', credentials=creds)

# ==== Função principal para ler e-mails ====
def ler_emails(service, remetente_filtro: str, assunto_filtro: str, max_emails: int = 5):
    """Lê os e-mails mais recentes do remetente com assunto especificado."""
    query = f'from:{remetente_filtro} subject:{assunto_filtro}'
    response = service.users().messages().list(userId='me', q=query, maxResults=max_emails).execute()
    mensagens = response.get('messages', [])

    emails = []

    for msg in mensagens:
        dados_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = dados_msg['payload']
        partes = payload.get('parts', [])
        anexos = []

        for parte in partes:
            filename = parte.get("filename")
            body = parte.get("body", {})
            if filename and 'data' in body:
                dados = base64.urlsafe_b64decode(body['data'])
                caminho = os.path.join("smart_documentos/temp", filename)
                with open(caminho, 'wb') as f:
                    f.write(dados)
                anexos.append(caminho)

        # Extrai corpo do e-mail
        corpo_email = ""
        if 'parts' in payload:
            for parte in payload['parts']:
                if parte['mimeType'] == 'text/plain':
                    corpo_email = base64.urlsafe_b64decode(parte['body']['data']).decode('utf-8')
                    break

        emails.append({"assunto": assunto_filtro, "corpo": corpo_email, "anexos": anexos})

    return emails

# ==== Função para enviar dados para a API principal (FastAPI) ====
def enviar_para_fastapi(lista_verificacao: str, anexos: list[str]) -> None:
    """
    Envia a lista de verificação e os documentos em anexo para a API /verificar da FastAPI.
    
    Parâmetros:
    - lista_verificacao: string com o conteúdo da lista.
    - anexos: lista de caminhos de arquivos PDF.
    """
    url = "http://localhost:8000/verificar"
    
    # Prepara os arquivos para upload
    files = [
        ('documentos', (os.path.basename(arquivo), open(arquivo, 'rb'), 'application/pdf'))
        for arquivo in anexos
    ]
    
    # Dados adicionais no corpo da requisição
    data = {'lista_verificacao': lista_verificacao}

    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        print("✅ Resposta da API:", response.json())
    except Exception as e:
        print("❌ Erro ao enviar para a API:", e)
    finally:
        # Garante o fechamento dos arquivos abertos
        for _, (nome, arquivo, _) in files:
            arquivo.close()
