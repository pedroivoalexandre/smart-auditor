import os
import traceback
from dotenv import load_dotenv
from pathlib import Path

# Módulos do sistema
from smart_email.email_reader import ler_emails_com_anexos
from smart_email.enviar_email_pdf import enviar_email_pdf
from smart_verificacao.verificador import verificar_e_retornar
from smart_utils.logger import registrar_log_execucao

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Ambiente
load_dotenv()
CAMINHO_TEMP = os.getenv("CAMINHO_TEMP", "smart_documentos/temp/")

def gerar_pdf_resposta(texto: str, caminho_saida: str):
    """Gera PDF a partir do texto da IA."""
    c = canvas.Canvas(caminho_saida, pagesize=A4)
    largura, altura = A4
    y = altura - 50
    # Remove marcações de markdown que não são bem renderizadas no PDF simples
    texto_formatado = texto.replace('```markdown', '').replace('```', '').strip()
    for linha in texto_formatado.split("\n"):
        c.drawString(50, y, linha[:100])
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50
    c.save()

def processar_fluxo(lista_verificacao: str):
    print("📥 Iniciando leitura de e-mails...")
    
    emails = ler_emails_com_anexos()

    if not emails:
        print("✅ Fluxo finalizado. Nenhum e-mail para processar.")
        return

    relatorio_md = []
    relatorio_txt = []
    total_respostas = 0

    for email in emails:
        remetente = email["remetente"]
        assunto = email.get("assunto", "[sem assunto]")
        anexos = email["anexos"]
        respostas = []

        print(f"\n📧 Processando: {remetente} | {len(anexos)} anexo(s)")

        for caminho_pdf in anexos:
            try:
                print(f"🔍 Verificando documento: {caminho_pdf}")
                resultado = verificar_e_retornar(caminho_pdf, lista_verificacao)
                
                print(f"🧠 Resultado bruto da IA:\n{resultado}\n")

                if resultado.get("status") == "ok" and resultado.get("resposta"):
                    resposta_md = resultado["resposta"]
                    nome_base = Path(caminho_pdf).stem
                    nome_saida = os.path.join(CAMINHO_TEMP, f"{nome_base}_verificado.pdf")
                    gerar_pdf_resposta(resposta_md, nome_saida)
                    print(f"✅ Resultado salvo em: {nome_saida}")
                    respostas.append(nome_saida)
                else:
                    msg_erro = resultado.get('mensagem', 'resultado não possui a chave "resposta"')
                    print(f"❌ Erro na verificação do {caminho_pdf}: {msg_erro}")

            except Exception as e:
                print(f"❌ Erro crítico ao processar {caminho_pdf}: {e}")
                traceback.print_exc()

        if respostas:
            try:
                print(f"📤 Enviando resposta para {remetente}...")
                assunto_resp = f"[Verificação] Resultado para: {assunto}"
                corpo_email = "Olá!\n\nSegue em anexo o resultado da verificação dos documentos enviados."
                
                enviar_email_pdf(
                    destinatarios=[remetente],
                    caminhos_pdfs=respostas,
                    assunto=assunto_resp,
                    corpo=corpo_email
                )
            except Exception as e:
                print(f"❌ Falha ao enviar e-mail: {e}")
                traceback.print_exc()

        relatorio_md.append(f"### E-mail de '{remetente}' - Assunto: '{assunto}'")
        if respostas:
            relatorio_md.extend([f"- [x] Verificado: {Path(r).name}" for r in respostas])
            relatorio_txt.append(f"E-mail de '{remetente}' ({assunto}):")
            relatorio_txt.extend([f"  - {Path(r).name}" for r in respostas])
            total_respostas += len(respostas)
        else:
            relatorio_md.append("- [ ] Nenhum documento verificado com sucesso.")
            relatorio_txt.append(f"E-mail de '{remetente}' ({assunto}): Nenhum documento verificado.")

    print(f"\n✅ Fluxo finalizado. Total de PDFs gerados: {total_respostas}")

    try:
        # --- CHAMADA CORRIGIDA ---
        # Adicionando o argumento 'titulo' que estava faltando.
        registrar_log_execucao(
            titulo="Relatório de Execução - Smart Auditor",
            conteudo_markdown="\n".join(relatorio_md),
            conteudo_texto="\n".join(relatorio_txt)
        )
    except Exception as e:
        print(f"⚠️ Falha ao salvar log de execução: {e}")
        traceback.print_exc()

