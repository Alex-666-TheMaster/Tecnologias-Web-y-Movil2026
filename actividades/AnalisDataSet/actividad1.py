"""
Actividad 1 — El retrato del dataset
Análisis exploratorio: crosstabs por clima y zona, estadísticas por medio,
verificación de reglas del negocio y camionetas en distancias cortas.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios'))

import pandas as pd
from usar_modelo import LIMITES, es_posible

CSV = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios', 'envios_medios.csv')
datos = pd.read_csv(CSV)

print("=" * 70)
print("ACTIVIDAD 1 — EL RETRATO DEL DATASET")
print("=" * 70)

# ── 1. Distribución general ───────────────────────────────────────────────
print("\n[1] Distribución de medios:")
print(datos["medio_recomendado"].value_counts())
print(datos["medio_recomendado"].value_counts(normalize=True).map("{:.1%}".format))

# ── 2. Crosstab clima × medio (normalizado por fila) ─────────────────────
print("\n[2] Clima vs medio (% por fila):")
ct_clima = pd.crosstab(datos["clima"], datos["medio_recomendado"], normalize="index")
print(ct_clima.round(3).to_string())

# ── 3. Crosstab zona_destino × medio (normalizado por fila) ───────────────
print("\n[3] Zona destino vs medio (% por fila):")
ct_zona = pd.crosstab(datos["zona_destino"], datos["medio_recomendado"], normalize="index")
print(ct_zona.round(3).to_string())

# ── 4. Estadísticas numéricas por medio ───────────────────────────────────
print("\n[4] Estadísticas por medio (distancia, peso, volumen):")
stats = datos.groupby("medio_recomendado")[["distancia_km", "peso_kg", "volumen_l"]].agg(["min", "median", "max"])
print(stats.round(2).to_string())

# ── 5. Máxima distancia de bicicleta ─────────────────────────────────────
max_dist_bici = datos[datos["medio_recomendado"] == "bicicleta"]["distancia_km"].max()
print(f"\n[5] Distancia máxima de bicicleta en los datos: {max_dist_bici:.2f} km")
print(f"    Límite según reglas: {LIMITES['bicicleta']['distancia_km']} km")

# ── 6. Zonas y climas donde dron = 0 ─────────────────────────────────────
print("\n[6] Dron por zona (conteos absolutos):")
print(pd.crosstab(datos["zona_destino"], datos["medio_recomendado"]))

print("\n[6] Dron por clima (conteos absolutos):")
print(pd.crosstab(datos["clima"], datos["medio_recomendado"]))

print("\n[6] Dron por hora (0-23):")
dron_hora = pd.crosstab(datos["hora_salida"], datos["medio_recomendado"])
print(dron_hora[["dron"]].to_string())

# ── 7. ¿Por qué bicicleta casi no va a periferia? ─────────────────────────
print("\n[7] Bicicleta a periferia — ¿qué lo explica? (distancia mediana):")
bici_zona = datos[datos["medio_recomendado"] == "bicicleta"].groupby("zona_destino")["distancia_km"].median()
print(bici_zona.round(2).to_string())

bici_periferia = datos[(datos["medio_recomendado"] == "bicicleta") & (datos["zona_destino"] == "periferia")]
print(f"    Cantidad de bicicletas a periferia: {len(bici_periferia)}")
print(f"    Su distancia mediana: {bici_periferia['distancia_km'].median():.2f} km")
print(f"    Paquetes a periferia con distancia <= 7 km: {len(datos[(datos['zona_destino']=='periferia') & (datos['distancia_km']<=7)])}")
print(f"    Paquetes a periferia con distancia > 7 km: {len(datos[(datos['zona_destino']=='periferia') & (datos['distancia_km']>7)])}")

# ── 8. Verificar que etiquetas respeten las reglas ────────────────────────
print("\n[8] Verificación de reglas del negocio (es_posible):")

def revisar_fila(fila):
    paquete = fila.to_dict()
    medio = paquete["medio_recomendado"]
    return es_posible(medio, paquete)

datos["cumple_reglas"] = datos.apply(revisar_fila, axis=1)
n_viola = (~datos["cumple_reglas"]).sum()
print(f"    Envíos que violan las reglas del negocio: {n_viola} de {len(datos)}")
if n_viola > 0:
    print(datos[~datos["cumple_reglas"]][["id_envio", "medio_recomendado", "distancia_km", "peso_kg", "clima", "hora_salida"]].head(10).to_string())

# ── 9. Camionetas en viajes < 2 km ────────────────────────────────────────
print("\n[9] Camionetas en viajes de menos de 2 km:")
cam_cortas = datos[(datos["medio_recomendado"] == "camioneta") & (datos["distancia_km"] < 2)]
print(f"    Total: {len(cam_cortas)}")
print(f"    Con refrigerado=1 (razón clara): {cam_cortas['refrigerado'].sum()}")
print(f"    Con peso > 25 kg (razón clara): {(cam_cortas['peso_kg'] > 25).sum()}")
print(f"    Con volumen > 90 L (razón clara): {(cam_cortas['volumen_l'] > 90).sum()}")
con_razon = cam_cortas[(cam_cortas["refrigerado"] == 1) |
                        (cam_cortas["peso_kg"] > 25) |
                        (cam_cortas["volumen_l"] > 90)]
sin_razon = cam_cortas[~cam_cortas.index.isin(con_razon.index)]
print(f"    Con razón clara: {len(con_razon)}")
print(f"    Sin razón evidente: {len(sin_razon)}")
if len(sin_razon) > 0:
    print("    Muestra de sin razón evidente:")
    print(sin_razon[["distancia_km", "peso_kg", "volumen_l", "refrigerado", "fragil", "valor_declarado_mxn", "prioridad"]].head(5).to_string())

print("\n[FIN ACTIVIDAD 1]")
