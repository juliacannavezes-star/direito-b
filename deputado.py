media/uploads/deputados_2022.csv
    return pd.read_csv("media/uploads/deputados_2022.csv")

df = carregar_dados()

# Mostrar a tabela completa
st.subheader("Visualização da Tabela Completa")
st.dataframe(df)

# Filtro interativo (por exemplo, partido, estado ou nome, conforme existam no CSV)
colunas = df.columns.tolist()
coluna_filtro = st.selectbox("Escolha uma coluna para filtrar:", colunas)
valores_unicos = df[coluna_filtro].unique()
valor_escolhido = st.selectbox("Escolha um valor:", valores_unicos)

# Aplicar filtro
df_filtrado = df[df[coluna_filtro] == valor_escolhido]

st.subheader("Tabela Filtrada")
st.dataframe(df_filtrado)

# Gráfico simples (exemplo: contar ocorrências de uma coluna)
st.subheader("📈 Gráfico de Distribuição")
coluna_grafico = st.selectbox("Escolha uma coluna para visualizar:", colunas)

fig, ax = plt.subplots()
df[coluna_grafico].value_counts().head(10).plot(kind="bar", ax=ax)
ax.set_title(f"Distribuição dos 10 principais valores em '{coluna_grafico}'")
ax.set_xlabel(coluna_grafico)
ax.set_ylabel("Frequência")

st.pyplot(fig)

# Rodapé
st.caption("Desenvolvido com ❤️ usando Streamlit e Pandas")
