"""S9.4 — Tests que escribe el alumnado.

Cada test empieza en rojo con `pytest.fail`. Sustituye esa línea por el test
real; la entrega se considera completa cuando toda la suite está en verde.
"""

import pytest
from fastapi.testclient import TestClient

from wine_api.dependencies import get_predictor  # noqa: F401 - pista S9.4a
from wine_api.predictor import UnavailablePredictor  # noqa: F401 - pista S9.4a
import json
from pathlib import Path

from wine_api.export_openapi import render_openapi

CONTRACT_PATH = Path(__file__).parents[1] / "contracts" / "openapi.json" #esta es la ruta del contrato 


def test_prediction_returns_503_when_model_is_unavailable(
    client: TestClient, valid_payload: dict
) -> None:
    # TODO S9.4a: sin tocar el código de la API, haz que `get_predictor`
    # devuelva un UnavailablePredictor con `app.dependency_overrides` (llega
    # desde `client.app`). Comprueba status 503 y `error.code`. Limpia el
    # override al terminar para no contaminar otros tests.
    
    app = client.app
    app.dependency_overrides[get_predictor] =lambda: UnavailablePredictor()
    try:
        response = client.post("/v1/predictions", json=valid_payload)
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "model_unavailable"
    finally:
        app.dependency_overrides.pop(get_predictor, None)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("alcohol", 4.99), #justo por debajo de 5 
        ("ph", 4.51), #justo por encima de 4.5
        ("chlorides", None),
        ("total_sulfur_dioxide","abc"),
        ("volatile_acidity",-0.01)

    ],
)
def test_out_of_contract_values_are_rejected(
    client: TestClient, valid_payload: dict , field:str , value:object 
) -> None:
    # TODO S9.4b: convierte este test en `@pytest.mark.parametrize` con al
    # menos cinco casos (justo por debajo y por encima de un rango, None, un
    # texto...). Para cada uno comprueba 422 y que `fields` señala exactamente
    # `features.<campo>`.

    payload = {"features": {**valid_payload["features"], field: value}}

    response = client.post("/v1/predictions", json=payload)

    assert response.status_code == 422
    body = response.json()
    errors = body["error"]["fields"]
    names = []
    for error in errors:
        names.append(error["field"])

    assert names == [f"features.{field}"]

 
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("alcohol", 5), #justo  5 
        ("alcohol", 20), #justo  20
         
    ],
)
def test_range_limits_are_inclusive(client: TestClient, valid_payload: dict, field: str,value : object) -> None:
    # TODO S9.4c: los límites del contrato son inclusivos. Demuéstralo con los
    # dos extremos de `alcohol` (5 y 20): ambos deben devolver 200.


    payload = {"features": {**valid_payload["features"], field: value}}

    response = client.post("/v1/predictions", json=payload)
    assert response.status_code == 200
     



def test_openapi_matches_versioned_contract() -> None:
    ## TODO S9.4d: genera `contracts/openapi.json` con
    ## `uv run python -m wine_api.export_openapi` y versiónalo en Git. Después
    ## compara el JSON de `render_openapi()` con el archivo: si alguien cambia el
    ## contrato sin querer, este test lo detecta en la revisión.
    expected = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    actual = json.loads(render_openapi())

    assert actual == expected