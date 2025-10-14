import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Deputados 2022", layout="wide")

# --- TÍTULO ---
st.title("📊 Análise Interativa dos Deputados Federais 2022")

# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def carregar_dados():
    df = pd.read_csv("media/uploads/deputados_2022.csv", sep=",", encoding="utf-8")
    return df

df = carregar_dados()

st.subheader("Visualização inicial dos dados")
st.dataframe(df.head())

# --- FILTROS INTERATIVOS ---
st.sidebar.header("🔍 Filtros")

partidos = st.sidebar.multiselect(
    "Selecione o(s) Partido(s):", 
    options=sorted(df["partido"].dropna().unique()),
    default=[]
)

estados = st.sidebar.multiselect(
    "Selecione o(s) Estado(s):",
    options=sorted(df["estado"].dropna().unique()),
    default=[]
)

# --- APLICAÇÃO DOS FILTROS ---
df_filtrado = df.copy()

if partidos:
    df_filtrado = df_filtrado[df_filtrado["partido"].isin(partidos)]

if estados:
    df_filtrado = df_filtrado[df_filtrado["estado"].isin(estados)]

st.write(f"Mostrando **{len(df_filtrado)}** deputados após filtragem.")
st.dataframe(df_filtrado)

# --- GRÁFICOS ---
st.subheader("📈 Gráficos Interativos")

col1, col2 = st.columns(2)

with col1:
    st.write("### Distribuição por Partido")
    fig1, ax1 = plt.subplots()
    df_filtrado["partido"].value_counts().plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Partido")
    ax1.set_ylabel("Número de Deputados")
    st.pyplot(fig1)

with col2:
    st.write("### Distribuição por Estado")
    fig2, ax2 = plt.subplots()
    df_filtrado["estado"].value_counts().plot(kind="bar", ax=ax2, color="orange")
    ax2.set_xlabel("Estado")
    ax2.set_ylabel("Número de Deputados")
    st.pyplot(fig2)

# --- INFORMAÇÕES ADICIONAIS ---
st.markdown("---")
st.caption("Desenvolvido com ❤️ usando Streamlit e Pandas.")
