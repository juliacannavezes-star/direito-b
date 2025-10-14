import streamlit as st
import pandas as pd
import altair as alt

def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df

def main():
    st.title("Deputados por Partido (2022)")

    url = "https://www.irdx.com.br/media/uploads/deputados_2022.csv"
    df = load_data(url)

    st.write("Dados originais (primeiras linhas):")
    st.dataframe(df.head())


    coluna_partido = "Partido"
    if coluna_partido not in df.columns:
        st.error(f"Coluna '{coluna_partido}' não encontrada no dataset.")
        return

    contagem = df.groupby(coluna_partido).size().reset_index(name="Quantidade")

    contagem = contagem.sort_values("Quantidade", ascending=False)

    chart = (
        alt.Chart(contagem)
        .mark_bar()
        .encode(
            x=alt.X("Quantidade:Q", title="Número de Deputados"),
            y=alt.Y(f"{coluna_partido}:N", sort='-x', title="Partido"),
            tooltip=[coluna_partido, "Quantidade"]
        )
        .properties(
            width=700,
            height=400,
            title="Número de Deputados por Partido (2022)"
        )
    )

    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
