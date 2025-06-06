import threading
import queue
import time
from smart_email.enviar_em_lote import enviar_em_lote

# Fila global para envio de emails
fila_envio = queue.Queue()

def worker_envio():
    while True:
        tarefa = fila_envio.get()
        if tarefa is None:
            print("🛑 Worker finalizado.")
            fila_envio.task_done()
            break
        try:
            print(f"🚀 Executando tarefa de envio para: {tarefa}")
            enviar_em_lote()
            print(f"✅ Envio concluído para: {tarefa}")
        except Exception as e:
            print(f"❌ Erro ao enviar para {tarefa}: {e}")
        finally:
            fila_envio.task_done()

def iniciar_worker():
    thread = threading.Thread(target=worker_envio, daemon=True)
    thread.start()
    return thread

def adicionar_tarefa_envio(destinatario: str):
    fila_envio.put(destinatario)

def finalizar_worker(thread):
    fila_envio.put(None)
    thread.join()
