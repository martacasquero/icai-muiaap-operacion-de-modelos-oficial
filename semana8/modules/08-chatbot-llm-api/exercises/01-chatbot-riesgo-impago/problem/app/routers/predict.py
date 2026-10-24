from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()

# TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)

@router.post("/predict", response_model=PrediccionSalida)
def predict(entrada: PrestamoEntrada):
    return predecir(entrada)

#Método y ruta: es un POST a /predict.
#response_model: lo que devuelves, la clase de salida del préstamo.
#entrada: lo que llega, la clase de entrada del préstamo. Como lleva extra="forbid" y los rangos, FastAPI devolverá 422 solo si llega edad: 200 o un campo inventado como pelo. Es lo que comprueban los tests.
#return: llama a tu función predecir con la entrada.