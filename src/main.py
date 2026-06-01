import os
import tempfile
import streamlit as st
import pandas as pd

from extrator_questoes import extrair_questoes
from leitor_provas import extrair_texto_pdf
from leitor_planos import carregar_todos_planos
from ia_selecao_questoes import selecionar_melhor_plano
from ia_avancada import analisar_questao_com_ia
from ia_curricular import criar_perfis_curriculares, sugerir_uso_pedagogico
from gerador_relatorio import gerar_relatorio
from blueprint_engine import gerar_blueprint


PASTA_PLANOS = "data/planos_aula"
PASTA_OUTPUTS = "outputs/relatorios"
SAIDA_RELATORIO = os.path.join(PASTA_OUTPUTS, "relatorio_enamed_intelligence.docx")


def identificar_fonte(nome_arquivo):
    nome = nome_arquivo.upper()
    if "ENAMED" in nome:
        return "ENAMED"
    if "ENADE" in nome:
        return "ENADE"
    if "ENARE" in nome:
        return "ENARE"
    return "Fonte não identificada"


def identificar_ano(nome_arquivo):
    import re
    ano = re.search(r"(20\d{2})", nome_arquivo)
    return ano.group(1) if ano else "Ano não identificado"


def identificar_conteudo(questao):
    texto = questao.lower()
    palavras_chave = [
        "atenção primária", "sus", "hipertensão", "diabetes", "gestante",
        "pré-natal", "criança", "idoso", "urgência", "emergência",
        "vacinação", "saúde mental", "depressão", "ansiedade", "infarto",
        "pneumonia", "sepse", "trauma", "ética", "bioética", "semiologia",
        "diagnóstico", "tratamento", "prevenção", "promoção da saúde",
    ]
    encontrados = [p for p in palavras_chave if p in texto]
    return ", ".join(encontrados) if encontrados else "Conteúdo não identificado automaticamente"


st.set_page_config(
    page_title="ENAMED Intelligence | Athena Sciences",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 ENAMED Intelligence")
st.caption("Módulo Athena Sciences para análise inteligente de provas médicas, questões, planos de aula e compatibilidade curricular.")

with st.sidebar:
    st.header("Configurações")
    limite_questoes = st.number_input(
        "Número máximo de questões para analisar",
        min_value=1,
        max_value=200,
        value=20,
        step=1,
    )
    usar_ia = st.toggle("Executar IA avançada", value=True)
    st.info("Para análises longas, reduza o número de questões no primeiro teste.")

arquivo_pdf = st.file_uploader(
    "Envie uma prova em PDF",
    type=["pdf"],
)

if arquivo_pdf is not None:
    os.makedirs(PASTA_OUTPUTS, exist_ok=True)

    nome_arquivo = arquivo_pdf.name
    fonte = identificar_fonte(nome_arquivo)
    ano = identificar_ano(nome_arquivo)

    # Métricas iniciais removidas: o Blueprint será o painel principal unificado.

    if st.button("Analisar prova", type="primary"):
        with st.spinner("Carregando planos de aula..."):
            planos = carregar_todos_planos(PASTA_PLANOS)
            perfis_curriculares = criar_perfis_curriculares(planos)

        st.success(f"Planos encontrados: {len(planos)}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(arquivo_pdf.read())
            caminho_pdf = tmp.name

        with st.spinner("Extraindo texto do PDF..."):
            texto = extrair_texto_pdf(caminho_pdf)

        with st.spinner("Extraindo questões..."):
            questoes = extrair_questoes(texto)

        questoes = questoes[:limite_questoes]

        tipo_blueprint, df_questoes_blueprint, df_resumo_blueprint = gerar_blueprint(
            questoes,
            nome_arquivo,
            texto
        )

        st.subheader("ATHENA Blueprint | ENAMED Intelligence")
        st.info(f"Tipo de prova reconhecido: {tipo_blueprint}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Arquivo", nome_arquivo)
        c2.metric("Total de questões", len(questoes))
        c3.metric("Ano", ano)

        st.markdown("### Percentual por grande área")
        st.dataframe(df_resumo_blueprint, use_container_width=True)

        st.markdown("### Questões classificadas")
        st.dataframe(df_questoes_blueprint, use_container_width=True)

        os.makedirs("outputs/planilhas", exist_ok=True)
        caminho_excel_blueprint = "outputs/planilhas/blueprint_enamed_intelligence.xlsx"

        with pd.ExcelWriter(caminho_excel_blueprint, engine="openpyxl") as writer:
            df_resumo_blueprint.to_excel(writer, sheet_name="Resumo por área", index=False)
            df_questoes_blueprint.to_excel(writer, sheet_name="Questões classificadas", index=False)

        with open(caminho_excel_blueprint, "rb") as f:
            st.download_button(
                "Baixar Blueprint Excel",
                f,
                file_name="blueprint_enamed_intelligence.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.success(f"Questões identificadas para análise curricular: {len(questoes)}")

        resultados = []
        barra = st.progress(0)

        for i, questao in enumerate(questoes, start=1):
            with st.expander(f"Questão {i}", expanded=False):
                st.write(questao[:2000])

            melhor_plano, score = selecionar_melhor_plano(questao, planos)
            conteudo = identificar_conteudo(questao)

            perfil_disciplina = perfis_curriculares.get(
                melhor_plano,
                {
                    "disciplina": melhor_plano,
                    "conteudos": [],
                    "competencias": [],
                    "habilidades": [],
                    "lacunas": ["Perfil curricular não encontrado."],
                },
            )

            sugestao_pedagogica = sugerir_uso_pedagogico(
                questao,
                score,
                conteudo,
                perfil_disciplina,
            )

            if usar_ia:
                analise_ia = analisar_questao_com_ia(
                    questao,
                    melhor_plano,
                    score,
                    conteudo,
                )
            else:
                analise_ia = "IA avançada desativada nesta execução."

            competencias = sugestao_pedagogica.get("competencias", [])
            habilidades = sugestao_pedagogica.get("habilidades", [])
            lacunas = sugestao_pedagogica.get("lacunas", [])

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

            barra.progress(i / len(questoes))

        st.subheader("Resultados resumidos")

        for r in resultados:
            st.markdown(f"### Questão {r['numero']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Disciplina recomendada", r["disciplina"])
            c2.metric("Compatibilidade", f"{r['score']}%")
            c3.metric("Conteúdo provável", r["conteudo"])
            st.write("**Competências:**", ", ".join(r["competencias"]) if r["competencias"] else "Não identificadas")
            st.write("**Habilidades:**", ", ".join(r["habilidades"]) if r["habilidades"] else "Não identificadas")
            st.write("**Lacunas:**", ", ".join(r["lacunas"]) if r["lacunas"] else "Sem lacunas evidentes")
            st.divider()

        with st.spinner("Gerando relatório Word..."):
            gerar_relatorio(resultados, SAIDA_RELATORIO)

        st.success("Relatório gerado com sucesso.")

        with open(SAIDA_RELATORIO, "rb") as f:
            st.download_button(
                label="Baixar relatório Word",
                data=f,
                file_name="relatorio_enamed_intelligence.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
else:
    st.info("Envie uma prova em PDF para iniciar a análise.")
