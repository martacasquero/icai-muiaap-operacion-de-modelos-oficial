"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

from pydantic import ValidationError

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityPrediction, WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES

ID_COLUMN = "sample_id"
INPUT_COLUMNS = (ID_COLUMN, *FEATURE_NAMES)
OUTPUT_COLUMNS = (ID_COLUMN, *WineQualityPrediction.model_fields)


def _read_requests(input_path: Path) -> list[tuple[str, WineQualityRequest]]:
    """Lee y valida todas las filas antes de inferir nada."""

    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        header = tuple(reader.fieldnames or ())
        if set(header) != set(INPUT_COLUMNS) or len(header) != len(INPUT_COLUMNS):
            missing = sorted(set(INPUT_COLUMNS) - set(header))
            extra = sorted(set(header) - set(INPUT_COLUMNS))
            raise ValueError(
                f"Cabecera inválida en {input_path}: faltan {missing}, sobran {extra}."
            )

        requests: list[tuple[str, WineQualityRequest]] = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"Línea {line_number}: hay más valores que columnas.")
            sample_id = (row.pop(ID_COLUMN) or "").strip()
            if not sample_id:
                raise ValueError(f"Línea {line_number}: sample_id vacío.")
            try:
                request = WineQualityRequest.model_validate(row)
            except ValidationError as error:
                raise ValueError(
                    f"Línea {line_number} ({sample_id}) inválida:\n{error}"
                ) from error
            requests.append((sample_id, request))

    if not requests:
        raise ValueError(f"{input_path} no contiene filas.")
    return requests


def _write_atomically(output_path: Path, rows: list[dict[str, object]]) -> None:
    """Escribe en un temporal y lo renombra para no dejar CSV parciales."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        newline="",
        encoding="utf-8",
        delete=False,
    ) as target:
        temporary = Path(target.name)
        writer = csv.DictWriter(target, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    try:
        os.replace(temporary, output_path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """Valida todas las filas y escribe el CSV solo al final."""

    input_path, output_path = Path(input_path), Path(output_path)
    bundle = load_model_bundle(Path(bundle_path))
    requests = _read_requests(input_path)

    rows: list[dict[str, object]] = []
    for sample_id, request in requests:
        try:
            prediction = infer_wine_quality(bundle, request)
        except ValueError as error:
            raise ValueError(f"Muestra {sample_id}: {error}") from error
        rows.append({ID_COLUMN: sample_id, **prediction.model_dump()})

    _write_atomically(output_path, rows)
    return len(rows)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


def main() -> int:
    """Ejecuta el CLI y traduce errores de contrato a código de salida."""

    arguments = parse_args()
    try:
        count = predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    except (ValueError, FileNotFoundError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"{count} predicciones escritas en {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
