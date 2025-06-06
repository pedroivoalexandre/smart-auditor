import pytest
import asyncio
from unittest.mock import AsyncMock
import smart_email.fila_envio_assincrono as fila_mod

# ✅ Teste de envio de email com mock
@pytest.mark.asyncio
async def test_envio_de_email_simulado():
    # Mocka a função real de envio
    mock_enviar = AsyncMock()
    fila_mod.enviar_email_com_anexo = mock_enviar

    # Zera a fila antiga e cria uma nova para isolar o teste
    fila_mod.fila = asyncio.Queue()

    # Inicia apenas 1 worker para o teste (evita concorrência no mock)
    asyncio.create_task(fila_mod.worker_envio(id_worker=1))

    # Tarefa simulada
    tarefa = {
        'destinatario': 'teste@exemplo.com',
        'assunto': 'Assunto Teste',
        'corpo': 'Este é um teste.',
        'anexo': 'teste.pdf'
    }

    # Adiciona a tarefa à fila
    await fila_mod.fila.put(tarefa)

    # Aguarda o worker processar a tarefa
    await asyncio.sleep(1.5)

    # Verifica se o mock foi chamado exatamente com os dados esperados
    mock_enviar.assert_awaited_once_with(**tarefa)
