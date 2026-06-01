import re
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from collections import Counter


def limpar_texto_excel(valor):
    if valor is None:
        return ""
    valor = str(valor)
    valor = ILLEGAL_CHARACTERS_RE.sub("", valor)
    valor = valor.replace("\x00", "").replace("\x0b", "").replace("\x0c", "")
    return valor

AREAS = {
    "Clínica Médica": [
        "hipertensão", "diabetes", "infarto", "angina", "asma", "dpoc",
        "pneumonia", "sepse", "insuficiência cardíaca", "avc", "renal",
        "hepatite", "cirrose", "anemia", "trombose", "clínica médica"
    ],
    "Cirurgia": [
        "cirurgia", "trauma", "abdome agudo", "apendicite", "colecistite",
        "hérnia", "fratura", "queimadura", "pós-operatório", "pré-operatório",
        "anestesia", "sutura"
    ],
    "Pediatria": [
        "criança", "lactente", "recém-nascido", "neonato", "pediatria",
        "adolescente", "vacinação infantil", "crescimento", "desenvolvimento",
        "bronquiolite"
    ],
    "Ginecologia e Obstetrícia": [
        "gestante", "pré-natal", "parto", "puerpério", "gravidez",
        "contracepção", "menstruação", "colo uterino", "pré-eclâmpsia",
        "ginecologia", "obstetrícia"
    ],
    "Saúde Coletiva": [
        "sus", "atenção primária", "ubs", "esf", "saúde coletiva",
        "epidemiologia", "vigilância", "notificação", "prevenção",
        "promoção da saúde", "determinantes sociais"
    ],
    "Ética/Bioética": [
        "ética", "bioética", "sigilo", "autonomia", "consentimento",
        "confidencialidade", "erro médico", "terminalidade"
    ],
    "Bases Biomédicas": [
        "anatomia", "fisiologia", "bioquímica", "histologia", "farmacologia",
        "microbiologia", "imunologia", "patologia", "genética"
    ]
}

def identificar_tipo_prova(nome_arquivo, texto=""):
    base = f"{nome_arquivo} {texto[:3000]}".upper()
    if "ENAMED" in base or "EXAME NACIONAL DE AVALIAÇÃO DA FORMAÇÃO MÉDICA" in base:
        return "ENAMED"
    if "ENADE" in base or "EXAME NACIONAL DE DESEMPENHO DOS ESTUDANTES" in base:
        return "ENADE"
    if "ENARE" in base or "EXAME NACIONAL DE RESIDÊNCIA" in base:
        return "ENARE"
    return "Fonte não identificada"

def classificar_grande_area(questao):
    texto = questao.lower()
    scores = {}
    for area, termos in AREAS.items():
        scores[area] = sum(1 for termo in termos if termo.lower() in texto)
    melhor = max(scores, key=scores.get)
    return melhor if scores[melhor] > 0 else "Não classificada"

def gerar_blueprint(questoes, nome_arquivo="", texto_completo=""):
    tipo = identificar_tipo_prova(nome_arquivo, texto_completo)
    linhas = []
    for i, q in enumerate(questoes, start=1):
        q = limpar_texto_excel(q)
        area = classificar_grande_area(q)
        linhas.append({
            "Questão": i,
            "Tipo de prova": tipo,
            "Grande área": area,
            "Texto": limpar_texto_excel(q[:1000])
        })

    df_questoes = pd.DataFrame(linhas)

    if df_questoes.empty:
        df_resumo = pd.DataFrame(columns=["Grande área", "N questões", "Percentual (%)"])
        return tipo, df_questoes, df_resumo

    total = len(df_questoes)
    contagem = Counter(df_questoes["Grande área"])

    df_resumo = pd.DataFrame([
        {
            "Grande área": area,
            "N questões": n,
            "Percentual (%)": round((n / total) * 100, 2)
        }
        for area, n in contagem.items()
    ]).sort_values("Percentual (%)", ascending=False)

    return tipo, df_questoes, df_resumo
