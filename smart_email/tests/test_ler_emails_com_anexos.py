import pytest
from unittest.mock import patch, MagicMock
from smart_email.email_reader import ler_emails_com_anexos

@patch("smart_email.email_reader.autenticar_gmail")
@patch("smart_email.email_reader.open", create=True)
@patch("smart_email.email_reader.base64.urlsafe_b64decode")
def test_ler_emails_com_anexos(mock_b64, mock_open, mock_autenticar):
    """
    Teste da função ler_emails_com_anexos com mocks para evitar chamadas reais ao Gmail.
    Verifica se o retorno está na estrutura esperada para o smart_core.
    """

    # Simula conteúdo de um arquivo PDF decodificado
    mock_b64.return_value = b"PDF content"

    # Simula o serviço Gmail autenticado
    mock_service = MagicMock()
    mock_autenticar.return_value = mock_service

    # Simula a listagem de mensagens com um único e-mail
    mock_service.users().messages().list().execute.return_value = {
        "messages": [{"id": "abc123"}]
    }

    # Simula o conteúdo de um e-mail com um anexo PDF
    mock_service.users().messages().get().execute.return_value = {
        "payload": {
            "headers": [
                {"name": "From", "value": "teste@dominio.com"},
                {"name": "Subject", "value": "Teste de verificação"}
            ],
            "parts": [
                {
                    "filename": "arquivo.pdf",
                    "body": {"data": "dGVzdGU="}  # base64 simulado
                }
            ]
        },
        "snippet": "Texto do corpo do email."
    }

    # Executa o teste
    resultado = ler_emails_com_anexos()

    # Validações
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0]["remetente"] == "teste@dominio.com"
    assert resultado[0]["assunto"] == "Teste de verificação"
    assert "anexos_salvos" in resultado[0]
    assert isinstance(resultado[0]["anexos_salvos"], list)
