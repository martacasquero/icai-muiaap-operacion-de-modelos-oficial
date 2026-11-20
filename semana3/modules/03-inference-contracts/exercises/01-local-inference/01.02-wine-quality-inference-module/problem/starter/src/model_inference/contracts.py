"""Contratos de entrada y salida de la inferencia de calidad del vino."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

QualityBand = Literal["needs_review", "acceptable", "excellent"]


class WineQualityRequest(BaseModel):
    """Las 11 características que consume el modelo.

    `sample_id` NO forma parte del contrato: identifica la fila, pero no es una
    característica. El CLI lo separa antes de validar.
    """

    model_config = ConfigDict(extra="forbid")

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=2)
    residual_sugar: float = Field(ge=0, le=20)
    chlorides: float = Field(ge=0, le=1)
    free_sulfur_dioxide: float = Field(ge=0, le=100)
    total_sulfur_dioxide: float = Field(ge=0, le=300)
    density: float = Field(ge=0.98, le=1.01)
    ph: float = Field(ge=2.5, le=4.5)
    sulphates: float = Field(ge=0, le=3)
    alcohol: float = Field(ge=5, le=20)


class WineQualityPrediction(BaseModel):
    """Resultado de una predicción, con trazabilidad de versiones."""

    quality_band: QualityBand
    confidence: float = Field(ge=0, le=1)
    model_version: str
    preprocessing_version: str
