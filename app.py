import pandas as pd
import streamlit as st
import plotly.express as px

#PALETA
COLORS = {
    "bg": "#d7d9de",        # Fondo general
    "card": "#F3F4F6",      # Tarjetas ligeras (KPIs)
    "title": "#0D33A6",     # Títulos azul oscuro
    "text": "#000000",      # Texto negro
    "button": "#0F71F2",    # Botón azul vivo
    "accent": "#0597F2",    # Azul medio detalles
    "border": "#8082A6",    # Gris azulado bordes
    "filter": "#E5F0FF",    # Azul claro filtros
    "chart_card": "#E3E5EB" # Tarjeta de gráficas
}

#Colores para Fake / Real en las gráficas
LABEL_COLORS = {
    "Fake": "#0D33A6",   # Azul oscuro
    "Real": "#0597F2"    # Azul medio
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
    /* Fondo general de la app */
    .stApp {{
        background-color: {COLORS["bg"]} !important;
        color: {COLORS["text"]} !important;
    }}

    /* Contenedor principal */
    main.block-container {{
        background-color: {COLORS["bg"]} !important;
        padding-top: 1rem;
    }}

    /* Títulos principales */
    h1, h2, h3, h4 {{
        color: {COLORS["title"]} !important;
    }}

    /* Valores y labels de métricas */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {{
        color: {COLORS["text"]} !important;
    }}

    /* Tarjetas tipo Power BI para KPIs */
    [data-testid="stMetric"] {{
        background-color: {COLORS["card"]};
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid {COLORS["border"]};
        box-shadow: 0 2px 6px rgba(15, 17, 32, 0.08);
    }}
    [data-testid="stMetric"] > div {{
        padding: 0 !important;
    }}

    /* Botones */
    .stButton>button {{
        background-color: {COLORS["button"]} !important;
        color: #FFFFFF !important;
        border-radius: 6px;
        padding: 0.35rem 0.9rem;
        border: 1px solid {COLORS["accent"]};
    }}

    /* Tabs */
    button[role="tab"] {{
        background-color: {COLORS["card"]} !important;
        color: {COLORS["text"]} !important;
        border-bottom: 2px solid {COLORS["border"]};
        border-radius: 0;
    }}

    /* Inputs / selects */
    .stMultiSelect div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {COLORS["filter"]} !important;
        color: {COLORS["text"]} !important;
        border-radius: 6px;
        border: 1px solid {COLORS["accent"]};
        box-shadow: 0 1px 3px rgba(15, 17, 32, 0.06);
    }}

    /* TAGS del multiselect (chips) */
    .stMultiSelect [data-baseweb="tag"] {{
        background-color: {COLORS["button"]} !important;
        color: #FFFFFF !important;
        border-radius: 12px;
    }}
    .stMultiSelect [data-baseweb="tag"] span {{
        color: #FFFFFF !important;
    }}
    .stMultiSelect [data-baseweb="tag"] svg {{
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }}

    /* Slider (rango de años) */
    div[data-baseweb="slider"] > div > div {{
        background-color: {COLORS["accent"]} !important;
    }}
    div[data-baseweb="slider"] [role="slider"] {{
        background-color: {COLORS["button"]} !important;
        border: 2px solid {COLORS["button"]} !important;
        box-shadow: 0 0 0 3px rgba(5, 151, 242, 0.3);
    }}

    /* Contenedor de la gráfica sin fondo "extra" */
    .stPlotlyChart, .stPlotlyChart > div, .stPlotlyChart iframe {{
        background-color: transparent !important;
    }}

    /* Tarjeta para las gráficas */
    .chart-card {{
        background-color: {COLORS["chart_card"]};
        border-radius: 14px;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 6px rgba(15, 17, 32, 0.10);
        border: 1px solid #C1C5CF;
    }}

    /* Texto general */
    .stText, label, p, span {{
        color: {COLORS["text"]} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# =========================
# CARGA DE DATOS DESDE GOOGLE DRIVE
# =========================
@st.cache_data
def load_data():
    # Enlace directo a tu CSV en Google Drive
    url = "https://drive.google.com/uc?id=1L5s_WqmSVn8CrASlL9mZ18bZ7rEIFP1Q"
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

df = load_data()
df["label_name"] = df["label"].map({0: "Fake", 1: "Real"})

# LAYOUT
def apply_layout(fig, title=None):
    """
    Aplica un estilo consistente a todas las gráficas.
    """
    # Título azul visible
    if title is not None:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    color="#0D33A6",  # Azul fuerte
                    size=18,
                    family="Arial"
                )
            )
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",      # Transparente
        plot_bgcolor=COLORS["chart_card"],  # Gris suave armonizado
        font_color="#000000",               # Texto general NEGRO
        xaxis=dict(
            title_font=dict(color="#000000"),  # Eje X negro
            tickfont=dict(color="#000000"),
            gridcolor="#CACFD8",
            zerolinecolor="#CACFD8",
            linecolor=COLORS["border"]
        ),
        yaxis=dict(
            title_font=dict(color="#000000"),  # Eje Y negro
            tickfont=dict(color="#000000"),
            gridcolor="#CACFD8",
            zerolinecolor="#CACFD8",
            linecolor=COLORS["border"]
        ),
        legend=dict(
            font=dict(color="#000000"),        # Leyenda en negro
            bgcolor=COLORS["chart_card"],
            bordercolor="#CACFD8",
            borderwidth=1
        )
    )
    return fig

#ENCABEZADO
st.title("📡 Fake vs Real News Dashboard")
st.markdown(
    """
Dashboard interactivo para explorar noticias **falsas y reales**.
"""
)
st.markdown("---")

#KPIS
total_news = len(df)
fake_count = int((df["label"] == 0).sum())
real_count = int((df["label"] == 1).sum())
avg_words = df["text_word_len"].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de noticias", f"{total_news:,}")
with col2:
    st.metric("Noticias Fake", f"{fake_count:,}")
with col3:
    st.metric("Noticias Reales", f"{real_count:,}")
with col4:
    st.metric("Longitud media (palabras)", f"{avg_words:.1f}")

st.markdown("---")

#TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribución por tipo",
    "📈 Evolución temporal",
    "📚 Longitud del texto",
    "🎭 Polaridad del sentimiento",
    "📄 Dataset"
])

#DISTRIBUCION POR TIPO(TAP1)
with tab1:
    st.header("📊 Distribución por tipo")

    col1, col2 = st.columns(2)

    with col1:
        labels_sel = st.multiselect(
            "Tipo de noticia",
            options=sorted(df["label_name"].dropna().unique()),
            default=sorted(df["label_name"].dropna().unique()),
            key="tab1_labels"
        )

    with col2:
        subjects_sel = st.multiselect(
            "Tema (subject)",
            options=sorted(df["subject"].dropna().unique()),
            default=sorted(df["subject"].dropna().unique()),
            key="tab1_subjects"
        )

    df_filt = df[
        (df["label_name"].isin(labels_sel)) &
        (df["subject"].isin(subjects_sel))
    ]

    conteo = df_filt.groupby("label_name").size().reset_index(name="count")

    fig_bar = px.bar(
        conteo,
        x="label_name",
        y="count",
        labels={"label_name": "Tipo de noticia", "count": "Número de noticias"},
        color="label_name",
        color_discrete_map=LABEL_COLORS
    )
    fig_bar = apply_layout(fig_bar, "Distribución de noticias Fake vs Real")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(f"Total de noticias filtradas: {len(df_filt):,}")

#EVOLUCION TEMPORAL (TAB2)
with tab2:
    st.header("📈 Evolución temporal (solo con fecha)")

    df_with_date = df[df["date"].notna()].copy()

    col1, col2 = st.columns(2)

    with col1:
        subjects_time = st.multiselect(
            "Tema (subject)",
            options=sorted(df_with_date["subject"].dropna().unique()),
            default=sorted(df_with_date["subject"].dropna().unique()),
            key="tab2_subjects"
        )

    with col2:
        min_year = int(df_with_date["date"].dt.year.min())
        max_year = int(df_with_date["date"].dt.year.max())
        year_range = st.slider(
            "Rango de años",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
            key="tab2_year_range"
        )

    df_time = df_with_date[
        (df_with_date["subject"].isin(subjects_time)) &
        (df_with_date["date"].dt.year.between(year_range[0], year_range[1]))
    ]

    if df_time.empty:
        st.warning("⚠ No hay noticias con fecha para los filtros seleccionados.")
    else:
        df_time["year_month"] = df_time["date"].dt.to_period("M").astype(str)

        serie = (
            df_time.groupby(["year_month", "label_name"])
            .size()
            .reset_index(name="count")
            .sort_values("year_month")
        )

        fig_time = px.line(
            serie,
            x="year_month",
            y="count",
            color="label_name",
            labels={"year_month": "Año-Mes", "count": "Cantidad"},
            color_discrete_map=LABEL_COLORS
        )
        fig_time = apply_layout(fig_time, "Noticias por mes")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.caption(f"Total de noticias con fecha: {len(df_time):,}")

#LONGITUD DE TEXTO (TAB3)
with tab3:
    st.header("📚 Longitud del texto")

    col1, col2 = st.columns(2)

    with col1:
        labels_len = st.multiselect(
            "Tipo de noticia",
            options=sorted(df["label_name"].dropna().unique()),
            default=sorted(df["label_name"].dropna().unique()),
            key="tab3_labels"
        )

    with col2:
        subjects_len = st.multiselect(
            "Tema (subject)",
            options=sorted(df["subject"].dropna().unique()),
            default=sorted(df["subject"].dropna().unique()),
            key="tab3_subjects"
        )

    min_words = int(df["text_word_len"].min())
    max_words = int(df["text_word_len"].max())

    word_range = st.slider(
        "Rango de palabras",
        min_value=min_words,
        max_value=max_words,
        value=(min_words, max_words),
        key="tab3_word_range"
    )

    df_len = df[
        (df["label_name"].isin(labels_len)) &
        (df["subject"].isin(subjects_len)) &
        (df["text_word_len"].between(word_range[0], word_range[1]))
    ]

    fig_len = px.histogram(
        df_len,
        x="text_word_len",
        color="label_name",
        nbins=40,
        labels={"text_word_len": "Palabras"},
        color_discrete_map=LABEL_COLORS
    )
    fig_len = apply_layout(fig_len, "Distribución de longitud del texto")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_len, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(f"Total de noticias filtradas: {len(df_len):,}")

#PLARIDAD DE SENTIMIENTO (TAB4)
with tab4:
    st.header("🎭 Polaridad del sentimiento")

    if "polarity" not in df.columns:
        st.error("La columna 'polarity' no existe. Asegúrate de calcular el sentimiento.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            labels_pol = st.multiselect(
                "Tipo de noticia",
                options=sorted(df["label_name"].dropna().unique()),
                default=sorted(df["label_name"].dropna().unique()),
                key="tab4_labels"
            )

        with col2:
            subjects_pol = st.multiselect(
                "Tema (subject)",
                options=sorted(df["subject"].dropna().unique()),
                default=sorted(df["subject"].dropna().unique()),
                key="tab4_subjects"
            )

        df_pol = df[
            (df["label_name"].isin(labels_pol)) &
            (df["subject"].isin(subjects_pol))
        ]

        fig_pol = px.box(
            df_pol,
            x="label_name",
            y="polarity",
            labels={"label_name": "Tipo", "polarity": "Polaridad"},
            color="label_name",
            color_discrete_map=LABEL_COLORS
        )
        fig_pol = apply_layout(fig_pol, "Polaridad del sentimiento por tipo de noticia")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_pol, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.caption(f"Total de noticias filtradas: {len(df_pol):,}")

#DATASET (TAB5)
with tab5:
    st.header("📄 Vista del dataset")

    st.dataframe(
        df[["date", "label_name", "subject", "title", "text_word_len"]].head(200),
        use_container_width=True,
    )

    st.caption("Mostrando solo las primeras 200 noticias.")
