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

# ====== FUNÇÃO PARA ENVIAR UM E-MAIL COM ANEXO PDF ======
def enviar_email(destinatario, assunto, corpo, nome_pdf=None):
    if not nome_pdf:
        nome_pdf = f"documento_teste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Gerar PDF com o conteúdo
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, corpo)
    pdf.output(nome_pdf)

    # Montar o e-mail
    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    with open(nome_pdf, 'rb') as f:
        anexo = MIMEApplication(f.read(), _subtype="pdf")
        anexo.add_header('Content-Disposition', 'attachment', filename=os.path.basename(nome_pdf))
        msg.attach(anexo)

    # Enviar e-mail
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_servidor, smtp_porta, context=contexto) as servidor:
        servidor.login(usuario, senha_app)
        servidor.send_message(msg)

    print(f"📧 E-mail enviado com sucesso para {destinatario} com anexo {nome_pdf}")

# ====== TESTE ISOLADO ======
if __name__ == "__main__":
    corpo_lista = """Fornecedor: CR Bluecast
CNPJ: 00.000.000/0001-91
Tipo de resíduo: Coprocessamento
Órgão emissor: SEMAD
Número da licença: 12345678
Validade da licença: 31/12/2025
Laudo: presente
Certificado do laboratório: válido
Validade do certificado: 30/11/2024
"""
    enviar_email("smartauditor.teste@gmail.com", "verificação", corpo_lista)
