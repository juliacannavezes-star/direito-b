import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Visualização de Países no Mapa")
url = "https://www.irdx.com.br/media/uploads/paises.csv"
dataset = pd.read_csv(url)
st.subheader("📄 Dados dos países")
st.dataframe(dataset)

st.subheader("Coordenadas dos países no mapa")
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

st.subheader("Mapa Coroplético dos países")

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
