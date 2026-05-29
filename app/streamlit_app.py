import os
import re
import sys
import streamlit as st

# =====================================================
# PYTHONPATH
# =====================================================

sys.path.append("src")

# =====================================================
# IMPORTS DO ENAMED
# =====================================================

from leitor_provas import extrair_texto_pdf
from extrator_questoes import extrair_questoes
from leitor_planos import carregar_todos_planos
from ia_selecao_questoes import selecionar_melhor_plano
from ia_avancada import analisar_questao_com_ia
from ia_curricular import (
    criar_perfis_curriculares,
    sugerir_uso_pedagogico
)
from gerador_relatorio import gerar_relatorio

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="ENAMED Intelligence",
    layout="wide"
)

# =====================================================
# PASTAS
# =====================================================

PASTA_PROVAS = "data/provas"
PASTA_PLANOS = "data/planos_aula"
PASTA_RELATORIOS = "outputs/relatorios"

os.makedirs(PASTA_PROVAS, exist_ok=True)
os.makedirs(PASTA_PLANOS, exist_ok=True)
os.makedirs(PASTA_RELATORIOS, exist_ok=True)

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def limpar_pasta(pasta):

    for arquivo in os.listdir(pasta):

        caminho = os.path.join(pasta, arquivo)

        if os.path.isfile(caminho):

            os.remove(caminho)


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

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("ATHENA SCIENCES")

st.sidebar.success(
    "Microserviço integrado ao ecossistema Athena Sciences."
)

st.sidebar.markdown("---")

st.sidebar.write("✅ VPS Linux")
st.sidebar.write("✅ Streamlit")
st.sidebar.write("✅ systemd")
st.sidebar.write("✅ Nginx")
st.sidebar.write("✅ IA Curricular")

# =====================================================
# TÍTULO
# =====================================================

st.title("ENAMED INTELLIGENCE")

st.markdown(
    """
Sistema inteligente de análise de questões
ENAMED, ENADE e ENARE com integração curricular.
"""
)

# =====================================================
# LIMPEZA
# =====================================================

if st.button("LIMPAR ARQUIVOS ANTIGOS"):

    limpar_pasta(PASTA_PROVAS)
    limpar_pasta(PASTA_PLANOS)

    st.success("Arquivos antigos removidos.")

# =====================================================
# UPLOAD PROVA
# =====================================================

st.header("1. Upload da prova")

arquivo_prova = st.file_uploader(
    "Envie a prova PDF",
    type=["pdf"]
)

# =====================================================
# UPLOAD PLANOS
# =====================================================

st.header("2. Upload dos planos")

arquivos_planos = st.file_uploader(
    "Envie planos de aula",
    type=["pdf", "docx", "xlsx", "xls"],
    accept_multiple_files=True
)

# =====================================================
# SALVAR PROVA
# =====================================================

if arquivo_prova:

    caminho_prova = os.path.join(
        PASTA_PROVAS,
        arquivo_prova.name
    )

    with open(caminho_prova, "wb") as f:

        f.write(arquivo_prova.getbuffer())

    st.success(f"Prova enviada: {arquivo_prova.name}")

# =====================================================
# SALVAR PLANOS
# =====================================================

if arquivos_planos:

    quantidade = 0

    for arquivo in arquivos_planos:

        caminho_plano = os.path.join(
            PASTA_PLANOS,
            arquivo.name
        )

        with open(caminho_plano, "wb") as f:

            f.write(arquivo.getbuffer())

        quantidade += 1

    st.success(f"{quantidade} planos enviados.")

# =====================================================
# STATUS
# =====================================================

st.header("3. Status")

total_provas = len(os.listdir(PASTA_PROVAS))
total_planos = len(os.listdir(PASTA_PLANOS))

st.write(f"📄 Provas: {total_provas}")
st.write(f"📚 Planos: {total_planos}")

# =====================================================
# PROCESSAMENTO
# =====================================================

st.header("4. Processamento Inteligente")

if st.button("PROCESSAR ANÁLISE"):

    try:

        provas = os.listdir(PASTA_PROVAS)

        if not provas:

            st.error("Nenhuma prova encontrada.")
            st.stop()

        prova_escolhida = os.path.join(
            PASTA_PROVAS,
            provas[0]
        )

        nome_arquivo = os.path.basename(
            prova_escolhida
        )

        fonte = identificar_fonte(nome_arquivo)

        ano = identificar_ano(nome_arquivo)

        st.info("Carregando planos...")

        planos = carregar_todos_planos(
            PASTA_PLANOS
        )

        st.success(
            f"{len(planos)} planos carregados."
        )

        st.info("Criando perfis curriculares...")

        perfis_curriculares = criar_perfis_curriculares(
            planos
        )

        st.info("Extraindo texto da prova...")

        texto = extrair_texto_pdf(
            prova_escolhida
        )

        questoes = extrair_questoes(texto)

        st.success(
            f"{len(questoes)} questões identificadas."
        )

        resultados = []

        progresso = st.progress(0)

        for i, questao in enumerate(questoes):

            progresso.progress(
                (i + 1) / len(questoes)
            )

            melhor_plano, score = selecionar_melhor_plano(
                questao,
                planos
            )

            conteudo = identificar_conteudo(
                questao
            )

            perfil_disciplina = perfis_curriculares.get(
                melhor_plano,
                {
                    "disciplina": melhor_plano,
                    "conteudos": [],
                    "competencias": [],
                    "habilidades": [],
                    "lacunas": []
                }
            )

            sugestao_pedagogica = sugerir_uso_pedagogico(
                questao,
                score,
                conteudo,
                perfil_disciplina
            )

            analise_ia = analisar_questao_com_ia(
                questao,
                melhor_plano,
                score,
                conteudo
            )

            resultados.append({
                "numero": i + 1,
                "fonte": fonte,
                "ano": ano,
                "arquivo": nome_arquivo,
                "disciplina": melhor_plano,
                "score": score,
                "conteudo": conteudo,
                "questao": questao,
                "analise_ia": analise_ia,
                "competencias": sugestao_pedagogica.get("competencias", []),
                "habilidades": sugestao_pedagogica.get("habilidades", []),
                "lacunas": sugestao_pedagogica.get("lacunas", []),
                "sugestao_pedagogica": sugestao_pedagogica
            })

        caminho_relatorio = os.path.join(
            PASTA_RELATORIOS,
            "relatorio_enamed_intelligence.docx"
        )

        st.info("Gerando relatório Word...")

        gerar_relatorio(
            resultados,
            caminho_relatorio
        )

        st.success("Relatório gerado com sucesso.")

        with open(caminho_relatorio, "rb") as file:

            st.download_button(
                label="BAIXAR RELATÓRIO WORD",
                data=file,
                file_name="relatorio_enamed_intelligence.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    except Exception as e:

        st.error(f"Erro durante processamento: {e}")
