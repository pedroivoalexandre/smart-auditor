import os
import tempfile
from unittest.mock import patch, MagicMock
from smart_email.email_reader import enviar_para_fastapi

@patch("smart_email.email_reader.requests.post")
def test_enviar_para_fastapi(mock_post):
    # Simular a resposta da API
    mock_response = MagicMock()
    mock_response.json.return_value = {'relatorio': '✔️ Documento verificado com sucesso.'}
    mock_post.return_value = mock_response

    # Criar um arquivo temporário simulando um PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(b"%PDF-1.4 Simulacao de PDF")
        tmp_path = tmp.name

    try:
        lista_verificacao = "Fornecedor: Exemplo\nCNPJ: 00.000.000/0001-00"
        anexos = [tmp_path]

        # Executar a função com os mocks
        enviar_para_fastapi(lista_verificacao, anexos)

        # Verificações
        assert mock_post.called, "❌ A função requests.post não foi chamada."
        args, kwargs = mock_post.call_args
        assert 'files' in kwargs, "❌ Parâmetro 'files' não encontrado no POST."
        assert 'data' in kwargs, "❌ Parâmetro 'data' não encontrado no POST."
        assert kwargs['data']['lista_verificacao'] == lista_verificacao, "❌ Lista de verificação não foi enviada corretamente."
        print("✅ Teste de envio para FastAPI com mock executado com sucesso.")

    finally:
        os.remove(tmp_path)
