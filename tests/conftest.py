import io
import pytest
import duckdb
import zipfile

from src.data.constants import PIPELINE_TABLES
from src.utils.manifesto import write_manifest
from tests.constants import (
    QUERY_PROCESSED_FIXTURE,
    QUERY_FACT_DIM_ATRIBUTOS,
    QUERY_FACT_DIM_CONTINUIDADE,
    QUERY_FACT_DIM_INTERRUPCOES,
    QUERY_FACT_DIM_LIMITES,
    QUERY_FACT_DIM_REGIAO,
)


# Classe FakeResponse para simular respostas de requisições HTTP durante os testes
class FakeResponse:
    def __init__(self, chunks, error=None, headers=None):
        self.chunks = chunks
        self.error = error
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def raise_for_status(self):
        if self.error:
            raise self.error

    def iter_content(self, chunk_size):
        return iter(self.chunks)


# Fornece a classe FakeResponse durante os testes
@pytest.fixture
def response_factory():
    return FakeResponse


@pytest.fixture
def zip_response_factory():
    def create_response(files):
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w") as archive:
            for file_name, content in files.items():
                archive.writestr(file_name, content)
        return FakeResponse([archive_buffer.getvalue()])

    return create_response


# Cria e gerencia a conexão com o DuckDB durante a sessão de testes
@pytest.fixture(scope="session")
def db_connection():
    con = duckdb.connect()
    yield con
    con.close()


@pytest.fixture
def star_schema_inputs(tmp_path):
    input_dir = tmp_path / "interim"
    output_dir = tmp_path / "processed"
    input_dir.mkdir()

    paths_and_queries = {
        "continuity_path": (
            input_dir / "continuidade.parquet",
            QUERY_FACT_DIM_CONTINUIDADE,
        ),
        "interruptions_path": (
            input_dir / "interrupcoes.parquet",
            QUERY_FACT_DIM_INTERRUPCOES,
        ),
        "limits_path": (input_dir / "limites.parquet", QUERY_FACT_DIM_LIMITES),
        "attributes_path": (
            input_dir / "atributos.parquet",
            QUERY_FACT_DIM_ATRIBUTOS,
        ),
        "region_path": (
            input_dir / "regiao.parquet",
            QUERY_FACT_DIM_REGIAO.replace("NomMunicipio", "Municipio").replace(
                "SigUF", "UF"
            ),
        ),
    }

    con = duckdb.connect()
    try:
        for path, query in paths_and_queries.values():
            con.sql(query).write_parquet(str(path))
    finally:
        con.close()

    write_manifest(input_dir, "interim")

    return {
        "input_dir": input_dir,
        "output_dir": output_dir,
        **{name: path for name, (path, _) in paths_and_queries.items()},
    }


@pytest.fixture
def raw_inputs(tmp_path):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    connection = duckdb.connect()
    try:
        connection.sql(QUERY_FACT_DIM_CONTINUIDADE).write_parquet(
            str(raw_dir / "raw_continuidade.parquet")
        )
        for year in range(2021, 2026):
            connection.sql(QUERY_FACT_DIM_INTERRUPCOES).write_parquet(
                str(raw_dir / f"raw_interrupcoes_{year}.parquet")
            )
        for file_name, query in {
            "raw_limites.csv": QUERY_FACT_DIM_LIMITES,
            "raw_atributos.csv": QUERY_FACT_DIM_ATRIBUTOS,
            "raw_regiao.csv": QUERY_FACT_DIM_REGIAO,
        }.items():
            target = (raw_dir / file_name).as_posix().replace("'", "''")
            connection.execute(f"COPY ({query}) TO '{target}' (FORMAT CSV, HEADER)")
    finally:
        connection.close()
    write_manifest(raw_dir, "raw")
    return raw_dir


@pytest.fixture
def processed_tables_output(tmp_path):
    output_dir = tmp_path / "processed"
    output_dir.mkdir()
    connection = duckdb.connect()
    try:
        for table_name in PIPELINE_TABLES:
            path = output_dir / f"{table_name}.parquet"
            connection.sql(QUERY_PROCESSED_FIXTURE).write_parquet(str(path))
    finally:
        connection.close()

    write_manifest(
        output_dir,
        "processed",
        motor="duckdb_sql_files",
        total_tabelas=len(PIPELINE_TABLES),
    )
    return output_dir
