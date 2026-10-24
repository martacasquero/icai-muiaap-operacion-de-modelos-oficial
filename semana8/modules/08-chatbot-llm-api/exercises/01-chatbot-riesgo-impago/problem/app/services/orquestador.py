import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir
NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada

def definir_tool():
    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,                                
            "description": "Calcula el riesgo del impago",      
            "parameters": PrestamoEntrada.model_json_schema(),  
        },
    }

# TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)

def ejecutar_tool(nombre,argumentos_json):
    if nombre != NOMBRE_TOOL: 
        return {"ok":False,"error":"el nombre no coincide con el nombre de la tool"}
    datos = leer_argumentos(argumentos_json)
    try:
        entrada = PrestamoEntrada(**datos)
    except ValidationError as error:
        return {"ok": False, "error": str(error)}

    prediccion_salida = predecir(entrada) #esto es un oBJ PrediccionSalida con dos campos 
    return {"ok":True, "probabilidad_impago" : prediccion_salida.probabilidad_impago, "decision":prediccion_salida.decision }


# TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm):
    #voy a preparar ek historial de lo q recibe el llm 
    historial = [{"role": "system", "content": SISTEMA}]
    for m in mensajes:
        historial.append({"role":m.role, "content":m.content})

    herramienta = None 
    # el buvle llm 
    for vuelta in range(MAX_VUELTAS):
        respuesta = llm.completar(historial, [definir_tool()])

        if not respuesta.get("tool_calls"):
            return ChatSalida(respuesta=respuesta["content"], herramienta=herramienta)
        
        historial.append(respuesta) #el llm pide la yool 
        for llamada in respuesta["tool_calls"]:

            nombre = llamada["function"]["name"]

            argumentos_json = llamada["function"]["arguments"]
            resultado = ejecutar_tool(nombre,argumentos_json)

            herramienta = HerramientaUsada(
                nombre=nombre,
                argumentos=leer_argumentos(argumentos_json),
                resultado=resultado,
            )
            historial.append({
                "role": "tool",
                "tool_call_id":llamada["id"],
                "content":json.dumps(resultado)})

    return ChatSalida(
        respuesta="No he podido completarlo", 
        herramienta=herramienta)