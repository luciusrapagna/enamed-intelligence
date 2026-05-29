from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calcular_similaridade(texto_questao, texto_plano):
    textos = [texto_questao, texto_plano]

    vetorizar = TfidfVectorizer(
        stop_words=None,
        lowercase=True,
        ngram_range=(1, 2)
    )

    matriz = vetorizar.fit_transform(textos)

    similaridade = cosine_similarity(matriz[0:1], matriz[1:2])[0][0]

    return round(similaridade * 100, 2)


def selecionar_melhor_plano(texto_questao, planos):
    melhor_plano = None
    melhor_score = 0

    for nome_plano, texto_plano in planos.items():
        score = calcular_similaridade(texto_questao, texto_plano)

        if score > melhor_score:
            melhor_score = score
            melhor_plano = nome_plano

    return melhor_plano, melhor_score