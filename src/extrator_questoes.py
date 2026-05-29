import re


def extrair_questoes(texto):

    padrao = r"(QUESTÃO\s+\d+.*?)(?=QUESTÃO\s+\d+|$)"

    questoes = re.findall(
        padrao,
        texto,
        re.DOTALL | re.IGNORECASE
    )

    return questoes