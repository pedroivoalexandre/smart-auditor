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
            break
        try:
            print("🚀 Executando tarefa de envio...")
            enviar_em_lote()
            print("✅ Envio concluído.")
        except Exception as e:
            print(f"❌ Erro ao enviar: {e}")
        finally:
            fila_envio.task_done()

def iniciar_worker():
    thread = threading.Thread(target=worker_envio, daemon=True)
    thread.start()
    return thread

def adicionar_tarefa_envio():
    fila_envio.put("enviar")

def finalizar_worker(thread):
    fila_envio.put(None)
    thread.join()
