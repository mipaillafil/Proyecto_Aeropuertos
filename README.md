# Operaciones de Aeropuertos - Data Cleaning Pipeline

## Integrantes
- LUNA CORTES
- JAVIERA MARCHESSE
- MILLARAY PAILLAFIL

---

## Descripción

Proyecto de limpieza y transformación de un dataset de operaciones de aeropuertos, aplicando técnicas de ciencia de datos para obtener un dataset limpio, estructurado y reproducible.

---

## Dataset

- `operaciones_aeropuertos_dirty.csv` (datos crudos)
- Contiene valores nulos, duplicados y variables sin procesar

---

## Metodología

### Limpieza
- Eliminación de duplicados
- Limpieza de strings
- Análisis de nulos

### Transformación (Pipeline)
- Variables numéricas:
  - Imputación con media
  - Escalamiento (StandardScaler)

- Variables categóricas:
  - Imputación con moda
  - OneHotEncoding

- Uso de `ColumnTransformer` para automatizar el proceso

### Feature Engineering
- Creación de `total_operaciones`

### Outliers
- Eliminación usando método IQR

### Visualización
- Histograma de `total_operaciones`

---
## Tecnologías

Python · Pandas · Scikit-learn · Matplotlib · Google Colab
