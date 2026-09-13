from __future__ import annotations
import logging
from pathlib import Path
import time
import duckdb

from src.config import DATASETS, INTERIM_DIR
from src.data.constants import (
    ANO_FIM,
    ANO_INICIO,
    COLUMN_CANDIDATES,
    DUCKDB_THREADS,
    DUCKDB_PRESERVE_INSERTION_ORDER,
    PARQUET_COMPRESSION,
    REQUIRED_COLUMNS,
    DUCKDB_MEMORY_LIMIT,
)
from src.utils.sql_loader import (
    detect_csv_encoding,
    load_sql_query,
    resolve_column_name,
)
from src.utils.manifesto import write_manifest

logger = logging.getLogger(__name__)


# Processar os dados brutos e gerar arquivos intermediários no formato Parquet.
def transform_data(
    con: duckdb.DuckDBPyConnection,
    query_name: str,
    raw_path: Path | str,
    out_path: Path | str,
    force: bool = False,
    **kwargs,
) -> None:
    raw_str = raw_path.as_posix() if isinstance(raw_path, Path) else str(raw_path)
    out_path_obj = Path(out_path)
    out_str = out_path_obj.resolve().as_posix()
    out_name = out_path_obj.name

    out_path_obj.parent.mkdir(parents=True, exist_ok=True)
    if out_path_obj.is_file() and out_path_obj.stat().st_size > 0 and not force:
        logger.info("[CACHE] Arquivo intermediário já existe: %s", out_name)
        return

    logger.info(
        "[DUCKDB] Processando pipeline via '%s.sql' -> %s...",
        query_name,
        out_name,
    )

    required_columns = REQUIRED_COLUMNS.get(query_name, tuple(COLUMN_CANDIDATES))
    resolved_columns = {
        name: resolve_column_name(con, raw_str, COLUMN_CANDIDATES[name])
        for name in required_columns
    }
    csv_encoding = (
        detect_csv_encoding(raw_str) if Path(raw_str).suffix.lower() == ".csv" else None
    )

    sql_query = load_sql_query(
        query_name=query_name,
        raw_path=raw_str,
        csv_encoding=csv_encoding,
        **resolved_columns,
        **kwargs,
    ).strip()

    if sql_query.endswith(";"):
        sql_query = sql_query[:-1]

    copy_statement = f"""
        COPY ({sql_query})
        TO '{out_str}'
        (FORMAT PARQUET, COMPRESSION {PARQUET_COMPRESSION});
    """
    con.execute(copy_statement)
    logger.info("[SUCESSO] Gerado: %s", out_name)


def run_transform_data(force: bool = False) -> None:
    tempo_inicio = time.time()
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect() as con:
        # Configurações de performance para evitar estouro de memória
        con.execute(f"SET memory_limit = {DUCKDB_MEMORY_LIMIT};")
        con.execute(f"SET threads = {DUCKDB_THREADS};")
        con.execute(
            f"SET preserve_insertion_order = {DUCKDB_PRESERVE_INSERTION_ORDER};"
        )

        # 1. Continuidade (DEC / FEC Apurados)
        logger.info("--- Processando Continuidade via DuckDB ---")
        transform_data(
            con=con,
            query_name=DATASETS["continuidade"]["query_name"],
            raw_path=DATASETS["continuidade"]["raw_path"],
            out_path=DATASETS["continuidade"]["out_path"],
            force=force,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
        )

        # 2. Limites Regulatórios ANEEL
        logger.info("--- Processando Limites Regulatórios via DuckDB ---")
        transform_data(
            con=con,
            query_name=DATASETS["limites"]["query_name"],
            raw_path=DATASETS["limites"]["raw_path"],
            out_path=DATASETS["limites"]["out_path"],
            force=force,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
        )

        # 3. Atributos dos Conjuntos
        logger.info("--- Processando Atributos dos Conjuntos via DuckDB ---")
        transform_data(
            con=con,
            query_name=DATASETS["atributos"]["query_name"],
            raw_path=DATASETS["atributos"]["raw_path"],
            out_path=DATASETS["atributos"]["out_path"],
            force=force,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
        )

        # 4. Regiões dos Conjuntos
        logger.info("--- Processando Regiões dos Conjuntos via DuckDB ---")
        transform_data(
            con=con,
            query_name=DATASETS["regiao"]["query_name"],
            raw_path=DATASETS["regiao"]["raw_path"],
            out_path=DATASETS["regiao"]["out_path"],
            force=force,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
        )

        # 5. Histórico de Interrupções
        logger.info("--- Processando Interrupções (Consolidado) via DuckDB ---")
        raw_interrupcoes = DATASETS["interrupcoes"].get(
            "raw_pattern", DATASETS["interrupcoes"].get("raw_path")
        )
        transform_data(
            con=con,
            query_name=DATASETS["interrupcoes"]["query_name"],
            raw_path=raw_interrupcoes,
            out_path=DATASETS["interrupcoes"]["out_path"],
            force=force,
            ano_inicio=ANO_INICIO,
            ano_fim=ANO_FIM,
        )

    tempo_execucao = time.time() - tempo_inicio
    manifest_path = write_manifest(
        INTERIM_DIR,
        "interim",
        motor="duckdb_sql_files",
        periodo={"ano_inicio": ANO_INICIO, "ano_fim": ANO_FIM},
        tempo_execucao_segundos=round(tempo_execucao, 2),
    )
    logger.info("Manifesto interim gerado: %s", manifest_path)


if __name__ == "__main__":
    run_transform_data()
