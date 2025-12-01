import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# PALETA DE COLORES
# =========================
COLORS = {
    "bg": "#d7d9de",
    "card": "#F3F4F6",
    "title": "#0D33A6",
    "text": "#000000",
    "button": "#0F71F2",
    "accent": "#0597F2",
    "border": "#8082A6",
    "filter": "#E5F0FF",
    "chart_card": "#E3E5EB"
}

LABEL_COLORS = {
    "Fake": "#0D33A6",
    "Real": "#0597F2"
}

# =========================
# CONFIG STREAMLIT + CSS
# =========================
st.set_page_config(page_title="Fake vs Real News Dashboard", page_icon="📡", layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {COLORS["bg"]} !important;
        color: {COLORS["text"]} !important;
    }}

    main.block-container {{
        background-color: {COLORS["bg"]} !important;
        padding-top: 1rem;
    }}

    h1, h2, h3, h4 {{
        color: {COLORS["title"]} !important;
    }}

    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {{
        color: {COLORS["text"]} !important;
    }}

    [data-testid="stMetric"] {{
        background-color: {COLORS["card"]};
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid {COLORS["border"]};
        box-shadow: 0 2px 6px rgba(15, 17, 32, 0.08);
    }}

    .chart-card {{
        background-color: {COLORS["chart_card"]};
        border-radius: 14px;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 6px rgba(15, 17, 32, 0.10);
        border: 1px solid #C1C5CF;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# CARGA DE DATOS (CORREGIDO)
# =========================
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1L5s_WqmSVn8CrASlL9mZ18bZ7rEIFP1Q"

    # Autodetección del separador (soluciona el KeyError)
    df = pd.read_csv(url, sep=None, engine="python")

    # Convertir fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

df = load_data()

# Validación de columna label
if "label" not in df.columns:
    st.error(f"❌ ERROR: No se encontró la columna 'label'. Columnas disponibles: {list(df.columns)}")
    st.stop()

df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype(int)
df["label_name"] = df["label"].map({0: "Fake", 1: "Real"})

# =========================
# FUNCIÓN DE LAYOUT
# =========================
def apply_layout(fig, title=None):
    if title:
        fig.update_layout(title=dict(
            text=title,
            font=dict(color="#0D33A6", size=18, family="Arial")
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLORS["chart_card"],
        font_color="#000000",
        xaxis=dict(
            title_font=dict(color="#000000"),
            tickfont=dict(color="#000000"),
            gridcolor="#CACFD8",
            zerolinecolor="#CACFD8",
            linecolor=COLORS["border"]
        ),
        yaxis=dict(
            title_font=dict(color="#000000"),
            tickfont=dict(color="#000000"),
            gridcolor="#CACFD8",
            zerolinecolor="#CACFD8",
            linecolor=COLORS["border"]
        ),
        legend=dict(
            font=dict(color="#000000"),
            bgcolor=COLORS["chart_card"],
            bordercolor="#CACFD8",
            borderwidth=1
        )
    )
    return fig

# =========================
# ENCABEZADO
# =========================
st.title("📡 Fake vs Real News Dashboard")
st.markdown("Dashboard interactivo para explorar noticias **falsas y reales**.")
st.markdown("---")

# =========================
# KPIS
# =========================
total_news = len(df)
fake_count = (df["label"] == 0).sum()
real_count = (df["label"] == 1).sum()
avg_words = df["text_word_len"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de noticias", f"{total_news:,}")
col2.metric("Noticias Fake", f"{fake_count:,}")
col3.metric("Noticias Reales", f"{real_count:,}")
col4.metric("Longitud media (palabras)", f"{avg_words:.1f}")

st.markdown("---")

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribución por tipo",
    "📈 Evolución temporal",
    "📚 Longitud del texto",
    "🎭 Polaridad del sentimiento",
    "📄 Dataset"
])


# ==========================================================
# TAB 1 — DISTRIBUCIÓN
# ==========================================================
with tab1:
    st.header("📊 Distribución por tipo")

    col1, col2 = st.columns(2)
    labels_sel = col1.multiselect("Tipo de noticia", sorted(df["label_name"].unique()), sorted(df["label_name"].unique()))
    subjects_sel = col2.multiselect("Tema (subject)", sorted(df["subject"].unique()), sorted(df["subject"].unique()))

    df_filt = df[(df["label_name"].isin(labels_sel)) & (df["subject"].isin(subjects_sel))]

    conteo = df_filt.groupby("label_name").size().reset_index(name="count")

    fig = px.bar(conteo, x="label_name", y="count", color="label_name",
                 color_discrete_map=LABEL_COLORS)
    fig = apply_layout(fig, "Distribución de noticias Fake vs Real")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# TAB 2 — EVOLUCIÓN TEMPORAL
# ==========================================================
with tab2:
    st.header("📈 Evolución temporal")

    df_date = df[df["date"].notna()].copy()
    if df_date.empty:
        st.warning("No hay fechas válidas en el dataset.")
    else:
        df_date["year_month"] = df_date["date"].dt.to_period("M").astype(str)

        fig = px.line(
            df_date.groupby(["year_month", "label_name"]).size().reset_index(name="count"),
            x="year_month", y="count", color="label_name",
            color_discrete_map=LABEL_COLORS
        )
        fig = apply_layout(fig, "Noticias por mes")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# TAB 3 — LONGITUD DEL TEXTO
# ==========================================================
with tab3:
    st.header("📚 Longitud del texto")

    fig = px.histogram(df, x="text_word_len", color="label_name",
                       nbins=40, color_discrete_map=LABEL_COLORS)
    fig = apply_layout(fig, "Distribución de longitud del texto")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# TAB 4 — POLARIDAD
# ==========================================================
with tab4:
    st.header("🎭 Polaridad del sentimiento")

    if "polarity" not in df.columns:
        st.error("El dataset no contiene la columna 'polarity'.")
    else:
        fig = px.box(df, x="label_name", y="polarity",
                     color="label_name", color_discrete_map=LABEL_COLORS)
        fig = apply_layout(fig, "Polaridad por tipo de noticia")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# TAB 5 — DATASET
# ==========================================================
with tab5:
    st.header("📄 Vista del dataset")

    cols = ["date", "label_name", "subject", "title", "text_word_len"]
    cols = [c for c in cols if c in df.columns]

    st.dataframe(df[cols].head(200), use_container_width=True)
    st.caption("Mostrando solo 200 registros.")
