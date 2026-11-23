"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)
from model_packaging.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    preprocess_wine_request,
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""


class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""

    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version=PREPROCESSING_VERSION,
        feature_names=FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__,
    )


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""

    if manifest is None:
        raise ValueError("Hace falta un manifiesto: usa create_manifest().")

    bundle_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(estimator, bundle_path / MODEL_FILENAME)
    (bundle_path / MANIFEST_FILENAME).write_text(manifest.model_dump_json(indent=2))
    return manifest


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""

    # 1. Primero el manifiesto.
    data = json.loads((bundle_path / MANIFEST_FILENAME).read_text())
    manifest = ArtifactManifest.model_validate(data)

    if manifest.schema_version != ARTIFACT_SCHEMA_VERSION:
        raise ValueError("schema_version no soportada.")
    if manifest.preprocessing_version != PREPROCESSING_VERSION:
        raise ValueError("preprocessing_version incompatible.")
    if manifest.feature_names != FEATURE_NAMES:
        raise ValueError("feature_names no coincide con el preprocesado.")
    if manifest.output_labels != OUTPUT_LABELS:
        raise ValueError("output_labels no coincide con el contrato.")

    # 2. Después el modelo.
    estimator = joblib.load(bundle_path / MODEL_FILENAME)
    if not hasattr(estimator, "predict") or not hasattr(estimator, "predict_proba"):
        raise ValueError("El estimador no tiene predict() y predict_proba().")

    return LoadedModelBundle(estimator=estimator, manifest=manifest)


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""

    features = [preprocess_wine_request(request).as_vector()]
    label = bundle.estimator.predict(features)[0]
    confidence = max(bundle.estimator.predict_proba(features)[0])

    # WineQualityPrediction rechaza etiquetas fuera de QualityBand.
    return WineQualityPrediction(
        quality_band=label,
        confidence=confidence,
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version,
    )
