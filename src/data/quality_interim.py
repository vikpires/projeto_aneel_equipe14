import logging
from pathlib import Path
import duckdb

from src.config import CONT_PATH, INT_PATH, REG_PATH
from src.data.constants import (
    ANO_FIM,
    ANO_INICIO,
    MAX_NULL_PERCENTAGE,
    QUERY_CONTINUIDADE_INTERIM_VALIDATE,
    QUERY_DUPLICATE_INTERIM_VALIDATE,
    QUERY_INTERRUPTIONS_INTERIM_VALIDATE,
)
from src.utils.manifesto import validate_manifest

logger = logging.getLogger(__name__)


# Valida as colunas obrigatórias e a integridade das tabelas intermediárias antes da modelagem dimensional.
def _require_columns(connection, path: Path, required_columns: set[str]) -> None:
    columns = {
        row[0]
        for row in connection.execute(
            "DESCRIBE SELECT * FROM read_parquet(?)", [str(path)]
        ).fetchall()
    }
    missing_columns = sorted(required_columns - columns)
    if missing_columns:
        raise ValueError(
            f"Colunas ausentes em {path.name}: {', '.join(missing_columns)}"
        )


# Valida os Parquets intermediários antes da modelagem dimensional.
def validate_interim_tables() -> None:
    required_inputs = {
        Path(CONT_PATH): {
            "AnoIndice",
            "NumPeriodoIndice",
            "IdeConjunto",
            "SigIndicador",
            "VlrIndiceEnviado",
        },
        Path(INT_PATH): {
            "AnoIndice",
            "IdeConjunto",
            "DatInicioInterrupcao",
            "DatFimInterrupcao",
            "DuracaoHoras",
            "NumConsumidorConjunto",
        },
        Path(REG_PATH): {
            "IdeConjunto",
            "CodMunicipio",
            "Municipio",
            "UF",
            "Regiao",
        },
    }
    for path in required_inputs:
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Arquivo intermediário ausente ou vazio: {path}")

    validate_manifest(Path(CONT_PATH).parent, None, "interim")

    with duckdb.connect() as connection:
        for path, required_columns in required_inputs.items():
            _require_columns(connection, path, required_columns)

        continuity = connection.execute(
            QUERY_CONTINUIDADE_INTERIM_VALIDATE,
            [str(CONT_PATH)],
        ).fetchone()
        if continuity is None or continuity[0] == 0:
            raise ValueError("Tabela intermediária de continuidade vazia")
        if continuity[1] < ANO_INICIO or continuity[2] > ANO_FIM:
            raise ValueError("Anos da continuidade fora do período configurado")
        if any(value > MAX_NULL_PERCENTAGE for value in continuity[3:5]):
            raise ValueError("Percentual de nulos acima do limite na continuidade")
        if continuity[5] or continuity[6]:
            raise ValueError("Falha de integridade na continuidade")

        duplicate_continuity = connection.execute(
            QUERY_DUPLICATE_INTERIM_VALIDATE,
            [str(CONT_PATH)],
        ).fetchone()
        if duplicate_continuity and duplicate_continuity[0] > 0:
            raise ValueError("Duplicidade encontrada na continuidade")

        interruptions = connection.execute(
            QUERY_INTERRUPTIONS_INTERIM_VALIDATE,
            [str(INT_PATH)],
        ).fetchone()
        if interruptions is None or interruptions[0] == 0:
            raise ValueError("Tabela intermediária de interrupções vazia")
        if interruptions[1] < ANO_INICIO or interruptions[2] > ANO_FIM:
            raise ValueError("Anos das interrupções fora do período configurado")
        if any(value > MAX_NULL_PERCENTAGE for value in interruptions[3:7]):
            raise ValueError("Percentual de nulos acima do limite nas interrupções")
        if any(interruptions[7:]):
            raise ValueError("Falha de integridade nas interrupções")

    logger.info("Quality gate intermediário aprovado")
