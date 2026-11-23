# S10.7 — Informe de carga

> **TODO S10.7c:** ejecuta Locust con `--csv reports/s10`, versiona los CSV
> generados y completa las tablas y el análisis de este archivo.

Plantilla del informe. Rellénala con **tus** resultados: dependen de la máquina,
del número de workers y de la configuración de `.env`. No copies cifras de otra
persona ni de la solución, que no incluye resultados.

## Cómo se ha medido

| Dato | Valor |
| --- | --- |
| Comando de la API | `uv run fastapi dev` (1 proceso) |
| Comando de Locust | `uv run --group load locust -f locustfile.py --headless -u 20 -r 5 -t 1m --host http://127.0.0.1:8000 --csv reports/s10` |
| Cliente usado | `front` (solo `predict`) |
| `rate_limit_per_minute` del cliente | 60 |
| Máquina | M5 |

Archivos generados por Locust y versionados junto a este informe:
`s10_stats.csv`, `s10_failures.csv` y `s10_stats_history.csv`.

## Resultados

Copia los valores de la fila `POST /v1/predictions` y de `Aggregated` de
`s10_stats.csv`.

| Endpoint | Peticiones | RPS | p50 (ms) | p95 (ms) | Fallos | % 429 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `POST /v1/predictions` | 693 | 12.1 | 4 | 7 | 641 | 92.5 % |
| `/v1/predictions [422]` | 89 | 1.6 | 3 | 6 | 81 | — |
| `GET /health` | 102 | 1.8 | 3 | 7 | 0 | — |
| Aggregated | 884 | 15.5 | 4 | 7 | 722 | — |

`% 429` = fallos `429` de `s10_failures.csv` / peticiones de
`POST /v1/predictions` × 100.

## Análisis (5–10 líneas)

- ¿Cuántas predicciones por minuto deja pasar el límite y cuántas ha pedido
  Locust? ¿Cuadra el `% 429` con esa cuenta?
- ¿Qué latencia (p50, p95) tiene `GET /health`, que no pasa por autenticación ni
  rate limit, frente a `POST /v1/predictions`?
- ¿Qué cambiaría con dos workers (`fastapi run --workers 2`) y un contador en
  memoria por proceso?
- Si quisieras medir la capacidad del servicio y no la política de cuotas, ¿qué
  cliente y qué límite usarías?

### Respuestas

- El límite deja pasar 60 predicciones por minuto y Locust ha pedido 782
  (693 válidas + 89 inválidas). Pasaron 52 + 8 = 60, justo la cuota. El
  `% 429` de `POST /v1/predictions` (641 / 693 = 92,5 %) cuadra con esa cuenta.
- Las peticiones inválidas también consumen cuota: el rate limit se comprueba
  antes de validar el cuerpo, por eso 81 de las 89 recibieron `429` y no `422`.
- `GET /health` (sin autenticación ni rate limit) tiene p50 3 ms y p95 7 ms;
  `POST /v1/predictions` tiene p50 4 ms y p95 7 ms. La diferencia es pequeña.
- Con dos workers cada proceso tendría su propio contador en memoria, así que
  el cliente podría hacer hasta 120 peticiones por minuto en vez de 60. Para
  evitarlo, el contador tendría que estar compartido (Redis o el API gateway).
- Para medir la capacidad del servicio y no la política de cuotas usaría un
  cliente de pruebas con un `rate_limit_per_minute` muy alto (por ejemplo
  1 000 000), para que nunca salte el `429`.
