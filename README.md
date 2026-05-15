# Enamed Intelligence

Plataforma inteligente para análise, classificação e mapeamento automatizado de questões do ENADE, ENARE e ENAMED integrada aos planos de aula do curso de Medicina.

## Objetivos

- Ler provas automaticamente
- Extrair e organizar questões
- Classificar por grandes áreas do ENAMED
- Comparar questões com planos de aula
- Gerar relatórios pedagógicos inteligentes
- Apoiar Teste de Progresso
- Auxiliar preparação para ENAMED/ENADE
- Criar banco institucional de questões

## Estrutura do Projeto

```bash
data/
├── provas/
├── planos_aula/

outputs/
├── relatorios/
├── planilhas/

src/
├── main.py
├── leitor_provas.py
├── classificador_enamed.py
├── comparador_planos.py
└── gerador_relatorio.py