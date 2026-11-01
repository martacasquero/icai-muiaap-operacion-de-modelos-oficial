"""Punto de entrada de la API: `fastapi dev` usa `wine_api.main:app`."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wine_api.errors import install_error_handlers
from wine_api.predictor import Predictor, build_predictor
from wine_api.request_id import request_id_middleware
from wine_api.routers import health, predictions

# TODO S9.3g: completa los metadatos que lee el consumidor en /docs:
# `version` (¿mayor, menor o parche tras S9.1c?), `summary`, una `description`
# en Markdown que explique `request_id` y el sobre de error, y `openapi_tags`
# con una descripción por tag. Comprobación: tests/test_s9_3_openapi.py
API_VERSION = "1.1.0"
API_SUMMARY = "API para predecir la calidad del vino"
API_DESCRIPTION = """
Esta API permite predecir la calidad del vino basándose en sus características físicas y químicas.

### Request ID
Cada respuesta incluye un campo `request_id`, que coincide con la cabecera `X-Request-Id`
y permite rastrear la solicitud a través del sistema.
### Error Response
Todos los errores usan el mismo sobre:
`{"error": {"code": ..., "message": ..., "fields": [...]}, "request_id": ...}`.
`fields` solo aparece en errores de validación.

"""

def create_app(predictor: Predictor | None = None) -> FastAPI:
    """Crea la aplicación; los tests inyectan su propio predictor."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.predictor = predictor or build_predictor(
            os.environ.get("WINE_API_MODE", "ready")
        )
        yield

    app = FastAPI(title="Wine Quality API", 
                  version=API_VERSION, 
                  description=API_DESCRIPTION,
                  lifespan=lifespan,
                  openapi_tags=[
                      {"name": "health", "description": "Endpoints relacionados con la salud del servicio"},
                      {"name": "predictions", "description": "Endpoints para realizar predicciones de calidad del vino"}
                  ],
                  summary=API_SUMMARY
                  )
    app.middleware("http")(request_id_middleware)
    install_error_handlers(app)
    app.include_router(health.router)
    app.include_router(predictions.router)
    return app


app = create_app()
