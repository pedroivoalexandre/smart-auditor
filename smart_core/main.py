from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
import os
import fitz  # PyMuPDF

# Carrega variáveis do .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("❌ A chave da API do Gemini não foi encontrada no arquivo .env")

# Configura a API do Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Cria app FastAPI
app = FastAPI(title="smart-auditor", version="1.0")

# === ROTA /gerar ===
class PromptInput(BaseModel):
    prompt: str

@app.post("/gerar", summary="Gerar resposta do Gemini 2.5 Flash")
async def gerar_resposta(prompt_input: PromptInput):
    try:
        resposta = model.generate_content(prompt_input.prompt)
        return {"resposta": resposta.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === ROTA /verificar ===
@app.post("/verificar", summary="Verifica múltiplos PDFs com base em uma lista de verificação")
async def verificar_documento(
    documentos: list[UploadFile] = File(...),
    lista_verificacao: str = Form(...)
):
    try:
        texto_extraido = ""
        for doc in documentos:
            conteudo = await doc.read()
            texto_extraido += f"\n\n--- Documento: {doc.filename} ---\n"
            texto_extraido += extrair_texto_pdf(conteudo)

        prompt = carregar_prompt(lista_verificacao, texto_extraido)
        resposta = model.generate_content(prompt)
        return {"relatorio": resposta.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Função auxiliar: leitura de PDF ===
def extrair_texto_pdf(conteudo: bytes) -> str:
    texto = ""
    with fitz.open(stream=conteudo, filetype="pdf") as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

# === Função auxiliar: carregar o template do prompt ===
def carregar_prompt(lista_verificacao: str, texto_extraido: str) -> str:
    caminho = Path("smart_verificacao/prompt_verificacao.txt")
    if not caminho.exists():
        raise RuntimeError("❌ Arquivo prompt_verificacao.txt não encontrado.")
    template = caminho.read_text(encoding="utf-8")
    return template.format(
        lista_verificacao=lista_verificacao,
        texto_extraido=texto_extraido
    )

# === ROTA /status ===
@app.get("/status", summary="Verificar se a API está online")
def status():
    return {"status": "online", "modelo": "gemini-1.5-flash"}

# === Integração com fila assíncrona ===
from smart_email.fila_envio_assincrono import iniciar_worker, finalizar_worker, adicionar_tarefa_envio
import atexit

# Inicializa o worker de envio de email
worker_thread = iniciar_worker()
atexit.register(lambda: finalizar_worker(worker_thread))

# === ROTA /teste-envio ===
@app.post("/teste-envio", summary="Simula adição de tarefa de envio à fila")
def teste_envio():
    adicionar_tarefa_envio({
        "destinatario": "destinatario@teste.com",
        "assunto": "Assunto de Teste",
        "corpo": "Este é o corpo do e-mail.",
        "caminho_anexo": "arquivo.pdf"
    })
    return {"mensagem": "📬 Tarefa de envio adicionada à fila."}

# === NOVA ROTA /verificar-memoria ===
from smart_email.modelos import VerificacaoRequest
from smart_email.verificacao_memoria import processar_verificacao_em_memoria

@app.post("/verificar-memoria", summary="Verifica documentos em memória com base na lista de verificação")
def verificar_em_memoria(requisicao: VerificacaoRequest):
    try:
        relatorio = processar_verificacao_em_memoria(requisicao)
        return {"relatorio": relatorio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
