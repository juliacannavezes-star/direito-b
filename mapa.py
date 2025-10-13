import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
url = "https://www.irdx.com.br/media/uploads/paises.csv"
dataset = pd.read_csv(url)

# Criar gráfico Scatter Geo
fig1 = px.scatter_geo(
    dataset,
    lat=dataset.latitude,
    lon=dataset.longitude,
    hover_name=dataset.nome
)

# Layout do gráfico
fig1.update_layout(
    showlegend=False,
    title="Coordenadas dos países no mapa",
    geo_scope='world'
)

# Exibir no Streamlit
st.plotly_chart(fig1)

