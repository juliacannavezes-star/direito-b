import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils import download_pdf, try_tabula_extract, pdfplumber_extract, normalize_table

PDF_URL = "https://www.gov.br/senappen/pt-br/servicos/sisdepen/relatorios/relatorios-de-informacoes-penitenciarias/relatorio-1o-semestre-de-2025.pdf"
LOCAL_PDF = "relatorio_sisdepen_1s2025.pdf"

st.set_page_config(layout="wide", page_title="SISDEPEN — Painel (demo)")

st.title("Painel interativo — Dados SISDEPEN (1º semestre 2025)")
st.markdown("Fonte: Relatório SENAPPEN — 1º semestre de 2025. (PDF oficial).")

# botão para baixar PDF
if st.button("Baixar/Atualizar PDF fonte"):
    with st.spinner("Baixando PDF..."):
        download_pdf(PDF_URL, LOCAL_PDF)
    st.success("PDF baixado para: " + LOCAL_PDF)

# garantir PDF disponível
if not os.path.exists(LOCAL_PDF):
    st.info("PDF não encontrado localmente. Vou baixar automaticamente (pode demorar).")
    with st.spinner("Baixando PDF..."):
        download_pdf(PDF_URL, LOCAL_PDF)
    st.success("Download concluído.")

st.sidebar.header("Configuração de extração")
mode = st.sidebar.selectbox("Tabela alvo", ["População prisional (cela física)", "Capacidade de vagas"])
extract_method = st.sidebar.selectbox("Método preferido", ["tabula (recomendado)", "pdfplumber (fallback)"])

# Páginas conhecidas (com base no relatório)
# Observação: as páginas do PDF exibidas na web.run mostram População em página 12 (index 12), Capacidade em 15.
# No PDF, página visual = 12 => pageno=11 (0-based). Ajuste conforme necessidade.
if mode == "População prisional (cela física)":
    pages_for_pop = "12"  # string para tabula
    pages_for_pdfplumber = [12]  # 1-based for pdfplumber_extract in utils
else:
    pages_for_pop = "15"
    pages_for_pdfplumber = [15]

st.sidebar.markdown(f"Páginas alvo: {pages_for_pop}")

# extração
@st.cache_data(ttl=600)
def extract_table(pdf_path, pages_tabula, pages_pdfplumber):
    df = None
    if extract_method == "tabula (recomendado)":
        df = try_tabula_extract(pdf_path, pages_tabula)
    if df is None:
        df = pdfplumber_extract(pdf_path, pages_pdfplumber)
    return df

with st.spinner("Extraindo tabelas do PDF..."):
    raw_df = extract_table(LOCAL_PDF, pages_for_pop, pages_for_pdfplumber)

if raw_df is None or raw_df.empty:
    st.error("Não foi possível extrair tabelas automaticamente desta página. Tente outro método no painel lateral ou atualize o PDF.")
    st.stop()

st.subheader("Preview das primeiras linhas da tabela extraída (crua)")
st.dataframe(raw_df.head(20))

# normalizar
try:
    norm = normalize_table(raw_df,
                           col_uf_candidates=['UF','Uf','UF '],
                           col_val_candidates=['População Prisional','População','Capacidade','Capacidade '])
except Exception as e:
    st.error("Erro ao normalizar a tabela: " + str(e))
    st.stop()

st.subheader("Tabela normalizada (UF | value)")
st.dataframe(norm)

# preparar para plot
norm['value'] = pd.to_numeric(norm['value'], errors='coerce')
norm = norm.dropna(subset=['value'])
norm = norm.sort_values('value', ascending=False)

st.markdown("### Gráfico: valores por UF")
chart = px.bar(norm, x='UF', y='value', hover_data=['value'], labels={'value':'Quantidade', 'UF':'UF'}, title=mode)
st.plotly_chart(chart, use_container_width=True)

# opção de download csv
csv = norm.to_csv(index=False).encode('utf-8')
st.download_button(label="Baixar dados (CSV)", data=csv, file_name="sisdepen_tabela_normalizada.csv", mime="text/csv")

st.markdown("---")
st.markdown("Observações:")
st.markdown("- O app faz uma heurística para identificar a coluna UF e a coluna de valores. Caso os resultados fiquem estranhos, experimente mudar o método de extração (sidebar) ou indicar manualmente as páginas no código.")
st.markdown("- Para maior precisão em tabelas complexas, instale Java para permitir o uso de `tabula-py`.")
