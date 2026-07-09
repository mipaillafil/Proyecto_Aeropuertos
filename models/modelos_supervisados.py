from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "operaciones_aeropuertos_clean.csv"
RESULTADOS_PATH = BASE_DIR / "models" / "resultados_modelos.txt"


def cargar_datos() -> pd.DataFrame:
    """
    Carga el dataset limpio generado por el ETL.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "No existe operaciones_aeropuertos_clean.csv. "
            "Primero ejecuta etl/etl_evaluacion.py"
        )

    return pd.read_csv(DATA_PATH)


def preparar_datos(df: pd.DataFrame):
    """
    Prepara los datos para modelos supervisados.

    La variable objetivo alta_operacion indica si el número de operaciones
    está sobre la mediana del dataset.
    """
    df = df.copy()

    df["alta_operacion"] = (
        df["cnt_operaciones"] > df["cnt_operaciones"].median()
    ).astype(int)

    X = df.select_dtypes(include=["int64", "float64"]).drop(
        columns=["alta_operacion"],
        errors="ignore"
    )

    y = df["alta_operacion"]

    X = X.fillna(X.median())

    return X, y


def entrenar_modelos() -> None:
    """
    Entrena, ajusta y compara múltiples modelos supervisados.
    """
    df = cargar_datos()
    X, y = preparar_datos(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    modelos = {
        "Regresión Logística": Pipeline([
            ("scaler", StandardScaler()),
            ("modelo", LogisticRegression(max_iter=1000))
        ]),
        "Árbol de Decisión": Pipeline([
            ("modelo", DecisionTreeClassifier(random_state=42))
        ]),
        "Random Forest": Pipeline([
            ("modelo", RandomForestClassifier(random_state=42))
        ])
    }

    parametros = {
        "Regresión Logística": {
            "modelo__C": [0.1, 1, 10]
        },
        "Árbol de Decisión": {
            "modelo__max_depth": [3, 5, 10, None],
            "modelo__min_samples_split": [2, 5, 10]
        },
        "Random Forest": {
            "modelo__n_estimators": [50, 100],
            "modelo__max_depth": [3, 5, None]
        }
    }

    RESULTADOS_PATH.parent.mkdir(exist_ok=True)

    mejor_modelo = None
    mejor_f1 = 0

    with open(RESULTADOS_PATH, "w", encoding="utf-8") as archivo:
        archivo.write("Comparación de modelos supervisados\n")
        archivo.write("=" * 60 + "\n\n")

        for nombre, pipeline in modelos.items():
            grid = GridSearchCV(
                estimator=pipeline,
                param_grid=parametros[nombre],
                cv=3,
                scoring="f1",
                n_jobs=-1
            )

            grid.fit(X_train, y_train)

            predicciones = grid.predict(X_test)

            accuracy = accuracy_score(y_test, predicciones)
            precision = precision_score(y_test, predicciones)
            recall = recall_score(y_test, predicciones)
            f1 = f1_score(y_test, predicciones)
            matriz = confusion_matrix(y_test, predicciones)
            reporte = classification_report(y_test, predicciones)

            archivo.write(f"Modelo: {nombre}\n")
            archivo.write(f"Mejores parámetros: {grid.best_params_}\n")
            archivo.write(f"Accuracy: {accuracy:.4f}\n")
            archivo.write(f"Precision: {precision:.4f}\n")
            archivo.write(f"Recall: {recall:.4f}\n")
            archivo.write(f"F1-score: {f1:.4f}\n")
            archivo.write(f"Matriz de confusión:\n{matriz}\n\n")
            archivo.write(f"Reporte de clasificación:\n{reporte}\n")
            archivo.write("-" * 60 + "\n\n")

            if f1 > mejor_f1:
                mejor_f1 = f1
                mejor_modelo = nombre

        archivo.write(f"Mejor modelo según F1-score: {mejor_modelo}\n")
        archivo.write(f"Mejor F1-score: {mejor_f1:.4f}\n")

    print("Modelos entrenados correctamente.")
    print(f"Mejor modelo: {mejor_modelo}")
    print(f"Mejor F1-score: {mejor_f1:.4f}")
    print(f"Resultados guardados en: {RESULTADOS_PATH}")


if __name__ == "__main__":
    entrenar_modelos()