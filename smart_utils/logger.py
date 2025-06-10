import os
from datetime import datetime


def registrar_log_execucao(conteudo_html: str, conteudo_texto: str):
    """
    Gera dois arquivos de log (HTML e TXT) com base no conteúdo fornecido.
    Os arquivos são salvos em 'logs/' com timestamp no nome.
    """
    # Garante que a pasta logs exista
    os.makedirs("logs", exist_ok=True)

    # Timestamp para nomear arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Caminhos dos arquivos de log
    caminho_html = os.path.join("logs", f"execucao_{timestamp}.html")
    caminho_txt = os.path.join("logs", f"execucao_{timestamp}.txt")

    # Salva HTML
    with open(caminho_html, "w", encoding="utf-8") as f_html:
        f_html.write(conteudo_html)

    # Salva texto puro
    with open(caminho_txt, "w", encoding="utf-8") as f_txt:
        f_txt.write(conteudo_texto)

    print(f"🗂️ Log salvo em: {caminho_html} e {caminho_txt}")
