# smart_email/email_reader.py

import base64
import os
import re
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from email import message_from_bytes
from smart_utils.gmail_auth import autenticar_gmail
from smart_utils.anexos import salvar_anexos_pdf


def ler_emails_com_anexos(pasta_destino="smart_documentos/temp"):
    print("📨 Lendo e-mails com anexos PDF...")

    # Autentica e cria o serviço
    service = autenticar_gmail()

    mensagens = []
    pagina = None

    while True:
        resposta = service.users().messages().list(
            userId='me',
            pageToken=pagina
        ).execute()

        mensagens.extend(resposta.get('messages', []))
        pagina = resposta.get('nextPageToken')
        if not pagina:
            break

    if not mensagens:
        print("⚠️ Nenhum e-mail encontrado.")
        return []

    emails_processados = []

    for msg in mensagens:
        try:
            email = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = email['payload'].get('headers', [])
            assunto = next((h['value'] for h in headers if h['name'] == 'Subject'), "(sem assunto)")
            remetente = next((h['value'] for h in headers if h['name'] == 'From'), "(desconhecido)")

            partes = email['payload'].get('parts', [])
            arquivos_salvos = salvar_anexos_pdf(partes, pasta_destino)

            lista_verificacao = ""
            try:
                for part in partes:
                    if part.get('mimeType') == 'text/plain':
                        corpo_bytes = base64.urlsafe_b64decode(part['body']['data'])
                        corpo = corpo_bytes.decode("utf-8")
                        lista_verificacao = corpo.strip().replace("\r\n", " ")
                        break
            except Exception:
                lista_verificacao = "[ERRO ao extrair lista]"

            emails_processados.append({
                "remetente": remetente,
                "assunto": assunto,
                "lista_verificacao": lista_verificacao,
                "anexos": arquivos_salvos
            })

            print(f"\n📧 E-mail de: {remetente}")
            print(f"🔖 Assunto: {assunto}")
            print(f"📄 Lista usada: {lista_verificacao}")
            print(f"📎 {len(arquivos_salvos)} anexos encontrados")

        except Exception as e:
            print(f"❌ Erro ao processar e-mail: {e}")

    return emails_processados
