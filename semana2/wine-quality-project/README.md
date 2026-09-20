El readme me lo ha creado CLAUDE. 

wine-quality

Proyecto de entrenamiento de un modelo sobre el dataset Wine, empaquetado con uv a partir del starter de S1 (WineQT.csv, train.py, test_train.py).

Instalación

Instala el proyecto y sus dependencias con el lock generado, sin resolver versiones nuevas:

bash
uv sync --locked
Estructura
semana2/wine-quality-project/
├── data/
│   └── raw/
│       └── WineQT.csv
├── src/
│   └── wine_quality/
│       └── train.py
├── tests/
│   └── test_train.py
├── pyproject.toml
└── uv.lock
data/raw/WineQT.csv: datos de partida.
src/wine_quality/train.py: módulo de entrenamiento.
tests/test_train.py: pruebas del entrenamiento.
Comprobaciones

Con el entorno bloqueado (--frozen), ejecuta:

bash
uv run --frozen python -m wine_quality.train
uv run --frozen pytest
uv run --frozen ruff check .

Esto arranca el entrenamiento como módulo, ejecuta los tests y comprueba el estilo del código con Ruff.

