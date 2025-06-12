# smart_utils/logger.py

import os
from datetime import datetime

def registrar_log_execucao(titulo: str, conteudo_markdown: str, conteudo_texto: str):
    """
    Gera dois arquivos: um relatório em HTML e um log em texto puro.
    Os arquivos são salvos em 'relatorios/' e 'logs/' com um timestamp único.

    Args:
        titulo (str): O título a ser usado no cabeçalho do arquivo HTML.
        conteudo_markdown (str): O conteúdo principal em formato Markdown para o relatório.
        conteudo_texto (str): O conteúdo de texto puro para o arquivo de log.
    """
    try:
        # Garante que as pastas de saída existam
        os.makedirs("relatorios", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # Cria um timestamp único para os nomes dos arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define os caminhos dos arquivos de saída
        caminho_html = os.path.join("relatorios", f"relatorio_final_{timestamp}.html")
        caminho_log = os.path.join("logs", f"execucao_{timestamp}.log")

        # --- Cria e salva o relatório em HTML ---
        # Converte o Markdown de forma simples para HTML
        html_body = conteudo_markdown.replace("\n", "<br/>\n")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titulo}</title>
            <style>
                body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
                h3 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
            </style>
        </head>
        <body>
            <h1>{titulo}</h1>
            <p><strong>Gerado em:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <hr>
            {html_body}
        </body>
        </html>
        """
        with open(caminho_html, "w", encoding="utf-8") as f_html:
            f_html.write(html_content)

        # --- Cria e salva o log em texto puro ---
        with open(caminho_log, "w", encoding="utf-8") as f_txt:
            f_txt.write(f"--- {titulo} ---\n")
            f_txt.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f_txt.write("-------------------------------------\n\n")
            f_txt.write(conteudo_texto)

        print(f"📝 Relatório salvo com sucesso em: {caminho_html}")
        print(f"🗂️ Log de execução salvo com sucesso em: {caminho_log}")

    except Exception as e:
        print(f"⚠️ Falha crítica ao tentar salvar os arquivos de log/relatório: {e}")

