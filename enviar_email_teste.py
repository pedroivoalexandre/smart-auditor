import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from datetime import datetime

# ====== CONFIGURAÇÕES ======
smtp_servidor = "smtp.gmail.com"
smtp_porta = 465
usuario = "smartauditor.teste@gmail.com"
senha_app = "mwxm beji zkaj afzq"  # <- Substitua aqui

destinatario = "smartauditor.teste@gmail.com"
assunto = "verificação"
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

# ====== GERAR PDF DE TESTE ======
nome_pdf = f"documento_teste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Este é um documento de teste gerado automaticamente.", ln=True, align='L')
pdf.output(nome_pdf)

# ====== MONTAR E-MAIL ======
msg = MIMEMultipart()
msg['From'] = usuario
msg['To'] = destinatario
msg['Subject'] = assunto
msg.attach(MIMEText(corpo_lista, 'plain'))

with open(nome_pdf, 'rb') as f:
    anexo = MIMEApplication(f.read(), _subtype="pdf")
    anexo.add_header('Content-Disposition', 'attachment', filename=nome_pdf)
    msg.attach(anexo)

# ====== ENVIAR ======
contexto = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_servidor, smtp_porta, context=contexto) as servidor:
    servidor.login(usuario, senha_app)
    servidor.send_message(msg)

print("📧 E-mail de teste enviado com sucesso!")
