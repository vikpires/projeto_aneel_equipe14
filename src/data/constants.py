# Período de análise do projeto
ANO_INICIO = 2021
ANO_FIM = 2025
MAX_NULL_PERCENTAGE = 1.0

# Nomes alternativos aceitos para as colunas das fontes de dados.
COLUMN_CANDIDATES = {
    "col_cnpj": ["NumCPFCNPJ", "NumCNPJ", "cnpj"],
    "col_conj": [
        "IdeConjuntoUnidadeConsumidora",
        "IdeConjUndConsumidoras",
        "IdeConjUnidConsumidoras",
        "id_conjunto",
    ],
    "col_desc": [
        "DscConjUndConsumidoras",
        "DscConjuntoUnidadeConsumidora",
        "nome_conjunto",
    ],
    "col_motivo": [
        "IdeMotivoInterrupcao",
        "IdeMotivoExpurgo",
        "id_motivo",
    ],
    "col_fato": [
        "DscFatoGeradorInterrupcao",
        "FatGeradorInterrupcao",
        "fato_gerador",
    ],
    "col_ordem": ["NumOrdemInterrupcao", "num_ordem"],
}

# Colunas obrigatórias para cada transformação de dados.
REQUIRED_COLUMNS = {
    "filter_continuidade": ("col_cnpj", "col_conj", "col_desc"),
    "filter_interrupcoes": (
        "col_cnpj",
        "col_conj",
        "col_motivo",
        "col_fato",
        "col_ordem",
    ),
    "filter_limites": ("col_cnpj", "col_conj"),
    "filter_atributos": ("col_cnpj", "col_conj", "col_desc"),
    "filter_regiao": ("col_conj",),
}

# Ordem estrita de dependência: Dimensões primeiro, Fatos depois
PIPELINE_TABLES = [
    "dim_data",
    "dim_distribuidora",
    "dim_conjunto",
    "dim_indicador",
    "dim_tipo_interrupcao",
    "dim_motivo_interrupcao",
    "dim_causa_interrupcao",
    "fato_continuidade",
    "fato_causa_mensal",
]

# Configuracões fixas usadas pela modelagem dimensional no DuckDB.
DUCKDB_MEMORY_LIMIT = "4GB"  # Ajuste conforme a capacidade do seu sistema
DUCKDB_THREADS = 4  # Ajuste conforme a capacidade do seu sistema
DUCKDB_PRESERVE_INSERTION_ORDER = False
PARQUET_COMPRESSION = "ZSTD"

# Consultas SQL para validação de qualidade dos dados intermediários (interim)
QUERY_CONTINUIDADE_INTERIM_VALIDATE = """
    SELECT COUNT(*), MIN(AnoIndice), MAX(AnoIndice),
        COUNT(*) FILTER (WHERE IdeConjunto IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE VlrIndiceEnviado IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE VlrIndiceEnviado < 0),
        COUNT(*) FILTER (WHERE NumPeriodoIndice IS NULL)
    FROM read_parquet(?)
    """

QUERY_DUPLICATE_INTERIM_VALIDATE = """
    SELECT COUNT(*)
    FROM (
        SELECT IdeConjunto, AnoIndice, NumPeriodoIndice, SigIndicador
        FROM read_parquet(?)
        GROUP BY IdeConjunto, AnoIndice, NumPeriodoIndice, SigIndicador
        HAVING COUNT(*) > 1
    ) duplicadas
    """

QUERY_INTERRUPTIONS_INTERIM_VALIDATE = """
    SELECT COUNT(*), MIN(AnoIndice), MAX(AnoIndice),
        COUNT(*) FILTER (WHERE IdeConjunto IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE DatInicioInterrupcao IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE DuracaoHoras IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE NumConsumidorConjunto IS NULL) * 100.0 / COUNT(*),
        COUNT(*) FILTER (WHERE DuracaoHoras < 0),
        COUNT(*) FILTER (WHERE DatFimInterrupcao < DatInicioInterrupcao),
        COUNT(*) FILTER (WHERE NumConsumidorConjunto < 0)
    FROM read_parquet(?)
    """
