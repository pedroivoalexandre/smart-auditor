# Subprojeto `smart_verificacao`

Este submódulo é responsável por **verificar documentos recebidos** e gerar relatórios automáticos com base na lista de verificação enviada pelo usuário ou recebida via integração com o Gmail.

---

## 📁 Estrutura Atual

```bash
smart_verificacao/
├── verificador.py               # Função principal de verificação e geração de relatório
├── modelos.py                   # Pydantic models para entrada/saída da API
├── testes/
│   ├── teste_verificador.py     # Teste de funcionalidade principal
```

---

## 🧠 Lógica de Verificação

1. Recebe:

   * Lista de verificação (em texto)
   * Conjunto de documentos (PDFs)

2. Processa:

   * Usa `fitz` (PyMuPDF) para extrair texto dos PDFs
   * Verifica presença de cada item da lista de verificação nos PDFs

3. Retorna:

   * Relatório em dicionário: ✅ encontrados / ❌ não encontrados

## Exemplo Simplificado:

```python
resultado = verificar_documentos("item1\nitem2", ["doc1.pdf"])
print(resultado)
# {"item1": True, "item2": False}
```

---

## 🔬 Teste Automático

```python
from smart_verificacao.verificador import verificar_documentos

def test_verificador():
    resultado = verificar_documentos("assinatura\ncarimbo", ["exemplo.pdf"])
    assert isinstance(resultado, dict)
    assert "assinatura" in resultado
```

---

## Integração

* Endpoint `/verificar` da API FastAPI espera multipart/form:

  * `lista_verificacao` (str)
  * `documentos` (List\[UploadFile])

---

## Próximos Passos

* [ ] Melhorar extração de texto com OCR fallback
* [ ] Geração de relatório em PDF
* [ ] Integração com histórico em banco de dados
* [ ] Testes com dados variados
