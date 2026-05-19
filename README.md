# Operaciones de Aeropuertos - Machine Learning Project

## Integrantes
- LUNA CORTES
- JAVIERA MARCHESSE
- MILLARAY PAILLAFIL

---

# Descripción

Proyecto de Ciencia de Datos y Machine Learning enfocado en el análisis de operaciones aeroportuarias, utilizando técnicas de limpieza, transformación, modelado supervisado y aprendizaje no supervisado para generar análisis predictivos y segmentación de datos.

El proyecto fue desarrollado en el contexto de la asignatura SCY1101 - Programación para la Ciencia de Datos.

---

# Objetivo del Proyecto

Desarrollar una solución completa de Machine Learning que permita:

- Analizar patrones en operaciones aeroportuarias.
- Predecir comportamientos utilizando modelos supervisados.
- Segmentar datos mediante técnicas no supervisadas.
- Optimizar modelos utilizando técnicas avanzadas de hiperparámetros.
- Interpretar resultados y apoyar la toma de decisiones.

---

# Dataset

## Archivos utilizados
- `operaciones_aeropuertos_dirty.csv` → Datos originales
- `operaciones_aeropuertos_clean.csv` → Datos limpios y procesados

## Características del dataset

El dataset contiene información relacionada con operaciones aeroportuarias, incluyendo variables numéricas y categóricas utilizadas para análisis exploratorio, modelado predictivo y segmentación de datos.

---

# Metodología

## 1. Limpieza de Datos

Se aplicaron distintas técnicas de limpieza para garantizar calidad y consistencia de los datos:

- Eliminación de duplicados
- Tratamiento de valores nulos
- Limpieza de strings
- Conversión de tipos de datos
- Eliminación de outliers mediante método IQR

---

## 2. Transformación de Datos

Se implementó un pipeline utilizando Scikit-learn.

### Variables numéricas
- Imputación con media
- Escalamiento utilizando `StandardScaler`

### Variables categóricas
- Imputación con moda
- Codificación usando `OneHotEncoder`

### Automatización
- Uso de `ColumnTransformer`
- Uso de pipelines reproducibles

---

## 3. Feature Engineering

Se generaron nuevas variables derivadas para mejorar el desempeño de los modelos.

### Variables creadas
- `total_operaciones`

---

# Modelos Supervisados

Se implementaron distintos algoritmos de Machine Learning utilizando Scikit-learn.

## Modelos utilizados

### Logistic Regression
Modelo base utilizado para clasificación debido a su interpretabilidad y eficiencia computacional.

### Decision Tree
Modelo capaz de detectar relaciones no lineales entre variables.

### Random Forest
Modelo basado en múltiples árboles de decisión que mejora robustez y capacidad de generalización.

### Support Vector Machine (SVM)
Modelo utilizado para encontrar fronteras de separación más complejas entre clases.

---

# Evaluación de Modelos Supervisados

Los modelos fueron evaluados utilizando múltiples métricas:

- Accuracy
- Precision
- Recall
- F1-Score
- Matriz de confusión
- Cross Validation

Se realizó una comparación entre modelos para seleccionar la alternativa con mejor rendimiento y capacidad de generalización.

---

# Optimización de Hiperparámetros

Se implementaron técnicas de optimización utilizando:

- GridSearchCV
- RandomizedSearchCV

La optimización permitió encontrar configuraciones más eficientes y mejorar el desempeño predictivo de los modelos.

---

# Modelos No Supervisados

También se aplicaron técnicas de aprendizaje no supervisado para segmentar y visualizar patrones ocultos dentro del dataset.

---

## K-Means Clustering

Se utilizó el algoritmo K-Means para agrupar registros con características similares.

### Objetivos del clustering
- Detectar patrones ocultos
- Identificar segmentos de datos
- Analizar similitudes entre operaciones aeroportuarias

---

## Método del Codo

Se utilizó el método del codo para determinar la cantidad óptima de clusters.

Esta técnica permitió evaluar la variación de la inercia según distintos valores de K.

---

## Silhouette Score

Se aplicó la métrica Silhouette Score para evaluar la calidad de los clusters generados.

### Interpretación
- Valores cercanos a 1 indican clusters bien definidos
- Valores cercanos a 0 indican solapamiento entre grupos

---

## PCA - Principal Component Analysis

Se utilizó PCA para reducir dimensionalidad y visualizar los clusters en un espacio bidimensional.

### Objetivos del PCA
- Reducir complejidad del dataset
- Facilitar visualización
- Identificar patrones de agrupamiento

---

# Visualizaciones

Se desarrollaron distintas visualizaciones utilizando Matplotlib y Seaborn:

- Histogramas
- Boxplots
- Heatmaps
- Matrices de confusión
- Comparación de métricas
- Método del codo
- Visualización PCA
- Scatterplots de clusters

---

# Tecnologías Utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Google Colab

---

# Resultados Principales

- Implementación exitosa de múltiples modelos supervisados.
- Comparación técnica utilizando métricas avanzadas.
- Optimización de hiperparámetros para mejorar rendimiento.
- Segmentación de datos mediante clustering.
- Visualización de patrones utilizando PCA.
- Identificación de grupos similares dentro del dataset.

---

# Conclusiones

El proyecto permitió aplicar un flujo completo de Machine Learning, desde limpieza y transformación de datos hasta evaluación, optimización y análisis de modelos supervisados y no supervisados.

Los modelos supervisados permitieron generar predicciones robustas utilizando distintas métricas de evaluación.

Por otra parte, las técnicas no supervisadas facilitaron la identificación de patrones y segmentaciones dentro del dataset, permitiendo visualizar relaciones complejas mediante PCA y clustering.

Los resultados obtenidos demostraron el uso práctico de técnicas de ciencia de datos aplicadas a problemas reales relacionados con operaciones aeroportuarias.

---

# Cómo Ejecutar

## Instalar dependencias

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Ejecutar notebooks

Abrir los notebooks en Google Colab o Jupyter Notebook y ejecutar las celdas en orden.

---

# Referencias

- Documentación oficial Scikit-learn
- Documentación oficial Pandas
- Documentación oficial Matplotlib
- Material de clases SCY1101
