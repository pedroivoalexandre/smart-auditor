import subprocess
import sys
import os
from datetime import datetime


def run_all_pytest_tests(subpasta: str = None):
    """
    Executa testes automatizados com pytest.
    Gera logs e relatório HTML na execução.
    """
    # Cria pastas de saída, se não existirem
    os.makedirs("logs", exist_ok=True)
    os.makedirs("relatorios", exist_ok=True)

    # Define nomes dos arquivos com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/testes_{timestamp}.log"
    html_path = f"relatorios/testes_{timestamp}.html"

    # Monta o comando
    comando = [
        sys.executable, "-m", "pytest", "-v",
        f"--html={html_path}",
        f"--self-contained-html"
    ]

    if subpasta:
        if not os.path.exists(subpasta):
            print(f"❌ Subpasta '{subpasta}' não encontrada.")
            sys.exit(1)
        comando.append(subpasta)
        print(f"🚀 Executando testes apenas em: {subpasta}\n")
    else:
        print("🚀 Executando TODOS os testes do projeto com pytest...\n")

    # Executa e salva saída no log
    with open(log_path, "w", encoding="utf-8") as log_file:
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_file.write(resultado.stdout)
        print("📋 Saída do pytest:\n")
        print(resultado.stdout)

    # Resultado final
    if resultado.returncode == 0:
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam. Veja os detalhes acima.")
        sys.exit(resultado.returncode)

    print(f"\n📝 Log salvo em: {log_path}")
    print(f"🌐 Relatório HTML em: {html_path}")


if __name__ == "__main__":
    subpasta = sys.argv[1] if len(sys.argv) > 1 else None
    run_all_pytest_tests(subpasta)
