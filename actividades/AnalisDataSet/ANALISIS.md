# Actividades de análisis con el dataset — Lo que aprendió el modelo

**Estudiante:** Kevin Alejandro Cuevas Crisantos (Matrícula: 21121503)  
**Equipo:** Equipo-CristianM-Kevin-Joel-CristianD-Dylan  
**Materia:** Tópicos Web y Móvil  

---

## Actividad 1 — El retrato del dataset

### 1. Predicción (antes de ejecutar)
- **Cuando llueve, ¿qué medio creemos que domina?:** Creemos que domina la **moto** o la **camioneta**, porque la bicicleta se vuelve peligrosa y lenta con lluvia, y el dron tiene prohibido volar bajo lluvia según las regulaciones operativas.
- **Para el centro de la ciudad:** Creemos que dominará la **bicicleta** y la **moto**, debido a que son distancias cortas, congestionamiento vehicular y agilidad de acceso; además, el dron no puede sobrevolar el centro.
- **Distancia más larga de bicicleta:** Predecimos que será de **7.0 km**, ya que la tabla de límites del negocio marca 7 km como la distancia máxima operativa de la bicicleta.
- **Envíos que rompan reglas:** Esperamos que haya **0 envíos** que rompan las reglas estrictas de capacidad física o restricciones legales, aunque podría haber ruido en costos si el generador aplicó ruido a la elección final.

---

### 2. Comprobación y Evidencia

#### Tabla: Clima vs. Medio (`normalize="index"`)
```text
medio_recomendado  bicicleta  camioneta   dron   moto
clima                                                
despejado              0.328      0.166  0.135  0.371
lluvia                 0.085      0.167  0.000  0.748
viento_fuerte          0.317      0.184  0.000  0.499
```

#### Tabla: Zona de destino vs. Medio (`normalize="index"`)
```text
medio_recomendado  bicicleta  camioneta   dron   moto
zona_destino                                         
centro                 0.584      0.135  0.000  0.280
periferia              0.009      0.140  0.126  0.725
residencial            0.262      0.146  0.173  0.419
rural                  0.000      0.408  0.000  0.592
```

#### Resumen estadístico (`min`, `median`, `max`)
```text
                  distancia_km               peso_kg               volumen_l               
                           min median    max     min median    max       min median     max
medio_recomendado                                                                          
bicicleta                 0.37   3.42   7.00     0.1   1.76   7.99       0.3   7.78   39.70
camioneta                 0.43   8.99  59.12     0.1   6.72  80.00       0.3  31.36  400.57
dron                      2.07   9.54  14.99     0.1   1.04   2.50       0.3   4.29   11.98
moto                      0.34  10.63  39.90     0.1   2.58  24.93       0.3  11.27   89.99
```

#### Verificación de reglas del negocio (`es_posible`)
- Envíos que violan las reglas del negocio: **0 de 10 000** (100% de cumplimiento).
- Distancia máxima observada para bicicleta: **7.00 km**.

---

### 3. Comparación y Respuestas

**¿En qué zonas y con qué climas el dron nunca aparece? ¿Qué regla del paso 12 lo explica en cada caso?**
- **Zonas:** El dron tiene **0 envíos en `centro`** (0%) y **0 envíos en `rural`** (0%).
  - *Explicación regla:* En el centro está expresamente prohibido porque es espacio aéreo restringido urbano. En la zona rural no aparece porque las distancias rurales exceden comúnmente su autonomía o no hay estaciones de despegue/cobertura.
- **Climas:** El dron tiene **0 envíos con `lluvia`** y **0 envíos con `viento_fuerte`**; únicamente vuela con clima `despejado` (13.5% de los envíos despejados, 948 envíos en total).
  - *Explicación regla:* Las limitaciones mecánicas y de seguridad prohíben el vuelo de drones con precipitación o rachas de viento que desestabilicen la aeronave o dañen la electrónica.

**La bicicleta casi no va a la periferia, aunque ninguna regla se lo prohíbe. ¿Qué otra columna lo explica? Demuéstralo con un número.**
- Lo explica la columna **`distancia_km`**.
- La bicicleta tiene un tope físico y normativo de **7 km**. Al analizar los destinos hacia la `periferia`:
  - Envíos a periferia con distancia > 7 km: **2,000 paquetes** (97.7% del total de la periferia).
  - Envíos a periferia con distancia $\le$ 7 km: apenas **46 paquetes**.
  - De esos 46 paquetes viables, la bicicleta tomó **18 envíos**, con una distancia mediana de **6.48 km**. Es decir, la periferia está geográficamente lejos del almacén central, superando casi siempre el alcance de la bicicleta.

**Comparen los máximos de distancia, peso y volumen de cada medio con la tabla LIMITES. ¿Qué límites se pueden adivinar solo mirando los datos? ¿Cuál no y por qué?**
- **Se pueden adivinar con exactitud:**
  - Bicicleta: `distancia_km` máx = 7.00 km (límite 7), `peso_kg` máx = 7.99 kg (límite 8), `volumen_l` máx = 39.70 L (límite 40).
  - Dron: `distancia_km` máx = 14.99 km (límite 15), `peso_kg` máx = 2.50 kg (límite 2.5), `volumen_l` máx = 11.98 L (límite 12).
  - Moto: `distancia_km` máx = 39.90 km (límite 40), `peso_kg` máx = 24.93 kg (límite 25), `volumen_l` máx = 89.99 L (límite 90).
- **Cuál NO se puede adivinar:** Los límites de la **camioneta**.
  - *Por qué:* En los datos la camioneta llega a 59.12 km, 80 kg y 400.57 L, pero la tabla teórica de límites fija valores de capacidad virtual infinita (1000 km, 1000 kg, 3000 L). Los datos solo muestran el tamaño de los pedidos que llegaron, no la cota técnica máxima del vehículo.

**Hay más de cien camionetas para viajes de menos de 2 km, lo que suena a desperdicio. ¿Cuántas tienen una razón clara para ir en camioneta? Para las que no, propongan una explicación.**
- Total de camionetas para viajes < 2 km: **107 envíos**.
- Con razón clara e ineludible (**95 envíos**):
  - 36 paquetes requieren refrigeración (`refrigerado = 1`, exclusivo de camioneta).
  - 47 paquetes pesan más de 25 kg (exceden el límite de la moto).
  - 61 paquetes tienen volumen mayor a 90 L (no caben en moto ni bicicleta).
- Sin razón evidente de capacidad física (**12 envíos**):
  - Paquetes ligeros y no refrigerados (ejemplo: ID 228 con 0.98 km, 0.84 kg, 2.26 L, prioridad `mismo_dia`).
  - *Explicación:* Ocurre por el ruido del 3% inyectado en el generador sintético o por consolidación de rutas donde la camioneta ya iba en esa dirección y absorbió el envío urgente para entrega inmediata sin esperar mensajero en moto.

---

### 4. Para pensar (Decisión)
**¿Podrían reconstruir las reglas del negocio solo mirando los datos? ¿Qué riesgo hay en dejar que un modelo «descubra» las reglas en lugar de escribirlas a mano?**
- **Postura:** Algunas reglas duras de corte numérico (como peso máximo del dron = 2.5 kg o distancia máxima de bici = 7 km) son fáciles de inducir estadísticamente por los valores máximos. Sin embargo, reglas compuestas y lógicas prohibitivas (como espacio aéreo del centro, restricciones nocturnas o exclusión de refrigerados fuera de camioneta) corren un riesgo enorme si se dejan al aprendizaje automático.
- **Riesgo:** El modelo probabilístico no conoce el "concepto" de ley o seguridad física; solo calcula correlaciones. Si el modelo no vio suficientes ejemplos nocturnos o paquetes en zonas límite, predecirá con cierta probabilidad un dron a las 3:00 am o un paquete de 9 kg en bicicleta, causando multas aeronáuticas, accidentes o paquetes dañados. Las reglas críticas deben estar programadas de forma determinista en el backend (`reglas.py` / `es_posible`).

---

## Actividad 2 — La hora y el dron

### 1. Predicción (antes de ejecutar)
- **¿Cuántos drones creemos que salen a las 3:00?:** Predecimos que saldrán **0 drones**, dado que existe una regla operativa que prohíbe el vuelo nocturno entre las 21:00 y las 5:59.
- **Porcentaje de envíos que sale de noche (antes de las 6 o desde las 21):** Calculamos aproximadamente un **15% a 20%** de los envíos, asumiendo menor actividad comercial de noche pero con operaciones de paquetería express activas.

---

### 2. Comprobación y Evidencia

#### Envíos por hora y medio (conteos)
```text
medio_recomendado  bicicleta  camioneta  dron  moto
hora_salida                                        
0                          2         12     0    63
1                          6         11     0    49
2                          5         19     0    59
3                          4         13     0    60
4                          2         10     0    47
5                          8         25     0   116
6                         94         50    33   136
7                        204         92    68   233
8                        205        118    57   252
...                       ...        ...   ...   ...
19                       166         78    45   199
20                       115         72    35   160
21                        20         58     0   240
22                         5         28     0   116
23                         5         15     0    55
```

- Horas sin ningún dron: **`[0, 1, 2, 3, 4, 5, 21, 22, 23]`** (9 horas en total).
- Total de envíos de noche: **816 envíos (8.2%)**.
- Total de envíos de día (6:00 a 20:59): **9,184 envíos (91.8%)**.
- Drones volando en horario nocturno: **0**.
- Gráfica generada y guardada en: `actividades/AnalisDataSet/hora_vs_medio.png`.

---

### 3. Comparación y Respuestas

**¿En qué horas no hay ni un solo dron? ¿Coincide exactamente con la regla?**
- En las horas 0, 1, 2, 3, 4, 5, 21, 22 y 23.
- Coincide **al 100%** con la regla del negocio: los drones tienen permiso de operación exclusivamente en la ventana de **6:00 a 20:59**.

**¿Cuántos envíos de noche hay, comparados con los de día? ¿Qué consecuencia tiene eso para lo que el modelo puede aprender sobre la noche?**
- Solo hay **816 envíos nocturnos (8.2%)** frente a **9,184 envíos diurnos (91.8%)**.
- *Consecuencia:* Al estar tan subrepresentada la noche en el dataset de entrenamiento, el árbol de decisión cuenta con muy pocos ejemplos negativos para aprender que la noche es un inhibidor estricto del dron. Al tener tan poca penalización en la función de impureza (Gini/Entropía), el modelo prefiere ignorar la variable `hora_salida` o clasificar en función de `distancia_km` y `peso_kg`, provocando que en producción proponga drones a las 3:00 am si el paquete es ligero.

**Entre las 20:00 y las 21:00 las bicicletas casi desaparecen y las motos aumentan. Busquen en el README.md qué lo explica.**
- En la hora 20 hay **115 bicicletas** y en la hora 21 caen dramáticamente a **20** (y luego a 5 en la hora 22).
- *Explicación del README:* El generador introduce un factor de riesgo: "la bicicleta de noche y con lluvia recibe penalizaciones severas de seguridad y velocidad". Al llegar la noche (21:00 en adelante), el algoritmo de costeo penaliza fuertemente a los ciclistas por visibilidad y peligro vial, haciendo que la moto gane en prácticamente todas las rutas cortas.

**Un árbol solo pregunta «¿la hora es menor o igual que X?». ¿Por qué le cuesta representar «de noche»? ¿Cuántas preguntas sobre la hora necesitaría como mínimo?**
- La noche es un intervalo disjunto en una escala de 0 a 23: $[0, 5] \cup [21, 23]$.
- Como los cortes del árbol son divisiones hiperplanas ortogonales simples ($\le c$), no puede capturar la condición de "noche" en una sola división.
- Necesita como mínimo **2 preguntas consecutivas**:
  1. `hora_salida <= 5.5` (captura la madrugada).
  2. Si es falso, evaluar en otra rama `hora_salida <= 20.5` para separar el día de la noche tardía.
- Si la profundidad máxima está limitada (ej. max_depth=8), gastar dos niveles solo en la hora compite contra divisiones mucho más informativas como `distancia_km` o `volumen_l`.

---

### 4. Para pensar (Decisión)
**Diseñen una columna nueva que le facilite al árbol entender la noche. Expliquen cómo la calcularían y cómo comprobarían que ayudó.**
- **Diseño de variable:** Crear la característica binaria `es_de_noche`:
  $$\text{es\_de\_noche} = 1 \quad \text{si } (\text{hora\_salida} < 6 \lor \text{hora\_salida} \ge 21), \quad 0 \text{ en caso contrario}.$$
- **Justificación:** Transforma un intervalo disjunto no lineal en una variable booleana directamente separable en un solo corte del árbol (`es_de_noche <= 0.5`).
- **Comprobación:** Entrenar el árbol agregando `es_de_noche` y medir la cantidad de falsos positivos nocturnos de dron en prueba (cuántas veces predice dron cuando `es_de_noche == 1`). Si los errores nocturnos caen a 0, la variable demostró su efectividad.

---

## Actividad 3 — Anatomía de los errores

### 1. Predicción (antes de ejecutar)
- **¿Qué confusión creemos que será la más frecuente?:** Predecimos que será entre **moto y bicicleta** (en viajes de 4 a 7 km con paquetes de 2 a 5 kg), ya que comparten un rango operativo amplio y el ruido de costos puede inclinar la balanza hacia cualquiera.
- **¿El modelo confundirá bicicleta con camioneta?:** Creemos que prácticamente **nunca**, salvo quizás en paquetes pequeños pero refrigerados donde la camioneta es obligatoria y el árbol olvide checar la bandera de frío.

---

### 2. Comprobación y Evidencia

#### Total de errores en conjunto de prueba (2 000 envíos):
- **158 errores en total** (tasa de error: **7.9%**, exactitud: **92.1%**).

#### Matriz de Confusiones más frecuentes (Real $\to$ Predicho)
```text
real       predicho 
moto       bicicleta    46
camioneta  moto         32
moto       dron         29
bicicleta  moto         20
dron       bicicleta    18
camioneta  bicicleta     9
camioneta  dron          4
```

#### Análisis Moto $\to$ Dron (29 casos):
- Casos que ocurren de noche ($<6$ o $\ge 21$): **26 casos** (89.7% de esta confusión).
- Casos descartados y corregidos por las reglas del negocio (`es_posible = False`): **26 casos**.
- Casos que pasan las reglas del negocio (`es_posible = True`): **3 casos** (IDs: 2484, 3722, 677, en horas de la tarde, clima despejado y peso $< 1.7$ kg).

#### Análisis Moto $\to$ Bicicleta (46 casos):
- Distancia promedio: **4.08 km** (máxima observada: **6.89 km**, ninguna mayor a 7 km).
- Peso promedio: **2.37 kg** (frente a 2.16 kg en bicicletas bien clasificadas).
- Clima: 24 despejado, 11 lluvia, 11 viento fuerte.

#### Bicicleta vs. Camioneta:
- Real Bicicleta $\to$ Predicho Camioneta: **0 casos**.
- Real Camioneta $\to$ Predicho Bicicleta: **9 casos** (paquetes pequeños con `refrigerado = 1` donde el árbol omitió evaluar la refrigeración en esa rama).

---

### 3. Comparación y Respuestas

**¿Cuáles son las tres confusiones más frecuentes? ¿Son entre medios parecidos o muy distintos? ¿Qué les dice eso?**
1. **Moto $\to$ Bicicleta:** 46 casos.
2. **Camioneta $\to$ Moto:** 32 casos.
3. **Moto $\to$ Dron:** 29 casos.
- Son confusiones entre **medios vecinos y sustitutos inmediatos**. Ocurren en las fronteras de decisión (paquetes de 5 km y 3 kg donde moto y bici son viables, o paquetes de 20 kg donde moto y camioneta compiten).
- Esto nos dice que el modelo aprendió con coherencia la física del problema: no comete disparates como asignar un paquete de 50 kg a una bicicleta. Sus errores reflejan la zona gris donde el costo y el ruido del 8% definen al ganador.

**Envíos que eran moto y el modelo mandó a dron: ¿Cuántos son de noche? ¿Cuáles corregirían las reglas y cuáles no?**
- De los 29 envíos, **26 ocurrieron de noche**.
- **Las reglas de negocio (`reglas.py`) corrigen 26 de los 29 errores** porque la función `es_posible` detecta inmediatamente que `hora_salida` está fuera de 6 a 20 y bloquea el dron, asignando la moto.
- Los **3 que no corrigen las reglas** son envíos de día (13:00, 17:00, 18:00 hrs) con paquetes muy ligeros ($<1.7$ kg) a distancias de 7 a 12 km. Físicamente el dron podía llevarlos, pero en la realidad se asignaron a moto por factores de riesgo (como tráfico bajo o penalizaciones menores).

**Envíos que eran moto y el modelo mandó a bicicleta: ¿Están cerca del límite de 7 km?**
- Sí, todos tienen distancia menor a 7 km (promedio 4.08 km).
- Lo que los distingue de las bicicletas reales es que en la realidad esos envíos tenían penalizaciones como lluvia o prisa (`mismo_dia`), donde la moto convenía más en tiempo, pero el árbol se fijó únicamente en el bajo costo de la distancia corta.

---

### 4. Para pensar (Decisión)
**Si solo pudieran arreglar un tipo de error, ¿cuál elegirían y por qué? ¿Lo arreglarían cambiando el modelo, los datos o las reglas del negocio?**
- **Elección:** El error **Moto $\to$ Dron**.
- **Por qué:** Mandar un paquete en dron indebidamente es el error con mayor impacto operativo, legal y financiero: el dron puede quedarse sin batería en vuelo, violar la ley aeronáutica nocturna o exponerse a pérdida total. En contraste, enviar una moto en lugar de una bici solo representa unos pesos de diferencia en combustible.
- **Cómo arreglarlo:** Mediante **las reglas del negocio (capa de software)** combinadas con ingeniería de características en los datos (`es_de_noche`). Las reglas del negocio ya actúan como un cortafuegos infranqueable con costo computacional cero ($O(1)$) que intercepta el 90% de estas fallas antes de que salgan a la calle.

---

## Actividad 4 — ¿Qué columnas usa de verdad el modelo?

### 1. Predicción (antes de ejecutar)
- **Orden predicho de importancia:**
  1. `distancia_km`
  2. `peso_kg`
  3. `volumen_l`
  4. `refrigerado`
  5. `clima`
  6. `hora_salida`
  7. `zona_destino`
  8. `fragil`
  9. `prioridad`
  10. `trafico`
  11. `largo_cm`
  12. `ancho_cm`
  13. `alto_cm`
  14. `valor_declarado_mxn`
- **Columnas que creemos que el modelo NO usa:** `largo_cm`, `ancho_cm`, `alto_cm` (porque ya tiene `volumen_l`), y posiblemente `valor_declarado_mxn`.

---

### 2. Comprobación y Evidencia

#### Importancia acumulada por columna original
```text
distancia_km           0.3220
volumen_l              0.1929
clima                  0.1438
refrigerado            0.1313
peso_kg                0.1263
hora_salida            0.0587
fragil                 0.0199
prioridad              0.0031
valor_declarado_mxn    0.0007
ancho_cm               0.0007
largo_cm               0.0003
alto_cm                0.0003
trafico                0.0002
zona_destino           0.0000
```

#### Impacto en la exactitud al eliminar cada columna (Ablation Test)
```text
columna_eliminada  exactitud  diferencia
     distancia_km     0.7930     -0.1280
            clima     0.8445     -0.0765
      refrigerado     0.8785     -0.0425
      hora_salida     0.8910     -0.0300
          peso_kg     0.9040     -0.0170
        volumen_l     0.9060     -0.0150
           fragil     0.9155     -0.0055
         largo_cm     0.9205     -0.0005
         ancho_cm     0.9205     -0.0005
          alto_cm     0.9205     -0.0005
valor_declarado_mxn   0.9210      0.0000
     zona_destino     0.9210      0.0000
          trafico     0.9210      0.0000
        prioridad     0.9215     +0.0005
```

---

### 3. Comparación y Respuestas

**¿Cuáles son las cuatro columnas más importantes? ¿Coinciden con su predicción?**
- Las 4 columnas principales son:
  1. **`distancia_km`** (32.2%)
  2. **`volumen_l`** (19.3%)
  3. **`clima`** (14.4%)
  4. **`refrigerado`** (13.1%)
  *(seguidas muy de cerca por `peso_kg` con 12.6%)*.
- Nuestra predicción acertó casi en su totalidad: colocamos distancia, peso, volumen y refrigerado en los primeros lugares, aunque el clima resultó ligeramente más discriminante que el peso debido a que descarta de golpe a todos los drones y frena bicicletas.

**¿Qué columna, al quitarla, baja más la exactitud? ¿Cuáles no la cambian nada?**
- La columna que más desploma la exactitud es **`distancia_km`**, cayendo de 92.1% a **79.3%** ($\Delta = -12.8\%$).
- Las columnas que prácticamente no alteran el rendimiento al ser retiradas son: **`zona_destino`** ($\Delta = 0.000$), **`trafico`** ($\Delta = 0.000$), **`valor_declarado_mxn`** ($\Delta = 0.000$) y las medidas individuales de la caja (`largo`, `ancho`, `alto`), ya que el volumen ya resume el espacio físico.

**La zona de destino tiene importancia cero, pero el dron nunca va al centro. ¿Cómo puede ser que el modelo no use la zona y, aun así, la plataforma nunca mande un dron al centro?**
- Porque la plataforma implementa una arquitectura desacoplada: **el modelo de machine learning no trabaja solo en producción**.
- La plataforma sigue el flujo visto en `usar_modelo.py` y en la etapa 5 de Django: el árbol sugiere un medio tentativo, pero la respuesta pasa obligatoriamente por la función `es_posible()` en `reglas.py`. Como dicha función evalúa `paquete["zona_destino"] == "centro"` y lo prohíbe para el dron, la regla de negocio intercepta la sugerencia y la corrige hacia moto o bicicleta. El modelo no necesita gastar divisiones en aprender la zona porque el software corporativo garantiza la regla al 100%.

---

### 4. Para pensar (Decisión)
**La app le pide al usuario catorce datos. Si el modelo no usa algunos, ¿deberían dejar de pedirlos?**
- **Postura:** **No deben dejar de pedirse.**
- **Argumentos:**
  1. *El modelo no es el único consumidor de los datos:* Atributos como `valor_declarado_mxn` son indispensables para calcular el seguro del envío y la póliza de indemnización. `zona_destino` es requerida por el enrutador logístico (GPS) y las reglas de negocio.
  2. *Auditoría y soporte:* Las dimensiones físicas individuales (`largo`, `ancho`, `alto`) son necesarias para que el chofer verifique en el almacén si la caja entra por la puerta de la camioneta o en la mochila del repartidor, más allá de la capacidad en litros.
  3. *Evolución de modelos futuros:* Si en el futuro se implementa un modelo de precios dinámicos o un optimizador de empaquetado 3D (Bin Packing), esos datos serán vitales para el entrenamiento.

---

## Actividad 5 — El dron es minoría: ¿hay que balancear el dataset?

### Parte A — Pensar antes de tocar los datos

**1. ¿Qué exactitud tendrían modelos ingenuos?**
- Un modelo que nunca predice dron y siempre acierta las demás clases tendría una exactitud del **90.5%** (porque el dron solo representa el 9.5% de los datos).
- Un modelo que siempre prediga la clase mayoritaria (moto con 45.8%) tendría **45.8%** de exactitud.
- *Conclusión:* La exactitud es una métrica engañosa en datasets desbalanceados. Un modelo mediocre que ignore por completo al dron obtendría más del 90% de exactitud aparente. En su lugar, deben usarse métricas desglosadas por clase: **Precision**, **Recall** y puntuación **F1-Score**.

**2. ¿Por qué hay tan pocos drones? ¿Es un error de los datos o refleja el negocio?**
- Refleja fielmente la **operación real de la empresa**: los drones tienen ventanas de operación sumamente restringidas (buen clima, peso menor a 2.5 kg, fuera del centro, solo de día). Por ende, es natural que representen menos del 10% de la flota. No es un error de muestreo, sino la distribución real del dominio.

**3. ¿Cuándo se balancea? ¿Se balancea la prueba?**
- Se balancea **únicamente después de separar los datos** de entrenamiento y prueba, aplicándolo **exclusivamente al conjunto de entrenamiento**.
- **El conjunto de prueba jamás se balancea**: debe mantenerse con la distribución original del mundo real para medir objetivamente cómo se comportará la plataforma con clientes reales. Balancear la prueba sería falsear la evaluación.

---

### Parte B — Probar estrategias (Resultados de la terminal)

Se evaluaron todas las estrategias contra el mismo conjunto de prueba intacto de 2 000 envíos (con 190 drones reales):

| Estrategia | Envíos entreno | Exactitud | Precision dron | Recall dron | Veces predice dron | Sugerencias imposibles |
|---|---|---|---|---|---|---|
| **Sin balancear (Línea base)** | 8,000 | 92.100% | 0.839 | 0.905 | 205 | 31 |
| **Submuestreo (Undersampling)** | 3,032 | 89.750% | 0.889 | 0.932 | 199 | 29 |
| **Sobremuestreo (Oversampling x4)**| 10,274 | 90.050% | 0.722 | 1.000 | 263 | 56 |
| **`class_weight='balanced'`** | 8,000 | 90.300% | 0.766 | 1.000 | 248 | 35 |
| **Trampa (Data Leakage antes split)**| 10,275 | 93.032% | 0.934 | 0.984 | 792 | 46 |

#### Explicación de la trampa:
Al sobremuestrear antes de dividir con `train_test_split`, copias exactas de los mismos envíos quedaron simultáneamente en entrenamiento y prueba. El modelo simplemente memorizó esos registros duplicados, arrojando un 93.0% ficticio y prediciendo 792 drones. Esta mejora es falsa porque el modelo fue evaluado con datos que ya había visto durante el entrenamiento.

---

### Parte C — Interpretar

**¿Qué pasó con el recall y la precision del dron?**
- Con el sobremuestreo y `class_weight='balanced'`, el **Recall subió al 100%** (1.000): el modelo no dejó escapar ni un solo dron posible.
- Sin embargo, la **Precision se desplomó de 0.839 a 0.722**: para atrapar todos los drones, el modelo se volvió temerario y predijo dron 263 veces (cuando en la prueba solo había 190). Uno de cada cuatro drones sugeridos era un error (falso positivo). Subir recall a la fuerza castiga la precisión.

**¿Alguna estrategia dejó al modelo con muchos menos datos?**
- El **Submuestreo (Undersampling)** redujo los datos de entrenamiento de 8,000 a solo **3,032 envíos**. Se desperdició más del 60% de los datos de motos y camionetas, perdiendo patrones valiosos sobre paquetes pesados o largas distancias.

**`class_weight='balanced'` vs. Sobremuestreo:**
- Ambas estrategias dieron resultados casi idénticos (Recall de 1.000 y caída similar de precision). Matemáticamente representan la misma idea: multiplicar el costo del error de la clase minoritaria en la función de pérdida del árbol de decisión equivale a duplicar artificialmente las muestras de esa clase.

**Significado del porcentaje de confianza (84%):**
- Después de balancear artificialmente, el porcentaje de confianza reportado por `predict_proba` ya **no representa la probabilidad real a posteriori bayesiana**. Como el modelo fue entrenado en un entorno donde 1 de cada 4 paquetes era un dron (en lugar del 9% real), las probabilidades predichas quedan infladas a favor de la clase sobreponderada.

---

### Parte D — Decidir

#### Recomendación Final para la Plataforma:
Recomendamos **mantener el modelo SIN BALANCEAR (o con un ajuste muy leve de `class_weight`)**.

**Justificación técnica y operativa:**
1. **El costo del error asimétrico:** Para la empresa es mucho más grave cometer un falso positivo (mandar un paquete en dron que no debía ir en dron por sobrepeso, clima o batería) que un falso negativo (mandar en moto un paquete que pudo ir en dron). El modelo sin balancear mantiene una **Precision saludable de 83.9%** y genera únicamente 31 sugerencias dudosas frente a las 56 que comete el modelo sobremuestreado.
2. **Defensa en profundidad con las reglas de negocio:** Aunque el modelo balanceado logre un recall perfecto, incrementa las peticiones rechazadas por `es_posible` en Django, saturando la capa de reglas para corregir predicciones disparatadas.
3. **Escalabilidad futura:** Si la empresa adquiere el doble de drones en el futuro, no se debe manipular artificialmente el modelo actual: se capturan los nuevos datos de operación real y se reentrena el modelo con la nueva distribución natural del negocio.
