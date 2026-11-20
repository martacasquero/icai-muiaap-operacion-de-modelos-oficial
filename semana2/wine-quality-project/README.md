Me he basado en lo que me ha proporcionado la inteligencia artificial para generar este readme. 
# wine -quality
Proyecto uv que entrena un clasificador sobre el dataset Wine. Nace del starter de S1
(`semana2/starter/WineQT.csv`, `train.py` y `test_train.py`).

 
## Instalación (desde la raíz del fork)

```bash
git clone https://github.com/martacasquero/icai-muiaap-operacion-de-modelos-oficial.git
cd icai-muiaap-operacion-de-modelos-oficial
git switch feature/s2-wine-project
cd semana2/wine-quality-project
uv sync --locked
```

`uv sync --locked` instala exactamente las versiones de `uv.lock` sin resolver versiones nuevas.
pandas y scikit-learn son dependencias de ejecución; Pytest y Ruff, de desarrollo.

## Estructura

```
semana2/wine-quality-project/
├── data/raw/WineQT.csv          # datos de partida
├── src/wine_quality/train.py    # módulo de entrenamiento
├── tests/test_train.py          # prueba del entrenamiento
├── pyproject.toml
└── uv.lock
```

## Comprobaciones

`--frozen` ejecuta con el entorno exactamente como está bloqueado en `uv.lock`.

```bash
uv run --frozen python -m wine_quality.train
```

```
Filas: 1143
Variables: 11
Clases: 6
F1 macro: 0.3402
```

El mismo entrenamiento también se lanza con el comando del proyecto: `uv run --frozen wine-quality`.

```bash
uv run --frozen pytest        # 1 passed
uv run --frozen ruff check .  # All checks passed!
```