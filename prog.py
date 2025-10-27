import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Leis Explicadas por Gráficos", page_icon="⚖️", layout="centered")

# Título e introdução
st.title("⚖️ Leis Explicadas por Gráficos")
st.write("""
Este aplicativo interativo mostra **estatísticas e impactos simulados** de algumas leis brasileiras importantes.
Escolha uma lei abaixo e explore os gráficos 📊
""")

# Leis disponíveis
leis = {
    "Lei Maria da Penha (11.340/2006)": "Protege mulheres contra a violência doméstica.",
    "Lei de Acesso à Informação (12.527/2011)": "Garante o direito de acesso a informações públicas.",
    "Lei Anticorrupção (12.846/2013)": "Responsabiliza empresas por atos de corrupção.",
    "Marco Civil da Internet (12.965/2014)": "Regula o uso da internet no Brasil.",
    "Lei Geral de Proteção de Dados - LGPD (13.709/2018)": "Protege dados pessoais e privacidade."
}

lei_escolhida = st.selectbox("📜 Escolha uma lei para visualizar:", list(leis.keys()))

st.info(leis[lei_escolhida])

# Função para gerar dados simulados
def gerar_dados(lei):
    if "Maria da Penha" in lei:
        anos = list(range(2006, 2025))
        casos = [2000 + i * 500 + (i**1.5)*30 for i in range(len(anos))]
        prisões = [x * 0.35 for x in casos]
        return pd.DataFrame({"Ano": anos, "Casos Registrados": casos, "Prisões Efetuadas": prisões})
    
    elif "Acesso à Informação" in lei:
        anos = list(range(2012, 2025))
        pedidos = [5000 + i * 1200 for i in range(len(anos))]
        respostas = [p * (0.9 + (i/100)) for i, p in enumerate(pedidos)]
        return pd.DataFrame({"Ano": anos, "Pedidos de Informação": pedidos, "Respostas Enviadas": respostas})
    
    elif "Anticorrupção" in lei:
        anos = list(range(2013, 2025))
        processos = [100 + i * 20 + (i**2) for i in range(len(anos))]
        multas = [p * 3.2 for p in processos]
        return pd.DataFrame({"Ano": anos, "Processos": processos, "Multas (em milhões R$)": multas})
    
    elif "Marco Civil" in lei:
        anos = list(range(2014, 2025))
        casos = [50 + i * 30 + (i**2)*2 for i in range(len(anos))]
        remoções = [c * 0.6 for c in casos]
        return pd.DataFrame({"Ano": anos, "Casos na Justiça": casos, "Remoções de Conteúdo": remoções})
    
    elif "LGPD" in lei:
        anos = list(range(2018, 2025))
        denúncias = [100 + i * 400 for i in range(len(anos))]
        empresas_autuadas = [d * 0.4 for d in denúncias]
        return pd.DataFrame({"Ano": anos, "Denúncias": denúncias, "Empresas Autuadas": empresas_autuadas})

# Gerar dados com base na escolha
df = gerar_dados(lei_escolhida)

# Escolha do tipo de gráfico
tipo_grafico = st.radio("📊 Escolha o tipo de gráfico:", ["Linha", "Barras", "Área"], horizontal=True)

# Mostrar gráfico
if tipo_grafico == "Linha":
    fig = px.line(df, x="Ano", y=df.columns[1:], markers=True, title=f"Evolução - {lei_escolhida}")
elif tipo_grafico == "Barras":
    fig = px.bar(df, x="Ano", y=df.columns[1:], barmode="group", title=f"Comparativo - {lei_escolhida}")
else:
    fig = px.area(df, x="Ano", y=df.columns[1:], title=f"Tendência - {lei_escolhida}")

st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Feito com ❤️ e Streamlit • Projeto educacional • Dados simulados para fins ilustrativos")
