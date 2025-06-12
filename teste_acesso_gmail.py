import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopo da permissão: Apenas leitura de e-mails.
# Se seu token.json original foi criado com mais permissões, não há problema.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Caminhos para os arquivos de configuração, baseados na sua estrutura de pastas.
# Este script deve ser executado da pasta raiz do projeto.
PATH_CREDENTIALS = os.path.join('smart-config', 'credentials.json')
PATH_TOKEN = os.path.join('smart-config', 'token.json')

def main():
    """
    Função principal que autentica na API do Gmail e lista os assuntos
    dos últimos 25 e-mails.
    """
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário.
    # Ele é criado automaticamente na primeira vez que o fluxo de autorização é concluído.
    if os.path.exists(PATH_TOKEN):
        print(f"INFO: Encontrado arquivo de token em '{PATH_TOKEN}'. Tentando usar...")
        try:
            creds = Credentials.from_authorized_user_file(PATH_TOKEN, SCOPES)
        except Exception as e:
            print(f"AVISO: Não foi possível carregar o token.json. Erro: {e}")
            creds = None

    # Se não houver credenciais (válidas), deixe o usuário fazer o login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("INFO: Credenciais expiradas. Tentando atualizar o token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"ERRO: Falha ao atualizar o token: {e}")
                print(">>> Por favor, execute o passo de autenticação manual.")
                creds = None # Força a re-autenticação
        else:
            print("INFO: Credenciais não encontradas ou inválidas. Iniciando fluxo de autenticação...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(PATH_CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"ERRO FATAL: Falha ao iniciar o fluxo de autenticação com '{PATH_CREDENTIALS}'.")
                print(f"Verifique se o caminho está correto e se o arquivo não está corrompido. Erro: {e}")
                return

        # Salve as credenciais para a próxima execução
        try:
            with open(PATH_TOKEN, "w") as token_file:
                token_file.write(creds.to_json())
            print(f"INFO: Token salvo com sucesso em '{PATH_TOKEN}'.")
        except Exception as e:
            print(f"ERRO: Falha ao salvar o novo token. Erro: {e}")


    try:
        # Constrói o serviço da API do Gmail
        print("\nINFO: Construindo o serviço da API do Gmail...")
        service = build("gmail", "v1", credentials=creds)

        # Chama a API para listar as mensagens
        results = service.users().messages().list(userId="me", maxResults=25).execute()
        messages = results.get("messages", [])

        if not messages:
            print("Nenhum e-mail encontrado na sua caixa de entrada.")
            return

        print("\n--- Assuntos dos Últimos E-mails ---")
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"], format='metadata', metadataHeaders=['Subject']).execute()
            payload = msg.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            print(f"- {subject}")
        
        print("\n--- Teste concluído com sucesso! ---")

    except HttpError as error:
        print(f"Ocorreu um erro na chamada da API: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()