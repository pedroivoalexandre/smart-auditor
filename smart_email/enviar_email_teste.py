from datetime import datetime
from enviar_email_pdf import enviar_email

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

    nome_arquivo_pdf = f"documento_teste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    destinatario = "smartauditor.teste@gmail.com"
    assunto = "verificação"

    enviar_email(destinatario, assunto, corpo_lista, nome_arquivo_pdf)
