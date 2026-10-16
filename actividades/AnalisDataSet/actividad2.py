"""
Actividad 2 — La hora y el dron
Análisis de la distribución de medios por hora del día.
Genera tabla y gráfica de barras apiladas.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios'))

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios', 'envios_medios.csv')
datos = pd.read_csv(CSV)

print("=" * 70)
print("ACTIVIDAD 2 - LA HORA Y EL DRON")
print("=" * 70)

# 1. Crosstab hora x medio
tabla = pd.crosstab(datos["hora_salida"], datos["medio_recomendado"])
print("\n[1] Envios por hora y medio (conteos absolutos):")
print(tabla.to_string())

# 2. Horas sin drones
horas_sin_dron = tabla[tabla["dron"] == 0].index.tolist()
print(f"\n[2] Horas sin ningun dron: {horas_sin_dron}")
print("    Regla del negocio: dron solo de 6:00 a 20:59 -> horas prohibidas: 0-5 y 21-23")

# 3. Porcentaje envios de noche vs dia
noche_mask = (datos["hora_salida"] >= 21) | (datos["hora_salida"] < 6)
n_noche = noche_mask.sum()
n_dia = (~noche_mask).sum()
print(f"\n[3] Envios de noche (antes 6 o desde 21): {n_noche} ({n_noche/len(datos):.1%})")
print(f"    Envios de dia (6 a 20): {n_dia} ({n_dia/len(datos):.1%})")
print(f"    Drones de noche: {datos[noche_mask & (datos['medio_recomendado']=='dron')].shape[0]} (deben ser 0)")

# 4. Bicicletas 20-21 vs motos
print("\n[4] Comparacion bicicleta vs moto en horas 18-22:")
horas_interes = tabla.loc[18:22, ["bicicleta", "moto", "dron"]]
print(horas_interes.to_string())
print("    (La bicicleta recibe penalizacion de noche segun README: riesgo aumenta a partir de las 20h)")

# 5. Cuantas preguntas sobre hora necesita el arbol
print("\n[5] Cuantas preguntas necesita el arbol para representar 'de noche'?")
print("    Noche = hora < 6 OR hora >= 21")
print("    -> El arbol pregunta: hora <= 5.5 y hora <= 20.5 -> 2 preguntas minimo")

# 6. Grafica de barras apiladas
fig, ax = plt.subplots(figsize=(14, 6))
tabla.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
ax.set_title("Envios por hora del dia y medio de transporte")
ax.set_xlabel("Hora de salida")
ax.set_ylabel("Cantidad de envios")
ax.legend(title="Medio")
plt.tight_layout()
grafica_path = os.path.join(os.path.dirname(__file__), "hora_vs_medio.png")
fig.savefig(grafica_path, dpi=100)
print(f"\n[6] Grafica guardada en: {grafica_path}")

# 7. Propuesta de columna nueva
print("\n[7] Columna nueva propuesta: 'es_de_noche'")
datos["es_de_noche"] = ((datos["hora_salida"] < 6) | (datos["hora_salida"] >= 21)).astype(int)
print(datos.groupby("es_de_noche")["medio_recomendado"].value_counts().unstack().fillna(0).astype(int).to_string())

print("\n[FIN ACTIVIDAD 2]")
