# Escopo do Projeto ANEEL - Energia em Risco
### Análise dos Indicadores DEC/FEC e Predição de Transgressões no Sistema de Distribuição de Energia

* **Documento:** Escopo do Projeto e Compreensão do Negócio (CRISP-DM Fase 1)

* **Equipe Responsável:** Equipe 14 - Antônio Marcel, Edivaldo Dias, Leonardo Gomes, Vanessa Vilela, Vitor Pires

* **Período de Execução:** 01/09/2026 a 30/09/2026 

* **Gestão:** CRISP-DM e Kanban | Repositório GitHub (Branch padrão: `develop`)

* **Links:** [Repositório GitHub](https://github.com/vikpires/projeto_aneel_equipe14) • [Quadro Kanban](https://github.com/users/vikpires/projects/7/views/1)

* **Versão:** 2.0

---

## Sumário

1. **Visão Estratégica e Negócio**
   - [1.1. Visão Geral](#11-visão-geral)
   - [1.2. Contextualização](#12-contextualização)
   - [1.3. Problema e Oportunidades](#13-problemas-e-oportunidades)
   - [1.4. Objetivo](#14-objetivo)
   - [1.5. Stakeholders e Usuários Finais](#15-stakeholders-e-usuários-finais)
   
2. **Escopo e Viabilidade**
   - [2.1.Escopo do Projeto](#21-escopo-do-projeto)
   - [2.2 Hipóteses de Negócio](#22-hipóteses-de-negócio)
   - [2.3 Riscos](#23-riscos)
   - [2.4 Estrutura de Custos](#24-estrutura-de-custos)

3. **Dados e Engenharia Analítica**
   - [3.1 Fontes e Ingestão de Dados](#31-fontes-e-ingestão-de-dados)
   - [3.2 Requisitos e Restrições](#32-requisitos-e-restrições)

4. **Solução Técnica**
   - [4.1. Solução](#41-solução)
   - [4.2 Metodologia](#42-metodologia)
   - [4.3. Métricas de Avaliação e Benchmarks de Sucesso](#43-métricas-de-avaliação-e-benchmarks-de-sucesso)

5. Entregáveis e Síntese Executiva
   - [5.1. Entregáveis](#51-entregáveis)
   - [5.2. Síntese Executiva](#52-síntese-executiva)


---

## 1. Visão Estratégica e Negócio
### 1.1. Visão Geral
Este documento consolida a **Fase 1 do CRISP-DM - Compreensão do Negócio (Business Understanding)**. Sua finalidade é formalizar o alinhamento estratégico, mapear as dores do setor elétrico e fixar critérios técnicos mensuráveis antes da manipulação dos dados brutos no pipeline de dados.

### 1.2. Contextualização
No Brasil, as distribuidoras de enérgia elétrica operam sob regime de concessão pública regulada pela AN

A distribuição de energia elétrica no Brasil opera sob regime de concessão pública regulada pela Agência Nacional de Energia Elétrica (ANEEL). A qualidade e a continuidade do fornecimento são mensuradas por dois indicadores operacionais fundamentais:

* **DEC (Duração Equivalente de Interrupção por Unidade Consumidora):** Mede o tempo médio acumulado, em horas, que um grupo de consumidores fica sem fornecimento de energia.

* **FEC (Frequência Equivalente de Interrupção por Unidade Consumidora):** Mede a quantidade média de eventos de interrupção no fornecimento de energia ao mesmo grupo de consumidores no período apurado.

**Dinâmica Regulatória e Penalidades:**

Anualmente, a ANEEL estebelece limites máximos toleráveis para vada conjunto de unidades consumidoras. Ultrpassar esses limites caracteriza descumprimento das cláusulas do contrato de concessão (PRODIST - Módulo 8), acarretando em:

1. Compensação financeira automática na fatura dos consumidores afetados;

2. Sujeição a processos punitivos, multas administrativas e elevação do risco reputacional da concessionária.

### 1.3. Problemas e Oportunidades
A gestão de continuidade do serviço nas concessionárias opera frequentemente de forma **reativa**, sendo caracterizado por:

1. Defasagem temporal de diagnóstico: A identificação de violações ocorre após o encerramento do ciclo regulatório, inviabilizando intervenções preventivas.
2. Passivos financeiros e punições: A ausência de alertas antecipados gera desembolsos imediatos em compensações aos consumidores afetados.
3. Fricção analítica em escala: As bases brutas possuem dezenas de milhões de ocorrências descentralizadas e não padronizadas limitando a visão operacional e as estratégias de negócio.

### 1.4. Objetivo
#### 1.4.1. Objetivo Geral
Construir uma solução integrada de Engenharia de Dados, Análise de Dados e Machine Learning para diagnosticar o comportamento histórico dos indicadores DEC e FEC, mapear a reincidência de transgressões e estimar a probabilidade mensal de estouro dos limites regulatórios futuros por conjunto elétrico.

#### 1.4.2. Objetivos Específicos
* Integrar e padronizar a série histórica (2021–2025) dos datasets regulatórios da ANEEL (Continuidade, Limites, Interrupções, Atributos e Regiões).

* Cruzar dados apurados contra limites legais, estruturando rankings de criticidade, taxas de transgressão e disparidades regionais/sazonais.

* Identificar comportamentos cíclicos e disparidades regionais no desempenho operacional.

* Treinar e validar um modelo de Machine Learning supervisionado para classificar o score de risco de transgressão (Apurado > Limite) no horizonte mensal subsequente (t + 1).

* Entregar a camada de dados modelada em *Star Schema* colunar via Parquet, consumida diretamente por painéis executivos e operacionais no Power BI.

### 1.5. Stakeholders e Usuários Finais

**Quem toma a decisão hoje?**  

* **Gestores regulatórios/diretoria:** Planejamento financeiro e prestação de contas à ANEEL. 
* **Operação e Manutenção (O&M):** Planejamento de vistorias e despacho de equipes de campo.

**Quem é afetado?**  

* **Consumidores Finais:** Sofrem diretamente com a falta de energia e recebem as compensações financeiras em fatura.
* **Concessionária:** Sofre com o passivo financeiro imediato das compensações e o desgaste de imagem institucional.
* **Times Técnicos (Analistas de Dados/BI e Cientistas de Dados):** São cobrados por agilidade na extração de insights, governança e modelos de retreino estruturados.

| Stakeholder | Papel na Tomada de Decisão | Dores Principais | Uso da Solução |
| :--- | :--- | :--- | :--- |
| **Gestores Regulatórios/Diretoria** | Decisor Estratégico | Dificuldade em antecipar passivos financeiros e ausência de visão consolidada de risco de concessão | Acompanhamento do dashboard executivo para monitorar taxas de transgressão e projetar passivos antes do fechamento oficial |
| **Operação e Manutenção (O&M)** | Decisor Operacional | Atuação reativa e falta de critério preditivo para priorizar vistorias preventivas |Priorização de cronogramas e manutenção preventiva com base no score preditivo de risco mensal por conjunto |
| **Concessionárias de Energia** | Entidade Regulada | Passivos financeiros com compensações compulsórias e risco de sanções regulatórias e reputacionais | Adoção corporativa da solução como ferramenta de governança regulatória e redução de custos operacionais e multas |
| **Consumidor Final** | Usuário do Serviço | Frequência de interrupções, danos a aparelhos elétricos e tempo excessivo de restabelecimento | Beneficiado indiretamente pela maior estabilidade do fornecimento e agilidade no restabelecimento da rede |
| **Analistas de Dados/BI** | Usuário Analítico | Bases da ANEEL pesadas, despadronizadas e com encodings legados, gerando lentidão no Power BI | Carga direta de tabelas modeladas em Star Schema colunar (Parquet), acelerando análises e auditorias |
| **Cientistas de Dados** | Usuário Técnico | Falta de dados saneados, ausência de pipeline reprodutível e dificuldade de retreino periódico | Consumo de uma camada de features histórica consistente para teste, retreino e validação de modelos preditivos |

---

## 2. Escopo e Viabilidade
### 2.1. Escopo do Projeto

| Dimensão | No escopo (In-Scope) | Fora de Escopo (Out-of-Scope) |
| :--- | :--- | :--- | 
| **Granularidade e Privacidade** | Dados regulatórios consolidados em nível de conjunto consumidor, distribuidora, município e UF | Não serão manipulados dados individualizados por consumidor, garantindo conformidade com a LGPD | 
| **Execução** | Pipeline ELT em lote, com processamento histórico mensal e inferência periódica | Rotinas de streaming em tempo real |
| **Fontes Externas** | Datasets oficiais de distribuição e qualidade comercial da ANEEL | Não serão integrados arquivos geoespaciais ou API de dados meteorológicos em tempo real |

### 2.2. Hipóteses de Negócio

* **Hipótese 01** - Conjuntos com histórico crônico de transgressões de DEC/FEC apresentam probabilidade de reincidência maior de ultrapassar os limites regulatórios nos períodos subsequentes.

* **Hipótese 02** - Interrupções não programadas possuem maior impacto na variação do estouro do limite (DEC) em comparação às paradas programadas de manutenção.

* **Hipótese 03** - A dispersão geográfica e fatores sazonais geram picos concentrados de transgressão em regiões específicas.

* **Hipótese 04** - Conjuntos com maior densidade de unidades consumidoras atendidas apresentam menor tempo médio de restabelecimento (DEC).

* **Hipótese 05** - O histórico recente de DEC/FEC e do volume de interrupções pode prever o risco de transgressão regulatória no período subsequente.

### 2.3. Riscos

1. **Risco de Dados**
    * Dados faltantes ou nulos, com ausência de registros pontuais em limites ou apurações de conjuntos desativados/reestruturados.

    * Inconsistências temporais e cadastrais, com mudança de identificador do conjunto elétrico ou alterações de metodologia cadastral ao longo dos anos.

    * Granularidade desigual, contendo conflito entre dados agregados mensalmente (DEC/FEC) e dados por ocorrência (interrupções individuais).

2. **Risco de Modelagem e Machine Learning**
    * Volume de meses em conformidade muito superior ao de transgressões, induzindo o modelo a prever sempre a classe majoritária.

    *  O algoritmo memorizar o comportamento (overfitting) de distribuidoras específicas sem conseguir prever o risco em novas regiões.

    * Uso de acurácia global em vez de métricas mais robustas (Recall, PR-AUC e F1-Score).

3. **Risco de Projeto e Negócio**
    * Gerar *insights* estatísticos avançados, mas que não auxiliam a tomada de decisão prática da equipe de manutenção.

    * Confundir correlação de variáveis operacionais com causalidade regulatória.

    * Não considerar alterações ou revisões tarifárias/metas aprovadas pela ANEEL no período.

### 2.4. Estrutura de custos 

* **Fontes de Dados:** Gratuitas (Portal de Dados Abertos da ANEEL sob licença pública).

* **Infraestrutura Computacional:** Execução em máquinas locais dos membros da equipe e instâncias gratuitas em nuvem (Google Colab / GitHub).

* **Armazenamento e Distribuição:** Hospedagem analítica via GitHub Releases, viabilizando consumo dos arquivos processados direto no Power BI.

* **Esforço Técnico:** Dedicação de 6 membros ao longo do ciclo do projeto, distribuídos entre as áreas de engenharia de dados, modelagem preditiva, construção do dashboard e documentação.

* **Manutenção Futura:** Esforço periódico estimado em poucas horas mensais para extração de novos períodos apurados e retreino do modelo.

---

## 3. Dados e Engenharia Analítica 
### 3.1. Fontes e Ingestão de Dados
O projeto consome dados exclusivamente operacionais e públicos disponibilizados pelo Portal de Dados Abertos da ANEEL, compreendendo a série temporal de 5 anos (2021–2025):

| Entidade / Recurso | Fonte Oficial | Periodicidade / Granularidade | Uso no Projeto |
| :--- | :--- | :--- | :--- |
| **Indicadores Coletivos de Continuidade (DEC/FEC)** | [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/pt_BR/dataset/indicadores-coletivos-de-continuidade-dec-e-fec) | Mensal por Conjunto Consumidor | Dados brutos de DEC e FEC (apurado e limites regulatórios) para métricas de BI e alvo do ML. |
**Interrupções de Energia Elétrica nas Redes de Distribuição** | [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/pt_BR/dataset/interrupcoes-de-energia-eletrica-nas-redes-de-distribuicao) | Por evento / Ocorrência | Mapeamento da tipologia de causas das quedas e duração. |
**Limites Regulatórios** | [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/pt_BR/dataset/indicadores-coletivos-de-continuidade-dec-e-fec/resource/fd69e1dd-fd66-4269-b60c-cc0b7eb221b4) | Anual/Mensal por Conjunto | Metas regulatórias contratuais |
**Atributos de Conjuntos** | [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/pt_BR/dataset/indicadores-coletivos-de-continuidade-dec-e-fec/resource/3c780aca-38cf-406d-9d45-f07a9216eef2) | Cadastral/Periódico | Quantitativo de unidades consumidoras e subestações |
**Indicadores por Município** | [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/dataset/indqual-municipio/resource/3f841488-80a8-42f2-a6ca-e0c593b228de) | Cadastral/Geográfico | Mapeamento geográfico por Código IBGE, UF e Macrorregião |
| **Regras e Parâmetros Regulatórios** | [ANEEL — PRODIST Módulo 8](https://www.gov.br/aneel/pt-br/centrais-de-conteudos/procedimentos-regulatórios/prodist) | Regulatório / Estático | Fórmulas conceituais de transgressão e parâmetros para cálculo da proxy de compensações financeiras |

**Armazenamento e Formato:**  
* `data/raw:` Arquivos originais em *.csv* e *.parquet*
* `data/interim:` Dados saneados em *.parquet*
* `data/processed:` Tabelas finais de dimensão e fato em formato *.parquet* colunar estruturadas em *Star Schema*

**Privacidade e Conformidade:** 
Os dados são 100% operacionais e anonimizados na fonte pela ANEEL, sem exposição de dados pessoais ou faturas individualizadas, garantindo conformidade com a LGPD.

### 3.2. Requisitos e Restrições 

| **Requisitos Funcionais (RF)** |
|:---|
| **RF01:** O pipeline deve extrair, validar e integrar os dados de continuidade e limites de 2021 a 2025 de forma automatizada. | 
| **RF02:** O sistema deve calcular o indicador de transgressão (Apurado > Limite) e a margem de desvio relativo percentual por conjunto/mês |
| **RF03:** A camada de dados deve validar schemas e tratar dados ausentes e inconsistentes antes do processamento nas camadas analíticas.|
| **RF04:** Disponibilizar a base processada em modelagem Star Schema contendo tabelas fato e dimensão documentadas. |
| **RF05:** O modelo de Machine Learning deve gerar uma coluna contendo o *Score de Risco* (probabilidade entre 0 e 1) de descumprimento para o período `t+1`.|

| **Requisitos Não Funcionais (RNF)**
|:---|
| **RNF01:** Pipeline de dados e modelagem versionados no Git e ambiente virtual configurado. |
| **RNF02:** Processamento de arquivos pesados via DuckDB deve operar em modo out-of-core, limitando o consumo de RAM a 4 GB.| 
| **RNF03:** Os artefatos processados em Parquet devem ser distribuídos via GitHub Releases, permitindo que o Power BI consuma as tabelas diretamente pela Web sem dependência de bancos locais.|

---

## 4. Solução e Metodologia
### 4.1. Solução

* Pipeline automatizado em Python/DuckDB para ingestão em lote, tratamento de dados, padronização de schemas, validação de qualidade dos dados e exportação no formato `.parquet`.

* Validação automatizada de schemas, tratamento de codificações legadas e garantia de integridade dos dados.

* Modelo supervisionado de classificação, gerando scores de probabilidade de violação regulatória para cada conjunto elétrico no período subsequente.

* Painel interativo em Power BI para apoio à tomada de decisão de stakeholders.

### 4.2. Metodologia

O projeto segue as seis fases do framework **CRISP-DM**, com entregas iterativas e gerenciadas via quadro Kanban:

1. **Compreensão do Negócio (Business Understanding):** Mapeamento das regras regulatórias (PRODIST/ANEEL), impacto operacional das violações de DEC/FEC, definição de KPIs de negócio, métricas técnicas e escopo do projeto.

2. **Compreensão dos Dados (Data Understanding):** Ingestão das bases anuais, auditoria de integridade e Análise Exploratória de Dados (EDA) para identificação de padrões sazonais e outliers.

3. **Preparação dos Dados (Data Preparation):** Limpeza, padronização e estruturação do modelo dimensional.

4. **Modelagem (Modeling):** Desenvolvimento de modelagem preditiva com a seleção de algoritmos de classificação, validação cruzada temporal e engenharia de features temporais.

5. **Avaliação (Evaluation):** Auditoria das regras de agregação e validação de desempenho dos modelos.

6. **Implantação (Deployment):** Publicação dos Parquets processados com predições, conexão com o modelo dimensional no Power BI, consolidação da documentação técnica no repositório, e apresentação final.

### 4.3. Métricas de Avaliação e Benchmarks de Sucesso

1. **Qualidade e Integridade dos Dados:**
   * **Percentual de Valores Ausentes:** Registros sem preenchimento em campos críticos (`DEC`, `FEC`, `Limites` e `IDs de Conjunto`) inferiores a **1%**.

   * **Consistência Temporal e Duplicidade:** Manter **0%** de duplicidade na granularidade chave (`Conjunto` + `Mês/Ano`) em todo o histórico de 2021 a 2025.

   * **Taxa de Registros Válidos:** Pelo menos **98%** das linhas em conformidade com as regras operacionais da ANEEL.

2. **Eficácia da Análise e Visualização:**
   * **Cobertura Cadastral:** **100%** das distribuidoras e conjuntos elétricos da base processada navegáveis no painel.

   * **Identificação de Concentração:** Mapeamento quantitativo comprovando a concentração de horas excedentes nos conjuntos mais críticos.

   * **Performance e Navegação:** Painel em Power BI estruturado em *Star Schema* com filtros dinâmicos e tempo de resposta inferior a **5 segundos** por visual.

3. **Desempenho do Modelo Preditivo (Machine Learning):**
   * **Recall (Sensibilidade) $\ge 75\%$:** Capacidade de antecipar a maioria das transgressões reais antes do fechamento do mês, minimizando multas surpresa.

   * **Precisão $\ge 60\%$:** Garantir que pelo menos 3 a cada 5 alertas emitidos pelo modelo correspondam a problemas reais, evitando deslocamento inútil de equipes.

   * **F1-Score ($\ge 0,65$ a $0,70$):** Balanço harmônico entre capturar o risco regulatório e não saturar a operação com alarmes falsos.

   * **PR-AUC e ROC-AUC ($\ge 0,80$):** Capacidade geral do modelo de ordenar e separar corretamente os conjuntos de alto risco dos conjuntos estáveis.

   * **Matriz de Confusão Calibrada:** Ajuste do limiar de decisão (*threshold*) priorizando a redução expressiva de falsos negativos (transgressões não previstas).

4. **Impacto e Acionabilidade de Negócio**
    * **Foco no Top Risco (Lift Operacional):** O modelo deve concentrar pelo menos 60% das transgressões reais do mês seguinte dentro dos 20% dos conjuntos sinalizados com maior probabilidade de violação.

    * **Priorização Acionável:** Geração de um ranking mensal dos conjuntos elétricos com maior urgência de vistoria preventiva.

    * **Simulação de Horas de Interrupção Evitadas:** estimativa do volume de horas acumuladas de corte (DEC excedente) potencialmente mitigadas pela atuação preventiva tempestiva nos conjuntos sinalizados.

---

## 5. Entregáveis e Síntese Executiva
### 5.1. Entregáveis

1. **Código e documentação:** repositório versionado com o código, instruções de execução, documentação da arquitetura e notebooks do projeto.

2. **Dados processados:** pipeline de ingestão e transformação, validações de qualidade, dados intermediários e modelo dimensional em Parquet.

3. **Análises Exploratória de Dados:** notebook de análise exploratória dos dados para identificar padrões, tendências, sazonalidades e possíveis relações relevantes para o projeto.

4. **Painel Power BI:** arquivo `.pbix` conectado às tabelas processadas, com indicadores de continuidade, criticidade, transgressões e apoio à operação.

5. **Modelo de Machine Learning:** modelo treinado para estimar o risco de transgressão no período seguinte, acompanhado de métricas de avaliação e resultados das previsões.


### 5.2. Síntese Executiva 

 <div align="center">
   <img src=".\assets\data_canvas.png" width=100% alt="Canvas do Problema de Dados" />
   <sub>Canvas do Problema de Dados</sub><br /> 
   <sub>Fonte: Elaborado pelos autores</sub> 
 </div>
 