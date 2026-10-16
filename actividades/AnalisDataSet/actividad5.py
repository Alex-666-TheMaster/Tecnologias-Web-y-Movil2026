"""
Actividad 5 — El dron es minoria: balanceo del dataset
Prueba diferentes estrategias de balanceo (submuestreo, sobremuestreo, class_weight, trampas)
y evalua precision, recall, y sugerencias imposibles con es_posible.
"""

import sys, os
dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios'))
sys.path.insert(0, dataset_dir)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score
from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO
from usar_modelo import es_posible

print("=" * 70)
print("ACTIVIDAD 5 — BALANCEO DEL DATASET")
print("=" * 70)

CSV = os.path.join(dataset_dir, 'envios_medios.csv')
datos = pd.read_csv(CSV)

x = datos[NUMERICAS + CATEGORICAS]
y = datos[OBJETIVO]

# 1. Separar primero (Regla de oro: prueba intacta de 2000 datos)
x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=42
)

def evaluar(x_tr, y_tr, x_te, y_te, class_weight=None, nombre=""):
    prep = ColumnTransformer([
        ("numericas", "passthrough", NUMERICAS),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
    ])
    
    modelo = Pipeline([
        ("preparacion", prep),
        ("arbol", DecisionTreeClassifier(
            max_depth=8, min_samples_leaf=5, random_state=42, class_weight=class_weight
        )),
    ])
    
    modelo.fit(x_tr, y_tr)
    pred = modelo.predict(x_te)
    
    acc = accuracy_score(y_te, pred)
    prec_dron = precision_score(y_te, pred, labels=["dron"], average=None)[0]
    rec_dron = recall_score(y_te, pred, labels=["dron"], average=None)[0]
    veces_dron = (pred == "dron").sum()
    
    # Contar sugerencias imposibles
    df_eval = x_te.copy()
    df_eval["predicho"] = pred
    imposibles = 0
    for _, fila in df_eval.iterrows():
        paq = fila.to_dict()
        med = paq["predicho"]
        if not es_posible(med, paq):
            imposibles += 1
            
    return {
        "Estrategia": nombre,
        "Envíos entreno": len(x_tr),
        "Exactitud": f"{acc:.3%}",
        "Precision dron": f"{prec_dron:.3f}",
        "Recall dron": f"{rec_dron:.3f}",
        "Veces predice dron": veces_dron,
        "Sugerencias imposibles": imposibles
    }

resultados = []

# Estrategia 1: Sin balancear
r1 = evaluar(x_entreno, y_entreno, x_prueba, y_prueba, nombre="Sin balancear")
resultados.append(r1)

# Estrategia 2: Submuestreo (Undersampling) de clases mayoritarias
df_tr = x_entreno.copy()
df_tr["target"] = y_entreno
n_drones = (df_tr["target"] == "dron").sum() # ~758
# Muestreamos a lo mucho n_drones * 2 para las demas o al tamaño del dron
df_sub = pd.concat([
    df_tr[df_tr["target"] == "dron"],
    df_tr[df_tr["target"] == "camioneta"].sample(n=min(len(df_tr[df_tr["target"] == "camioneta"]), n_drones), random_state=42),
    df_tr[df_tr["target"] == "bicicleta"].sample(n=min(len(df_tr[df_tr["target"] == "bicicleta"]), n_drones), random_state=42),
    df_tr[df_tr["target"] == "moto"].sample(n=min(len(df_tr[df_tr["target"] == "moto"]), n_drones), random_state=42),
])
r2 = evaluar(df_sub[NUMERICAS + CATEGORICAS], df_sub["target"], x_prueba, y_prueba, nombre="Submuestreo (Undersampling)")
resultados.append(r2)

# Estrategia 3: Sobremuestreo (Oversampling) de dron (duplicar/triplicar drones)
drones_tr = df_tr[df_tr["target"] == "dron"]
df_over = pd.concat([df_tr, drones_tr, drones_tr, drones_tr]) # x4 drones
r3 = evaluar(df_over[NUMERICAS + CATEGORICAS], df_over["target"], x_prueba, y_prueba, nombre="Sobremuestreo (Oversampling x4)")
resultados.append(r3)

# Estrategia 4: class_weight='balanced'
r4 = evaluar(x_entreno, y_entreno, x_prueba, y_prueba, class_weight="balanced", nombre="class_weight='balanced'")
resultados.append(r4)

# Estrategia TRAMPA: Sobremuestreo ANTES de separar train/test (fuga de datos / data leakage)
df_todo = x.copy()
df_todo["target"] = y
drones_todo = df_todo[df_todo["target"] == "dron"]
df_trampa = pd.concat([df_todo, drones_todo, drones_todo, drones_todo])
x_trampa_tr, x_trampa_te, y_trampa_tr, y_trampa_te = train_test_split(
    df_trampa[NUMERICAS + CATEGORICAS], df_trampa["target"], test_size=0.2, random_state=42
)
r_trampa = evaluar(x_trampa_tr, y_trampa_tr, x_trampa_te, y_trampa_te, nombre="Trampa (Data Leakage antes split)")
resultados.append(r_trampa)

df_res = pd.DataFrame(resultados)
print("\n[RESULTADOS COMPARATIVOS]")
print(df_res.to_string(index=False))

print("\n[FIN ACTIVIDAD 5]")
