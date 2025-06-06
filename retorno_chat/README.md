Perfeito! Aqui está o conteúdo atualizado e estruturado para o arquivo `retorno_chat/README.md` com:

* Visão geral do projeto
* Estrutura de diretórios
* Instruções de execução
* Execução de testes automatizados
* Requisitos

---

### ✅ `retorno_chat/README.md`

```markdown
# 🧠 Smart Auditor

O **Smart Auditor** é um sistema modular para auditoria automatizada de documentos com apoio de IA. Ele processa e valida listas de verificação via e-mail, integrando-se a uma API de verificação (FastAPI + Gemini) e gera relatórios automaticamente.

---

## 📁 Estrutura do Projeto

```

smart\_auditor\_org/
├── retorno\_chat/              # Relatórios de progresso e documentação em Markdown
├── smart\_core/                # Processamento principal fim-a-fim
├── smart\_documentos/          # Documentos PDF usados para teste
│   └── temp/                  # Arquivos temporários
├── smart\_email/               # Leitura e envio de e-mails
│   └── tests/                 # Testes automatizados
├── smart\_utils/               # Utilitários e padrões de resposta
├── smart\_verificacao/         # Comunicação com API de verificação
├── pytest.ini                 # Configuração de testes
├── requirements.txt           # Dependências principais
├── requirements-doc.txt       # Dependências adicionais (doc, dev)
└── smart\_auditor\_org.code-workspace  # Arquivo do workspace VSCode

````

---

## 🚀 Como executar

1. **Clone o repositório**
```bash
git clone https://github.com/pedroivoalexandre/smart-auditor.git
cd smart-auditor
````

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate    # Linux/macOS
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure o acesso ao Gmail**

* Crie as credenciais (`credentials.json`) no Google Cloud Console.
* O arquivo `token.json` será criado automaticamente na primeira execução.

5. **Execute o sistema**

```bash
python smart_email/enviar_em_lote.py
```

---

## ✅ Como rodar os testes automatizados

```bash
$env:PYTHONPATH="."    # Windows
export PYTHONPATH="."  # Linux/macOS

pytest smart_email/tests/test_fila_envio.py -v
```

---

## 📦 Requisitos

* Python 3.10+
* `pip install -r requirements.txt`
* Credenciais OAuth 2.0 válidas para acesso ao Gmail (scopo `readonly`)
* FastAPI rodando localmente em `http://127.0.0.1:8000/verificar`

---

## ✍️ Créditos e licença

Desenvolvido por Pedro Ivo Alexandre como parte do projeto **Smart Auditor**
Licença: MIT (ou a definir)

---

```

Se quiser, posso salvar esse conteúdo automaticamente no arquivo `retorno_chat/README.md` e preparar o `git commit` para você. Deseja isso agora?
```
