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
