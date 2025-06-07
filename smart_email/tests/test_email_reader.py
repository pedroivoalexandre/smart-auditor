import os
from unittest.mock import patch, mock_open
from enviar_email_pdf import enviar_email

@patch("builtins.open", new_callable=mock_open, read_data=b"PDF")
@patch("smtplib.SMTP_SSL")
def test_enviar_email_com_pdf(mock_smtp, mock_file):
    destinatario = "teste@exemplo.com"
    assunto = "Teste"
    corpo = "Este é um teste de envio."
    nome_pdf = "teste_envio.pdf"

    enviar_email(destinatario, assunto, corpo, nome_pdf)

    assert mock_file.called
    assert mock_smtp.called
