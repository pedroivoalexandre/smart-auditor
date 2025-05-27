import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
EMAIL_ORIGEM = os.getenv("EMAIL_ORIGEM")
EMAIL_SENHA_APP = os.getenv("EMAIL_SENHA_APP")

# Configurações de envio
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 465
DESTINATARIO = EMAIL_ORIGEM  # Envia para ele mesmo
ASSUNTO = "verificação"

# Caminho da pasta com os conjuntos de teste
PASTA_CONJUNTOS = Path("Dados Analise")
if not PASTA_CONJUNTOS.exists():
    raise FileNotFoundError("❌ Pasta 'Dados Analise' não encontrada.")

# Lista todos os conjuntos
conjuntos = sorted([c for c in PASTA_CONJUNTOS.iterdir() if c.is_dir()])
print(f"📁 {len(conjuntos)} conjuntos encontrados para envio.")

# Função para enviar e-mail
def enviar_email(nome_conjunto, corpo_lista, anexos):
    print(f"✉️ Enviando e-mail: {nome_conjunto}")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = DESTINATARIO
    msg['Subject'] = f"{ASSUNTO} - {nome_conjunto}"
    msg.attach(MIMEText(corpo_lista, 'plain'))

    for anexo_path in anexos:
        print(f"📎 Anexando: {anexo_path.name}")
        with open(anexo_path, 'rb') as f:
            anexo = MIMEApplication(f.read(), _subtype="pdf")
            anexo.add_header('Content-Disposition', 'attachment', filename=anexo_path.name)
            msg.attach(anexo)

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVIDOR, SMTP_PORTA, context=contexto) as servidor:
        servidor.login(EMAIL_ORIGEM, EMAIL_SENHA_APP)
        servidor.send_message(msg)

    print(f"✅ E-mail enviado com sucesso para: {DESTINATARIO}\n")

# Loop para cada conjunto
for conjunto in conjuntos:
    print(f"📦 Processando conjunto: {conjunto.name}")

    # Localiza o PDF da lista de verificação
    lista_path = next(conjunto.glob("lista*.pdf"), None)
    if not lista_path:
        print(f"⚠️ Lista de verificação não encontrada em {conjunto.name}, pulando...\n")
        continue

    # Extrai o texto da lista de verificação
    try:
        import fitz  # PyMuPDF
        with fitz.open(lista_path) as doc:
            corpo_lista = "\n".join([p.get_text() for p in doc])
    except Exception as e:
        print(f"❌ Erro ao ler lista de verificação: {e}")
        continue

    # Coleta todos os PDFs do conjunto, exceto a lista
    anexos = [f for f in conjunto.glob("*.pdf") if f.name != lista_path.name]
    if not anexos:
        print(f"⚠️ Nenhum anexo encontrado para {conjunto.name}, pulando...\n")
        continue

    # Envia o e-mail
    try:
        enviar_email(conjunto.name, corpo_lista, anexos)
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail do conjunto {conjunto.name}: {e}")
