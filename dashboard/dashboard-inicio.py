import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import requests
from requests.exceptions import RequestException

API_DEFAULT_URL = "http://127.0.0.1:8000"

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Sistema Inteligente de Monitoreo Aeroportuario",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# HELPER DE API
# ============================================

def normalize_api_url(base_url: str) -> str:
    return base_url.rstrip("/")

@st.cache_data
def fetch_api_json(endpoint: str):
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as exc:
        return {"error": str(exc)}

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mipaillafil/Proyecto_Aeropuertos_Cortes_Marchesse_Paillafil/main/data/operaciones_aeropuertos_clean.csv"
    df = pd.read_csv(url)

    aeropuertos = [c for c in df.columns if c.startswith("aeropuerto_oaci_")]

    df["aeropuerto"] = (
        df[aeropuertos]
        .idxmax(axis=1)
        .str.replace("aeropuerto_oaci_", "")
    )

    if "fecha" in df.columns:
        try:
            df["fecha"] = pd.to_datetime(df["fecha"])
            df["año"] = df["fecha"].dt.year
            df["mes"] = df["fecha"].dt.month
            df["mes_nombre"] = df["fecha"].dt.strftime("%B")
            df["dia_semana"] = df["fecha"].dt.day_name()
        except:
            pass

    return df

@st.cache_data
def load_data_from_api(base_url: str):
    endpoint = f"{normalize_api_url(base_url)}/api/v1/operaciones"
    result = fetch_api_json(endpoint)

    if isinstance(result, dict) and result.get("error"):
        return None

    df = pd.DataFrame(result)
    if df.empty:
        return None

    if "fecha" in df.columns:
        try:
            df["fecha"] = pd.to_datetime(df["fecha"])
            df["año"] = df["fecha"].dt.year
            df["mes"] = df["fecha"].dt.month
            df["mes_nombre"] = df["fecha"].dt.strftime("%B")
            df["dia_semana"] = df["fecha"].dt.day_name()
        except:
            pass

    if "aeropuerto" not in df.columns:
        aeropuertos = [c for c in df.columns if c.startswith("aeropuerto_oaci_")]
        if aeropuertos:
            df["aeropuerto"] = (
                df[aeropuertos]
                .idxmax(axis=1)
                .str.replace("aeropuerto_oaci_", "")
            )

    return df

# ============================================
# ESTILOS CSS PERSONALIZADOS
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .sub-title {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    .nav-card {
        background: white;
        border-radius: 15px;
        padding: 30px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        border: 2px solid transparent;
    }
    .nav-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    .nav-card .icon {
        font-size: 4rem;
        margin-bottom: 15px;
    }
    .nav-card .title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .nav-card .description {
        color: #7f8c8d;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .nav-card .badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 10px;
    }
    .metric-inicio {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-inicio .value {
        font-size: 2.2rem;
        font-weight: bold;
    }
    .metric-inicio .label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 2px solid #e8e8e8;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    .sidebar-info {
        padding: 15px;
        background: #7f8c8d;
        border-radius: 10px;
        margin: 10px 0;
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
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INICIALIZAR SESSION STATE
# ============================================
if 'vista_actual' not in st.session_state:
    st.session_state.vista_actual = "inicio"

# ============================================
# CARGA DE DATOS (CACHÉ)
# ============================================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mipaillafil/Proyecto_Aeropuertos_Cortes_Marchesse_Paillafil/main/data/operaciones_aeropuertos_clean.csv"
    df = pd.read_csv(url)
    
    # Identificar columnas de aeropuertos
    aeropuertos = [c for c in df.columns if c.startswith("aeropuerto_oaci_")]
    
    # Crear columna de aeropuerto
    df["aeropuerto"] = (
        df[aeropuertos]
        .idxmax(axis=1)
        .str.replace("aeropuerto_oaci_", "")
    )
    
    # Intentar convertir fecha si existe
    if "fecha" in df.columns:
        try:
            df["fecha"] = pd.to_datetime(df["fecha"])
            df["año"] = df["fecha"].dt.year
            df["mes"] = df["fecha"].dt.month
            df["mes_nombre"] = df["fecha"].dt.strftime("%B")
            df["dia_semana"] = df["fecha"].dt.day_name()
        except:
            pass
    
    return df

@st.cache_data
def load_data_source(base_url: str):
    df_api = load_data_from_api(base_url)
    if df_api is not None:
        return df_api, "API"
    
    return load_data(), "CSV"


df, data_source = load_data_source(API_DEFAULT_URL)

# ============================================
# SIDEBAR - CONTROLES PARA TODOS LOS DASHBOARDS
# ============================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092065.png", width=80)
    st.markdown("### ✈️ Sistema SIMA")
    st.markdown("---")
    
    # Información del sistema
    st.markdown("**📊 Estado del Sistema**")
    st.markdown(f"""
    <div class="sidebar-info">
        ✅ Sistema Operativo<br>
        📊 {len(df):,} registros<br>
        🏢 {df['aeropuerto'].nunique()} aeropuertos<br>
        🛠️ Fuente: {data_source}
        <br>
        🕐 {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Selector de vista rápida
    st.markdown("**🔍 Acceso Rápido**")
    
    vista_options = ["🏠 Inicio", "📊 Ejecutivo", "⚙️ Operativo", "🤖 Técnico"]
    vista_map = {
        "🏠 Inicio": "inicio",
        "📊 Ejecutivo": "ejecutivo",
        "⚙️ Operativo": "operativo",
        "🤖 Técnico": "tecnico"
    }
    
    current_label = next((k for k, v in vista_map.items() if v == st.session_state.vista_actual), "🏠 Inicio")
    current_index = vista_options.index(current_label)
    
    vista_seleccionada = st.radio(
        "Ir a:",
        options=vista_options,
        index=current_index
    )
    
    st.session_state.vista_actual = vista_map[vista_seleccionada]
    
    st.markdown("---")
    
    # ============================================
    # FILTROS GLOBALES (CORREGIDOS)
    # ============================================
    st.markdown("**🎯 Filtros Globales**")
    
    # Filtro de Aeropuerto
    aeropuerto_options = ["Todos"] + sorted(df["aeropuerto"].unique())
    aeropuerto_seleccionado = st.selectbox(
        "📍 Aeropuerto",
        options=aeropuerto_options,
        index=0
    )
    
    # Filtro de Rango de Operaciones - CORREGIDO
    min_ops = float(df["cnt_operaciones"].min())
    max_ops = float(df["cnt_operaciones"].max())
    
    # Si min y max son iguales, ajustar
    if min_ops == max_ops:
        min_ops = max(0, min_ops - 1)
        max_ops = max_ops + 1
    
    rango_operaciones = st.slider(
        "📊 Rango de Operaciones",
        min_value=min_ops,
        max_value=max_ops,
        value=(min_ops, max_ops),
        step=0.1,
        format="%.1f"
    )
    
    st.markdown("---")
    
    # Botón de descarga
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode("utf-8")
    
    csv = convert_df_to_csv(df)
    st.download_button(
        label="📥 Descargar Datos (CSV)",
        data=csv,
        file_name=f"datos_sima_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    st.caption("v2.0 | SIMA System")

# ============================================
# APLICAR FILTROS GLOBALES
# ============================================
df_filtrado = df.copy()

# Filtro de aeropuerto
if aeropuerto_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["aeropuerto"] == aeropuerto_seleccionado]

# Filtro de rango de operaciones
df_filtrado = df_filtrado[
    (df_filtrado["cnt_operaciones"] >= rango_operaciones[0]) & 
    (df_filtrado["cnt_operaciones"] <= rango_operaciones[1])
]

# ============================================
# CONTENIDO PRINCIPAL - NAVEGACIÓN
# ============================================

# ============================================
# VISTA DE INICIO
# ============================================
if st.session_state.vista_actual == "inicio":
    st.markdown('<div class="main-title">✈️ Sistema Inteligente de Monitoreo Aeroportuario</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">SIMA - Plataforma integral para análisis y monitoreo de operaciones aeroportuarias</div>', unsafe_allow_html=True)
    
    # Métricas rápidas con datos filtrados
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-inicio">
            <div class="value">{len(df_filtrado):,}</div>
            <div class="label">📋 Registros Totales</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-inicio">
            <div class="value">{df_filtrado['aeropuerto'].nunique()}</div>
            <div class="label">✈️ Aeropuertos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-inicio">
            <div class="value">{df_filtrado['cnt_operaciones'].mean():,.1f}</div>
            <div class="label">📊 Promedio Operaciones</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-inicio">
            <div class="value">{df_filtrado['cnt_operaciones'].max():,.0f}</div>
            <div class="label">📈 Máximo Operaciones</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tarjetas de navegación
    st.markdown("### 🎯 Seleccione un Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="nav-card" style="border-color: #667eea;">
            <div class="icon">📊</div>
            <div class="title">Dashboard Ejecutivo</div>
            <div class="description">
                Visión estratégica de todos los aeropuertos. 
                Rankings, métricas globales y comparativas.
            </div>
            <span class="badge">Recomendado</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Ver Ejecutivo", key="btn_ejecutivo", use_container_width=True):
            st.session_state.vista_actual = "ejecutivo"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="nav-card" style="border-color: #f093fb;">
            <div class="icon">⚙️</div>
            <div class="title">Dashboard Operativo</div>
            <div class="description">
                Análisis detallado por aeropuerto. 
                Evolución temporal y datos específicos.
            </div>
            <span class="badge">Detallado</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙️ Ver Operativo", key="btn_operativo", use_container_width=True):
            st.session_state.vista_actual = "operativo"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="nav-card" style="border-color: #4facfe;">
            <div class="icon">🤖</div>
            <div class="title">Dashboard Técnico</div>
            <div class="description">
                Análisis avanzado con Machine Learning. 
                Clustering, PCA y métricas técnicas.
            </div>
            <span class="badge">Avanzado</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🤖 Ver Técnico", key="btn_tecnico", use_container_width=True):
            st.session_state.vista_actual = "tecnico"
            st.rerun()
    
    # Información adicional
    st.markdown("---")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("""
        **📌 ¿Qué puede hacer con SIMA?**
        
        - Monitorear operaciones en tiempo real
        - Identificar aeropuertos con mayor actividad
        - Analizar patrones y tendencias
        - Detectar anomalías con Machine Learning
        - Tomar decisiones basadas en datos
        """)
    with col_info2:
        st.success("""
        **✅ Beneficios**
        
        - Visión 360° de operaciones
        - Análisis predictivo
        - Interfaz intuitiva
        - Datos actualizados
        - Reportes automáticos
        """)

# ============================================
# DASHBOARD EJECUTIVO (CORREGIDO)
# ============================================
elif st.session_state.vista_actual == "ejecutivo":
    st.markdown('<div class="main-title">📊 Dashboard Ejecutivo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Visión estratégica de todos los aeropuertos</div>', unsafe_allow_html=True)
    
    # Mostrar filtros activos
    filtros_texto = []
    if aeropuerto_seleccionado != "Todos":
        filtros_texto.append(f"🏷️ {aeropuerto_seleccionado}")
    filtros_texto.append(f"📊 {rango_operaciones[0]:.1f} - {rango_operaciones[1]:.1f} ops")
    st.caption(f"🔍 **Filtros activos:** {' | '.join(filtros_texto)}")
    
    st.markdown("---")
    
    # Métricas CORREGIDAS
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">📋 Total Registros</div>
            <div class="value">{len(df_filtrado):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">📊 Promedio</div>
            <div class="value">{df_filtrado['cnt_operaciones'].mean():,.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">⬆️ Máximo</div>
            <div class="value">{df_filtrado['cnt_operaciones'].max():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">⬇️ Mínimo</div>
            <div class="value">{df_filtrado['cnt_operaciones'].min():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🏢 Aeropuertos</div>
            <div class="value">{df_filtrado['aeropuerto'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top 10 aeropuertos
    top = df_filtrado["aeropuerto"].value_counts().head(10).reset_index()
    top.columns = ["Aeropuerto", "Operaciones"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(top) > 0:
            fig = px.bar(
                top,
                x="Operaciones",
                y="Aeropuerto",
                orientation="h",
                color="Operaciones",
                color_continuous_scale="Viridis",
                text="Operaciones",
                title="🏆 Top 10 Aeropuertos"
            )
            fig.update_layout(height=400, showlegend=False)
            fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos para mostrar")
    
    with col2:
        fig2 = px.histogram(
            df_filtrado,
            x="cnt_operaciones",
            nbins=30,
            title="📊 Distribución de Operaciones",
            color_discrete_sequence=["#667eea"],
            marginal="box"
        )
        fig2.update_layout(height=400)
        if len(df_filtrado) > 0:
            fig2.add_vline(
                x=df_filtrado["cnt_operaciones"].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Media: {df_filtrado['cnt_operaciones'].mean():,.1f}"
            )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabla resumen
    if len(df_filtrado) > 0:
        st.subheader("📋 Resumen por Aeropuerto")
        resumen = df_filtrado.groupby("aeropuerto").agg({
            "cnt_operaciones": ["count", "mean", "sum", "std", "min", "max"]
        }).round(2)
        resumen.columns = ["Registros", "Promedio", "Total", "Desviación", "Mínimo", "Máximo"]
        resumen = resumen.sort_values("Total", ascending=False)
        
        st.dataframe(
            resumen,
            use_container_width=True,
            height=300,
            column_config={
                "Registros": st.column_config.NumberColumn("📝 Registros", format="%d"),
                "Promedio": st.column_config.NumberColumn("📊 Promedio", format="%.1f"),
                "Total": st.column_config.NumberColumn("📈 Total", format="%d"),
                "Desviación": st.column_config.NumberColumn("📉 Desviación", format="%.2f"),
                "Mínimo": st.column_config.NumberColumn("⬇️ Mínimo", format="%.1f"),
                "Máximo": st.column_config.NumberColumn("⬆️ Máximo", format="%.1f")
            }
        )
    
    if st.button("🏠 Volver al Inicio", key="volver_ejecutivo", use_container_width=True):
        st.session_state.vista_actual = "inicio"
        st.rerun()

# ============================================
# DASHBOARD OPERATIVO (CORREGIDO)
# ============================================
elif st.session_state.vista_actual == "operativo":
    st.markdown('<div class="main-title">⚙️ Dashboard Operativo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Análisis detallado por aeropuerto</div>', unsafe_allow_html=True)
    
    # Selector de aeropuerto (usando datos filtrados)
    aeropuertos_disponibles = sorted(df_filtrado["aeropuerto"].unique())
    if len(aeropuertos_disponibles) == 0:
        st.warning("⚠️ No hay datos con los filtros seleccionados")
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.session_state.vista_actual = "inicio"
            st.rerun()
        st.stop()
    
    aeropuerto = st.selectbox(
        "📍 Seleccionar Aeropuerto",
        options=aeropuertos_disponibles
    )
    
    filtrado = df_filtrado[df_filtrado["aeropuerto"] == aeropuerto]
    
    # Métricas
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("📋 Registros", len(filtrado))
    with col_m2:
        st.metric("📊 Promedio", f"{filtrado['cnt_operaciones'].mean():,.1f}")
    with col_m3:
        st.metric("⬆️ Máximo", f"{filtrado['cnt_operaciones'].max():,.0f}")
    with col_m4:
        st.metric("⬇️ Mínimo", f"{filtrado['cnt_operaciones'].min():,.0f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📊 Distribución - {aeropuerto}")
        fig = px.histogram(
            filtrado,
            x="cnt_operaciones",
            nbins=20,
            title="",
            color_discrete_sequence=["#f5576c"],
            marginal="box"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if "fecha" in filtrado.columns and pd.api.types.is_datetime64_any_dtype(filtrado["fecha"]):
            st.subheader("📈 Evolución Temporal")
            temporal = filtrado.groupby("fecha")["cnt_operaciones"].sum().reset_index()
            fig2 = px.line(
                temporal,
                x="fecha",
                y="cnt_operaciones",
                title="",
                color_discrete_sequence=["#f5576c"]
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("ℹ️ No hay datos temporales disponibles")
    
    st.subheader("📋 Datos Recientes")
    columnas_mostrar = ["aeropuerto", "cnt_operaciones"]
    if "fecha" in filtrado.columns:
        columnas_mostrar.insert(1, "fecha")
    st.dataframe(
        filtrado[columnas_mostrar].head(50),
        use_container_width=True,
        height=300
    )
    
    if st.button("🏠 Volver al Inicio", key="volver_operativo", use_container_width=True):
        st.session_state.vista_actual = "inicio"
        st.rerun()

# ============================================
# DASHBOARD TÉCNICO (CORREGIDO)
# ============================================
elif st.session_state.vista_actual == "tecnico":
    st.markdown('<div class="main-title">🤖 Dashboard Técnico</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Análisis avanzado con Machine Learning</div>', unsafe_allow_html=True)
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ No hay datos con los filtros seleccionados")
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            st.session_state.vista_actual = "inicio"
            st.rerun()
        st.stop()
    
    numeric_cols = df_filtrado.select_dtypes(include=[np.number]).columns.tolist()
    exclude_cols = ["aeropuerto"]
    numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    st.subheader("⚙️ Configuración del Modelo")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        selected_cols = st.multiselect(
            "Variables para análisis",
            options=numeric_cols,
            default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
        )
    
    with col_config2:
        n_clusters = st.slider(
            "Número de Clusters",
            min_value=2,
            max_value=6,
            value=3
        )
    
    if selected_cols:
        st.markdown("---")
        
        X = df_filtrado[selected_cols].fillna(df_filtrado[selected_cols].mean())
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        with st.spinner("🔄 Entrenando modelo..."):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
        
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(X_scaled)
        pca_df = pd.DataFrame(pca_result, columns=["PCA1", "PCA2"])
        pca_df["Cluster"] = clusters.astype(str)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                pca_df,
                x="PCA1",
                y="PCA2",
                color="Cluster",
                title=f"Clusters K-Means (k={n_clusters})",
                color_discrete_sequence=px.colors.qualitative.Set1,
                opacity=0.7
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                x=[f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
                y=pca.explained_variance_ratio_,
                title="Varianza Explicada",
                labels={"x": "Componente", "y": "Varianza"},
                color_discrete_sequence=["#4facfe"]
            )
            fig2.update_layout(height=450)
            fig2.add_hline(y=0.1, line_dash="dash", line_color="red", annotation_text="Umbral 10%")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("📈 Distribución de Clusters")
        cluster_counts = pd.Series(clusters).value_counts().sort_index()
        fig3 = px.pie(
            values=cluster_counts.values,
            names=[f"Cluster {i}" for i in cluster_counts.index],
            title=f"Distribución de {n_clusters} Clusters",
            color_discrete_sequence=px.colors.qualitative.Set1,
            hole=0.3
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ Selecciona al menos una variable")
    
    if st.button("🏠 Volver al Inicio", key="volver_tecnico", use_container_width=True):
        st.session_state.vista_actual = "inicio"
        st.rerun()

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <strong>✈️ SIMA - Sistema Inteligente de Monitoreo Aeroportuario</strong> | 
    📊 {len(df_filtrado):,} registros | 
    🏢 {df_filtrado['aeropuerto'].nunique()} aeropuertos |
    🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)