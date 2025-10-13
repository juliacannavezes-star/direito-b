import streamlit as st
import pandas as pd
import plotly.express as px

# Título do app
st.title("Visualização de Países no Mapa 🌍")

# Carregamento do dataset
url = "https://www.irdx.com.br/media/uploads/paises.csv"
dataset = pd.read_csv(url)

# Exibição da tabela de dados
st.subheader("📄 Dados dos países")
st.dataframe(dataset)

# Gráfico de dispersão geográfica (Scatter Geo)
st.subheader("🗺️ Coordenadas dos países no mapa (Scatter Geo)")

fig1 = px.scatter_geo(
    dataset,
    lat=dataset.latitude,
    lon=dataset.longitude,
    hover_name=dataset.nome
)
fig1.update_layout(
    showlegend=False,
    title="Coordenadas dos países no mapa",
    geo_scope='world'
)
st.plotly_chart(fig1)

# Gráfico coroplético (Choropleth Map)
st.subheader("🌐 Mapa Coroplético dos países")

fig2 = px.choropleth(
    dataset,
    locations=dataset['iso3'],
    color=dataset['nome'],
    hover_name=dataset['nome']
)
fig2.update_layout(
    title="Mapa Coroplético dos países!",
    geo_scope='world'
)
st.plotly_chart(fig2)
