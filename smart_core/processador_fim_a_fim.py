# processador_fim_a_fim.py
import os
import requests
import base64
import time
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64

# Inicializa variáveis de ambiente
load_dotenv()
EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")

# Pastas de trabalho
PASTA_PDFS = "pdfs_recebidos"
PASTA_RELATORIOS = "relatorios_gerados"
os.makedirs(PASTA_PDFS, exist_ok=True)
os.makedirs(PASTA_RELATORIOS, exist_ok=True)

# Carrega credenciais do Gmail
creds = Credentials.from_authorized_user_file("token.json")
service = build("gmail", "v1", credentials=creds)

# Função para buscar emails não processados
def buscar_emails():
    print("🔍 Buscando e-mails com anexos PDF...")
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="has:attachment filename:pdf").execute()
    messages = results.get("messages", [])
    return messages

# Função para baixar e salvar o PDF
def baixar_pdf(message_id):
    msg = service.users().messages().get(userId="me", id=message_id).execute()
    remetente = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')
    for part in msg['payload'].get('parts', []):
        if part['filename'].endswith(".pdf"):
            data = part['body'].get('data')
            if data:
                decoded_file = base64.urlsafe_b64decode(data)
                filename = os.path.join(PASTA_PDFS, f"{message_id}_{part['filename']}")
                with open(filename, "wb") as f:
                    f.write(decoded_file)
                print(f"📥 PDF salvo: {filename}")
                return filename, remetente
    return None, remetente

# Função para enviar o PDF para a API local
def verificar_documento(pdf_path):
    print(f"📨 Enviando {pdf_path} para API...")
    with open(pdf_path, "rb") as f:
        response = requests.post("http://localhost:8000/gerar", files={"file": f})
    if response.status_code == 200:
        nome_relatorio = os.path.basename(pdf_path).replace(".pdf", "_relatorio.txt")
        caminho = os.path.join(PASTA_RELATORIOS, nome_relatorio)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Relatório salvo: {caminho}")
        return caminho
    else:
        print("❌ Erro ao enviar para API.")
        return None

# Função para enviar relatório por e-mail
def enviar_relatorio(destinatario, relatorio_path):
    print(f"📧 Enviando relatório para {destinatario}...")
    import smtplib
    import ssl
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = destinatario
    msg['Subject'] = "📋 Relatório da Verificação - SmartAuditor"
    msg.attach(MIMEText("Segue relatório em anexo.", "plain"))

    with open(relatorio_path, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="txt")
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(relatorio_path))
        msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ORIGEM, EMAIL_SENHA_APP)
        server.send_message(msg)
        print("✅ Relatório enviado com sucesso!")

# Roda o fluxo completo
def processar_emails():
    mensagens = buscar_emails()
    for m in mensagens:
        try:
            pdf_path, remetente = baixar_pdf(m['id'])
            if pdf_path:
                relatorio_path = verificar_documento(pdf_path)
                if relatorio_path:
                    enviar_relatorio(remetente, relatorio_path)
        except Exception as e:
            print(f"⚠️ Erro no processamento: {e}")
        time.sleep(5)  # pequena pausa entre os envios

if __name__ == "__main__":
    print("🚀 Iniciando processamento fim a fim...")
    processar_emails()
