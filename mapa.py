import pandas as pd
import streamlit as st
st.title("Visualização de Países no Mapa")
dataset = pd.read_csv ('https://www.irdx.com.br/media/uploads/paises.csv')
st.dataframe(dataset)

st.subheader("🗺️ Coordenadas dos países no mapa (Scatter Geo)")

fig1 = px.scatter_geo(
    dataset,
    lat=dataset.latitude,
    lon=dataset.longitude,
    hover_name=dataset.nome
