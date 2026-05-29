import os

from dotenv import load_dotenv

from openai import OpenAI


# =====================================================
# CARREGAR VARIÁVEIS
# =====================================================

load_dotenv()


# =====================================================
# CLIENTE OPENAI
# =====================================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# IA AVANÇADA
# =====================================================

def analisar_questao_com_ia(
    questao,
    disciplina_recomendada,
    score,
    conteudo
):

    prompt = f"""
Você é uma IA especialista em:

- Educação médica
- ENAMED
- ENADE
- ENARE
- Planejamento curricular
- Avaliação por competências
- Teste de Progresso

Analise a questão abaixo.

QUESTÃO:
{questao}

DISCIPLINA RECOMENDADA PELA IA LOCAL:
{disciplina_recomendada}

COMPATIBILIDADE:
{score}%

CONTEÚDO IDENTIFICADO:
{conteudo}

Responda exatamente neste formato:

Conteúdo central:
[descreva o conteúdo principal]

Área médica provável:
[indique a grande área]

Disciplina recomendada:
[indique a disciplina]

Justificativa pedagógica:
[explique a relação com o plano de aula]

Sugestão de uso:
[indique se pode ser usada em aula, revisão, simulado, TP ou avaliação]
"""

    try:

        resposta = client.responses.create(

            model="gpt-4.1-mini",

            input=prompt
        )

        return resposta.output_text

    except Exception as erro:

        return (
            f"Erro na IA avançada:\n{erro}"
        )