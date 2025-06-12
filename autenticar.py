# autenticar.py

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

# --- Adiciona a raiz do projeto ao path do Python ---
# Isso garante que a linha 'from smart_config.config...' funcione corretamente.
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Agora podemos importar do nosso pacote de configuração
from smart_config.config import SCOPES, PATH_CREDENTIALS, PATH_TOKEN

print("INFO: Iniciando o fluxo de autenticação do Google.")
print(f"INFO: Usando o arquivo de credenciais em: {PATH_CREDENTIALS}")

# Verifica se o arquivo de credenciais existe antes de continuar
if not os.path.exists(PATH_CREDENTIALS):
    print(f"❌ ERRO FATAL: O arquivo 'credentials.json' não foi encontrado no caminho esperado.")
    print("Por favor, verifique se o arquivo está na pasta 'smart_config' e se o nome está correto.")
    sys.exit(1) # Encerra o script se o arquivo não for encontrado

# Inicia o fluxo para obter novas credenciais
flow = InstalledAppFlow.from_client_secrets_file(PATH_CREDENTIALS, SCOPES)
creds = flow.run_local_server(port=0)

# Salva o novo token no arquivo token.json
with open(PATH_TOKEN, "w") as token:
    token.write(creds.to_json())

print(f"\n✅ Novo token gerado com sucesso e salvo em: {PATH_TOKEN}")
