from __future__ import annotations
import logging
from pathlib import Path
import shutil
import sys
import time
import duckdb

from src.config import (
    CONT_PATH,
    INT_PATH,
    INTERIM_DIR as DEFAULT_INPUT_DIR,
    LIM_PATH,
    ATR_PATH,
    REG_PATH,
    PROCESSED_DIR as DEFAULT_OUTPUT_DIR,
)
from src.data.constants import (
    ANO_FIM,
    ANO_INICIO,
    DUCKDB_MEMORY_LIMIT,
    DUCKDB_PRESERVE_INSERTION_ORDER,
    DUCKDB_THREADS,
    PARQUET_COMPRESSION,
    PIPELINE_TABLES,
)
from src.utils.sql_loader import load_sql_query
from src.utils.time_formatter import set_time_formatter
from src.utils.manifesto import write_manifest

logger = logging.getLogger(__name__)


# Executa fatos volumosas particionadas por ano para proteger a memória.
def _executar_fato_anual(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    target_parquet: Path,
    anos: list[int],
    params: dict,
) -> None:
    temp_table = f"temp_{table_name}"
    con.execute(f"DROP TABLE IF EXISTS {temp_table};")

    for a_idx, ano in enumerate(anos):
        t_sub = time.time()
        logger.info("Ano %s (%s/%s)...", ano, a_idx + 1, len(anos))

        query_ano = load_sql_query(table_name, ano=ano, **params).strip()
        if query_ano.endswith(";"):
            query_ano = query_ano[:-1]

        if a_idx == 0:
            con.execute(f"CREATE TEMP TABLE {temp_table} AS {query_ano};")
        else:
            con.execute(f"INSERT INTO {temp_table} {query_ano};")

        logger.info("Ano %s concluído (%.1fs)", ano, time.time() - t_sub)

    logger.info("Exportando Parquet consolidado...")
    con.execute(
        f"COPY {temp_table} TO '{target_parquet.resolve().as_posix()}' "
        f"(FORMAT PARQUET, COMPRESSION {PARQUET_COMPRESSION});"
    )
    con.execute(f"DROP TABLE IF EXISTS {temp_table};")


# Executa a modelagem dimensional completa
def run_fato_dim(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    ano_inicio: int = ANO_INICIO,
    ano_fim: int = ANO_FIM,
    force_rebuild: bool = False,
) -> Path:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = input_dir.parent / "temp_duckdb"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Identificação dos quatro Parquets dentro do diretório de entrada.
    def input_path(configured_path: Path, default_name: str) -> Path:
        expected_path = input_dir / default_name
        configured_name_path = input_dir / configured_path.name
        return expected_path if expected_path.exists() else configured_name_path

    cont_path = input_path(
        Path(CONT_PATH), f"continuidade_{ano_inicio}_{ano_fim}.parquet"
    )
    int_path = input_path(
        Path(INT_PATH), f"interrupcoes_{ano_inicio}_{ano_fim}.parquet"
    )
    limites_path = input_path(Path(LIM_PATH), Path(LIM_PATH).name)
    atributos_path = input_path(Path(ATR_PATH), Path(ATR_PATH).name)
    regiao_path = input_path(Path(REG_PATH), Path(REG_PATH).name)

    # Validação de integridade dos arquivos intermediários
    arquivos_obrigatorios = [
        ("Continuidade", cont_path),
        ("Interrupções", int_path),
        ("Limites", limites_path),
        ("Atributos", atributos_path),
        ("Região", regiao_path),
    ]
    faltando = [
        f"- {rotulo}: {p.as_posix()}"
        for rotulo, p in arquivos_obrigatorios
        if not p.exists()
    ]
    if faltando:
        raise FileNotFoundError(
            "Arquivos ausentes na pasta interim:\n" + "\n".join(faltando)
        )

    # Parâmetros injetados em data/sql/*.sql
    params = {
        "continuidade_path": cont_path.resolve().as_posix(),
        "interrupcoes_path": int_path.resolve().as_posix(),
        "limites_path": limites_path.resolve().as_posix(),
        "atributos_path": atributos_path.resolve().as_posix(),
        "regiao_path": regiao_path.resolve().as_posix(),
        "output_dir": output_dir.resolve().as_posix(),
        "ano_inicio": ano_inicio,
        "ano_fim": ano_fim,
    }

    con = duckdb.connect()
    con.execute(f"SET memory_limit = '{DUCKDB_MEMORY_LIMIT}';")
    con.execute(f"SET threads = {DUCKDB_THREADS};")
    con.execute(f"SET temp_directory = '{temp_dir.resolve().as_posix()}';")
    con.execute(
        f"SET preserve_insertion_order = {str(DUCKDB_PRESERVE_INSERTION_ORDER).lower()};"
    )

    total_tabelas = len(PIPELINE_TABLES)
    tempo_inicio_total = time.time()
    anos = list(range(ano_inicio, ano_fim + 1))

    logger.info("Iniciando modelagem Star Schema (%s tabelas)", total_tabelas)
    logger.info("Destino: %s", output_dir.resolve())

    try:
        for idx, table_name in enumerate(PIPELINE_TABLES, start=1):
            pct_macro = ((idx - 1) / total_tabelas) * 100
            target_parquet = output_dir / f"{table_name}.parquet"

            if target_parquet.exists() and not force_rebuild:
                logger.info(
                    "[%02d/%02d] (%4.1f%%) Pulando (já existe): %s.parquet",
                    idx,
                    total_tabelas,
                    pct_macro,
                    table_name,
                )
                continue

            t_etapa = time.time()
            logger.info(
                "[%02d/%02d] (%4.1f%%) Gerando: %s.parquet...",
                idx,
                total_tabelas,
                pct_macro,
                table_name,
            )

            # Fatos volumosas processadas em lotes anuais
            if table_name == "fato_causa_mensal":
                _executar_fato_anual(con, table_name, target_parquet, anos, params)
            else:
                query = load_sql_query(table_name, **params).strip()
                if query.endswith(";"):
                    query = query[:-1]

                con.execute(
                    f"COPY ({query}) "
                    f"TO '{target_parquet.resolve().as_posix()}' "
                    f"(FORMAT PARQUET, COMPRESSION {PARQUET_COMPRESSION});"
                )

            tempo_etapa = time.time() - t_etapa
            tempo_acumulado = time.time() - tempo_inicio_total
            logger.info(
                "Concluído em %s (Total: %s)",
                set_time_formatter(tempo_etapa),
                set_time_formatter(tempo_acumulado),
            )

        tempo_total = time.time() - tempo_inicio_total
        logger.info(
            "Modelagem Star Schema concluída com sucesso em %s!",
            set_time_formatter(tempo_total),
        )

        manifest_path = write_manifest(
            output_dir,
            "processed",
            motor="duckdb_sql_files",
            tempo_execucao_segundos=round(tempo_total, 2),
            total_tabelas=len(list(output_dir.glob("*.parquet"))),
        )
        logger.info("Manifesto processed gerado: %s", manifest_path)
        return output_dir

    finally:
        con.close()
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    rebuild = "--force" in sys.argv
    run_fato_dim(force_rebuild=rebuild)
