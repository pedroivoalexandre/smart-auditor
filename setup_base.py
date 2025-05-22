from pathlib import Path

# Lista de arquivos e diretórios
arquivos = [
    "main.py",
    ".env.example",
    "requirements.txt",
    ".gitignore",
    "README.md"
]

# Conteúdo inicial opcional (todos vazios ou com instruções mínimas)
conteudos = {
    "main.py": "# ponto de entrada da API FastAPI\n",
    ".env.example": "GEMINI_API_KEY=sua-chave-aqui\n",
    "requirements.txt": "# Preencher com pip freeze > requirements.txt após instalar os pacotes\n",
    ".gitignore": "venv/\n.env\n__pycache__/\n",
    "README.md": "# Projeto smart-auditor\n\nAPI com FastAPI + Gemini 2.5 Flash para verificação inteligente de documentos."
}

# Criação dos arquivos
for nome in arquivos:
    caminho = Path(nome)
    if not caminho.exists():
        caminho.write_text(conteudos[nome])
        print(f"Arquivo criado: {nome}")
    else:
        print(f"Arquivo já existe: {nome}")
