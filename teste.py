import streamlit as st

st.title("Meu APP - Aula do Josir")
st.write("Olá! Esse é o meu app do streamlit")
st.image (https://www.xbasic.org/wp-content/uploads/2022/07/Python-533x400.jpg)

nome = st.text_input ("Digite seu nome:")
if nome:
  st.write(nome.upper())
