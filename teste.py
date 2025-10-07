import streamlit as st

st.title("Meu APP - Aula do Josir")
st.write("Olá! Esse é o meu app do streamlit")

nome = st.text_input ("Digite seu nome:")
if nome:
  st.write(Bem-vindo(a)_nome.upper())
