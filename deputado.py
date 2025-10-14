
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Visualização de Países no Mapa")

dataset = pd.read_csv ('https://www.irdx.com.br/media/uploads/deputados_2022.csv')

st.plotly_chart(fig, use_container_with=True, theme='streamlit')
