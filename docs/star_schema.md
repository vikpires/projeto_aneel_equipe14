# Modelo Estrela (Star Schema)

Este documento descreve as tabelas dimensão e fato, além do modelo dimensional (Star Schema).

## Dimensões

* **dim_data:** Calendário contínuo no nível diário (2021–2025)

* **dim_distribuidora:** Concessionárias de distribuição de energia elétrica (identificadas por CNPJ e sigla)

* **dim_conjunto:** Conjuntos elétricos de unidades consumidoras, distribuidora responsável e localização regional

* **dim_indicador:** Indicadores de qualidade de continuidade do serviço (DEC e FEC)

* **dim_tipo_interrupcao:** Classificação operacional do evento (Programada vs. Não Programada)

* **dim_motivo_interrupcao:** Motivos regulatórios de expurgo da ANEEL (PRODIST Módulo 8)

* **dim_causa_interrupcao:** Classificação padronizada da origem, programação, grupo e causa detalhada da interrupção

## Fatos

* **fato_continuidade:** Indicadores mensais apurados de DEC e FEC confrontados com os limites regulatórios (grão mensal por conjunto e indicador)

* **fato_causa_mensal:** Agregação mensal por conjunto, tipo, motivo e causa, com volume de interrupções, duração, tensão, unidades afetadas e contribuições estimadas ao DEC/FEC

>[!WARNING]
>Não relacione fatos diretamente entre si. Use dimensões conformadas com cardinalidade 1:*.

---

## Modelo Conceitual
O modelo conceitual representa as entidades do domínio de distribuição de energia elétrica e suas relações de negócio.

```mermaid
erDiagram
    DISTRIBUIDORA ||--o{ CONJUNTO_ELETRICO : "atende"
    CONJUNTO_ELETRICO ||--|| LOCALIZACAO : "possui"
    CONJUNTO_ELETRICO ||--o{ INDICADOR_CONTINUIDADE : "tem apuração"
    INDICADOR_CONTINUIDADE }o--|| LIMITE_REGULATORIO : "é comparado a"
    CONJUNTO_ELETRICO ||--o{ INTERRUPCAO : "registra"
    INTERRUPCAO }o--|| CLASSIFICACAO_INTERRUPCAO : "é classificada por"
    TEMPO ||--o{ INDICADOR_CONTINUIDADE : "contextualiza"
    TEMPO ||--o{ INTERRUPCAO : "ocorre em"

    DISTRIBUIDORA {
        string agente
        string identificacao_fiscal
    }

    CONJUNTO_ELETRICO {
        string identificador
        string descricao
    }

    LOCALIZACAO {
        string municipio
        string uf
        string regiao
    }

    INDICADOR_CONTINUIDADE {
        string tipo_indicador
        decimal valor_apurado
    }

    LIMITE_REGULATORIO {
        string indicador
        decimal valor_limite
    }

    INTERRUPCAO {
        datetime inicio
        datetime fim
        decimal duracao
    }

    CLASSIFICACAO_INTERRUPCAO {
        string tipo
        string motivo
        string causa
    }

    TEMPO {
        date data_referencia
        int ano
        int mes
    }
```

---

## Star Schema
O Star Schema é a implementação física do modelo conceitual na camada `data/processed`. Ele organiza o modelo em dimensões e fatos relacionados por chaves primárias e estrangeiras, permitindo análises por tempo, distribuidora, conjunto, indicador, tipo, motivo e causa de interrupção.

```mermaid
erDiagram
    dim_data {
        int DataKey PK
        date Data
        smallint Ano
        tinyint MesNumero
        string MesNome
        string AnoMes
        string Trimestre
    }

    dim_distribuidora {
        bigint DistribuidoraKey PK
        string SigAgente
        string NumCNPJ
    }

    dim_conjunto {
        bigint ConjuntoKey PK
        bigint DistribuidoraKey FK
        string NumCNPJ
        bigint IdeConjunto
        string DscConjunto
        string CodMunicipio
        string Municipio
        string UF
        string Regiao
    }

    dim_indicador {
        tinyint IndicadorKey PK
        string SigIndicador
        string NomeIndicador
        string Unidade
    }

    dim_tipo_interrupcao {
        bigint TipoInterrupcaoKey PK
        string TipoInterrupcao
    }

    dim_motivo_interrupcao {
        bigint MotivoInterrupcaoKey PK
        int MotivoCodigo
        string MotivoDescricao
        tinyint EhExpurgada
    }

    dim_causa_interrupcao {
        bigint CausaKey PK
        string Origem
        string Programacao
        string GrupoCausa
        string CausaDetalhada
    }

    fato_continuidade {
        bigint FatoContinuidadeKey PK
        int DataKey FK
        bigint DistribuidoraKey FK
        bigint ConjuntoKey FK
        tinyint IndicadorKey FK
        double VlrIndicador
        double VlrLimite
        tinyint UltrapassouLimite
        double ExcessoSobreLimite
        double PercentualDoLimite
    }

    fato_causa_mensal {
        bigint FatoCausaMensalKey PK
        int DataKey FK
        bigint DistribuidoraKey FK
        bigint ConjuntoKey FK
        bigint TipoInterrupcaoKey FK
        bigint MotivoInterrupcaoKey FK
        bigint CausaKey FK
        double NivelTensao
        int QtdInterrupcoes
        double DuracaoTotalHoras
        double DuracaoMediaHoras
        double MaiorInterrupcaoHoras
        bigint UnidadesAfetadasSoma
        double ConsumidorHoras
        double ContribDEC_Estimada
        double ContribFEC_Estimada
    }

    dim_distribuidora ||--o{ dim_conjunto : "atende"

    dim_data ||--o{ fato_continuidade : "ocorre em"
    dim_distribuidora ||--o{ fato_continuidade : "apurado para"
    dim_conjunto ||--o{ fato_continuidade : "mede"
    dim_indicador ||--o{ fato_continuidade : "classifica indicador"

    dim_data ||--o{ fato_causa_mensal : "consolidado em"
    dim_distribuidora ||--o{ fato_causa_mensal : "pertence a"
    dim_conjunto ||--o{ fato_causa_mensal : "afeta"
    dim_tipo_interrupcao ||--o{ fato_causa_mensal : "tipo"
    dim_motivo_interrupcao ||--o{ fato_causa_mensal : "enquadrado em"
    dim_causa_interrupcao ||--o{ fato_causa_mensal : "origem"

  ```