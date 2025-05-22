import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ A chave não foi encontrada no .env")
    exit()

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("models/gemini-pro")
    response = model.generate_content("Explique o que é inteligência artificial.")
    print("✅ RESPOSTA DA IA:")
    print(response.text)
except Exception as e:
    print("❌ ERRO AO USAR O MODELO:")
    print(e)
