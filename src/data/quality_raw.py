import logging
from pathlib import Path
import duckdb

from src.config import DATASETS, RAW_DIR, CONT_PATH
from src.utils.manifesto import validate_manifest

logger = logging.getLogger(__name__)


# Valida a existência e o schema mínimo das tabelas brutas, intermediárias e finais do pipeline de dados.
def _read_columns(connection, path: Path) -> set[str]:
    if path.suffix.lower() != ".csv":
        reader = "read_parquet(?)"
        rows = connection.execute(
            f"DESCRIBE SELECT * FROM {reader}", [str(path)]
        ).fetchall()
        return {row[0] for row in rows}

    last_error = None
    for encoding in ("utf-8", "cp1252"):
        try:
            rows = connection.execute(
                "DESCRIBE SELECT * FROM read_csv_auto(?, encoding=?, header=true)",
                [str(path), encoding],
            ).fetchall()
            return {row[0] for row in rows}
        except duckdb.Error as error:
            last_error = error

    raise last_error


# Valida a existência e o schema mínimo das tabelas brutas, intermediárias e finais do pipeline de dados.
def _require_raw_columns(
    connection, path: Path, candidates: tuple[tuple[str, ...], ...]
) -> None:
    columns = {column.lower() for column in _read_columns(connection, path)}
    missing = [
        "/".join(options)
        for options in candidates
        if not any(option.lower() in columns for option in options)
    ]
    if missing:
        raise ValueError(f"Colunas ausentes em {path.name}: {', '.join(missing)}")


# Valida a existência e o schema mínimo das tabelas brutas, intermediárias e finais do pipeline de dados.
def validate_raw_tables(raw_dir: Path | str = RAW_DIR) -> None:
    raw_dir = Path(raw_dir)
    interruption_years = DATASETS["interrupcoes"]["urls"]
    expected_files = {
        raw_dir
        / "raw_continuidade.parquet": (
            ("AnoIndice",),
            ("NumCPFCNPJ", "NumCNPJ", "cnpj"),
            (
                "IdeConjuntoUnidadeConsumidora",
                "IdeConjUndConsumidoras",
                "IdeConjunto",
                "id_conjunto",
            ),
            ("SigIndicador",),
        ),
        raw_dir
        / "raw_limites.csv": (
            ("AnoLimiteQualidade", "AnoIndice"),
            ("NumCPFCNPJ", "NumCNPJ", "cnpj"),
            (
                "IdeConjuntoUnidadeConsumidora",
                "IdeConjUndConsumidoras",
                "IdeConjunto",
                "id_conjunto",
            ),
        ),
        raw_dir
        / "raw_atributos.csv": (
            ("DatGeracaoConjuntoDados",),
            ("NumCPFCNPJ", "NumCNPJ", "cnpj"),
            (
                "IdeConjuntoUnidadeConsumidora",
                "IdeConjUndConsumidoras",
                "IdeConjunto",
                "id_conjunto",
            ),
        ),
        raw_dir
        / "raw_regiao.csv": (
            ("IdeConjUnidConsumidoras", "IdeConjunto"),
            ("CodMunicipio",),
            ("NomMunicipio",),
            ("SigUF",),
        ),
    }
    for year in interruption_years:
        expected_files[raw_dir / f"raw_interrupcoes_{year}.parquet"] = (
            ("NumAno", "AnoIndice"),
            ("NumCPFCNPJ", "NumCNPJ", "cnpj"),
            (
                "IdeConjuntoUnidadeConsumidora",
                "IdeConjUndConsumidoras",
                "IdeConjunto",
                "id_conjunto",
            ),
            ("DatInicioInterrupcao",),
            ("DatFimInterrupcao",),
        )

    with duckdb.connect() as connection:
        for path, candidates in expected_files.items():
            if not path.is_file() or path.stat().st_size == 0:
                raise FileNotFoundError(f"Arquivo raw ausente ou vazio: {path}")
            _require_raw_columns(connection, path, candidates)

    validate_manifest(
        raw_dir,
        (path.name for path in expected_files),
        "raw",
    )

    logger.info("Quality gate raw aprovado: %s arquivos", len(expected_files))
