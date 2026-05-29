import os
import fitz
import pandas as pd
from docx import Document


def listar_planos(pasta):

    arquivos = []

    for arquivo in os.listdir(pasta):

        if arquivo.lower().endswith((".pdf", ".docx", ".xlsx", ".xls")):

            arquivos.append(os.path.join(pasta, arquivo))

    return arquivos


def ler_pdf(caminho):

    texto = ""

    pdf = fitz.open(caminho)

    for pagina in pdf:

        texto += pagina.get_text()

    return texto


def ler_docx(caminho):

    documento = Document(caminho)

    textos = []

    for paragrafo in documento.paragraphs:

        textos.append(paragrafo.text)

    return "\n".join(textos)


def ler_excel(caminho):

    abas = pd.read_excel(caminho, sheet_name=None)

    textos = []

    for nome_aba, tabela in abas.items():

        textos.append(f"\nABA: {nome_aba}\n")

        textos.append(tabela.to_string(index=False))

    return "\n".join(textos)


def ler_plano(caminho):

    if caminho.lower().endswith(".pdf"):
        return ler_pdf(caminho)

    elif caminho.lower().endswith(".docx"):
        return ler_docx(caminho)

    elif caminho.lower().endswith((".xlsx", ".xls")):
        return ler_excel(caminho)

    return ""


def carregar_todos_planos(pasta):

    planos = {}

    arquivos = listar_planos(pasta)

    for arquivo in arquivos:

        nome = os.path.basename(arquivo)

        texto = ler_plano(arquivo)

        planos[nome] = texto

    return planos