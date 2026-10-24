from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()

@router.post("/chat", response_model= ChatSalida)
def chat(entrada: ChatEntrada, llm=Depends(get_llm)):
    return responder(entrada.mensajes, llm)

#EXPLICACIÓN DE LA CLASE CHAT.PY => 

# TODO: POST /chat (entrada ChatEntrada, salida ChatSalida). Recibe el LLM con Depends(get_llm)

#tengo que hacer un post a /chat => la entrada es la respuesta del cliente. el output es la respuesta a esa pregunta.
# 
# 
#esto sería la primera cosa que habría que hacer, ya que en el flujo de la 
# comunicación tenemos primero que hacer un post a /chat con la info que ha pasado 
# por pantalla el cliente => eso justamente se hace en app.py y es este fichero quien 
#lo recibe. 

# esto se hace de esta manera en el front, se arma un mensaje así
#cuerpo = {"mensajes": []}
#for m in st.session_state.mensajes:
    #cuerpo["mensajes"].append({"role": m["role"], "content": m["content"]})

#por la red viaja un json de esta manera => {"mensajes": [{"role": "user", "content": "edad 30, ingresos 2500..."}]}
# 
# 

#como el mensaje lo tipo como Chat entrada, fast api solo comprueba esto (está en schema de chat.py)

#class ChatEntrada(BaseModel):
#    mensajes: list[Mensaje] = Field(min_length=1)

#Si algo no cumple, FastAPI responde 422 y tu función ni se ejecuta

#@router.???: ¿qué método HTTP usa app.py para enviar el mensaje? (Mira httpx.____(API_URL + "/chat", ...).)
#"???": ¿en qué ruta escucha el endpoint?
#response_model=???: ¿qué clase define lo que devuelves al frontend?
#entrada: ???: ¿qué clase define lo que llega en el cuerpo? Al tiparlo así, FastAPI valida y devuelve 422 si algo está mal.
#Depends(???): ¿qué función devuelve el LLM? Está importada arriba, desde app.services.llm. Se pasa sin paréntesis, porque la llama FastAPI.
#responder(???, llm): responder necesita la lista de mensajes, no el objeto entero. ¿En qué campo de entrada está esa lista?

