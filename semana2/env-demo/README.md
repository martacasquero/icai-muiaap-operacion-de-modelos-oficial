EXPLICACIÓN DE LA PRÁCTICA 2.1
## ENV-DEMO 

# Se ha construido env-demo. 
    Env-demo (explicación) => es un pequeño programa de python que muestra en la terminal en que entorno estoy ejecutando.

# Entornos del trabajo. 

Un mismo programa suele pasar por tres entornos. 
    
    1. dev (desarrollo) => donde se programa y se prueban los cambios 

    2. pre (preproducción) => donde se revisa que todo funcione antes de publicarlo 

    3. pro (producción) => la versión final, la que usa la gente 

# Qué demuestra el proyecto 

Lo que demuestra el proyecto es que una sola base de código se comporta de forma predecible en los tres entornos. Por eso, en este proyecto usamos lo siguiente: 

    1. Un sólo código => no tenemos una copia diferente para cada entorno 

    2. Un sólo uv.lock => el archivo que fija las versiones exactas de las dependencias

    3. Un sólo .venv => el entorno virtual donde se instalan las dependencias

Lo único que cambia entre los entornos es el valor de la variable APP_ENV que puede ser o dev o pre o pro. 

Lo que hace el programa es leer la variable y muestra un mensaje como por ejemplo ENTORNO ACTIVO PRE 

Si no se define la variable se usa dev. 

## INSTALACIÓN 

Para empezar, hay que tener uv instalado. uv es la herramienta que gestiona Python y as dependencias de este proyecto. 

La versión de este proyecto de uv es la siguiente (uv --version) : 
    uv 0.12.9 (9f9286029 2026-09-01 aarch64-apple-darwin)

    # Pasos para instalar

    Entramos en la carpeta del proyecto : 

            cd env-demo
    
    Lo sincronizamos cpon el siguiente comando: 

        uv sync => Este comando crea el entorno virtual .venv dentro de la carpeta e instala las dependencias con las versiones exactas definidas en uv.lock 

        UV.LOCK => 

            RICH => para mostrar el mensaje en la terminal 

            PYTEST => para ejecutar las pruebas

            RUFF => para revisar el estilo del código 


        Sólo lo haremos una vez. 
    

## EJECUCIÓN 

Tdos los comandos los escribimos en la terminal dentro de la carpeta env-demo 

1. 
    Entorno por defecto => uv run python -m env_demo.main

    Resultado => Entorno activo: DEV

2. Elegimos el entorno cambiado el valor de la variable APP _ ENV 

    2.1 
        APP_ENV=pre uv run python -m env_demo.main
        Entorno activo: PRE

    2.2 
        APP_ENV=pro uv run python -m env_demo.main
        Entorno activo: PRO

 
## COMPROBACIÓN 

# Ejecutamos las pruebas

El rpoyecto incluye pruebas automaticas en tests/test_main.py 

Las ejecutamos con el siguiente comando => 

    uv run pytest

    Resultado => 

======================== test session starts ========================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/martacasquero/icai-muiaap-operacion-de-modelos-oficial/semana2/env-demo
configfile: pyproject.toml
collected 4 items                                                   

tests/test_main.py ....                                       [100%]

========================= 4 passed in 0.01s =========================

# Cuántas pruebas hay => 

    3 que comprueban que pro pre y dev muestran lo correcto 
    1 que comprueba que el valor no admitido da error 

    Otra para revisar el código 

        uv run ruff check

 


 
  

