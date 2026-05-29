import os
import re

from leitor_provas import escolher_prova, extrair_texto_pdf
from extrator_questoes import extrair_questoes
from leitor_planos import carregar_todos_planos
from ia_selecao_questoes import selecionar_melhor_plano
from ia_avancada import analisar_questao_com_ia
from ia_curricular import criar_perfis_curriculares, sugerir_uso_pedagogico
from gerador_relatorio import gerar_relatorio


PASTA_PROVAS = "data/provas"
PASTA_PLANOS = "data/planos_aula"
SAIDA_RELATORIO = "outputs/relatorios/relatorio_enamed_intelligence.docx"


def identificar_fonte(nome_arquivo):
    nome = nome_arquivo.upper()

    if "ENAMED" in nome:
        return "ENAMED"
    elif "ENADE" in nome:
        return "ENADE"
    elif "ENARE" in nome:
        return "ENARE"

    return "Fonte não identificada"


def identificar_ano(nome_arquivo):
    ano = re.search(r"(20\d{2})", nome_arquivo)

    if ano:
        return ano.group(1)

    return "Ano não identificado"


def identificar_conteudo(questao):
    texto = questao.lower()

    palavras_chave = [
        "atenção primária",
        "sus",
        "hipertensão",
        "diabetes",
        "gestante",
        "pré-natal",
        "criança",
        "idoso",
        "urgência",
        "emergência",
        "vacinação",
        "saúde mental",
        "depressão",
        "ansiedade",
        "infarto",
        "pneumonia",
        "sepse",
        "trauma",
        "ética",
        "bioética",
        "semiologia",
        "diagnóstico",
        "tratamento",
        "prevenção",
        "promoção da saúde",
    ]

    encontrados = []

    for palavra in palavras_chave:
        if palavra in texto:
            encontrados.append(palavra)

    if encontrados:
        return ", ".join(encontrados)

    return "Conteúdo não identificado automaticamente"


print("=" * 60)
print("ENAMED INTELLIGENCE")
print("=" * 60)


print("\nCarregando planos de aula...\n")

planos = carregar_todos_planos(PASTA_PLANOS)

print(f"Planos encontrados: {len(planos)}")


print("\nCriando perfis curriculares...\n")

perfis_curriculares = criar_perfis_curriculares(planos)

print(f"Perfis curriculares criados: {len(perfis_curriculares)}")


prova_escolhida = escolher_prova(PASTA_PROVAS)

if prova_escolhida is None:
    print("\nNenhuma prova foi encontrada.")
    print("Adicione PDFs em data/provas.")
    exit()


nome_arquivo = os.path.basename(prova_escolhida)
fonte = identificar_fonte(nome_arquivo)
ano = identificar_ano(nome_arquivo)


print("\n" + "=" * 60)
print(f"PROVA SELECIONADA: {nome_arquivo}")
print(f"Fonte: {fonte}")
print(f"Ano: {ano}")
print("=" * 60)


print("\nExtraindo texto da prova...\n")

texto = extrair_texto_pdf(prova_escolhida)


questoes = extrair_questoes(texto)

print(f"Questões identificadas: {len(questoes)}")


resultados = []


for i, questao in enumerate(questoes, start=1):

    print("\n" + "-" * 60)
    print(f"ANALISANDO QUESTÃO {i}")

    melhor_plano, score = selecionar_melhor_plano(
        questao,
        planos
    )

    conteudo = identificar_conteudo(questao)

    perfil_disciplina = perfis_curriculares.get(
        melhor_plano,
        {
            "disciplina": melhor_plano,
            "conteudos": [],
            "competencias": [],
            "habilidades": [],
            "lacunas": ["Perfil curricular não encontrado."]
        }
    )

    sugestao_pedagogica = sugerir_uso_pedagogico(
        questao,
        score,
        conteudo,
        perfil_disciplina
    )

    print("Executando IA avançada...\n")

    analise_ia = analisar_questao_com_ia(
        questao,
        melhor_plano,
        score,
        conteudo
    )

    competencias = sugestao_pedagogica.get("competencias", [])
    habilidades = sugestao_pedagogica.get("habilidades", [])
    lacunas = sugestao_pedagogica.get("lacunas", [])

    print(f"Disciplina recomendada: {melhor_plano}")
    print(f"Compatibilidade: {score}%")
    print(f"Conteúdo provável: {conteudo}")
    print(f"Competências: {', '.join(competencias) if competencias else 'Não identificadas'}")
    print(f"Habilidades: {', '.join(habilidades) if habilidades else 'Não identificadas'}")
    print(f"Lacunas: {', '.join(lacunas) if lacunas else 'Sem lacunas evidentes'}")

    resultados.append({
        "numero": i,
        "fonte": fonte,
        "ano": ano,
        "arquivo": nome_arquivo,
        "disciplina": melhor_plano,
        "score": score,
        "conteudo": conteudo,
        "questao": questao,
        "analise_ia": analise_ia,
        "competencias": competencias,
        "habilidades": habilidades,
        "lacunas": lacunas,
        "sugestao_pedagogica": sugestao_pedagogica,
    })


print("\nGerando relatório Word...\n")

gerar_relatorio(
    resultados,
    SAIDA_RELATORIO
)

print("=" * 60)
print("RELATÓRIO GERADO COM SUCESSO!")
print(f"Arquivo salvo em:\n{SAIDA_RELATORIO}")
print("=" * 60)