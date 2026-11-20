import os
import json
import requests
from dotenv import load_dotenv

# Carga las variables del archivo .env (que NO se sube al repositorio)
load_dotenv()

# La clave se lee de la variable de entorno AEMET_API_KEY (no se escribe en el código)
API_KEY = os.environ.get("AEMET_API_KEY")
if not API_KEY:
    raise SystemExit("Falta la variable de entorno AEMET_API_KEY")

params = {"api_key": API_KEY}

# 1) Inventario de estaciones buscar el indicativo de MADRID, CIUDAD UNIVERSITARIA
URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

resp = requests.get(URL, params=params)
respuesta = resp.json()
# {'descripcion': 'exito', 'estado': 200, 'datos': '...', 'metadatos': '...'}

url_datos = respuesta["datos"]
resp2json = requests.get(url_datos).json()

for estacion in resp2json:
    if estacion.get("nombre") == "MADRID, CIUDAD UNIVERSITARIA":
        print(estacion["indicativo"])
# resultado: 3194U

# 2) Climatología diaria de la estación entre dos fechas
fecha_ini = "2019-10-01T00:00:00UTC"
fecha_fin = "2019-10-30T23:59:59UTC"
estacion = "3194U"

url_estacion = (
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/"
    f"fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{estacion}"
)

response_estacion = requests.get(url_estacion, params=params)
# No imprimir response_estacion.url: incluye la api_key en la URL
respuesta_estac = response_estacion.json()
print("respuesta de la estacion: ", respuesta_estac)

datos_json = requests.get(respuesta_estac["datos"]).json()
print("datos de la estacion: ", json.dumps(datos_json))