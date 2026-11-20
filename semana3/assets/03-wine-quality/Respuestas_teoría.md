### CHECKPOINT 1

# 1. ¿Qué campo identifica la muestra?
Lo que identifica la muestra es `sample_id`. Es un identificador de la fila, **no** una
característica del modelo: se separa antes de validar y se vuelve a añadir en la salida.

# 2. ¿Qué once campos consume el modelo?
fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol

(`sample_id` no está entre ellos.)

# 3. Proponed una nueva columna que el contrato debería rechazar
`unexpected_field`, por ejemplo:

    sample_id,fixed_acidity,...,alcohol,unexpected_field
    red-001,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,no permitido

El contrato tiene `extra="forbid"`, así que falla con `extra_forbidden`.
(Otra opción realista: `quality`, la etiqueta, que nunca debe llegar en inferencia.)

# 4. Proponed dos valores inválidos y explicad por qué
- `ph = 99.0`: el pH del vino está en la escala 2.5–4.5; 99 es físicamente imposible
  → error `less_than_equal`.
- `alcohol = -1`: un porcentaje de alcohol no puede ser negativo (límite 5–20 % vol.)
  → error `greater_than_equal`.

### CHECKPOINT 2
