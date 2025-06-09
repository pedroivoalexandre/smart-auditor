# ✅ Subprojeto: smart-email (Finalizado)

Este subprojeto faz parte da arquitetura modular do sistema `smart-auditor-org`. Sua responsabilidade é realizar a **leitura de e-mails com anexos** (via Gmail API), o **envio de relatórios em PDF**, e a **integração com a API FastAPI** para encaminhar os resultados.

---

## 📦 Estrutura de Arquivos

- `email_reader.py` – Lê e-mails com anexos e salva arquivos na pasta `smart-documentos/temp/`
- `enviar_email_pdf.py` – Envia um ou mais PDFs por e-mail com controle de anexos e logging
- `enviar_email_teste.py` – Contém a função `enviar_para_fastapi()` para integração com a API FastAPI
- `tests/` – Testes automatizados com `pytest` e `mock`

---

## ✅ Funcionalidades Entregues

- [x] Leitura de e-mails via Gmail API com salvamento estruturado
- [x] Envio de PDFs em lote por e-mail com tratamento de erros
- [x] Integração com FastAPI (`/verificar`) via função `enviar_para_fastapi`
- [x] Logs com `try/except` e mensagens de sucesso/erro
- [x] Docstrings em todas as funções principais
- [x] Testes automatizados para todos os fluxos
- [x] Organização modular e uso de variáveis do `.env`

---

## 🧪 Testes Automatizados

- `test_email_reader.py`
- `test_enviar_email_pdf.py`
- `test_enviar_para_fastapi.py`

Testes simulam:
- Falha de envio
- Sucesso no envio
- Exceções de rede
- Manipulação de múltiplos anexos

---

## 🔄 Integrações

- 📥 Recebe documentos de `smart-documentos/`
- 📤 Integra com `smart-verificacao` via requisição HTTP
- 🧠 Será coordenado por `smart-core` (a ser implementado)

---

## 🔚 Status Final

🟩 Subprojeto `smart-email`: **FINALIZADO**  
🕐 Última tarefa: testes finais e docstrings + sucesso na execução

---

## 📅 Histórico

- Etapa 1: leitura de e-mails – ✅
- Etapa 2: envio de PDF – ✅
- Etapa 3: integração FastAPI – ✅
- Etapa 4: testes finais – ✅
