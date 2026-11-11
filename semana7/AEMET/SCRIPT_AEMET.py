import requests
import json
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJ0YWNhc3F1ZXJvb0BnbWFpbC5jb20iLCJqdGkiOiIyY2EzMDFlMy04NzA2LTQzMjMtODMyZC05ZDY5NDc0ZjQ5NWUiLCJleHAiOjE4MDE2Njc1NzMsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzkzMDI3NTczLCJ1c2VySWQiOiIyY2EzMDFlMy04NzA2LTQzMjMtODMyZC05ZDY5NDc0ZjQ5NWUiLCJyb2xlIjoiIn0.IRusrnqgtd9QW6lDRoWFlxwP2MgafJYpSOhCEkF6xPY"
URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

headers = {"api_key": API_KEY}

resp = requests.get(URL, headers=headers)
#print(resp)

#print((resp.json()))
# {'descripcion': 'exito', 'estado': 200, 
# 'datos': 'https://opendata.aemet.es/opendata/sh/d0cd68f4', 
# 'metadatos': 'https://opendata.aemet.es/opendata/sh/0556af7a'}

respuesta = resp.json()
url_datos = respuesta["datos"]
#print(url_datos)
respuesta2 = requests.get(url_datos)
resp2json = respuesta2.json()

#print(json.dumps(resp2json))
for estacion in resp2json:
    if estacion.get("nombre") == "MADRID, CIUDAD UNIVERSITARIA":
        print(estacion["indicativo"])

#resultado 3194U estacion 

#url climatologia del indicador 
# 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios
# /datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{idema}'

#datos añadir 2019 10 01T00 00 00UTC fecha ini 
#fecha fin 2019 10 30T23 59 59UTC

fecha_ini = "2019-10-01T00:00:00UTC"
fecha_fin = "2019-10-31T23:59:59UTC"
estacion = "3194U"

url_estacion = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{estacion}")

response_estacion = requests.get(url_estacion,headers=headers)
respuesta_estac = response_estacion.json()
print(respuesta_estac)

#'descripcion': "El campo fecha final inicial tener formato: 'AAAA-MM-DDTHH:MM:SSUTC'", 'estado': 400}