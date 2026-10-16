"""
Actividad 3 — Anatomia de los errores
Evalua el modelo con los mismos datos de prueba (random_state=42, test_size=0.2, stratify).
Identifica las confusiones mas frecuentes, analiza errores de moto a dron y moto a bicicleta.
"""

import sys, os
dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios'))
sys.path.insert(0, dataset_dir)

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO
from usar_modelo import es_posible

print("=" * 70)
print("ACTIVIDAD 3 — ANATOMIA DE LOS ERRORES")
print("=" * 70)

CSV = os.path.join(dataset_dir, 'envios_medios.csv')
MODELO_PATH = os.path.join(dataset_dir, 'modelo_medios.joblib')

datos = pd.read_csv(CSV)
x = datos[NUMERICAS + CATEGORICAS]
y = datos[OBJETIVO]

x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=42
)

modelo = joblib.load(MODELO_PATH)
prediccion = modelo.predict(x_prueba)

tabla_eval = x_prueba.copy()
tabla_eval["real"] = y_prueba
tabla_eval["predicho"] = prediccion
tabla_eval["acierto"] = tabla_eval["real"] == tabla_eval["predicho"]

errores = tabla_eval[~tabla_eval["acierto"]].copy()
total_errores = len(errores)
print(f"\n[1] Total de errores en prueba (de {len(x_prueba)}): {total_errores} ({(total_errores/len(x_prueba)):.1%})")

# Confusiones mas frecuentes
confusiones = errores.groupby(["real", "predicho"]).size().sort_values(ascending=False)
print("\n[2] Top confusiones más frecuentes (Real -> Predicho):")
print(confusiones.to_string())

# Errores: Real MOTO -> Predicho DRON
moto_a_dron = errores[(errores["real"] == "moto") & (errores["predicho"] == "dron")].copy()
print(f"\n[3] Moto confundida con Dron: {len(moto_a_dron)} casos")
moto_a_dron["es_posible_dron"] = moto_a_dron.apply(lambda fila: es_posible("dron", fila.to_dict()), axis=1)
moto_a_dron["es_noche"] = (moto_a_dron["hora_salida"] >= 21) | (moto_a_dron["hora_salida"] < 6)

print(f"    - De noche (<6 o >=21): {moto_a_dron['es_noche'].sum()}")
print(f"    - Descartados por reglas del negocio (es_posible=False): {(~moto_a_dron['es_posible_dron']).sum()}")
print(f"    - Que pasan las reglas del negocio (es_posible=True): {moto_a_dron['es_posible_dron'].sum()}")
if moto_a_dron['es_posible_dron'].sum() > 0:
    print("    Detalle de los que SI pasan las reglas pero eran moto:")
    print(moto_a_dron[moto_a_dron['es_posible_dron']][["distancia_km", "peso_kg", "volumen_l", "clima", "hora_salida", "fragil", "valor_declarado_mxn"]].to_string())

# Errores: Real MOTO -> Predicho BICICLETA
moto_a_bici = errores[(errores["real"] == "moto") & (errores["predicho"] == "bicicleta")].copy()
print(f"\n[4] Moto confundida con Bicicleta: {len(moto_a_bici)} casos")
print(f"    - Distancia promedio: {moto_a_bici['distancia_km'].mean():.2f} km (max: {moto_a_bici['distancia_km'].max():.2f} km)")
print(f"    - Casos con distancia > 7 km: {(moto_a_bici['distancia_km'] > 7).sum()}")
bici_acertadas = tabla_eval[(tabla_eval["real"] == "bicicleta") & (tabla_eval["predicho"] == "bicicleta")]
print(f"    - Distancia promedio de bicis bien acertadas: {bici_acertadas['distancia_km'].mean():.2f} km")
print(f"    - Peso promedio en moto->bici: {moto_a_bici['peso_kg'].mean():.2f} kg vs bicis acertadas: {bici_acertadas['peso_kg'].mean():.2f} kg")
print("    - Clima en moto->bici:")
print(moto_a_bici["clima"].value_counts())

# Confusión Bici con Camioneta
bici_a_cam = len(errores[(errores["real"] == "bicicleta") & (errores["predicho"] == "camioneta")])
cam_a_bici = len(errores[(errores["real"] == "camioneta") & (errores["predicho"] == "bicicleta")])
print(f"\n[5] ¿Confunde Bicicleta con Camioneta? Bici->Cam: {bici_a_cam}, Cam->Bici: {cam_a_bici}")

print("\n[FIN ACTIVIDAD 3]")
