import smart_email.fila_envio_assincrono as fila_mod

def test_envio_de_email_simulado(capsys):
    """
    Testa se a fila de envio executa corretamente e imprime as mensagens esperadas.
    """
    # Inicia o worker em segundo plano
    thread = fila_mod.iniciar_worker()

    # Adiciona uma tarefa de envio
    fila_mod.adicionar_tarefa_envio()

    # Aguarda o processamento da fila
    fila_mod.fila_envio.join()

    # Finaliza o worker
    fila_mod.finalizar_worker(thread)

    # Captura o que foi impresso no console
    captured = capsys.readouterr()

    # Verifica se a saída contém as mensagens esperadas
    assert "🚀 Executando tarefa de envio..." in captured.out
    assert "✅ Envio concluído." in captured.out
