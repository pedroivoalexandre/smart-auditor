import smart_email.fila_envio_assincrono as fila_mod
import time

def test_envio_multiplo_com_fila(capsys):
    """
    Testa se múltiplas tarefas de envio são processadas na fila.
    """
    thread = fila_mod.iniciar_worker()

    fila_mod.adicionar_tarefa_envio("destinatario1@teste.com")
    fila_mod.adicionar_tarefa_envio("destinatario2@teste.com")

    # Aguarda processamento
    time.sleep(2)

    fila_mod.finalizar_worker(thread)

    captured = capsys.readouterr()
    assert "🚀 Executando tarefa de envio para: destinatario1@teste.com" in captured.out
    assert "🚀 Executando tarefa de envio para: destinatario2@teste.com" in captured.out
    assert "✅ Envio concluído para: destinatario1@teste.com" in captured.out
    assert "✅ Envio concluído para: destinatario2@teste.com" in captured.out
