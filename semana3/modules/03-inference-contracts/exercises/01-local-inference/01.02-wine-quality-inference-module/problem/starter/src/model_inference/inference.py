"""Carga del modelo preentrenado e inferencia sobre características preparadas."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

import joblib

from model_inference.preprocess import FEATURE_NAMES, WineFeatures

DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")


class WineQualityEstimator(Protocol):
	"""Interfaz mínima requerida al clasificador serializado."""

	def predict(self, features: list[list[float]]) -> Sequence[str]:
		"""Devuelve una categoría por muestra."""

	def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
		"""Devuelve las probabilidades por categoría y muestra."""


@dataclass(frozen=True)
class LoadedWineModel:
	"""Clasificador cargado y versión declarada en el artefacto."""

	estimator: WineQualityEstimator
	model_version: str


def load_wine_quality_model(model_path: Path = DEFAULT_MODEL_PATH,) -> LoadedWineModel:
	"""Carga el artefacto y comprueba su contrato antes de usarlo."""

	if not model_path.is_file():
		raise FileNotFoundError(f"No se encontró el modelo en {model_path}.")

	payload = joblib.load(model_path)
	if not isinstance(payload, Mapping):
		raise ValueError("El artefacto debe contener metadatos y un clasificador compatible.")

	artifact_features = tuple(payload.get("feature_names", []))
	if artifact_features != FEATURE_NAMES:
		raise ValueError("Los feature_names del artefacto no coinciden con el contrato.")

	estimator = payload.get("estimator")
	model_version = payload.get("model_version")
	if not isinstance(model_version, str):
		raise ValueError("El artefacto no declara una versión de modelo válida.")
	if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
		raise ValueError("El artefacto no contiene un clasificador compatible.")

	return LoadedWineModel(
		estimator=cast(WineQualityEstimator, estimator),
		model_version=model_version,
	)


def infer_wine_quality( model: LoadedWineModel, features: WineFeatures,) -> tuple[str, float]:
	#Predice la categoría y su confianza para una muestra preprocesada.

	feature_vector = [features.as_vector()]
	quality_band = model.estimator.predict(feature_vector)[0]
	confidence = max(model.estimator.predict_proba(feature_vector)[0])
	return str(quality_band), round(float(confidence), 2)
