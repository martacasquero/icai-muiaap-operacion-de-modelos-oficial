### CHECKPOINT 1 

# 1. qué campo identifica la muestra ? 
Lo que identifica la muestra es el sample_id

# 2. Qué once campos consume el modelo? 
sample_id,fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol

# 3. Proponed una nueva conlumna que el contrato debería rechazar 
red-001,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,"0.56",9.4
he cambiado el 0.56 por "0.56"

# 4.  Proponed dos valores inválidos y explicad por qué 
9,7.4,0.7,0.0,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,[9.4,10]

el sample_id => he cambiado de red-001 a 9. esta columna tiene que ser un valor de ese formato y el 9 es inválido 
el alcohol => he cambiado de 9.4 a un rango. es inválido porque en vez de un float es una lista 

### CHECKPOINT 2




