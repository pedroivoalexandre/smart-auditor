# verificacao_em_lote.py

"""
Processa uma fila de documentos para verificação automática com Gemini.
Usa queue.Queue para simular múltiplos documentos sendo verificados.
"""

import queue
from verificador import verificar_e_retornar

def processar_fila(lista_documentos):
    """
    Recebe uma lista de tuplas (path_pdf, lista_verificacao) e processa em fila.
    """
    fila = queue.Queue()

    # Enfileirar documentos
    for doc in lista_documentos:
        fila.put(doc)

    resultados = []

    while not fila.empty():
        caminho_pdf, checklist = fila.get()
        print(f"\n📄 Verificando: {caminho_pdf}")
        resultado = verificar_e_retornar(caminho_pdf, checklist)
        resultados.append((caminho_pdf, resultado))
        fila.task_done()

    return resultados

if __name__ == "__main__":
    checklist_certificado = """Nome da empresa certificada
Número do certificado
Data de emissão
Data de validade
Responsável técnico
Órgão certificador"""

    documentos = [
        ("../smart_documentos/temp/certificado.pdf", checklist_certificado),
        ("../smart_documentos/temp/laudo.pdf", checklist_certificado),  # mesmo checklist por simplicidade
    ]

    saidas = processar_fila(documentos)

    for caminho, resultado in saidas:
        print(f"\n✅ Resultado para: {caminho}\n")
        print(resultado["resposta"] if "resposta" in resultado else resultado)
