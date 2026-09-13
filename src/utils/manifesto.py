from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable

MANIFEST_FILENAME = "_manifesto.json"


# Escreve um manifesto JSON no diretório especificado, contendo informações sobre os arquivos presentes e metadados adicionais.
def write_manifest(
    directory: Path,
    layer: str,
    *,
    status: str = "SUCCESS",
    manifest_filename: str = MANIFEST_FILENAME,
    **metadata: Any,
) -> Path:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.name not in {manifest_filename, ".gitkeep"}
    )
    manifest = {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "camada": layer,
        "status": status,
        "total_arquivos": len(files),
        "arquivos": [path.name for path in files],
        "tamanhos_bytes": {path.name: path.stat().st_size for path in files},
        "extensoes": {path.name: path.suffix.lower() for path in files},
        **metadata,
    }

    manifest_path = directory / manifest_filename
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest_path


# Valida o contrato do manifesto JSON para uma camada de dados, verificando a presença de arquivos esperados e consistência de metadados.
def validate_manifest(
    directory: Path,
    expected_files: Iterable[str] | None,
    layer: str,
    *,
    manifest_filename: str = MANIFEST_FILENAME,
) -> dict[str, Any]:
    directory = Path(directory)
    manifest_path = directory / manifest_filename
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifesto ausente: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "SUCCESS":
        raise ValueError(f"Manifesto da camada {layer} não indica sucesso")
    if manifest.get("camada") != layer:
        raise ValueError(
            f"Camada inválida no manifesto: esperado {layer}, "
            f"encontrado {manifest.get('camada')}"
        )

    actual = {
        path.name
        for path in directory.iterdir()
        if path.is_file() and path.name not in {manifest_filename, ".gitkeep"}
    }
    expected = actual if expected_files is None else set(expected_files)
    listed = set(manifest.get("arquivos", []))
    missing_files = sorted(expected - listed)
    if missing_files:
        raise FileNotFoundError(
            f"Arquivos ausentes no manifesto de {layer}: {', '.join(missing_files)}"
        )

    unexpected_files = sorted(listed - expected)
    if unexpected_files:
        raise ValueError(
            f"Arquivos inesperados no manifesto de {layer}: "
            f"{', '.join(unexpected_files)}"
        )

    missing_from_directory = sorted(listed - actual)
    if missing_from_directory:
        raise FileNotFoundError(
            f"Arquivos listados no manifesto de {layer} não encontrados: "
            f"{', '.join(missing_from_directory)}"
        )

    if manifest.get("total_arquivos") != len(listed):
        raise ValueError(f"Total de arquivos inconsistente no manifesto de {layer}")

    return manifest
