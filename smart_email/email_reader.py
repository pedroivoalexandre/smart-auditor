# email_reader.py
import os
import base64
import traceback
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Importa as configurações centralizadas
from smart_config.config import PATH_TOKEN, PATH_CREDENTIALS, SCOPES
from smart_utils.anexos import salvar_anexos_pdf

def autenticar_gmail():
    """
    Autentica na API do Gmail de forma robusta.
    """
    creds = None
    if os.path.exists(PATH_TOKEN):
        creds = Credentials.from_authorized_user_file(PATH_TOKEN, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("INFO: Credenciais expiradas, atualizando o token...")
            creds.refresh(Request())
        else:
            print("INFO: Token não encontrado ou inválido. Iniciando novo fluxo de autenticação...")
            flow = InstalledAppFlow.from_client_secrets_file(PATH_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(PATH_TOKEN, "w") as token:
            token.write(creds.to_json())
            print(f"INFO: Token salvo em '{PATH_TOKEN}'")
            
    return build("gmail", "v1", credentials=creds)

def ler_emails_com_anexos():
    """
    Lê os e-mails, aplicando o filtro de assunto, e salva seus anexos.
    """
    print("📨 Iniciando leitura de e-mails (filtro: assunto contém 'verificação')...")
    
    try:
        service = autenticar_gmail()
        print("✅ Serviço Gmail autenticado com sucesso.")
    except Exception as e:
        print(f"❌ Erro fatal durante a autenticação: {e}")
        traceback.print_exc()
        return []

    try:
        query = 'subject:verificação has:attachment filename:pdf'
        result = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
        mensagens = result.get("messages", [])
    except HttpError as e:
        print(f"❌ Erro ao buscar mensagens na API do Gmail: {e}")
        return []

    if not mensagens:
        print("⚠️ Nenhum e-mail correspondente ao filtro foi encontrado.")
        return []

    print(f"📬 Total de e-mails encontrados: {len(mensagens)}")
    
    emails_processados = []

    for mensagem in mensagens:
        try:
            msg = service.users().messages().get(userId="me", id=mensagem["id"]).execute()
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])

            remetente = next((h["value"] for h in headers if h["name"] == "From"), "desconhecido")
            assunto = next((h["value"] for h in headers if h["name"] == "Subject"), "[sem assunto]")

            partes = payload.get("parts", [])
            anexos_salvos = []

            for parte in partes:
                filename = parte.get("filename")
                if not filename or not filename.lower().endswith(".pdf"):
                    continue

                body = parte.get("body", {})
                anexo_id = body.get("attachmentId")
                if not anexo_id:
                    continue

                anexo = service.users().messages().attachments().get(
                    userId="me", messageId=mensagem["id"], id=anexo_id
                ).execute()

                dados = anexo.get("data")
                if not dados:
                    continue

                conteudo_bytes = base64.urlsafe_b64decode(dados.encode("UTF-8"))
                
                # Chama a função para salvar o anexo
                caminho_salvo = salvar_anexos_pdf(filename, conteudo_bytes)
                
                # Adiciona à lista apenas se o arquivo foi salvo com sucesso
                if caminho_salvo:
                    anexos_salvos.append(caminho_salvo)

            if anexos_salvos:
                emails_processados.append({
                    "remetente": remetente,
                    "assunto": assunto,
                    "anexos": anexos_salvos
                })

        except Exception as e:
            print(f"⚠️ Erro inesperado ao processar o e-mail ID {mensagem.get('id', 'N/A')}: {e}")
            traceback.print_exc()

    return emails_processados
