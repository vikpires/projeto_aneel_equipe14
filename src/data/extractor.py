import logging
import time

from src.config import DATASETS, RAW_DIR
from src.utils.download_utils import download_stream
from src.utils.manifesto import write_manifest

logger = logging.getLogger(__name__)


# Executar o processo de ingestão de dados.
def run_extract_data() -> None:
    tempo_inicio = time.time()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Download do Arquivo Raw de Continuidade (arquivo único)
    logger.info("--- Baixando Dataset de Continuidade ---")
    download_stream(
        DATASETS["continuidade"]["url"], DATASETS["continuidade"]["raw_path"]
    )

    # 2. Download dos Arquivos Raw de Interrupções (em lote por ano)
    logger.info("--- Baixando Datasets de Interrupções (2021 a 2025) ---")
    for ano, url in DATASETS["interrupcoes"]["urls"].items():
        destino_ano = RAW_DIR / f"raw_interrupcoes_{ano}.parquet"
        logger.info("-> Baixando base de %s...", ano)
        download_stream(url, destino_ano)

    # 3. Download do Arquivo Raw de Limites (arquivo único)
    logger.info("--- Baixando Dataset de Limites ---")
    download_stream(DATASETS["limites"]["url"], DATASETS["limites"]["raw_path"])

    # 4. Download do Arquivo Raw de Atributos (arquivo único)
    logger.info("--- Baixando Dataset de Atributos ---")
    download_stream(DATASETS["atributos"]["url"], DATASETS["atributos"]["raw_path"])

    # 5. Região e UF dos conjuntos
    logger.info("--- Baixando Dataset de Região ---")
    download_stream(DATASETS["regiao"]["url"], DATASETS["regiao"]["raw_path"])

    tempo_execucao = time.time() - tempo_inicio
    manifest_path = write_manifest(
        RAW_DIR,
        "raw",
        fonte="ANEEL",
        tempo_execucao_segundos=round(tempo_execucao, 2),
    )
    logger.info("Manifesto raw gerado: %s", manifest_path)


if __name__ == "__main__":
    run_extract_data()
