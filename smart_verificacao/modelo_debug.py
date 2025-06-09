
def resposta_fake(lista_verificacao, caminho_pdf):
    return {
        "status": "debug",
        "resposta": "\n".join([
            f"[OK] {item.strip()}: Simulado com sucesso" 
            for item in lista_verificacao.strip().split("\n") if item.strip()
        ])
    }
