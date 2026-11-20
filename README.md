# env-demo

Pequeño paquete de Python que muestra en qué entorno se ejecuta (`dev`, `pre` o `pro`).
Demuestra que un solo código, un solo `uv.lock` y un solo `.venv` se comportan de forma
predecible en los tres entornos: lo único que cambia es la variable `APP_ENV`.
Si no se define, se usa `dev`; cualquier otro valor (por ejemplo `local`) provoca `ValueError`.

## Requisitos

- uv y Git instalados.

## Instalación

Desde un checkout limpio:

```bash
cd env-demo
uv sync --locked
```

`uv sync --locked` crea `.venv` e instala las versiones exactas de `uv.lock` sin resolver versiones nuevas:

- Rich: dependencia de ejecución (muestra el mensaje).
- Pytest y Ruff: dependencias de desarrollo.

## Ejecución

```bash
APP_ENV=dev uv run python -m env_demo.main     # Entorno activo: DEV
APP_ENV=pre uv run python -m env_demo.main     # Entorno activo: PRE
APP_ENV=pro uv run python -m env_demo.main     # Entorno activo: PRO
APP_ENV=local uv run python -m env_demo.main   # ValueError: APP_ENV debe ser dev, pre o pro
```

## Comprobación

### Tests

```bash
uv run pytest
```

`tests/test_main.py` tiene 4 casos: 3 comprueban `dev`, `pre` y `pro`, y 1 comprueba que un
valor no admitido lanza `ValueError`. Resultado esperado: `4 passed`.

### Calidad de código

```bash
uv run ruff check .
```

Resultado esperado: `All checks passed!`

### Controles de Git

```bash
git log --oneline     # 3 commits: bootstrap uv project / add environment-aware command / add tests and usage documentation
git ls-files .venv    # sin salida: .venv no está versionado
git ls-files uv.lock  # uv.lock sí está versionado
git remote -v         # sin salida: el proyecto no tiene remoto
```