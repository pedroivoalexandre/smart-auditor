import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Lê do .env
EMAIL = os.getenv("EMAIL_ORIGEM")
SENHA = os.getenv("EMAIL_SENHA_APP")

# Validação básica
if not EMAIL or not SENHA:
    print("❌ Erro: EMAIL_ORIGEM ou EMAIL_SENHA_APP não encontrados no .env")
    exit(1)

# Monta o e-mail
msg = MIMEMultipart()
msg['From'] = EMAIL
msg['To'] = EMAIL
msg['Subject'] = "✅ Teste simples de envio"
msg.attach(MIMEText("Este é um teste de envio de e-mail SEM anexo via script Python.", 'plain'))

# Envia
try:
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(EMAIL, SENHA)
        server.send_message(msg)
    print("✅ E-mail enviado com sucesso!")
except Exception as e:
    print("❌ Falha no envio:", e)
