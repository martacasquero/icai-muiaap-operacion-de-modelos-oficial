"""CLI para validar un CSV y guardar predicciones del modelo de vino."""

import argparse
import csv
import sys
from pathlib import Path
from typing import Sequence

from pydantic import ValidationError

from model_inference.contracts import WineQualityPrediction, WineQualityRequest
from model_inference.inference import (
	DEFAULT_MODEL_PATH,
	infer_wine_quality,
	load_wine_quality_model,
)
from model_inference.preprocess import (
	PREPROCESSING_VERSION,
	preprocess_wine_request,
)

OUTPUT_COLUMNS = (
	"sample_id",
	"quality_band",
	"confidence",
	"model_version",
	"preprocessing_version",
)


def main(argv: Sequence[str] | None = None) -> int:
	"""Valida todas las filas antes de crear el archivo de salida."""

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--input", required=True, type=Path)
	parser.add_argument("--output", required=True, type=Path)
	parser.add_argument("--model", default=DEFAULT_MODEL_PATH, type=Path)
	args = parser.parse_args(argv)

	try:
		model = load_wine_quality_model(args.model)
		predictions: list[dict[str, str | float]] = []

		with args.input.open(newline="", encoding="utf-8") as source:
			reader = csv.DictReader(source)
			if reader.fieldnames is None:
				raise ValueError("El CSV de entrada no contiene una cabecera.")

			for line_number, row in enumerate(reader, start=2):
				sample_id = row.pop("sample_id", None)
				if not isinstance(sample_id, str) or not sample_id.strip():
					raise ValueError(
						f"Fila {line_number}: sample_id debe ser un texto no vacío."
					)

				try:
					request = WineQualityRequest.model_validate(row)
				except ValidationError as error:
					raise ValueError(f"Muestra {sample_id}: {error}") from error

				features = preprocess_wine_request(request)
				quality_band, confidence = infer_wine_quality(model, features)
				prediction = WineQualityPrediction(
					quality_band=quality_band,
					confidence=confidence,
					model_version=model.model_version,
					preprocessing_version=PREPROCESSING_VERSION,
				)
				predictions.append(
					{"sample_id": sample_id, **prediction.model_dump()}
				)

		with args.output.open("w", newline="", encoding="utf-8") as target:
			writer = csv.DictWriter(target, fieldnames=OUTPUT_COLUMNS)
			writer.writeheader()
			writer.writerows(predictions)
	except (OSError, ValueError, ValidationError) as error:
		print(f"Error: {error}", file=sys.stderr)
		return 2

	return 0


if __name__ == "__main__":
	raise SystemExit(main())

