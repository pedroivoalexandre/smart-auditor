import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import requests

load_dotenv()
MODO_DEBUG = os.getenv("MODO_DEBUG_VERIFICACAO", "false").lower() == "true"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
URL_MODELO_LOCAL = os.getenv("URL_MODELO_LOCAL")

def carregar_prompt():
    # Caminho seguro, relativo ao próprio arquivo .py
    caminho = os.path.join(os.path.dirname(__file__), "prompt_verificacao.txt")
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def extrair_texto_pdf(caminho_pdf):
    try:
        leitor = PdfReader(caminho_pdf)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto.strip()
    except Exception as e:
        return f"[ERRO] Falha ao extrair texto: {e}"

def substituir_variaveis_do_prompt(prompt, lista_verificacao, texto_extraido):
    return prompt.replace("{lista_verificacao}", lista_verificacao).replace("{texto_extraido}", texto_extraido)

def verificar_documento(caminho_pdf, lista_verificacao):
    if MODO_DEBUG:
        from modelo_debug import resposta_fake
        return resposta_fake(lista_verificacao, caminho_pdf)

    prompt = carregar_prompt()
    texto_doc = extrair_texto_pdf(caminho_pdf)

    # 🔍 Mostrar o conteúdo extraído do PDF para debug
    print("\n📝 Texto extraído do PDF:\n")
    print(texto_doc)

    prompt_completo = substituir_variaveis_do_prompt(prompt, lista_verificacao, texto_doc)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        # Modelo Gemini 2.5 Flash
        modelo = genai.GenerativeModel("gemini-1.5-flash")
        resposta = modelo.generate_content(prompt_completo)

        return {"status": "ok", "resposta": resposta.text}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

def verificar_e_retornar(path_pdf: str, lista_verificacao: str) -> dict:
    """
    Função de integração com o smart-core.
    Recebe o caminho do PDF e a lista de verificação (em string),
    e retorna um dicionário com o resultado da verificação.
    
    Exemplo de retorno:
    {
        "status": "ok",
        "resposta": "...texto em markdown..."
    }
    """
    return verificar_documento(path_pdf, lista_verificacao)
