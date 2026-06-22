import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import requests

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Sistema Inteligente de Monitoreo Aeroportuario",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    padding: 20px 0 10px 0;
}
.sub-title {
    text-align: center;
    color: #7f8c8d;
    font-size: 1.2rem;
    margin-bottom: 30px;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 10px 0;
}
.metric-card .value {
    font-size: 2rem;
    font-weight: bold;
}
.metric-card .label {
    font-size: 0.9rem;
}
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    border-top: 2px solid #e8e8e8;
    color: #7f8c8d;
}
</style>
""", unsafe_allow_html=True)


if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "inicio"


@st.cache_data(ttl=60)
def cargar_datos_api():
    response = requests.get(f"{API_URL}/operaciones")
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    aeropuertos = [
        c for c in df.columns
        if c.startswith("aeropuerto_oaci_")
    ]

    if aeropuertos:
        df["aeropuerto"] = (
            df[aeropuertos]
            .idxmax(axis=1)
            .str.replace("aeropuerto_oaci_", "")
        )
    else:
        df["aeropuerto"] = "No definido"

    return df


@st.cache_data(ttl=60)
def cargar_estadisticas_api():
    response = requests.get(f"{API_URL}/estadisticas")
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def cargar_clima_api():
    response = requests.get(f"{API_URL}/clima")
    response.raise_for_status()
    return response.json()


try:
    df = cargar_datos_api()
    stats = cargar_estadisticas_api()
    api_activa = True
except Exception as e:
    st.error("❌ No se pudo conectar con la API FastAPI.")
    st.info("Primero ejecuta la API con: uvicorn api.main:app --reload")
    st.exception(e)
    st.stop()


with st.sidebar:
    st.markdown("### ✈️ Sistema SIMA")
    st.success("✅ Conectado a FastAPI")
    st.caption("Datos consumidos desde SQLite mediante API REST")

    st.markdown("---")

    vista = st.radio(
        "Ir a:",
        ["🏠 Inicio", "📊 Ejecutivo", "⚙️ Operativo", "🤖 Técnico"]
    )

    mapa_vistas = {
        "🏠 Inicio": "inicio",
        "📊 Ejecutivo": "ejecutivo",
        "⚙️ Operativo": "operativo",
        "🤖 Técnico": "tecnico"
    }

    st.session_state.vista_actual = mapa_vistas[vista]

    st.markdown("---")
    st.markdown("### 🎯 Filtros Globales")

    aeropuerto_options = ["Todos"] + sorted(df["aeropuerto"].unique())

    aeropuerto_seleccionado = st.selectbox(
        "📍 Aeropuerto",
        aeropuerto_options
    )

    min_ops = float(df["cnt_operaciones"].min())
    max_ops = float(df["cnt_operaciones"].max())

    rango_operaciones = st.slider(
        "📊 Rango de operaciones",
        min_value=min_ops,
        max_value=max_ops,
        value=(min_ops, max_ops),
        step=0.1
    )

    st.markdown("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar datos",
        data=csv,
        file_name="datos_sima.csv",
        mime="text/csv"
    )


df_filtrado = df.copy()

if aeropuerto_seleccionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["aeropuerto"] == aeropuerto_seleccionado
    ]

df_filtrado = df_filtrado[
    (df_filtrado["cnt_operaciones"] >= rango_operaciones[0]) &
    (df_filtrado["cnt_operaciones"] <= rango_operaciones[1])
]


if st.session_state.vista_actual == "inicio":
    st.markdown(
        '<div class="main-title">✈️ Sistema Inteligente de Monitoreo Aeroportuario</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Dashboard conectado a SQLite mediante FastAPI</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registros API", stats["total_registros"])

    with col2:
        st.metric("Registros filtrados", len(df_filtrado))

    with col3:
        st.metric("Aeropuertos", df_filtrado["aeropuerto"].nunique())

    with col4:
        st.metric(
            "Promedio operaciones",
            round(df_filtrado["cnt_operaciones"].mean(), 2)
        )

    st.markdown("---")

    st.info("""
    Este dashboard consume datos desde una API REST desarrollada con FastAPI.
    La API obtiene los datos desde una base SQLite, cumpliendo la arquitectura:
    CSV → SQLite → FastAPI → Streamlit.
    """)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("📊 Dashboard Ejecutivo", use_container_width=True):
            st.session_state.vista_actual = "ejecutivo"
            st.rerun()

    with col_b:
        if st.button("⚙️ Dashboard Operativo", use_container_width=True):
            st.session_state.vista_actual = "operativo"
            st.rerun()

    with col_c:
        if st.button("🤖 Dashboard Técnico", use_container_width=True):
            st.session_state.vista_actual = "tecnico"
            st.rerun()


elif st.session_state.vista_actual == "ejecutivo":
    st.markdown(
        '<div class="main-title">📊 Dashboard Ejecutivo</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total registros", len(df_filtrado))

    with col2:
        st.metric(
            "Promedio",
            round(df_filtrado["cnt_operaciones"].mean(), 2)
        )

    with col3:
        st.metric(
            "Máximo",
            round(df_filtrado["cnt_operaciones"].max(), 2)
        )

    with col4:
        st.metric(
            "Mínimo",
            round(df_filtrado["cnt_operaciones"].min(), 2)
        )

    with col5:
        st.metric("Aeropuertos", df_filtrado["aeropuerto"].nunique())

    st.markdown("---")

    top = (
        df_filtrado["aeropuerto"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top.columns = ["Aeropuerto", "Operaciones"]

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig = px.bar(
            top,
            x="Operaciones",
            y="Aeropuerto",
            orientation="h",
            title="Top 10 Aeropuertos"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        fig2 = px.histogram(
            df_filtrado,
            x="cnt_operaciones",
            nbins=30,
            title="Distribución de operaciones"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Resumen por aeropuerto")

    resumen = df_filtrado.groupby("aeropuerto").agg({
        "cnt_operaciones": ["count", "mean", "sum", "std", "min", "max"]
    }).round(2)

    resumen.columns = [
        "Registros",
        "Promedio",
        "Total",
        "Desviación",
        "Mínimo",
        "Máximo"
    ]

    st.dataframe(resumen, use_container_width=True)


elif st.session_state.vista_actual == "operativo":
    st.markdown(
        '<div class="main-title">⚙️ Dashboard Operativo</div>',
        unsafe_allow_html=True
    )

    aeropuertos = sorted(df_filtrado["aeropuerto"].unique())

    if len(aeropuertos) == 0:
        st.warning("No hay datos con los filtros seleccionados.")
        st.stop()

    aeropuerto = st.selectbox(
        "Seleccionar aeropuerto",
        aeropuertos
    )

    filtrado = df_filtrado[
        df_filtrado["aeropuerto"] == aeropuerto
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registros", len(filtrado))

    with col2:
        st.metric(
            "Promedio",
            round(filtrado["cnt_operaciones"].mean(), 2)
        )

    with col3:
        st.metric(
            "Máximo",
            round(filtrado["cnt_operaciones"].max(), 2)
        )

    with col4:
        st.metric(
            "Mínimo",
            round(filtrado["cnt_operaciones"].min(), 2)
        )

    st.markdown("---")

    st.subheader("🌦️ Condiciones meteorológicas desde Open-Meteo")

    try:
        clima = cargar_clima_api()
        clima_actual = clima["current_weather"]

        col_c1, col_c2, col_c3, col_c4 = st.columns(4)

        with col_c1:
            st.metric(
                "Temperatura",
                f"{clima_actual['temperature']} °C"
            )

        with col_c2:
            st.metric(
                "Viento",
                f"{clima_actual['windspeed']} km/h"
            )

        with col_c3:
            st.metric(
                "Dirección viento",
                clima_actual["winddirection"]
            )

        with col_c4:
            st.metric(
                "Código clima",
                clima_actual["weathercode"]
            )

    except Exception as e:
        st.warning("No se pudo obtener el clima desde la API.")
        st.exception(e)

    st.markdown("---")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig = px.histogram(
            filtrado,
            x="cnt_operaciones",
            nbins=20,
            title=f"Distribución de operaciones - {aeropuerto}"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        fig2 = px.box(
            filtrado,
            y="cnt_operaciones",
            title=f"Variabilidad operacional - {aeropuerto}"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Datos operativos")

    st.dataframe(
        filtrado[["aeropuerto", "cnt_operaciones"]].head(50),
        use_container_width=True
    )


elif st.session_state.vista_actual == "tecnico":
    st.markdown(
        '<div class="main-title">🤖 Dashboard Técnico</div>',
        unsafe_allow_html=True
    )

    if len(df_filtrado) == 0:
        st.warning("No hay datos con los filtros seleccionados.")
        st.stop()

    numeric_cols = df_filtrado.select_dtypes(
        include=[np.number]
    ).columns.tolist()

    selected_cols = st.multiselect(
        "Variables para análisis técnico",
        options=numeric_cols,
        default=numeric_cols[:3]
    )

    n_clusters = st.slider(
        "Número de clusters",
        min_value=2,
        max_value=6,
        value=3
    )

    if len(selected_cols) == 0:
        st.warning("Selecciona al menos una variable.")
        st.stop()

    X = df_filtrado[selected_cols].fillna(
        df_filtrado[selected_cols].mean()
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    clusters = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame(
        pca_result,
        columns=["PCA1", "PCA2"]
    )

    pca_df["Cluster"] = clusters.astype(str)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            pca_df,
            x="PCA1",
            y="PCA2",
            color="Cluster",
            title=f"K-Means con PCA - k={n_clusters}"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            x=["PC1", "PC2"],
            y=pca.explained_variance_ratio_,
            title="Varianza explicada por PCA",
            labels={
                "x": "Componente",
                "y": "Varianza explicada"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Distribución de clusters")

    cluster_counts = pd.Series(clusters).value_counts().sort_index()

    fig3 = px.pie(
        values=cluster_counts.values,
        names=[f"Cluster {i}" for i in cluster_counts.index],
        title="Distribución de clusters"
    )

    st.plotly_chart(fig3, use_container_width=True)


st.markdown("---")
st.markdown(f"""
<div class="footer">
    <strong>✈️ SIMA - Sistema Inteligente de Monitoreo Aeroportuario</strong> |
    Datos consumidos desde FastAPI |
    {len(df_filtrado):,} registros filtrados |
    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)