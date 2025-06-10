import os
import base64
from datetime import datetime
from pathlib import Path

def salvar_anexos_pdf(parts, pasta_saida="smart_documentos/temp/"):
    """
    Salva arquivos PDF a partir das partes de um e-mail, que podem conter anexos codificados em base64.

    Args:
        parts (list): Lista de partes do e-mail, onde cada parte pode conter um anexo.
        pasta_saida (str): Caminho onde os PDFs devem ser salvos.

    Returns:
        list: Lista com os caminhos completos dos arquivos PDF salvos.
    """
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    arquivos_salvos = []

    for idx, part in enumerate(parts):
        filename = part.get("filename")
        body = part.get("body", {})
        data = body.get("data")

        # Verifica se é um arquivo PDF
        if filename and filename.lower().endswith(".pdf") and data:
            try:
                conteudo = base64.urlsafe_b64decode(data)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                nome_seguro = f"{timestamp}_{idx}_{filename}"
                caminho_completo = os.path.join(pasta_saida, nome_seguro)

                with open(caminho_completo, "wb") as f:
                    f.write(conteudo)

                arquivos_salvos.append(caminho_completo)
                print(f"📎 PDF salvo: {caminho_completo}")

            except Exception as e:
                print(f"⚠️ Erro ao salvar anexo {filename}: {e}")

    return arquivos_salvos
