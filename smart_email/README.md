# 📬 smart-email

Subprojeto responsável por gerenciar **leitura e envio de e-mails** no sistema `smart-auditor-org`.

---

## ✅ Funcionalidades

- **📥 Leitura de e-mails recebidos** via Gmail API:
  - Filtra por assunto (`verificação`)
  - Extrai corpo do e-mail (lista de verificação)
  - Baixa anexos PDF e salva em `smart_documentos/temp/`

- **📤 Envio de e-mails**:
  - Gera PDF a partir de texto
  - Anexa e envia para um destinatário
  - Pode ser usado para responder relatórios processados

- **📂 Interface de integração** com o `smart-core`:
  - Prepara dados extraídos para consumo pela API `/verificar`
  - Simula fluxo real de entrada e saída de documentos

---

## ⚙️ Requisitos

Crie ou edite o arquivo `.env` na raiz com as variáveis:

```env
EMAIL_ORIGEM=seu_email@gmail.com
EMAIL_SENHA_APP=sua_senha_de_aplicativo
# 📬 smart_email

Subprojeto do sistema `smart-auditor-org`, responsável pela **leitura de e-mails com anexos**, **envio de relatórios por e-mail** e **comunicação com a API principal (FastAPI)**.

---

## 🎯 Objetivo

Automatizar o fluxo de comunicação por e-mail no sistema Smart Auditor, incluindo:

- 📥 Leitura de e-mails via Gmail API.
- 📎 Download e organização de anexos em PDF.
- 📤 Envio em lote de relatórios gerados.
- 🔄 Integração com FastAPI para registrar o envio.

---

## 📁 Estrutura

```
smart_email/
├── email_reader.py             # Lê e-mails com anexos via Gmail API
├── enviar_em_lote.py           # Envia múltiplos arquivos PDF em lote
├── enviar_email_pdf.py         # Função base de envio de e-mails com anexo
├── enviar_email_debug_021840.py# Versão auxiliar com logs adicionais
├── enviar_email_teste.py       # Envia requisição para API FastAPI
├── teste_envio_simples.py      # Exemplo de envio pontual
├── tests/
│   ├── test_email_reader.py
│   ├── test_enviar_email_pdf.py
│   └── test_enviar_para_fastapi.py
└── README.md                   # Este documento
```

---

## 🛠️ Dependências

- `smtplib`, `ssl`, `email`, `fpdf`
- `google-auth`, `google-api-python-client`
- `requests`, `python-dotenv`, `pytest`, `unittest.mock`

---

## 📦 Como usar

1. Configure as variáveis no `.env` (exemplo em `smart-config/.env.example`)
2. Execute `python smart_email/enviar_email_teste.py` para testes locais
3. Execute os testes com `pytest smart_email/tests/`

---

## 🔐 Arquivos Sensíveis

- Os arquivos abaixo devem ser protegidos (já listados no .gitignore):

```
smart-config/
├── credentials.json   # Credenciais do Gmail API
├── token.json         # Token de autenticação do Gmail
```

---

## ✅ Status do Subprojeto

- [x] Leitura e envio de e-mails funcionais
- [x] Envio em lote de documentos
- [x] Integração com FastAPI testada
- [x] Testes automatizados com `mock`
- [x] Documentação completa

---

© 2025 - Projeto Smart Auditor Org
