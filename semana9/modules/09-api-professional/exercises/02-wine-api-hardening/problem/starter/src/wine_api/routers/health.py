from fastapi import APIRouter, HTTPException

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import HealthResponse  # noqa: F401 - pista para S9.1d

from wine_api.schemas import ErrorResponse
SERVICE_NAME = "wine-quality-prediction"

# TODO S9.3a: declara `tags=["health"]` en el router, no en include_router().
router = APIRouter(tags=["health"])


# TODO S9.3b: añade `summary=`, `response_description=` y un docstring que diga
# cuándo usar el endpoint y qué significa un 503. Documenta el 503 con
# `responses={503: {"mod
# el": ErrorResponse, "description": ...}}`.
@router.get("/health", 
    summary="Check the health of the API", 
    response_description="Health status of the API", 
    responses={503: {"model": ErrorResponse, "description": "Model not ready"}}
)
def read_health(predictor: PredictorDep, request_id: RequestIdDep):
    # TODO S9.2f: sustituye el HTTPException por `ModelUnavailableError`: el
    # dominio no debería saber de HTTP y el manejador produce el sobre común.
    """
    Úsalo para comprobar si el servicio puede atender predicciones.

    - **200**: el servicio y el modelo están listos
    - **503**: el modelo no está cargado; la respuesta usa el error común
    """
    if not predictor.is_ready():
        raise ModelUnavailableError()
    # TODO S9.1d: declara `-> HealthResponse` y devuelve una instancia.
    
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        model_status="ready",
        model_version=predictor.model_version,
        request_id=request_id,
    )
