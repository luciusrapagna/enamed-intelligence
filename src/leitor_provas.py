import fitz
import os


def listar_pdfs(pasta):
    arquivos = []

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            arquivos.append(os.path.join(pasta, arquivo))

    return arquivos


def extrair_texto_pdf(caminho_pdf):
    texto = ""

    pdf = fitz.open(caminho_pdf)

    for pagina in pdf:
        texto += pagina.get_text()

    return texto


def escolher_prova(pasta):
    provas = listar_pdfs(pasta)

    if not provas:
        print("Nenhuma prova em PDF foi encontrada.")
        return None

    print("\nPROVAS DISPONÍVEIS:\n")

    for i, prova in enumerate(provas, start=1):
        print(f"{i} - {os.path.basename(prova)}")

    entrada = input("\nDigite o número da prova que deseja analisar: ").strip()

    if not entrada.isdigit():
        print("Entrada inválida. Digite apenas o número da prova.")
        return None

    escolha = int(entrada)

    return provas[escolha - 1]