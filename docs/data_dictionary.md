# Dicionário de Dados: Camada Raw
Este documento descreve o catálogo e os metadados das 5 fontes de dados brutas extraídas do **Portal de Dados Abertos da ANEEL** para o período de 2021 a 2025.

---

## 1. `raw_continuidade.parquet`

- **Fonte:** Indicadores coletivos de continuidade (DEC e FEC)
- **Periodicidade:** Mensal.
- **Granularidade:** Indicador por conjunto, indicador, ano e periodo
- **Descrição:** Fornece os valores apurados de continuidade do serviço de distribuição

| Coluna raw | Tipo observado | Descrição | 
| --- | --- | --- | 
| `DatGeracaoConjuntoDados` | DATE | Data de geração do conjunto de dados | 
| `IdeConjUndConsumidoras` | BIGINT | Identificador do conjunto da unidade consumidora |
| `DscConjUndConsumidoras` | VARCHAR | Descrição ou nome do conjunto | 
| `SigAgente` | VARCHAR | Sigla do agente ou distribuidora | 
| `NumCNPJ` | BIGINT | CNPJ da distribuidora na fonte |
| `SigIndicador` | VARCHAR | Sigla do tipo de indicador | 
| `AnoIndice` | BIGINT | Ano de referência do indicador. |
| `NumPeriodoIndice` | BIGINT | Período mensal do indicador, de 1 a 12 |
| `VlrIndiceEnviado` | DOUBLE | Valor do indicador enviado |

---

## 2. `raw_limites.csv`

- **Fonte:** Limites dos indicadores coletivos de continuidade.
- **Periodicidade:** Anual.
- **Granularidade:** Limite por distribuidora, conjunto, indicador e ano.
- **Descrição:** O conjunto de dados apresenta os limites dos indicadores coletivos de continuidade DEC e FEC.

| Coluna raw | Tipo na fonte | Descrição |
| --- | --- | --- | 
| `DatGeracaoConjuntoDados` | VARCHAR | Data de geração do conjunto de dados |
| `SigAgente` | VARCHAR | Sigla do agente ou distribuidora | 
| `NumCNPJ` | VARCHAR | CNPJ da distribuidora na fonte | 
| `IdeConjUndConsumidoras` | VARCHAR | Identificador do conjunto da unidade consumidora |
| `DscConjUndConsumidoras` | VARCHAR | Descrição ou nome do conjunto | 
| `SigIndicador` | VARCHAR | Sigla do tipo de indicador | 
| `AnoLimiteQualidade` | VARCHAR | Ano de referência do limite regulatório. |
| `VlrLimite` | VARCHAR | Valor máximo regulatório do indicador |

---

## 3. `raw_interrupcoes_{ANO}.parquet`

Arquivos recebidos para os anos de 2021 a 2025. Todos possuem a mesma estrutura de origem.

- **Fonte:** Interrupcões de energia elétrica nas redes de distribuição.
- **Periodicidade:** Mensal.
- **Granularidade:** Uma ocorrência de interrupção.
- **Descrição:** 

| Coluna raw | Tipo observado | Descrição | 
| --- | --- | --- | 
| `DatGeracaoConjuntoDados` | DATE | Data de geração do conjunto de dados |
| `IdeConjuntoUnidadeConsumidora` | BIGINT | Identificador do conjunto da unidade consumidora |
| `DscConjuntoUnidadeConsumidora` | VARCHAR | Descrição ou nome do conjunto |
| `DscAlimentadorSubestacao` | VARCHAR | Alimentador ou subestação associada | 
| `DscSubestacaoDistribuicao` | VARCHAR | Descrição da subestação de distribuição | 
| `NumOrdemInterrupcao` | VARCHAR | Número ou ordem do evento de interrupcao | 
| `DscTipoInterrupcao` | VARCHAR | Tipo operacional da interrupção | 
| `IdeMotivoInterrupcao` | BIGINT | Código do motivo da interrupção ou expurgo |
| `DatInicioInterrupcao` | TIMESTAMP | Data e hora de início do evento | 
| `DatFimInterrupcao` | TIMESTAMP | Data e hora de fim do evento | 
| `DscFatoGeradorInterrupcao` | VARCHAR | Descrição do fato gerador da interrupção. |
| `NumNivelTensao` | BIGINT | Nível de tensão associado ao evento em Volts. |
| `NumUnidadeConsumidora` | BIGINT | Quantidade de unidades consumidoras afetadas. |
| `NumConsumidorConjunto` | BIGINT | Quantidade de consumidores do conjunto |
| `NumAno` | BIGINT | Ano do evento |
| `NomAgenteRegulado` | VARCHAR | Nome do agente regulado | 
| `SigAgente` | VARCHAR | Sigla do agente ou distribuidora | 
| `NumCPFCNPJ` | BIGINT | CNPJ da distribuidora na fonte |

---

## 4. `raw_atributos.csv`

- **Fonte:** Atributos dos conjuntos de unidades consumidoras.
- **Periodicidade:** Mensal.
- **Granularidade:** Registro cadastral do conjunto.
- **Descrição:** O conjunto de dados apresenta os atributos físicos-elétricos dos conjuntos de unidades consumidoras.

| Coluna raw | Tipo na fonte | Descrição | 
| --- | --- | --- | 
| `DatGeracaoConjuntoDados` | VARCHAR | Data de geração do conjunto de dados |
| `SigAgente` | VARCHAR | Sigla do agente ou distribuidora. |
| `NumCNPJ` | VARCHAR | CNPJ da distribuidora |
| `IdeConjUndConsumidoras` | VARCHAR | Identificador do conjunto da unidade consumidora |
| `DscConjUndConsumidoras` | VARCHAR | Descrição do conjunto | 
| `SigIndicador` | VARCHAR | Sigla do tipo de indicador | 
| `AnoIndice` | VARCHAR | Ano de competência do índice |
| `NumPeriodoIndice` | VARCHAR | Período do índice, expresso em meses |
| `VlrIndiceEnviado` | VARCHAR | Valor do índice enviado |

---

## 5. `raw_regiao.csv`

- **Fonte:** Indicadores de municipio e região dos Conjuntos de Unidades Consumidoras.
- **Periodicidade:** Mensal.
- **Granularidade:** Registro de conjunto e municipio.
- **Descrição:** Conjunto de dados contendo a relação de municípios com a identificação do Identificador do Conjunto de Unidades Consumidoras.

| Coluna raw | Tipo na fonte | Descrição | 
| --- | --- | --- | 
| `DatGeracaoConjuntoDados` | VARCHAR | Data de geração do conjunto de dados |
| `IdeConjUnidConsumidoras` | VARCHAR | Identificador do conjunto da unidade consumidora |
| `CodMunicipio` | VARCHAR | Código do município cadastrado no IBGE |
| `NomMunicipio` | VARCHAR | Nome do municipio em que se situa o Empreendimento de Geração Distribuída | 
| `SigUF` | VARCHAR | Sigla das unidades federativa dos estados brasileiros | 

## Observações sobre a camada raw

- Os arquivos raw são preservados como recebidos, antes da padronização de nomes, tipos e valores.
- CNPJ, identificadores de conjunto, datas e valores numéricos podem chegar como texto ou número, dependendo do arquivo ou release.
- O pipeline aceita aliases de colunas para lidar com variações das fontes, mas não altera os arquivos raw.