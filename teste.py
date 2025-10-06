import streamlit as st

st.title("Meu Programa")
st.write("oi mundo")

nome = st.text_input("Digite seu nome:")
if nome:
  st.write(nome.upper())
