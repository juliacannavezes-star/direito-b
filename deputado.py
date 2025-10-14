
import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df

def main():
    st.title("Visualização de Deputados 2022")

    csv_url = "https://www.irdx.com.br/media/uploads/deputados_2022.csv"
    try:
        df = load_data(csv_url)
    except Exception as e:
        st.error(f"Não foi possível carregar os dados: {e}")
        return

    st.write("Dados carregados (primeiras linhas):")
    st.dataframe(df.head())

    # Exemplo de gráfico: número de deputados por estado
    if "uf" in df.columns:
        st.subheader("Número de deputados por estado (UF)")
        contagem = df["uf"].value_counts().reset_index()
        contagem.columns = ["uf", "count"]
        chart = alt.Chart(contagem).mark_bar().encode(
            x=alt.X("uf:N", sort="-y", title="Estado (UF)"),
            y=alt.Y("count:Q", title="Número de deputados"),
            tooltip=["uf", "count"]
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("A coluna 'uf' não foi encontrada no CSV.")

    # Exemplo adicional: deputados por partido (se existir coluna)
    if "partido" in df.columns:
        st.subheader("Número de deputados por partido")
        cont_p = df["partido"].value_counts().reset_index()
        cont_p.columns = ["partido", "count"]
        chart_p = alt.Chart(cont_p).mark_bar().encode(
            x=alt.X("partido:N", sort="-y", title="Partido"),
            y=alt.Y("count:Q", title="Número de deputados"),
            tooltip=["partido", "count"]
        )
        st.altair_chart(chart_p, use_container_width=True)

if __name__ == "__main__":
    main()
