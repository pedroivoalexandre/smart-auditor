import base64
import requests
from pathlib import Path

# === CONFIGURAÇÕES ===
URL = "http://127.0.0.1:8000/verificar-memoria"
CAMINHOS_PDF = [
    "Dados Analise/V01/acordo.pdf",
    "Dados Analise/V01/laudo.pdf",
    "Dados Analise/V01/licenca.pdf"
]
LISTA_VERIFICACAO = """
1. Verifique se o CNPJ está presente e válido.
2. Confirme se há assinatura digital visível.
3. Certifique-se que o laudo possui validade.
"""

# === FUNÇÃO PARA CODIFICAR PDFs EM BASE64 ===
def carregar_pdfs_em_base64(caminhos):
    documentos_codificados = []
    for caminho in caminhos:
        with open(caminho, "rb") as f:
            conteudo = f.read()
            codificado = base64.b64encode(conteudo).decode("utf-8")
            documentos_codificados.append(codificado)
    return documentos_codificados

# === MONTAGEM DA REQUISIÇÃO ===
documentos_base64 = carregar_pdfs_em_base64(CAMINHOS_PDF)
payload = {
    "lista_verificacao": LISTA_VERIFICACAO.strip(),
    "documentos": documentos_base64
}

# === ENVIO ===
response = requests.post(URL, json=payload)

# === RESULTADO ===
print("Status:", response.status_code)
print("Resposta:")
print(response.json())
