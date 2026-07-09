# ✈️ SIMA - Sistema Inteligente de Monitoreo Aeroportuario

## Proyecto End-to-End de Ciencia de Datos e Ingeniería de Software

SIMA (Sistema Inteligente de Monitoreo Aeroportuario) es una solución desarrollada bajo un enfoque **End-to-End**, cuyo propósito es integrar, procesar, almacenar, analizar y visualizar información relacionada con operaciones aeroportuarias.

El proyecto implementa un pipeline completo de Ciencia de Datos, integrando procesos ETL, una base de datos SQLite, una API REST desarrollada con FastAPI, dashboards interactivos en Streamlit, técnicas de Machine Learning y una estrategia de despliegue mediante Docker.

---

# 👥 Integrantes

- Millaray Paillafil
- Luna Cortés
- Javiera Marchesse
- Kimberly Bobadilla

---

# 🎯 Objetivo

Desarrollar una plataforma capaz de:

- Integrar múltiples fuentes de datos.
- Automatizar procesos ETL.
- Almacenar información en SQLite.
- Exponer datos mediante una API REST.
- Visualizar información mediante dashboards interactivos.
- Aplicar técnicas de Machine Learning para análisis de datos.
- Facilitar el despliegue mediante Docker.

---

# 🏗 Arquitectura del proyecto

```
                CSV + API Open-Meteo
                         │
                         ▼
                    ETL (Python)
                         │
                         ▼
                    SQLite Database
                         │
                         ▼
                   FastAPI REST API
                         │
                         ▼
                Dashboard Streamlit
                         │
                         ▼
             Machine Learning + Análisis
                         │
                         ▼
                 Docker + Docker Compose
```

---

# 📂 Estructura del proyecto

```
Proyecto_Aeropuertos/

│
├── api/
│   ├── database.py
│   ├── main.py
│   └── openmeteo.py
│
├── dashboard/
│   └── dashboard_inicio.py
│
├── data/
│
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.dashboard
│   └── docker-compose.yml
│
├── docs/
│
├── etl/
│   ├── ETL.ipynb
│   └── etl_evaluacion.py
│
├── models/
│   └── modelos_supervisados.py
│
├── tests/
│
├── README.md
│
└── requirements.txt
```

---

# ⚙️ Tecnologías utilizadas

- Python
- Pandas
- NumPy
- SQLite
- FastAPI
- Streamlit
- Scikit-Learn
- Plotly
- Open-Meteo API
- Docker
- Docker Compose
- Pytest

---

# 🔄 Pipeline ETL

El proyecto implementa un proceso ETL compuesto por las siguientes etapas:

## Extracción

- Dataset de operaciones aeroportuarias (CSV).
- Información meteorológica desde Open-Meteo.

## Transformación

- Validación del esquema.
- Eliminación de duplicados.
- Tratamiento de valores nulos.
- Conversión de tipos de datos.
- Agrupaciones mediante Pandas.
- Pivot Tables.
- Ranking de aeropuertos.
- Transformaciones vectorizadas.

## Carga

Los datos procesados son almacenados en SQLite para ser consumidos posteriormente por la API REST.

---

# 🤖 Machine Learning

Se implementaron modelos de aprendizaje supervisado y no supervisado.

## Supervisados

- Regresión Logística
- Árbol de Decisión
- Random Forest

Se comparan utilizando:

- Accuracy
- Precision
- Recall
- F1-score
- Matriz de Confusión
- GridSearchCV

## No supervisados

- K-Means
- PCA

Estos modelos permiten identificar patrones y realizar análisis exploratorios sobre las operaciones aeroportuarias.

---

# 🌐 API REST

La API fue desarrollada utilizando FastAPI.

Principales endpoints:

- /estadisticas
- /operaciones
- /aeropuertos
- /clima

La documentación interactiva se encuentra disponible mediante Swagger.

---

# 📊 Dashboard

El sistema incorpora un dashboard desarrollado con Streamlit que permite:

- Visualizar KPIs.
- Consultar operaciones aeroportuarias.
- Visualizar gráficos interactivos.
- Mostrar información meteorológica.
- Explorar resultados de Machine Learning.

---

# 🗄 Base de datos

Se utilizó SQLite debido a que:

- Es ligera.
- No requiere servidor.
- Es portable.
- Facilita el despliegue.
- Se integra fácilmente con FastAPI.

---

# 🧪 Testing

Se desarrollaron pruebas automatizadas utilizando Pytest para validar:

- API REST.
- Base de datos SQLite.
- Integración con Open-Meteo.
- Funciones principales del proyecto.

---

# 🐳 Docker

El proyecto incorpora contenedores Docker para facilitar su despliegue.

Archivos incluidos:

- Dockerfile API
- Dockerfile Dashboard
- Docker Compose

Permite ejecutar toda la solución mediante un único comando.

---

# 🚀 Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/mipaillafil/Proyecto_Aeropuertos.git
```

---

## 2. Crear entorno virtual

```bash
python -m venv .venv
```

---

## 3. Activar entorno virtual

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶ Ejecutar ETL

```bash
python etl/etl_evaluacion.py
```

---

# ▶ Ejecutar API

```bash
uvicorn api.main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# ▶ Ejecutar Dashboard

```bash
streamlit run dashboard/dashboard_inicio.py
```

---

# ▶ Ejecutar Tests

```bash
pytest tests/
```

---

# ▶ Ejecutar Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

---

# 📈 Resultados obtenidos

Durante el desarrollo del proyecto se logró:

- Automatizar el proceso ETL.
- Integrar múltiples fuentes de datos.
- Implementar una API REST.
- Centralizar la información en SQLite.
- Construir dashboards interactivos.
- Aplicar modelos de Machine Learning.
- Incorporar pruebas automatizadas.
- Preparar el proyecto para despliegue mediante Docker.

---

# 📖 Documentación

La documentación técnica y el informe del proyecto se encuentran disponibles en la carpeta:

```
docs/
```

---

# 📌 Conclusiones

SIMA constituye una solución End-to-End que integra Ciencia de Datos e Ingeniería de Software para apoyar el monitoreo de operaciones aeroportuarias.

La combinación de ETL, SQLite, FastAPI, Streamlit, Machine Learning, Testing y Docker permitió construir una plataforma modular, escalable y preparada para escenarios reales de análisis de datos.

