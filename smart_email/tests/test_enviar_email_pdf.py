import os
import sys
import tempfile
from unittest.mock import patch, mock_open, MagicMock

# Ajuste do path para permitir importar enviar_email_pdf corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enviar_email_pdf import enviar_email, gerar_pdf

@patch("builtins.open", new_callable=mock_open, read_data=b"PDF")
@patch("smtplib.SMTP_SSL")
def test_enviar_email_com_pdf(mock_smtp_ssl, mock_open_file):
    destinatario = "teste@exemplo.com"
    assunto = "Teste de envio"
    corpo = "Corpo do e-mail"
    nome_pdf = "teste_envio.pdf"

    enviar_email(destinatario, assunto, corpo, nome_pdf)

    # Validações básicas
    assert mock_smtp_ssl.called
    assert mock_open_file.called
    instancia_smtp = mock_smtp_ssl.return_value.__enter__.return_value
    instancia_smtp.login.assert_called_once()
    instancia_smtp.send_message.assert_called_once()

def test_gerar_pdf_cria_arquivo_temporario():
    corpo = "Conteúdo de teste para o PDF"
    with tempfile.TemporaryDirectory() as temp_dir:
        nome_pdf = os.path.join(temp_dir, "saida_teste.pdf")
        gerar_pdf(corpo, nome_pdf)
        assert os.path.exists(nome_pdf)
        assert os.path.getsize(nome_pdf) > 0
