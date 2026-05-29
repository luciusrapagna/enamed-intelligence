from ia_avancada import analisar_questao_com_ia


# ==========================================================
# CRIAR PERFIL CURRICULAR
# ==========================================================

def criar_perfil_disciplina(nome_plano, texto_plano):

    texto = texto_plano.lower()

    perfil = {

        "disciplina": nome_plano,

        "conteudos": [],

        "competencias": [],

        "habilidades": [],

        "lacunas": []
    }

    # ======================================================
    # CONTEÚDOS
    # ======================================================

    palavras_conteudo = [

        "hipertensão",
        "diabetes",
        "sus",
        "atenção primária",
        "urgência",
        "emergência",
        "vacinação",
        "pré-natal",
        "saúde mental",
        "cirurgia",
        "pediatria",
        "clínica médica",
        "bioética",
        "semiologia",
        "diagnóstico",
        "terapêutica"
    ]

    # ======================================================
    # COMPETÊNCIAS
    # ======================================================

    palavras_competencias = [

        "raciocínio clínico",
        "tomada de decisão",
        "abordagem integral",
        "gestão do cuidado",
        "promoção da saúde",
        "prevenção",
        "comunicação",
        "ética profissional",
        "trabalho em equipe",
        "humanização",
        "liderança",
        "educação em saúde"
    ]

    # ======================================================
    # HABILIDADES
    # ======================================================

    palavras_habilidades = [

        "diagnosticar",
        "prescrever",
        "interpretar exames",
        "realizar anamnese",
        "exame físico",
        "manejo clínico",
        "procedimentos",
        "atendimento",
        "escuta qualificada",
        "intervenção terapêutica",
        "acolhimento"
    ]

    # ======================================================
    # IDENTIFICAR CONTEÚDOS
    # ======================================================

    for palavra in palavras_conteudo:

        if palavra in texto:
            perfil["conteudos"].append(palavra)

    # ======================================================
    # IDENTIFICAR COMPETÊNCIAS
    # ======================================================

    for palavra in palavras_competencias:

        if palavra in texto:
            perfil["competencias"].append(palavra)

    # ======================================================
    # IDENTIFICAR HABILIDADES
    # ======================================================

    for palavra in palavras_habilidades:

        if palavra in texto:
            perfil["habilidades"].append(palavra)

    # ======================================================
    # LACUNAS
    # ======================================================

    if len(perfil["conteudos"]) < 3:

        perfil["lacunas"].append(
            "Poucos conteúdos identificados automaticamente."
        )

    if len(perfil["competencias"]) < 2:

        perfil["lacunas"].append(
            "Poucas competências identificadas."
        )

    return perfil


# ==========================================================
# CRIAR TODOS PERFIS
# ==========================================================

def criar_perfis_curriculares(planos):

    perfis = {}

    for nome_plano, texto_plano in planos.items():

        perfil = criar_perfil_disciplina(
            nome_plano,
            texto_plano
        )

        perfis[nome_plano] = perfil

    return perfis


# ==========================================================
# SUGERIR QUESTÃO PARA AULA
# ==========================================================

def sugerir_uso_pedagogico(
    questao,
    score,
    conteudo,
    perfil
):

    sugestao = {

        "disciplina": perfil["disciplina"],

        "conteudos": perfil["conteudos"],

        "competencias": perfil["competencias"],

        "habilidades": perfil["habilidades"],

        "lacunas": perfil["lacunas"],

        "score": score,

        "conteudo_questao": conteudo
    }

    return sugestao