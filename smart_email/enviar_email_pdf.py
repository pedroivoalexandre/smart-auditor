import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def enviar_email_pdf(destinatarios: list[str], caminhos_pdfs: list[str], assunto: str, corpo: str) -> None:
    """
    Envia um e-mail com múltiplos arquivos PDF anexados.

    Parâmetros:
        destinatarios (list[str]): Lista de e-mails dos destinatários.
        caminhos_pdfs (list[str]): Lista de caminhos dos arquivos PDF a anexar.
        assunto (str): Assunto do e-mail.
        corpo (str): Corpo do e-mail.
    """

    email_remetente = os.getenv("EMAIL_ORIGEM")
    senha_app = os.getenv("EMAIL_SENHA_APP")

    if not email_remetente or not senha_app:
        raise ValueError("❌ Variáveis de ambiente EMAIL_ORIGEM ou EMAIL_SENHA_APP não configuradas.")

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = email_remetente
    msg["To"] = ", ".join(destinatarios)
    msg.set_content(corpo)

    for caminho_pdf in caminhos_pdfs:
        with open(caminho_pdf, "rb") as f:
            dados_pdf = f.read()
            nome_pdf = os.path.basename(caminho_pdf)
            msg.add_attachment(dados_pdf, maintype="application", subtype="pdf", filename=nome_pdf)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
        servidor.login(email_remetente, senha_app)
        servidor.send_message(msg)
        print("📧 E-mail enviado com sucesso!")
