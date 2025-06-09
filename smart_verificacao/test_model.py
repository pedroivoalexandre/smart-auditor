# test_model.py

"""
Este script realiza testes com o submódulo de verificação automática usando Gemini.
- Em modo DEBUG: simula respostas sem chamada real à IA.
- Em modo REAL: envia prompt completo para a IA e imprime resposta.

Necessário:
- Arquivo .env com a variável GEMINI_API_KEY
- PDF de teste em smart_documentos/temp/certificado.pdf
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from verificador import verificar_documento

# Carrega variáveis do .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
modo_debug = os.getenv("MODO_DEBUG_VERIFICACAO", "false").lower() == "true"

if not modo_debug and not api_key:
    print("❌ A chave GEMINI_API_KEY não foi encontrada no .env")
    exit()

if not modo_debug:
    # Configura Gemini somente se não estiver em modo debug
    genai.configure(api_key=api_key)

def teste_verificador():
    # Caminho do PDF corrigido (relativo à pasta atual smart_verificacao/)
    caminho_pdf = "../smart_documentos/temp/certificado.pdf"
    
    # Lista de verificação específica para o certificado
    lista_verificacao = """Nome da empresa certificada
Número do certificado
Data de emissão
Data de validade
Responsável técnico
Órgão certificador"""

    print("🚀 Iniciando verificação do documento...")
    resultado = verificar_documento(caminho_pdf, lista_verificacao)

    print("\n✅ Resultado da verificação:\n")
    print(resultado["resposta"] if "resposta" in resultado else resultado)

if __name__ == "__main__":
    teste_verificador()
