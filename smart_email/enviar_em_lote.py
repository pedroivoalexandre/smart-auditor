import os
from dotenv import load_dotenv
from smart_email.email_reader import ler_lista_verificacao_pdf

# Carregar variáveis de ambiente do .env
load_dotenv()

DIRETORIO_DADOS = os.getenv("DIRETORIO_DADOS", "smart_documentos")

def enviar_em_lote():
    print("📁 11 conjuntos encontrados para envio.")
    diretorios = os.listdir(DIRETORIO_DADOS)

    for nome_conjunto in diretorios:
        caminho = os.path.join(DIRETORIO_DADOS, nome_conjunto)

        if not os.path.isdir(caminho):
            continue

        print(f"📦 Processando conjunto: {nome_conjunto}")

        caminho_lista = os.path.join(caminho, "lista_verificacao_" + nome_conjunto.lower() + ".pdf")
        if not os.path.exists(caminho_lista):
            print(f"⚠️ Lista de verificação não encontrada em {nome_conjunto}, pulando...\n")
            continue

        try:
            dados = ler_lista_verificacao_pdf(caminho_lista)
            print(f"📨 Simulando envio de e-mail para {dados['email']} com {dados['arquivos']}")
        except Exception as e:
            print(f"❌ Erro ao ler lista de verificação: {e}")

# Para testes manuais
if __name__ == "__main__":
    enviar_em_lote()
