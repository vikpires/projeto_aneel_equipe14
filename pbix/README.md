# 📊 Dashboard Power BI — Energia em Risco

Este diretório contém o relatório desenvolvido em Power BI para o projeto de análise de continuidade do fornecimento de energia elétrica com dados da ANEEL.

## 🔗 Relatório Power BI

Acesse o relatório interativo:

[Visualizar relatório no Power BI](https://app.powerbi.com/links/-X4mTs0D8b?ctid=06655ccd-8dbf-433f-b20d-ee4f29227b59&pbi_source=linkShare)

> O acesso ao relatório pode exigir autenticação e permissão no Power BI Service.

## 📈 Páginas do relatório

- Resumo Executivo
- Diagnóstico das Interrupções
- Análise Territorial e Temporal
- Previsão e Prioridade de Ação

## 📌 Período analisado

2021–2025

## 🗂️ Principais tabelas utilizadas

### Dimensões
- dim_data
- dim_distribuidora
- dim_conjunto
- dim_indicador
- dim_tipo_interrupcao
- dim_motivo_interrupcao
- dim_causa_interrupcao

### Fatos
- fato_continuidade
- fato_causa_mensal

## 📊 Indicadores

- DEC
- FEC
- Limite regulatório
- Percentual do limite
- Quantidade de transgressões
- Índice de conformidade
- Conjuntos em transgressão
- Conjuntos críticos
- Contribuição estimada ao DEC
- Contribuição estimada ao FEC

## 🤖 Machine Learning

O projeto também contempla uma etapa de Machine Learning para classificação de risco e priorização de conjuntos com maior probabilidade de transgressão.

Principais métricas:
- ROC-AUC
- Precisão
- Recall
- F1-Score
- Matriz de confusão
- Importância das variáveis

## 📚 Fonte dos dados

Dados públicos disponibilizados pela Agência Nacional de Energia Elétrica — ANEEL.
