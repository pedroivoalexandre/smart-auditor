import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv

# ====== ETAPA 1: Carregar variáveis de ambiente ======
print("🔄 Carregando variáveis do .env...")
load_dotenv()

EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")
DESTINATARIO = "smartauditor.teste@gmail.com"

if not EMAIL_ORIGEM or not EMAIL_SENHA_APP:
    print("❌ Erro: Variáveis de ambiente não carregadas corretamente.")
    exit(1)

print(f"✅ E-mail de origem: {EMAIL_ORIGEM}")

# ====== ETAPA 2: Conteúdo do corpo do e-mail ======
print("📝 Definindo corpo do e-mail...")
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

# ====== ETAPA 3: Gerar PDF ======
print("🧾 Gerando PDF de teste...")
nome_pdf = f"documento_teste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Este é um documento de teste gerado automaticamente.", ln=True, align='L')
pdf.multi_cell(0, 10, corpo_lista)
pdf.output(nome_pdf)
print(f"✅ PDF gerado: {nome_pdf}")

# ====== ETAPA 4: Montar e-mail ======
print("✉️ Montando o e-mail...")
msg = MIMEMultipart()
msg['From'] = EMAIL_ORIGEM
msg['To'] = DESTINATARIO
msg['Subject'] = "verificação - exemplo de teste"
msg.attach(MIMEText(corpo_lista, 'plain'))

with open(nome_pdf, 'rb') as f:
    anexo = MIMEApplication(f.read(), _subtype="pdf")
    anexo.add_header('Content-Disposition', 'attachment', filename=nome_pdf)
    msg.attach(anexo)

# ====== ETAPA 5: Enviar e-mail ======
print("📤 Conectando ao servidor SMTP...")

try:
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
        servidor.login(EMAIL_ORIGEM, EMAIL_SENHA_APP)
        servidor.send_message(msg)
    print("✅ E-mail enviado com sucesso!")
except smtplib.SMTPAuthenticationError:
    print("❌ Erro de autenticação SMTP. Verifique a senha de app.")
except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")
