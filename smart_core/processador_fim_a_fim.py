import os
import traceback
from dotenv import load_dotenv
from pathlib import Path

from smart_email.email_reader import ler_emails_com_anexos
from smart_email import enviar_email_pdf
from smart_verificacao import verificar_e_retornar

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Carrega variáveis do .env
load_dotenv()
MODO_DEBUG = os.getenv("MODO_DEBUG_CORE", "true").lower() == "true"
CAMINHO_TEMP = os.getenv("CAMINHO_TEMP", "smart_documentos/temp/")


def gerar_pdf_resposta(texto: str, caminho_saida: str):
    c = canvas.Canvas(caminho_saida, pagesize=A4)
    largura, altura = A4
    y = altura - 50
    for linha in texto.split("\n"):
        c.drawString(50, y, linha[:100])  # Limita a largura da linha
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50
    c.save()


def processar_fluxo(lista_verificacao: str):
    print("📥 Iniciando leitura de e-mails...")
    try:
        emails = ler_emails_com_anexos()
    except Exception as e:
        print(f"❌ Erro na leitura de e-mails: {e}")
        traceback.print_exc()
        return

    if not emails:
        print("⚠️ Nenhum e-mail com anexo encontrado.")
        return

    for email in emails:
        remetente = email["remetente"]
        assunto = email.get("assunto", "[sem assunto]")
        mensagem = email.get("mensagem", "")
        anexos = email["anexos_salvos"]

        print(f"📧 Processando e-mail de: {remetente} | Anexos: {len(anexos)}")

        respostas = []
        for caminho_pdf in anexos:
            try:
                print(f"🔍 Verificando documento: {caminho_pdf}")
                resultado = verificar_e_retornar(caminho_pdf, lista_verificacao)

                if not resultado["status"]:
                    print(f"⚠️ Verificação falhou: {resultado.get('mensagem', 'sem mensagem')}")
                    continue

                resposta_md = resultado["resposta"]
                nome_base = Path(caminho_pdf).stem
                nome_saida = os.path.join(CAMINHO_TEMP, f"{nome_base}_verificado.pdf")

                gerar_pdf_resposta(resposta_md, nome_saida)
                print(f"✅ Resultado salvo em: {nome_saida}")
                respostas.append(nome_saida)

            except Exception as e:
                print(f"❌ Erro ao processar {caminho_pdf}: {e}")
                traceback.print_exc()

        if respostas:
            try:
                print(f"📤 Enviando resposta para {remetente}...")
                assunto_resp = f"[Verificação] Resultado para: {assunto}"
                corpo = "Olá! Segue anexo o resultado da verificação dos documentos enviados."
                enviar_email_pdf([remetente], respostas, assunto_resp, corpo)
                print("📨 E-mail enviado com sucesso.")
            except Exception as e:
                print(f"❌ Falha ao enviar e-mail: {e}")
                traceback.print_exc()

    print("✅ Fluxo finalizado.")
