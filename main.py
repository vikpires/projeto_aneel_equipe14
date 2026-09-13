import logging
import time
from datetime import datetime

from src.config import INTERIM_DIR, PROCESSED_DIR, RAW_DIR
from src.data.extractor import run_extract_data
from src.data.transformer import run_transform_data
from src.data.fato_dim import run_fato_dim
from src.data.quality_raw import validate_raw_tables
from src.data.quality_interim import validate_interim_tables
from src.data.quality_processed import validate_processed_tables
from src.utils.time_formatter import set_time_formatter


# Orquestrador local do pipeline de download, processamento, validação de qualidade dos datasets e modelagem dimensional.
def main() -> None:

    start_time = time.time()

    logging.info(
        "Início: %s",
        datetime.fromtimestamp(start_time).strftime("%d/%m/%Y %H:%M:%S"),
    )

    # 1. Ingestão de dados
    logging.info("[1/6] Iniciando ingestão de dados...")
    run_extract_data()
    logging.info("Ingestão de dados concluída! Verifique a pasta %s.", RAW_DIR)

    # 2. Quality gate das fontes brutas
    logging.info("[2/6] Iniciando quality gate das fontes brutas...")
    validate_raw_tables()
    logging.info("Quality gate das fontes brutas concluída.")

    # 3. Processamento via DuckDB
    logging.info("[3/6] Iniciando processamento via DuckDB...")
    run_transform_data()
    logging.info("Processamento concluído! Verifique a pasta %s.", INTERIM_DIR)

    # 4. Quality gate dos dados intermediários
    logging.info("[4/6] Iniciando quality gate dos dados intermediários...")
    validate_interim_tables()
    logging.info("Quality gate dos dados intermediários concluída.")

    # 5. Geração do modelo dimensional (fato e dimensões)
    logging.info("[5/6] Iniciando geração do modelo dimensional (fato e dimensões)...")
    run_fato_dim()
    logging.info(
        "Geração do modelo dimensional concluída! Verifique a pasta %s.", PROCESSED_DIR
    )

    # 6. Quality gate dos artefatos finais
    logging.info("[6/6] Iniciando quality gate dos artefatos finais...")
    validate_processed_tables()
    logging.info("Quality gate dos artefatos finais concluída.")

    end_time = time.time()
    tempo_total = end_time - start_time

    logging.info(
        "Fim: %s",
        datetime.fromtimestamp(end_time).strftime("%d/%m/%Y %H:%M:%S"),
    )
    logging.info("Tempo total: %s", set_time_formatter(tempo_total))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main()
