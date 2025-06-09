import pytest
import requests
from unittest.mock import patch
from smart_email.enviar_email_teste import enviar_para_fastapi


@patch("requests.post")
def test_enviar_para_fastapi_sucesso(mock_post):
    """
    Testa se a função enviar_para_fastapi retorna True quando a requisição é bem-sucedida.
    """
    mock_post.return_value.status_code = 200
    sucesso = enviar_para_fastapi("grupo-teste", "Este é um corpo de teste.")
    assert sucesso is True

@patch("requests.post")
def test_enviar_para_fastapi_falha(mock_post):
    """
    Testa se a função enviar_para_fastapi retorna False quando a requisição falha.
    """
    mock_post.return_value.status_code = 500
    sucesso = enviar_para_fastapi("grupo-teste", "Este é um corpo de teste.")
    assert sucesso is False

@patch("requests.post", side_effect=requests.exceptions.RequestException("Erro na conexão"))
def test_enviar_para_fastapi_excecao(mock_post):
    """
    Testa se a função enviar_para_fastapi lida corretamente com exceções de rede.
    """
    sucesso = enviar_para_fastapi("grupo-teste", "Este é um corpo de teste.")
    assert sucesso is False
