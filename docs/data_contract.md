# Contrato de Dados

Este documento descreve como os conjuntos de dados da camada `data/raw` são convertidos em Parquet na camada `data/interim` pelos arquivos `src/sql/filter_*.sql`.

O período considerado pelo pipeline é de **2021** a **2025**. As transformações têm três objetivos principais:

- padronizar nomes e tipos
- preparar chaves e métricas para o modelo dimensional
- filtrar registros inválidos ou fora do escopo

A camada `interim` não é uma cópia integral dos arquivos raw. Algumas colunas são descartadas porque não participam do contrato usado pela modelagem dimensional.

---

## Sumário
- [1. Visão Geral](#1-visão-geral)
- [2. Regras Gerais](#2-regras-gerais)
- [3. Indicadores de continuidade](#3-indicadores-de-continuidade)
- [4. Interrupções](#4-interrupções)
- [5. Limites regulatórios](#5-limites-regulatórios)
- [6. Atributos dos conjuntos](#6-atributos-dos-conjuntos)
- [7. Região](#7-região)
- [8. Resumo das perdas e preservações](#8-resumo-das-perdas-e-preservações)
- [9. Modelo dimensional](#9-modelo-dimensional)

---

## 1. Visão geral

```text
raw_continuidade.parquet       -> continuidade_2021_2025.parquet
raw_interrupcoes_YYYY.parquet  -> interrupcoes_2021_2025.parquet
raw_limites.csv                -> limites_2021_2025.parquet
raw_atributos.csv              -> atributos.parquet
raw_regiao.csv                 -> regiao.parquet
```

O arquivo `transformer.py` resolve aliases de colunas antes de carregar cada SQL. Por isso, nomes como `NumCPFCNPJ` e `NumCNPJ` podem representar o mesmo campo lógico.

---

## 2. Regras gerais

### Normalização textual

Quando indicado pelo SQL:

- `TRIM` remove espaços nas extremidades;
- `UPPER(TRIM(...))` padroniza indicadores para maiúsculas;
- Valores textuais ausentes recebem um valor padrão, quando necessário;
- CNPJ é convertido para texto, caracteres não numéricos são removidos e o resultado é preenchido à esquerda com zeros até 14 posições.

### Conversão numérica

- `TRY_CAST` evita que um valor inválido interrompa toda a transformação, resultando em `NULL`;
- valores monetários ou decimais com vírgula usam `REPLACE(',', '.')` antes da conversão;
- números inteiros são convertidos para `INT`, `BIGINT` ou tipos equivalentes;
- valores decimais são arredondados para quatro casas quando representam métricas calculadas ou limites.

### Filtros

Os filtros comuns são:

- ano entre `2021` e `2025`;
- registros de continuidade apenas para `DEC` e `FEC`;
- períodos mensais entre 1 e 12, representanto os meses do ano;
- registros de limites apenas para `DEC` e `FEC`;
- registros de atributos com identificador de conjunto não nulo.

---

## 3. Indicadores de continuidade

### Origem e destino

```text
raw_continuidade.parquet
-> filter_continuidade.sql
-> continuidade_2021_2025.parquet
```

### Colunas raw observadas

| Coluna raw | Tipo observado | Tratamento | Coluna interim | Motivo |
|---|---:|---|---|---|
| `DatGeracaoConjuntoDados` | `DATE` | Não selecionada | Não existe | Data de geração do arquivo não é necessária para o fato de continuidade. |
| `IdeConjUndConsumidoras` | `BIGINT` | `CAST(... AS BIGINT)` | `IdeConjunto` | Padroniza o nome lógico usado nas dimensões e fatos. |
| `DscConjUndConsumidoras` | `VARCHAR` | `TRIM` | `DscConjunto` | Remove espaços e padroniza o contrato de descrição do conjunto. |
| `SigAgente` | `VARCHAR` | `TRIM` | `SigAgente` | Remove espaços sem alterar o valor de negócio. |
| `NumCNPJ` | `BIGINT` | Remove caracteres não numéricos, converte para texto e aplica `LPAD(..., 14, '0')` | `NumCNPJ` | Preserva zeros à esquerda e cria uma representação consistente do CNPJ. |
| `SigIndicador` | `VARCHAR` | `UPPER(TRIM(...))` | `SigIndicador` | Evita duplicações entre `dec`, `DEC` e variações com espaços. |
| `AnoIndice` | `BIGINT` | `CAST(... AS INT)` | `AnoIndice` | Reduz e padroniza o tipo do ano. |
| `NumPeriodoIndice` | `BIGINT` | `CAST(... AS INT)` | `NumPeriodoIndice` | Padroniza o tipo do mês/período. |
| `VlrIndiceEnviado` | `DOUBLE` | Conversão tolerante e `ROUND(..., 4)` | `VlrIndiceEnviado` | Mantém precisão e permite valores inválidos como `NULL`. |

### Saída interim

| Coluna | Tipo | Origem |
|---|---:|---|
| `AnoIndice` | `INTEGER` | `AnoIndice` raw |
| `NumPeriodoIndice` | `INTEGER` | `NumPeriodoIndice` raw |
| `SigAgente` | `VARCHAR` | `SigAgente` raw |
| `NumCNPJ` | `VARCHAR` | `NumCNPJ` raw normalizado |
| `IdeConjunto` | `BIGINT` | `IdeConjUndConsumidoras` |
| `DscConjunto` | `VARCHAR` | `DscConjUndConsumidoras` |
| `SigIndicador` | `VARCHAR` | `SigIndicador` normalizado |
| `VlrIndiceEnviado` | `DOUBLE` | `VlrIndiceEnviado` convertido |

### Colunas não agregadas

O SQL não agrega registros de continuidade. Cada linha permanece no grão original de conjunto, ano, período e indicador. A validação de duplicidades ocorre posteriormente no quality gate.

### Colunas descartadas

`DatGeracaoConjuntoDados` é descartada porque não participa do cálculo de DEC/FEC, da comparação com limites ou das chaves do fato de continuidade, sendo apenas um metadado da ANEEL.

---

## 4. Interrupções

### Origem e destino

```text
raw_interrupcoes_2021.parquet
raw_interrupcoes_2022.parquet
...
raw_interrupcoes_2025.parquet
-> filter_interrupcoes.sql
-> interrupcoes_2021_2025.parquet
```

Todos os arquivos anuais seguem o mesmo contrato. O transformer lê o padrão `raw_interrupcoes_*.parquet` e consolida o resultado em um único Parquet.

### Colunas raw observadas

| Coluna raw | Tipo observado | Tratamento | Coluna interim | Motivo |
|---|---:|---|---|---|
| `DatGeracaoConjuntoDados` | `DATE` | Não selecionada | Não existe | Metadado da fonte, não necessário para o evento de interrupção. |
| `IdeConjuntoUnidadeConsumidora` | `BIGINT` | `CAST(... AS BIGINT)` | `IdeConjunto` | Padroniza o identificador do conjunto. |
| `DscConjuntoUnidadeConsumidora` | `VARCHAR` | Não selecionada | Não existe | A descrição é obtida pela dimensão de conjunto; não é necessária em cada evento. |
| `DscAlimentadorSubestacao` | `VARCHAR` | Não selecionada | Não existe | Não participa das métricas atuais nem das dimensões implementadas. |
| `DscSubestacaoDistribuicao` | `VARCHAR` | Não selecionada | Não existe | Não participa do contrato atual do fato. |
| `NumOrdemInterrupcao` | `VARCHAR` | `CAST` e `TRIM`; nulo vira texto vazio | `NumOrdemInterrupcao` | Mantém o identificador do evento em formato estável. |
| `DscTipoInterrupcao` | `VARCHAR` | `TRIM`; nulo vira `NAO INFORMADO` | `DscTipoInterrupcao` | Preserva a classificação para a dimensão de tipo. |
| `IdeMotivoInterrupcao` | `BIGINT` | `TRY_CAST(... AS INT)` | `IdeMotivoInterrupcao` | Liga o evento à dimensão de motivos e tolera valores inválidos. |
| `DatInicioInterrupcao` | `TIMESTAMP` | `TRY_CAST` | `DatInicioInterrupcao` | Garante timestamp legível pelo DuckDB. |
| `DatFimInterrupcao` | `TIMESTAMP` | `TRY_CAST` | `DatFimInterrupcao` | Garante timestamp legível pelo DuckDB. |
| `DscFatoGeradorInterrupcao` | `VARCHAR` | `TRIM`; nulo vira `NAO INFORMADO` | `DscFatoGeradorInterrupcao` | Preserva a causa textual para normalização posterior. |
| `NumNivelTensao` | `BIGINT` | `TRY_CAST(... AS DOUBLE)` | `NumNivelTensao` | Permite valores decimais e evita falha por conversão inválida. |
| `NumUnidadeConsumidora` | `BIGINT` | `TRY_CAST(... AS BIGINT)` | `NumUnidadeConsumidora` | Padroniza unidades afetadas. |
| `NumConsumidorConjunto` | `BIGINT` | `TRY_CAST(... AS BIGINT)` | `NumConsumidorConjunto` | Padroniza consumidores do conjunto. |
| `NumAno` | `BIGINT` | `CAST(... AS INT)` | `AnoIndice` | Usa um nome comum ao restante do modelo. |
| `NomAgenteRegulado` | `VARCHAR` | Não selecionada | Não existe | `SigAgente` é o atributo utilizado no modelo atual. |
| `SigAgente` | `VARCHAR` | `TRIM` | `SigAgente` | Remove espaços sem alterar o identificador do agente. |
| `NumCPFCNPJ` | `BIGINT` | Remove caracteres não numéricos, converte para texto e aplica `LPAD(..., 14, '0')` | `NumCNPJ` | Padroniza o identificador da distribuidora. |

### Colunas calculadas

| Coluna interim | Regra |
|---|---|
| `NumPeriodoIndice` | Mês extraído de `DatInicioInterrupcao` com `EXTRACT(MONTH ...)`. |
| `DuracaoHoras` | Diferença entre início e fim em minutos dividida por 60, arredondada a quatro casas. |

### Colunas não agregadas

A transformação mantém uma linha por evento de interrupção. Não há `GROUP BY` nessa etapa, pois a granularidade transacional é necessária para análises de duração, eventos e causas.

A agregação mensal ocorre posteriormente em `fato_causa_mensal.sql`.

---

## 5. Limites regulatórios

### Origem e destino

```text
raw_limites.csv
-> filter_limites.sql
-> limites_2021_2025.parquet
```

### Colunas raw observadas

| Coluna raw | Tipo observado | Tratamento | Coluna interim | Motivo |
|---|---:|---|---|---|
| `DatGeracaoConjuntoDados` | `VARCHAR` | Não selecionada | Não existe | Metadado de geração, não parte da chave do limite. |
| `SigAgente` | `VARCHAR` | `TRIM` | `SigAgente` | Remove espaços. |
| `NumCNPJ` | `VARCHAR` | Remove caracteres não numéricos e aplica `LPAD(..., 14, '0')` | `NumCNPJ` | Padroniza a chave da distribuidora. |
| `IdeConjUndConsumidoras` | `VARCHAR` | `CAST(... AS BIGINT)` | `IdeConjunto` | Padroniza a chave do conjunto. |
| `DscConjUndConsumidoras` | `VARCHAR` | Não selecionada | Não existe | A descrição pertence à dimensão de conjunto. |
| `SigIndicador` | `VARCHAR` | `UPPER(TRIM(...))` | `SigIndicador` | Padroniza `DEC` e `FEC`. |
| `AnoLimiteQualidade` | `VARCHAR` | `CAST(... AS INT)` | `AnoIndice` | Usa o nome de ano comum ao modelo. |
| `VlrLimite` | `VARCHAR` | Troca vírgula por ponto, `TRY_CAST` e arredondamento | `VlrLimite` | Converte o formato textual brasileiro em métrica numérica. |

### Deduplicação

O SQL cria `ROW_NUMBER()` por:

```text
NumCNPJ + IdeConjunto + SigIndicador + AnoIndice
```

Somente `rn = 1` é mantido. Isso garante um limite por combinação lógica, mesmo que a fonte contenha linhas repetidas.

O `ORDER BY 1` não define preferência semântica entre duplicatas. Como melhoria futura, pode ser substituído por uma regra explícita, como data de atualização ou prioridade da fonte.

### Colunas não agregadas

O Parquet final não é uma agregação numérica. Ele é uma seleção deduplicada da primeira linha de cada chave lógica.

---

## 6. Atributos dos conjuntos

### Origem e destino

```text
raw_atributos.csv
-> filter_atributos.sql
-> atributos.parquet
```

### Colunas raw observadas

| Coluna raw | Tipo observado | Tratamento | Coluna interim | Motivo |
|---|---:|---|---|---|
| `DatGeracaoConjuntoDados` | `VARCHAR` | `TRY_CAST(... AS DATE)` | `DatGeracaoConjuntoDados` | Preserva a data mais recente disponível do cadastro. |
| `SigAgente` | `VARCHAR` | Mantida pelo `* EXCLUDE` | `SigAgente` | Atributo útil para identificar a distribuidora. |
| `NumCNPJ` | `VARCHAR` | Normalizado explicitamente | `NumCNPJ` | Chave de ligação com conjunto e distribuidora. |
| `IdeConjUndConsumidoras` | `VARCHAR` | Convertido explicitamente | `IdeConjunto` | Chave de ligação com o conjunto. |
| `DscConjUndConsumidoras` | `VARCHAR` | `TRIM` explicitamente | `DscConjunto` | Nome padronizado do conjunto. |
| `SigIndicador` | `VARCHAR` | Preservada pelo `* EXCLUDE` | `SigIndicador` | Mantida porque faz parte do arquivo recebido, embora não seja usada no join da dimensão de conjunto. |
| `AnoIndice` | `VARCHAR` | Preservada pelo `* EXCLUDE` | `AnoIndice` | Mantida para rastreabilidade do registro de origem. |
| `NumPeriodoIndice` | `VARCHAR` | Preservada pelo `* EXCLUDE` | `NumPeriodoIndice` | Mantida para rastreabilidade; não é convertida neste SQL. |
| `VlrIndiceEnviado` | `VARCHAR` | Preservada pelo `* EXCLUDE` | `VlrIndiceEnviado` | Mantida como valor original do arquivo de atributos. |

### Deduplicação

O SQL particiona por:

```text
NumCNPJ + IdeConjunto
```

E mantém a linha com a maior `DatGeracaoConjuntoDados` válida. Assim, o Parquet representa o cadastro mais recente de cada conjunto.

`SigIndicador`, `AnoIndice`, `NumPeriodoIndice` e `VlrIndiceEnviado` são preservadas pelo `* EXCLUDE` porque o arquivo de atributos contém uma estrutura semelhante à base de indicadores. O SQL ainda não os utiliza para enriquecer `dim_conjunto`, mas mantê-los preserva rastreabilidade e evita perda de informação na camada interim.

Como consequência, esses campos continuam textuais no Parquet de atributos. Se forem usados em análise numérica, devem receber uma transformação própria no futuro.

---

## 7. Região

### Origem e destino

```text
raw_regiao.csv
-> filter_regiao.sql
-> regiao.parquet
```

### Saída interim

| Coluna | Tipo | Regra |
|---|---:|---|
| `IdeConjunto` | `BIGINT` | Identificador do conjunto convertido para inteiro. |
| `CodMunicipio` | `BIGINT` | Código do município convertido para inteiro quando possível. |
| `Municipio` | `VARCHAR` | Texto aparado com `TRIM`. |
| `UF` | `VARCHAR` | Texto aparado e convertido para maiúsculas. |
| `Regiao` | `VARCHAR` | Região calculada a partir da UF; valores não mapeados recebem `NAO INFORMADO`. |

### Deduplicação e filtros

- Registros sem `IdeConjunto` são descartados.
- A saída mantém uma linha por `IdeConjunto`.
- Quando existem várias linhas para o mesmo conjunto, a primeira é escolhida por `CodMunicipio` e `Municipio` em ordem crescente.

---

## 8. Resumo das perdas e preservações

| Dataset | Campos calculados | Campos deduplicados | Campos descartados | Campos preservados sem alteração completa |
|---|---|---|---|---|
| Continuidade | Nenhum campo novo; apenas normalizações de tipo e texto | Nenhum | `DatGeracaoConjuntoDados` | Não há campos raw preservados sem transformação relevante. |
| Interrupções | `NumPeriodoIndice`, `DuracaoHoras` | Nenhum | `DatGeracaoConjuntoDados`, descrições cadastrais, subestação/alimentador, `NomAgenteRegulado` | Campos textuais e identificadores selecionados são mantidos após `TRIM`/conversão. |
| Limites | `rn` técnico, removido na saída | Chave de limite por ano/conjunto/indicador/distribuidora | `DatGeracaoConjuntoDados`, descrição do conjunto | `SigAgente` é apenas aparado. |
| Atributos | `rn` técnico, removido na saída | Cadastro mais recente por CNPJ/conjunto | Nenhuma das colunas extras do arquivo; campos extras são preservados | `SigIndicador`, `AnoIndice`, `NumPeriodoIndice`, `VlrIndiceEnviado` permanecem textuais. |
| Região | `rn` técnico, removido na saída; `Regiao` calculada pela UF | Um registro por `IdeConjunto` | Nenhuma além das linhas sem identificador de conjunto | `Municipio` e `UF` são preservados após normalização textual. |

---

## 9. Modelo dimensional

Os Parquets da camada `interim` alimentam o Star Schema gerado por `src/data/fato_dim.py`. As dimensões são criadas primeiro. Em seguida, os fatos usam suas chaves inteiras para estabelecer os relacionamentos. Os arquivos gerados são salvos na pasta `data/processed`.

### Dimensões

| Tabela | Granularidade | Chave principal | Colunas principais | Origem |
|---|---|---|---|---|
| `dim_data` | Um registro por dia entre 2021 e 2025 | `DataKey` | `Data`, `Ano`, `MesNumero`, `MesNome`, `AnoMes`, `Trimestre` | Calendário gerado por `generate_series`; não vem diretamente dos Parquets interim. |
| `dim_distribuidora` | Uma distribuidora por `NumCNPJ` | `DistribuidoraKey` | `SigAgente`, `NumCNPJ` | `NumCNPJ` e `SigAgente` de continuidade e interrupções. |
| `dim_conjunto` | Um conjunto por distribuidora e `IdeConjunto` | `ConjuntoKey` | `DistribuidoraKey`, `NumCNPJ`, `IdeConjunto`, `DscConjunto`, `CodMunicipio`, `NomMunicipio`, `SigUF`, `Regiao` | Continuidade e interrupções; a descrição é consolidada e os dados de localização vêm de `regiao.parquet`. |
| `dim_indicador` | Um registro por indicador | `IndicadorKey` | `SigIndicador`, `NomeIndicador`, `Unidade` | Catálogo estático de `DEC` e `FEC`. |
| `dim_tipo_interrupcao` | Um registro por tipo normalizado | `TipoInterrupcaoKey` | `TipoInterrupcao` | Interrupções; tipos padronizados como `PROGRAMADA`, `NAO PROGRAMADA` e `NAO INFORMADO`. |
| `dim_motivo_interrupcao` | Um registro por código regulatório | `MotivoInterrupcaoKey` | `MotivoCodigo`, `MotivoDescricao`, `EhExpurgada` | Catálogo estático de motivos da ANEEL. |
| `dim_causa_interrupcao` | Uma combinação distinta de causa normalizada | `CausaKey` | `Origem`, `Programacao`, `GrupoCausa`, `CausaDetalhada` | `DscFatoGeradorInterrupcao`, com normalização de caixa, acentos e separadores. |

#### Regras das dimensões

- `DistribuidoraKey` e `ConjuntoKey` são chaves inteiras substitutas; o CNPJ permanece como atributo técnico e de ligação.
- `IdeConjunto` permanece como identificador original inteiro da ANEEL.
- `CodMunicipio` é armazenado como `VARCHAR`, pois recebe `NÃO INFORMADO` quando não existe correspondência na dimensão de região.
- `NomMunicipio`, `SigUF` e `Regiao` recebem `NÃO INFORMADO` quando os dados de localização estão ausentes.
- `DatGeracaoConjuntoDados` não faz parte de `dim_conjunto`, pois não participa dos relacionamentos nem das métricas atuais.
- `TipoInterrupcaoKey` usa códigos pequenos e estáveis para os tipos normalizados.
- `MotivoInterrupcaoKey` usa o próprio `MotivoCodigo` regulatório.
- `CausaKey` é gerada para combinações distintas das categorias normalizadas de causa.

### Tabelas fato

| Tabela | Granularidade | Chave principal | Chaves estrangeiras | Conteúdo |
|---|---|---|---|---|
| `fato_continuidade` | Conjunto + mês + indicador | `FatoContinuidadeKey` | `DataKey`, `DistribuidoraKey`, `ConjuntoKey`, `IndicadorKey` | Valor apurado, limite, ultrapassagem, excesso e percentual do limite. |
| `fato_causa_mensal` | Mês + distribuidora + conjunto + tipo + motivo + causa | `FatoCausaMensalKey` | `DataKey`, `DistribuidoraKey`, `ConjuntoKey`, `TipoInterrupcaoKey`, `MotivoInterrupcaoKey`, `CausaKey` | `NivelTensao`, quantidade de interrupções, duração total, duração média, maior duração, unidades afetadas, consumidor-horas e contribuições estimadas. |

#### Regras dos fatos

- `fato_continuidade` relaciona apuração e limite pelo conjunto, indicador e ano.
- `fato_causa_mensal` agrega os eventos depois de normalizar e relacionar as dimensões.
- `fato_causa_mensal` contém `NivelTensao`, `QtdInterrupcoes`, `DuracaoTotalHoras`, `DuracaoMediaHoras`, `MaiorInterrupcaoHoras`, `UnidadesAfetadasSoma`, `ConsumidorHoras`, `ContribDEC_Estimada` e `ContribFEC_Estimada`.
- As chaves estrangeiras dos fatos vêm de joins com as dimensões, evitando hashes diferentes para o mesmo registro.
- `FatoContinuidadeKey` e `FatoCausaMensalKey` são identificadores técnicos determinísticos das linhas dos fatos.
- Os fatos volumosos são processados por ano para reduzir o uso de memória e depois consolidados em Parquet.

### Fluxo de relacionamento

```text
fato_continuidade
	-> dim_data
	-> dim_distribuidora
	-> dim_conjunto
	-> dim_indicador

fato_causa_mensal
	-> dim_data
	-> dim_distribuidora
	-> dim_conjunto
	-> dim_tipo_interrupcao
	-> dim_motivo_interrupcao
	-> dim_causa_interrupcao
```

As tabelas fato não devem ser relacionadas diretamente entre si. A análise deve utilizar as dimensões conformadas para preservar a granularidade de cada fato.
