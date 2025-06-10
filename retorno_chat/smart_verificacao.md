# Contexto para retorno ao chat principal – smart-verificacao

Este subprojeto lida com os modelos de verificação e testes baseados em IA, sendo responsável por:
- Extrair texto de PDFs
- Gerar prompts com base em uma lista de verificação
- Chamar a API Gemini 2.5 Flash
- Retornar relatórios estruturados para uso no sistema principal

---

## ✅ Funcionalidades Implementadas

- [x] Integração com Gemini 2.5 Flash (`gemini-1.5-flash`)
- [x] Modo debug com respostas simuladas
- [x] Extração de texto com PyPDF2
- [x] Substituição dinâmica no prompt
- [x] Impressão do texto extraído para debug
- [x] Função pública `verificar_e_retornar()`
- [x] Teste individual com `test_model.py`
- [x] Teste com `test_funcao_core.py`
- [x] Verificação em lote com `queue.Queue`

---

## 📂 Arquivos do Subprojeto

- `verificador.py` – Contém `verificar_documento()` e `verificar_e_retornar()`
- `modelo_debug.py` – Modo simulado para testes locais
- `test_model.py` – Testes com mock
- `test_funcao_core.py` – Integração com comportamento da API
- `verificacao_em_lote.py` – Suporte a múltiplos arquivos usando fila
- `prompt_verificacao.txt` – Modelo de lista de verificação

---

## 🔜 Pendências

- [ ] Integração direta com `smart-core` (chamada pela API FastAPI)
- [ ] Retorno automático para `smart-email` (após resposta do Gemini)
- [ ] Suporte a OCR (documentos com imagem scanneada)

---

## 📥 Entrada esperada

- PDF com texto legível, armazenado em `smart-documentos/temp/`
- Lista de verificação (string padrão no `prompt_verificacao.txt`)

## 📤 Saída esperada

- Markdown estruturado por item verificado
- JSON contendo status e mensagem do processo

---

## 🧪 Testes Realizados

- `certificado.pdf`: texto extraído corretamente, resposta do Gemini válida
- `laudo.pdf`: texto extraído corretamente, resultado coerente

---

## 📌 Observações para Integração

- A função `verificar_e_retornar()` está pronta para ser chamada por FastAPI (`smart-core`)
- Todo resultado é retornado em JSON ou Markdown para facilitar uso em interface ou e-mail
- A fila de verificação por `queue.Queue` suporta múltiplos arquivos em paralelo

---

🟩 Status do subprojeto `smart-verificacao`: **FINALIZADO (exceto integração)**  
🕐 Próximo passo: **ligação com `smart-core` via rota `/verificar`**
