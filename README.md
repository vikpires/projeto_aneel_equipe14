 <div align="center">
   <img src=".\docs\assets\energy_towers.jpg" width=100% alt="Imagem de torres de energia elétrica" /> 
 </div>
<br />

# Projeto ANEEL - Energia em Risco
### *Análise de Dados de Continuidade Elétrica e Previsão de Risco Regulatório (ANEEL)*

---

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
</p>

<p align=left>

  ![Last Commit](https://img.shields.io/github/last-commit/vikpires/projeto_aneel_equipe14?style=flat-square&logo=git&logoColor=white)
  ![Open Issues](https://img.shields.io/github/issues/vikpires/projeto_aneel_equipe14?style=flat-square&logo=github&logoColor=white)
  ![Release](https://img.shields.io/github/v/release/vikpires/projeto_aneel_equipe14?style=flat-square&logo=github&logoColor=white)
  ![License](https://img.shields.io/github/license/vikpires/projeto_aneel_equipe14?style=flat-square&logo=github&logoColor=white)

</p>

---

## Descrição

Projeto de **Análise de Dados e Machine Learning** desenvolvido sobre dados públicos da Agência Nacional de Energia Elétrica (ANEEL), com foco no diagnóstico dos indicadores de continuidade do fornecimento elétrico (DEC e FEC) e na mitigação de riscos e compensações regulatórias no Brasil. Trabalho desenvolvido como projeto prático da formação **AI Talent Academy**, da _White Cube_.

---

## Sumário

- [1. Contexto](#1-contexto)
- [2. Objetivo](#2-objetivo)
- [3. Base de Dados](#3-base-de-dados)
- [4. Tecnologias](#4-tecnologias)
- [5. Como Executar](#5-como-executar)
- [6. Organização dos Diretorios](#6-organização-dos-diretórios)
- [7. Cronograma e Fases](#7-cronograma-e-fases)
- [8. Equipe](#8-equipe)

---

## 1. Contexto

No setor de distribuição de energia elétrica no Brasil, a **Agência Nacional de Energia Elétrica (ANEEL)** estabelece metas e padrões contratuais estritos de qualidade por meio de dois indicadores coletivos de continuidade:

- **DEC (Duração Equivalente de Interrupção por Unidade Consumidora):** Mede o tempo médio (em horas) que os consumidores atendidos por determinado conjunto ficaram sem energia.

- **FEC (Frequência Equivalente de Interrupção por Unidade Consumidora):** Mede a quantidade média de vezes em que ocorreram interrupções no fornecimento.

A transgressão desses limites regulatórios acarreta compensações financeiras obrigatórias repassadas diretamente na fatura dos consumidores afetados, impactando a receita operacional líquida das concessionárias e sua reputação institucional.

---

## 2. Objetivo

Construir uma solução integrada de Análise de Dados e Machine Learning que permita analisar o comportamento histórico dos indicadores DEC e FEC, diagnosticar reincidências de transgressões e estimar a probabilidade de descumprimento dos limites regulatórios futuros em nível de conjunto consumidor.

---

## 3. Base de Dados

Os dados utilizados são públicos e extraídos do portal de dados abertos da ANEEL. Para fins de análise, o conjunto de dados será delimitado a um período de 5 anos **(2021-2025)**:

**Datasets:** 
- [Indicadores Coletivos de Continuidade (DEC e FEC)](https://dadosabertos.aneel.gov.br/pt_BR/dataset/indicadores-coletivos-de-continuidade-dec-e-fec) 
- [Interrupções de Energia Elétrica nas Redes de Distribuição)](https://dadosabertos.aneel.gov.br/dataset/interrupcoes-de-energia-eletrica-nas-redes-de-distribuicao)

---

### 4. Tecnologias

**Tecnologia / Versão** | **Função** |
| --- | --- |
| ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)  | Execução do código e módulos do projeto |
| ![DuckDB](https://img.shields.io/badge/DuckDB-1.0-FFF000?style=flat-square&logo=duckdb&logoColor=black) | Transformação SQL e geração dos Parquets |
| ![Pytest](https://img.shields.io/badge/pytest-7.0-0A9EDC?style=flat-square&logo=pytest&logoColor=white) | Execução de testes automatizados |
| ![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=flat-square&logo=pandas&logoColor=white) <br> ![NumPy](https://img.shields.io/badge/NumPy-1.26-013243?style=flat-square&logo=numpy&logoColor=white) | Apoio na leitura tabular e cálculos numéricos |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8-11557C?style=flat-square) <br> ![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0?style=flat-square) | Gráficos e diagnósticos estatísticos |
| ![Scikit-Learn](https://img.shields.io/badge/scikit_learn-1.4-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) | Algoritmos de ML e testes estatísticos |
| ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black) | Criação do dashboard gerencial |
| ![Git](https://img.shields.io/badge/Git-2.43-F05032?style=flat-square&logo=git&logoColor=white) | Controle de versão do repositório |

---

## 5. Como Executar

**Pré-requisitos:**

* Python 3.11+
* Git
* Ambiente Linux ou WSL 2 (requisito necessário para compatibilidade com chamadas de sistema do Airflow).

**1. Clonar o repositório e configurar o ambiente virtual**

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

python3.11 -m venv .venv
source .venv/bin/activate  # No Windows/WSL
pip install --upgrade pip
pip install -r requirements.txt

```

**2. Execução**

Na raiz do projeto, instale as dependências e execute:

```bash
python main.py
```

Para executar os testes automatizados:

```bash
pytest -v tests/
```

---

## 6. Organização dos Diretórios

```markdown
├── 📁 data/
│   ├── 📁 raw/            # Dados brutos originais (Camada Bronze)
│   ├── 📁 interim/        # Dados intermediários tratados (Camada Silver)
│   ├── 📁 external/       # Dados externos e bases de apoio
│   └── 📁 processed/      # Dados finais consolidados para consumo analítico (Camada Gold)
│
├── 📁 docs/               # Documentação técnica, arquitetura e dicionário de dados
│   └── 📁 assets/         # Imagens, fluxogramas e diagramas da documentação
│
├── 📁 models/             # Artefatos e arquivos de modelos treinados
├── 📁 notebooks/          # Notebooks Jupyter para análise exploratória e prototipagem
├── 📁 pbix/               # Relatórios e modelos de dados do Power BI
├── 📁 references/         # Manuais normativos, notas técnicas e materiais de consulta
├── 📁 reports/            # Relatórios consolidados e apresentações executivas
├── 📁 src/                # Código-fonte modular do projeto (extractors, transformers, validators)
├── 📁 tests/              # Suíte de testes automatizados e regras do Quality Gate
├── 📄 .gitignore          # Regras de arquivos e pastas ignorados pelo Git
├── 📄 CONTRIBUTING.md     # Guia de contribuição, padrões de código e fluxo de Git
├── 📄 LICENSE             # Termos de licença de uso e distribuição do projeto
├── 📄 README.md           # Apresentação geral, arquitetura e instruções de execução
├── 📄 requirements.txt    # Dependências e bibliotecas Python do projeto
└── 📄 setup_colab.sh      # Script de automação e provisionamento de ambiente no Google Colab

```
---

## 7. Cronograma e Fases

<p align="left">
  <a href="https://github.com/users/vikpires/projects/7/views/4?sliceBy[columnId]=Milestone">
    <img src="https://img.shields.io/badge/Backlog_&_Roadmap-1074e7?style=flat-square&logo=github&logoColor=white" alt="Backlog e Roadmap" />
  </a>
</p>

O projeto adotará o framework **CRISP-DM**. O cronograma do projeto segue as seis fases do framework:


| Fase / Marco | Status | Período | Tarefas |
| :--- | :---: | :---: | :---: |
| **01:  Compreensão do Negócio (Business Understanding)** | Concluído | Semana 4 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/1) |
| **02: Compreensão dos Dados (Data Understanding)** | Em Progresso | Semana 5 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/6) |
| **03: Preparação dos Dados (Data Preparation)** | A Iniciar | Semana 6 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/2) |
| **04: Modelagem (Modeling)** | A Iniciar | Semana 7 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/3) |
| **05: Avaliação (Evaluation)** | A Iniciar | Semana 8 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/4) |
| **06: Implantação (Deployment) & Demo Day** | A Iniciar | Semana 8 | [Ver Tarefas](https://github.com/vikpires/projeto_aneel_equipe14/milestone/5) |

---

## 8. Equipe

- [Antônio Marcel](https://github.com/MarcelProgram)
- [Edivaldo Dias](https://github.com/Edy-Ap-Dias)
- [Leonardo Gomes](https://github.com/LeonardoFGs)
- [Leonardo Santos](https://github.com/leojosants)
- [Vanessa Vilela](https://github.com/vsvilela39-oss)
- [Vitor Pires](https://github.com/vikpires)
