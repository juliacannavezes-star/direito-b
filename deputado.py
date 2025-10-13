import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("Votação da PEC da Blindagem - Deputados 2022")

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("media/uploads/deputados_2022.csv")
    return df

df = load_data()

# Mostrar os primeiros dados para referência
st.subheader("Prévia dos dados")
st.dataframe(df.head())

# Verificar os nomes das colunas disponíveis
st.subheader("Colunas disponíveis")
st.write(df.columns)

# Filtrar votos a favor
if 'voto' in df.columns:
    votos_favor = df[df['voto'].str.lower() == 'a favor']

    # Contagem total
    total_favor = len(votos_favor)

    st.subheader("Total de votos a favor:")
    st.metric(label="Deputados que votaram a favor", value=total_favor)

    # Agrupar por partido (ou outro critério)
    votos_por_partido = votos_favor['partido'].value_counts()

    # Gráfico
    st.subheader("Votos a favor por partido")
    st.bar_chart(votos_por_partido)

else:
    st.error("Coluna 'voto' não encontrada no CSV. Verifique o nome correto.")

