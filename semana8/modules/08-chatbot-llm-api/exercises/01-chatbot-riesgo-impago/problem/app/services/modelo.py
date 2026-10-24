import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida

# Orden en el que el modelo espera las variables
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

# TODO: cargar el modelo joblib una sola vez, al importar el modulo
modelo= joblib.load(MODEL_PATH)
# TODO: funcion decidir(probabilidad) -> "aprobar", "revisar" o "rechazar" (umbrales en el enunciado)
def decidir (probabilidad): 
    #Decisión según la probabilidad: menor de 0,2 → aprobar; 
    # menor de 0,5 → revisar; resto → rechazar.
    if probabilidad < 0.2 : 
        return "aprobar"
    elif probabilidad < 0.5 and probabilidad >= 0.2 : 
        return "revisar"
    else : 
        return "rechazar"
# TODO: funcion predecir(entrada) -> PrediccionSalida, usando VARIABLES para ordenar los valores

def predecir(entrada):
    fila = []
    for nombre in VARIABLES:
        fila.append(getattr(entrada,nombre))                

    probabilidad = modelo.predict_proba([fila])[0][1]                   # paso 2: modelo.predict_proba(...)[0][1]

    return PrediccionSalida(              
        probabilidad_impago=float(probabilidad),
        decision=decidir(probabilidad),                    # usa tu función decidir
    )
