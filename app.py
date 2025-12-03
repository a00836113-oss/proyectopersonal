import pandas as pd
import streamlit as st
import plotly.express as px

#PALETA DE COLORES 
COLORS = {
    # Fondo general claro
    "bg_from": "#E5E7EB",
    "bg_to": "#F9FAFB",

    # Panel principal oscuro
    "panel": "#0B1220",

    # Tarjetas
    "card": "#111827",

    # Tipografía
    "title": "#F9FAFB",
    "subtitle": "#D1D5DB",
    "text": "#E5E7EB",

    # Acentos azules
    "accent": "#2563EB",       # Azul principal
    "accent_soft": "#38BDF8",  # Azul claro

    # Bordes / filtros
    "border": "#1F2937",
    "filter": "#020617",

    # Fondo de gráficas
    "chart_card": "#020617"
}

#Colores de las etiquetas
LABEL_COLORS = {
    "Fake": "#2563EB",   # Azul medio
    "Real": "#38BDF8"    # Azul claro
}


#CONFIG STREAMLIT + CSS
st.set_page_config(
    page_title="Fake vs Real News Dashboard",
    page_icon="📡",
    layout="wide"
)

st.markdown(
    f"""
    <style>
    /* ======== FONDO GENERAL ======== */
    .stApp {{
        background: linear-gradient(180deg, {COLORS["bg_from"]} 0%, {COLORS["bg_to"]} 35%, #FFFFFF 100%) !important;
        color: {COLORS["text"]} !important;
    }}

    main.block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}

    /* ======== TIPOGRAFÍA ======== */
    h1, h2, h3, h4 {{
        color: {COLORS["title"]} !important;
        font-family: "Segoe UI", system-ui, sans-serif;
    }}

    p, span, li, label, .markdown-text-container {{
        color: {COLORS["subtitle"]} !important;
        font-family: "Segoe UI", system-ui, sans-serif;
    }}

    /* ======== HERO / ENCABEZADO (PANEL AZUL) ======== */
    .hero-card {{
        background: linear-gradient(135deg, #0F172A 0%, #0B1120 40%, #1D4ED8 100%);
        border-radius: 24px;
        padding: 1.8rem 2rem;
        border: 1px solid rgba(55, 65, 81, 0.7);
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.55);
        display: flex;
        justify-content: space-between;
        gap: 2rem;
        margin-bottom: 1.5rem;
    }}

    .hero-left {{
        max-width: 70%;
    }}

    .hero-title {{
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: {COLORS["title"]};
    }}

    .hero-subtitle {{
        font-size: 0.95rem;
        color: {COLORS["subtitle"]};
    }}

    .hero-badges {{
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        align-items: flex-end;
        justify-content: center;
    }}

    .hero-badge {{
        padding: 0.35rem 0.75rem;
        font-size: 0.75rem;
        border-radius: 999px;
        border: 1px solid rgba(156, 163, 175, 0.9);
        background: rgba(15, 23, 42, 0.9);
        color: {COLORS["text"]};
    }}

    /* ======== METRIC CARDS (KPIs) ======== */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {{
        color: {COLORS["text"]} !important;
    }}

    [data-testid="stMetric"] {{
        background: {COLORS["card"]};
        padding: 0.9rem 1.1rem;
        border-radius: 1rem;
        border: 1px solid rgba(55, 65, 81, 0.9);
        box-shadow: 0 14px 25px rgba(15, 23, 42, 0.55);
    }}

    /* ======== SELECTS / INPUTS ======== */
    .stSelectbox, .stMultiSelect, .stDateInput {{
        background-color: transparent !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: #020617 !important;
        border-radius: 999px !important;
        border: 1px solid #1F2937 !important;
        color: {COLORS["text"]} !important;
    }}

    /* ======== TABS (ESTILO GA: PÍLDORAS AZULES) ======== */
    div[data-baseweb="tab-list"] {{
        gap: 0.35rem;
    }}

    button[role="tab"] {{
        background-color: #111827 !important;
        border-radius: 999px !important;
        border: 1px solid #1F2937 !important;
        padding: 0.4rem 0.9rem !important;
        color: {COLORS["subtitle"]} !important;
        font-size: 0.85rem;
    }}

    button[role="tab"][aria-selected="true"] {{
        background: linear-gradient(90deg, #1D4ED8, #2563EB) !important;
        color: #F9FAFB !important;
        border: none !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#CARGA DE DATOS
@st.cache_data
def load_data():
    url = (
        "https://drive.usercontent.google.com/download"
        "?id=1L5s_WqmSVn8CrASlL9mZ18bZ7rEIFP1Q"
        "&export=download&confirm=t"
    )
    df = pd.read_csv(url)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

df = load_data()

if "label" not in df.columns:
    st.error(f"❌ ERROR: No se encontró la columna 'label'. Columnas disponibles: {list(df.columns)}")
    st.stop()

df["label"] = pd.to_numeric(df["label"], errors="coerce").fillna(0).astype(int)
df["label_name"] = df["label"].map({0: "Fake", 1: "Real"})

#FUNCIÓN DE LAYOUT PARA GRÁFICAS
def apply_layout(fig, title=None):
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color="#FFFFFF", size=20, family="Segoe UI"),
                x=0.02,
                xanchor="left"
            )
        )

    fig.update_layout(
        paper_bgcolor="#0B1120",   
        plot_bgcolor="#0B1120",
        font_color="#FFFFFF",

        margin=dict(l=60, r=40, t=60, b=60),
        autosize=True,

        xaxis=dict(
            title_font=dict(color="#FFFFFF", size=16),
            tickfont=dict(color="#FFFFFF", size=14),
            automargin=True,
            gridcolor="#334155",
            zerolinecolor="#334155",
            linecolor="#64748B",
        ),
        yaxis=dict(
            title_font=dict(color="#FFFFFF", size=16),
            tickfont=dict(color="#FFFFFF", size=14),
            automargin=True,
            gridcolor="#334155",
            zerolinecolor="#334155",
            linecolor="#64748B",
        ),
        legend=dict(
            font=dict(color="#F8FAFC", size=13),
            bgcolor="rgba(15,23,42,0.7)",
            bordercolor="#475569",
            borderwidth=1,
        ),
    )

    return fig

#ENCABEZADO
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-left">
            <div class="hero-title">
                Dashboards para Fake vs Real News
            </div>
            <div class="hero-subtitle">
                Explora la distribución, evolución temporal y características de las noticias 
                etiquetadas como <strong>Fake</strong> y <strong>Real</strong>, 
                para mejorar el entendimiento y monitoreo de la información.
            </div>
        </div>
        <div class="hero-badges">
            <div class="hero-badge">Classification Analytics</div>
            <div class="hero-badge">NLP · Sentiment</div>
            <div class="hero-badge">Streamlit · Plotly</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

#KPIs PRINCIPALES
total_news = len(df)
fake_count = (df["label"] == 0).sum()
real_count = (df["label"] == 1).sum()
avg_words = df["text_word_len"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de noticias", f"{total_news:,}")
kpi2.metric("Noticias Fake", f"{fake_count:,}")
kpi3.metric("Noticias Reales", f"{real_count:,}")
kpi4.metric("Longitud media (palabras)", f"{avg_words:.1f}")

st.write("") 

#TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribución por tipo",
    "📈 Evolución temporal",
    "📚 Longitud del texto",
    "🎭 Polaridad del sentimiento",
    "📄 Dataset"
])

#DISTRIBUCIÓN(TAB 1)
with tab1:
    st.subheader("Distribución por tipo de noticia")

    col1, col2 = st.columns(2)
    labels_sel = col1.multiselect(
        "Tipo de noticia",
        sorted(df["label_name"].unique()),
        sorted(df["label_name"].unique())
    )
    subjects_sel = col2.multiselect(
        "Tema (subject)",
        sorted(df["subject"].unique()),
        sorted(df["subject"].unique())
    )

    df_filt = df[
        (df["label_name"].isin(labels_sel)) &
        (df["subject"].isin(subjects_sel))
    ]

    conteo = df_filt.groupby("label_name").size().reset_index(name="count")

    fig = px.bar(
        conteo,
        x="label_name",
        y="count",
        color="label_name",
        color_discrete_map=LABEL_COLORS
    )
    fig = apply_layout(fig, "Distribución de noticias Fake vs Real")

    st.plotly_chart(fig, use_container_width=True)

#EVOLUCIÓN TEMPORAL(TAB 2)

with tab2:
    st.subheader("Evolución temporal de las noticias")

    df_date = df[df["date"].notna()].copy()
    if df_date.empty:
        st.warning("No hay fechas válidas en el dataset.")
    else:
        df_date["year_month"] = df_date["date"].dt.to_period("M").astype(str)

        temporal = (
            df_date.groupby(["year_month", "label_name"])
            .size()
            .reset_index(name="count")
        )

        fig = px.line(
            temporal,
            x="year_month",
            y="count",
            color="label_name",
            color_discrete_map=LABEL_COLORS
        )
        fig = apply_layout(fig, "Noticias por mes")

        st.plotly_chart(fig, use_container_width=True)

#LONGITUD DEL TEXTO(TAB 3)
with tab3:
    st.subheader("Distribución de la longitud del texto")

    fig = px.histogram(
        df,
        x="text_word_len",
        color="label_name",
        nbins=40,
        barmode="overlay",
        opacity=0.8,
        color_discrete_map=LABEL_COLORS
    )
    fig = apply_layout(fig, "Longitud del texto por tipo de noticia")

    st.plotly_chart(fig, use_container_width=True)

#POLARIDAD(TAB 4)
with tab4:
    st.subheader("Polaridad del sentimiento")

    if "polarity" not in df.columns:
        st.error("El dataset no contiene la columna 'polarity'.")
    else:
        fig = px.box(
            df,
            x="label_name",
            y="polarity",
            color="label_name",
            color_discrete_map=LABEL_COLORS
        )
        fig = apply_layout(fig, "Polaridad por tipo de noticia")

        st.plotly_chart(fig, use_container_width=True)

#DATASET(TAB 5)
with tab5:
    st.subheader("Vista del dataset")

    cols = ["date", "label_name", "subject", "title", "text_word_len"]
    cols = [c for c in cols if c in df.columns]

    st.dataframe(df[cols].head(200), use_container_width=True)
    st.caption("Mostrando solo 200 registros.")

