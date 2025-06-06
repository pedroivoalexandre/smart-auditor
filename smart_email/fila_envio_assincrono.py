import asyncio
from smart_email.enviar_em_lote import enviar_em_lote

fila = asyncio.Queue()

async def worker_envio(id_worker):
    while True:
        tarefa = await fila.get()
        try:
            print(f"👷 Worker {id_worker} enviando: {tarefa['destinatario']}")
            await enviar_email_com_anexo(**tarefa)
        except Exception as e:
            print(f"❌ Erro no envio para {tarefa['destinatario']}: {e}")
        finally:
            fila.task_done()

async def adicionar_tarefa(destinatario, assunto, corpo, anexo):
    await fila.put({
        'destinatario': destinatario,
        'assunto': assunto,
        'corpo': corpo,
        'anexo': anexo
    })

async def iniciar_workers(n=3):
    for i in range(n):
        asyncio.create_task(worker_envio(i + 1))
