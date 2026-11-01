 
from fastapi import APIRouter

from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import PredictionRequest, PredictionResponse, VALID_FEATURES_EXAMPLE ,ErrorResponse,Prediction
from typing import Annotated
from datetime import UTC, datetime
from fastapi import APIRouter, Body
# TODO S9.3a: mueve aquí `prefix="/v1/predictions"` y `tags=["predictions"]`.
# TODO S9.3c: declara a nivel de router `responses=` para 400, 422 y 503 con
# `{"model": ErrorResponse, "description": ...}`. Así el 422 deja de
# documentarse como `HTTPValidationError`, que ya no es lo que devolvemos.

router = APIRouter(prefix="/v1/predictions",tags=["predictions"],responses={
    400: {"model": ErrorResponse, "description": "servidor no ha podido procesar la solicitud enviada por el cliente"},
    422: {"model": ErrorResponse, "description": "validation error or invalid input"},
    503 : {"model": ErrorResponse, "description": "model_unavailable"}

})

PREDICTION_EXAMPLES = {

    "valid": {"summary": "vINO válido", "value": {"features":VALID_FEATURES_EXAMPLE}},
    "missing_field": {
        "summary": "Inválido: no se ha insertado alcohol", 
        "description": "falta un valor para el campo alcohol. Devuelve 422", 
        "value":{"features": {k: v for k, v in VALID_FEATURES_EXAMPLE.items() if k != "alcohol"}}},
    "wrong type" : {
        "summary": "Inválido: ph no numérico",
        "description": "ph es un texto en vez de un número. Devuelve 422",
        "value": {"features": {**VALID_FEATURES_EXAMPLE, "ph": "abc"}},
    }
}

@router.post("",
             summary= "crea una predicción pls",
             response_description= "objeto de tipo Prediction Response con quality band confidence y version"
)
def create_prediction(
    payload: Annotated[
        PredictionRequest,
        Body(openapi_examples= PREDICTION_EXAMPLES)
    ],
    predictor: PredictorDep,
    request_id: RequestIdDep,
) -> PredictionResponse:
    # TODO S9.3e: añade summary, response_description y un docstring útil para
    # quien consume la API (campos, rangos, decimales de confidence).

    #El docstring va dentro de la función, como primera línea del cuerpo y entre comillas triples.

    '''devuelve una predicción para el PredictionRequest recibido 
    quality_band: uno de los valores de QualityBand 
    confidence: float entre 0 y 1, redondeado a 2 dec
    model_version: version del modelo que produce la prediccion 
    preprocessing_version: version del preprocesado aplicado a la enrtada. ''' 

    # TODO S9.3f: ofrece en Swagger al menos tres ejemplos de cuerpo (uno válido
# y dos inválidos). Investiga `Annotated[PredictionRequest, Body(...)]` con
    # `openapi_examples=`; usa VALID_FEATURES_EXAMPLE como base.

    output = predictor.predict(payload.features)
    # TODO S9.1e: este dict expone `raw_score` y la confianza sin redondear.
    #Declara `-> PredictionResponse` y construye el modelo; para pasar de la
    #dataclass ModelOutput a Prediction investiga `from_attributes=True`.
    #return PredictionResponse({"prediction": asdict(output), "request_id": request_id})
    return PredictionResponse(
        prediction=Prediction.model_validate(output),
        request_id=request_id,
        served_at= datetime.now(UTC)

    )

