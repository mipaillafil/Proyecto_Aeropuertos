# Sistema Inteligente de Monitoreo Aeroportuario

## Integrantes
- LUNA CORTES
- JAVIERA MARCHESSE
- MILLARAY PAILLAFIL

## Video Explicativo
[Video Explicativo SIMA]([https://docs.google.com/presentation/d/1yfsZC-XnGhXcnPUYcO-Szv88AsTuREfW/edit?usp=drive_link&ouid=117212070881843989884&rtpof=true&sd=true](https://drive.google.com/file/d/1ZcUxbGLnGgDdEpzNlXXXOu1QAvv_KkIF/view?usp=drive_link))


## Descripción del Proyecto

SIMA (Sistema Inteligente de Monitoreo Aeroportuario) es una solución End-to-End desarrollada para la asignatura Programación para la Ciencia de Datos.

El proyecto tiene como objetivo centralizar, procesar, analizar y visualizar información relacionada con operaciones aeroportuarias mediante técnicas de Ciencia de Datos, Ingeniería de Datos y Machine Learning. Para ello se implementó una arquitectura modular que integra procesos ETL, almacenamiento en SQLite, servicios REST mediante FastAPI y dashboards interactivos desarrollados con Streamlit.

La solución permite transformar datos operacionales en información útil para distintos tipos de usuarios, apoyando la toma de decisiones estratégicas, operativas y técnicas.

---

# Objetivos

## Objetivo General

Desarrollar una plataforma integral para el monitoreo y análisis de operaciones aeroportuarias utilizando herramientas modernas de Ciencia de Datos.

## Objetivos Específicos

* Implementar un pipeline ETL para la preparación y limpieza de datos.
* Integrar múltiples fuentes de información.
* Construir una base de datos SQLite para almacenamiento persistente.
* Desarrollar una API REST utilizando FastAPI.
* Diseñar dashboards interactivos para diferentes perfiles de usuario.
* Aplicar técnicas de Machine Learning para análisis exploratorio avanzado.
* Implementar pruebas automatizadas para garantizar la calidad del sistema.

---

# Arquitectura de la Solución

```text
Dataset Operaciones Aeroportuarias
            │
            ▼
      Pipeline ETL
            │
            ▼
          SQLite
            │
            ▼
         FastAPI
            │
            ├── Estadísticas
            ├── Operaciones
            ├── Aeropuertos
            └── Open-Meteo
            │
            ▼
    Dashboard Streamlit
            │
            ├── Ejecutivo
            ├── Operativo
            └── Técnico
            │
            ▼
     Machine Learning
      (K-Means y PCA)
```

---

# Estructura del Proyecto

```text
Proyecto_Aeropuertos_Cortes_Marchesse_Paillafil
│
├── api/
│   ├── main.py
│   ├── database.py
│   └── openmeteo.py
│
├── dashboard/
│   └── dashboard-inicio.py
│
├── data/
│   ├── operaciones_aeropuertos.csv
│   ├── operaciones_aeropuertos_clean.csv
│   └── aeropuertos.db
│
├── etl/
│   └── ETL.ipynb
│
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_openmeteo.py
│
├── requirements.txt
└── README.md
```

---

# Pipeline ETL

El proceso ETL contempla tres etapas fundamentales:

## Extracción

Obtención de datos desde:

* Dataset de operaciones aeroportuarias.
* API Open-Meteo.
* Base de datos SQLite.

## Transformación

Se realizaron:

* Limpieza de datos.
* Tratamiento de valores faltantes.
* Validación de registros.
* One-Hot Encoding.
* Normalización de variables.

## Carga

Los datos procesados son almacenados en SQLite para su posterior explotación mediante la API REST.

---

# Base de Datos

Se utiliza SQLite como sistema de almacenamiento local.

Base de datos:

```text
aeropuertos.db
```

Tabla principal:

```text
operaciones
```

La API consulta directamente esta base de datos para entregar información actualizada al dashboard.

---

# API REST (FastAPI)

La API fue desarrollada utilizando FastAPI.

## Endpoints Disponibles

### Estado de la API

```http
GET /
```

### Estadísticas Generales

```http
GET /api/v1/estadisticas
```

### Operaciones

```http
GET /api/v1/operaciones
```

### Aeropuertos

```http
GET /api/v1/aeropuertos
```

### Información Meteorológica

```http
GET /api/v1/clima
```

## Documentación Swagger

```text
http://localhost:8000/docs
```

---

# Dashboard Ejecutivo

Orientado a usuarios estratégicos.

Funcionalidades:

* KPIs generales.
* Ranking de aeropuertos.
* Métricas agregadas.
* Distribución de operaciones.

---

# Dashboard Operativo

Orientado a usuarios operacionales.

Funcionalidades:

* Filtros por aeropuerto.
* Métricas operativas.
* Integración con Open-Meteo.
* Monitoreo de actividad aeroportuaria.

---

# Dashboard Técnico

Orientado a analistas y científicos de datos.

Funcionalidades:

* Clustering mediante K-Means.
* PCA (Principal Component Analysis).
* Visualización de clusters.
* Análisis exploratorio avanzado.

---

# Machine Learning

## Algoritmos Utilizados

### K-Means

Permite identificar segmentos operacionales y agrupaciones de comportamiento.

### PCA

Reduce la dimensionalidad del conjunto de datos para facilitar la visualización de patrones.

---

# Integración Open-Meteo

La plataforma consume información meteorológica en tiempo real utilizando Open-Meteo.

Variables utilizadas:

* Temperatura.
* Velocidad del viento.
* Dirección del viento.
* Código meteorológico.

---

# Testing Automatizado

Se implementaron pruebas automatizadas para validar el correcto funcionamiento de los principales componentes del sistema.

## Pruebas Implementadas

### API

* Validación de endpoints.
* Respuesta HTTP correcta.
* Integridad de respuestas JSON.

### Base de Datos

* Verificación de conexión SQLite.
* Validación de consultas.
* Integridad de datos.

### Open-Meteo

* Consumo correcto de la API.
* Validación de estructura de respuesta.

Objetivo:

Garantizar la estabilidad, calidad y confiabilidad de la solución.

---

# Próximas Mejoras

## Containerización con Docker

Como siguiente etapa del proyecto se contempla la incorporación de Docker para facilitar el despliegue y la reproducibilidad del sistema.

Implementaciones planificadas:

* Dockerfile para FastAPI.
* Dockerfile para Streamlit.
* docker-compose para orquestación de servicios.
* Configuración mediante variables de entorno.

Beneficios esperados:

* Portabilidad.
* Despliegue simplificado.
* Reproducibilidad del entorno.
* Escalabilidad futura.

---

# Ejecución del Proyecto

## Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar API

```bash
uvicorn api.main:app --reload
```

## Ejecutar Dashboard

```bash
streamlit run dashboard/dashboard-inicio.py
```

## Ejecutar Tests

```bash
pytest tests/
```

---

# Tecnologías Utilizadas

* Python
* Pandas
* NumPy
* SQLite
* FastAPI
* Streamlit
* Plotly
* Scikit-Learn
* Pytest
* Open-Meteo API

---

# Asignatura
 Programación para la Ciencia de Datos

Duoc UC
