
## INFORMACIÓN ANTES DE HACER LA PRÁCTICA 

# TEST2 => TEST_INFERENCE_COMPONENTS.PY 

Regla de API => Qué hace este test? Este test lo que hace es crear un request con 11 valores y comprueba que as_vector() los devuyelve en el mismo orden que FEATURE_NAMES de preprocess.py .
Si los valores entrarían en otro orden, el test fallaría. 

El float (que yo creía que sí lo comprobaba, no lo hace) => El assert lo que hace es comparar dos listas en python con == entronces por ejemplo , 1 = 1.0 devolvería True. El float no lo comprueba porque no hace falta, lo diseño yo en los contratos 

el orden es este=> 

                        FEATURE_NAMES = (
                            "fixed_acidity",
                            "volatile_acidity",
                            "citric_acid",
                            "residual_sugar",
                            "chlorides",
                            "free_sulfur_dioxide",
                            "total_sulfur_dioxide",
                            "density",
                            "ph",
                            "sulphates",
                            "alcohol",
                        )

                                # QUÉ REGLAS SALEN DE ESTE TEST 

De este test salen las siguientes reglas : 

from model_inference.contracts import WineQualityRequest => Esto me dice que WineQualityRequest está en contracts.py 

from model_inference.preprocess import preprocess_wine_request => Esto me dice que preprocess_wine_request está en preprocess.py y recibe un WineQualityRequest

Lo que devuelve tiene una función as_vector(). Como he dicho antes, esa función lo que hace es comprobar que lo devuelve en el mismo orden (una lista). 


# TEST => TEST_PREDICT_FILE.PY  (PYTEST EJECUTA LAS FUNCIONES QUE EMPIEZAN POR TEST)

Inciso => Lo que hay que saber de este test es que hay 3 funciones auxiliares que se llaman en otras funciones. Estas tres son las siguientes => 

write_instructor_model => crea un modelo falso 
write_input_csv => crea un csv de entrada 
run_predict_file => ejecuta el comando 

Los assert comprueban el resultado 

Si no tiuvieramos estas funciones auxiliares, cada función tendría que repetir el diccionario de filas. 

def test_predict_file_rejects_a_missing_required_field(tmp_path):
    ...
    write_instructor_model(model_path)                    # 1. modelo válido
    write_input_csv(input_path, missing_field="alcohol")  # 2. CSV sin alcohol
    completed = run_predict_file(model_path, input_path, output_path)  # 3. ejecutar
    assert completed.returncode == 2                      # 4. comprobar
    assert "alcohol" in completed.stderr
    assert not output_path.exists()

eSTO SE LEERÍA COMO : "con un modelo válido y un CSV al que le falta alcohol, el comando debe fallar con código 2, mencionar alcohol y no crear la salida."


### Antes de escribir código hay que resolver una tensión entre los dos archivos de tests, porque condiciona cómo voy a diseñar WineQualityRequest.

El problema del sample_id

En test_inference_components.py, la request se crea sin sample_id.
En test_predict_file.py, un sample_id vacío debe dar error, y el CSV trae sample_id como columna.

Voy a hacer lo siguiente : sample_id: str | None = Field(default=None, min_length=1)




Regla de API => 

