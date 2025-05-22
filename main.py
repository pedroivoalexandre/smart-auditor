from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém a chave da API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("❌ A chave da API do Gemini não foi encontrada no arquivo .env")

# Configura a biblioteca Gemini
genai.configure(api_key=api_key)

# Usa o modelo Gemini 2.5 Flash
model = genai.GenerativeModel("gemini-1.5-flash")

# Instancia a aplicação FastAPI
app = FastAPI(title="smart-auditor", version="1.0")

# Modelo de entrada da API
class PromptInput(BaseModel):
    prompt: str

# Rota principal para gerar respostas com IA
@app.post("/gerar", summary="Gerar resposta do Gemini 2.5 Flash")
async def gerar_resposta(prompt_input: PromptInput):
    try:
        resposta = model.generate_content(prompt_input.prompt)
        return {"resposta": resposta.text}
    except Exception as e:
        print("❌ Erro ao gerar resposta:", e)
        raise HTTPException(status_code=500, detail=str(e))

# Rota opcional de status para verificar se a API está viva
@app.get("/status", summary="Verificar status da API")
async def status():
    return {"status": "online", "modelo": "gemini-1.5-flash"}
