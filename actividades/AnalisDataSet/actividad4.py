"""
Actividad 4 — ¿Que columnas usa de verdad el modelo?
Calcula la importancia de caracteristicas del arbol y mide el impacto en exactitud al omitir cada columna.
"""

import sys, os
dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset-medios', 'dataset-medios'))
sys.path.insert(0, dataset_dir)

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO

print("=" * 70)
print("ACTIVIDAD 4 — QUE COLUMNAS USA DE VERDAD EL MODELO")
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
acc_base = (modelo.predict(x_prueba) == y_prueba).mean()
print(f"\n[1] Exactitud base con todas las columnas: {acc_base:.3%}")

# Importancias
importancias = modelo.named_steps["arbol"].feature_importances_
nombres = modelo.named_steps["preparacion"].get_feature_names_out()
nombres_limpios = [n.split("__", 1)[1] for n in nombres]

df_imp = pd.DataFrame({"caracteristica": nombres_limpios, "importancia": importancias})
df_imp = df_imp.sort_values(by="importancia", ascending=False).reset_index(drop=True)
print("\n[2] Importancia de cada caracteristica en el Pipeline (árbol):")
print(df_imp.to_string())

# Agrupando importancia por columna original
importancia_por_col = {}
for col in NUMERICAS:
    importancia_por_col[col] = df_imp[df_imp["caracteristica"] == col]["importancia"].sum()
for col in CATEGORICAS:
    importancia_por_col[col] = df_imp[df_imp["caracteristica"].str.startswith(col + "_")]["importancia"].sum()

serie_col = pd.Series(importancia_por_col).sort_values(ascending=False)
print("\n[3] Importancia acumulada por columna original:")
print(serie_col.map("{:.4f}".format).to_string())

# Impacto de quitar columnas
print("\n[4] Impacto de quitar cada columna (entrenando arbol depth=8, random_state=42):")
resultados_ablation = []

for col_drop in (NUMERICAS + CATEGORICAS):
    num_sub = [c for c in NUMERICAS if c != col_drop]
    cat_sub = [c for c in CATEGORICAS if c != col_drop]
    
    prep_sub = ColumnTransformer([
        ("numericas", "passthrough", num_sub),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), cat_sub),
    ])
    
    pipe_sub = Pipeline([
        ("preparacion", prep_sub),
        ("arbol", DecisionTreeClassifier(max_depth=8, min_samples_leaf=5, random_state=42)),
    ])
    
    pipe_sub.fit(x_entreno[num_sub + cat_sub], y_entreno)
    acc_sub = (pipe_sub.predict(x_prueba[num_sub + cat_sub]) == y_prueba).mean()
    delta = acc_sub - acc_base
    resultados_ablation.append({
        "columna_eliminada": col_drop,
        "exactitud": round(acc_sub, 4),
        "diferencia": round(delta, 4)
    })

df_ablation = pd.DataFrame(resultados_ablation).sort_values(by="exactitud")
print(df_ablation.to_string(index=False))

print("\n[FIN ACTIVIDAD 4]")
