# test_funcao_core.py

"""
Este script simula o uso da função verificar_e_retornar()
como se fosse chamada pelo módulo smart-core.

Ele testa a integração completa da função pública do subprojeto smart_verificacao.
"""

from verificador import verificar_e_retornar

def main():
    # Caminho relativo ao diretório atual (smart_verificacao/)
    caminho = "../smart_documentos/temp/certificado.pdf"

    # Lista de verificação usada no exemplo de certificado
    checklist = """Nome da empresa certificada
Número do certificado
Data de emissão
Data de validade
Responsável técnico
Órgão certificador"""

    resultado = verificar_e_retornar(caminho, checklist)

    print("\n📋 Resultado via função verificar_e_retornar:\n")
    print(resultado["resposta"] if "resposta" in resultado else resultado)

if __name__ == "__main__":
    main()
