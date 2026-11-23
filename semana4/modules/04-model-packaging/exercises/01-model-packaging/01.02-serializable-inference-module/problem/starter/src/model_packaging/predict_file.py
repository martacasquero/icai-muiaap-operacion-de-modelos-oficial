"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""

    bundle = load_model_bundle(bundle_path)

    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != ["sample_id", *FEATURE_NAMES]:
            raise ValueError(f"Cabecera inesperada: {reader.fieldnames}")
        rows = list(reader)

    # 1. Validar e inferir todas las filas en memoria.
    results = []
    for row in rows:
        sample_id = row.pop("sample_id")
        request = WineQualityRequest.model_validate(row)
        prediction = infer_wine_quality(bundle, request)
        results.append({"sample_id": sample_id, **prediction.model_dump()})

    # 2. Solo si todo ha ido bien, escribir el CSV.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    return len(results)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
