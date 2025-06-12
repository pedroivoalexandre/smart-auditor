# smart_utils/anexos.py
import os
from datetime import datetime
from pathlib import Path

# Caminho padrão para salvar os arquivos
PASTA_SAIDA = "smart_documentos/temp/"

def salvar_anexos_pdf(nome_original: str, conteudo_bytes: bytes) -> str:
    """
    Salva o conteúdo de um único anexo PDF em disco, garantindo um nome de arquivo único.

    Args:
        nome_original (str): O nome original do arquivo anexo.
        conteudo_bytes (bytes): O conteúdo do arquivo em bytes.

    Returns:
        str: O caminho completo onde o arquivo foi salvo, ou None se ocorrer um erro.
    """
    try:
        # Garante que o diretório de saída exista
        Path(PASTA_SAIDA).mkdir(parents=True, exist_ok=True)

        # Cria um nome de arquivo seguro com timestamp para evitar sobrescrever arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_seguro = f"{timestamp}_{nome_original}"
        caminho_completo = os.path.join(PASTA_SAIDA, nome_seguro)

        # Salva o arquivo em modo de escrita binária ("wb")
        with open(caminho_completo, "wb") as f:
            f.write(conteudo_bytes)
        
        print(f"📎 Anexo salvo com sucesso em: {caminho_completo}")
        return caminho_completo

    except Exception as e:
        print(f"⚠️ Erro crítico ao tentar salvar o anexo '{nome_original}': {e}")
        return None
