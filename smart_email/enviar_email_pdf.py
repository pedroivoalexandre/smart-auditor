import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv

# ====== CARREGAR VARIÁVEIS DE AMBIENTE ======
load_dotenv()
smtp_servidor = "smtp.gmail.com"
smtp_porta = 465
usuario = os.getenv("EMAIL_ORIGEM")
senha_app = os.getenv("EMAIL_SENHA_APP")

if not usuario or not senha_app:
    raise ValueError("❌ EMAIL_ORIGEM ou EMAIL_SENHA_APP não definidos no arquivo .env")

def gerar_pdf(corpo: str, nome_pdf: str) -> None:
    """Gera um PDF com o conteúdo especificado."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, corpo)
    pdf.output(nome_pdf)

def enviar_email(destinatario: str, assunto: str, corpo: str, nome_pdf: str) -> None:
    """Envia um e-mail com o corpo e anexo PDF gerado."""
    gerar_pdf(corpo, nome_pdf)

    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    with open(nome_pdf, 'rb') as f:
        anexo = MIMEApplication(f.read(), _subtype="pdf")
        anexo.add_header('Content-Disposition', 'attachment', filename=os.path.basename(nome_pdf))
        msg.attach(anexo)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_servidor, smtp_porta, context=contexto) as servidor:
        servidor.login(usuario, senha_app)
        servidor.send_message(msg)

    print(f"📧 E-mail enviado para {destinatario} com anexo {nome_pdf}")
