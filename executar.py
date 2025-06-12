# executar.py (na raiz do projeto)
import sys
import os

# Garante que a raiz do projeto esteja no sys.path para que os imports funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_core.processador_fim_a_fim import processar_fluxo

if __name__ == "__main__":
    print("🚀 Executando processador fim a fim...")

    # Define o CONTEÚDO da lista de verificação aqui.
    # Isto resolve o problema da IA não saber o que verificar.
    lista_de_verificacao_real = """
    - Nome do fornecedor
    - CNPJ do fornecedor
    - Número da Licença de Operação
    - Validade da Licença de Operação
    - Nome do órgão emissor da licença
    - Tipo ou nome do resíduo analisado
    - Nome do laboratório responsável pelo laudo
    - Data do laudo
    - Assinatura ou identificação do responsável técnico
    - Número ou código do certificado do laboratório
    - Validade do certificado do laboratório
    """

    # Chama o fluxo principal passando o CONTEÚDO da lista.
    processar_fluxo(lista_verificacao=lista_de_verificacao_real)
