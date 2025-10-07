import streamlit as st

st.title("🌟 Meu APP Interativo - Aula Josir ⚖️")
st.markdown("## Boas-vindas ao App da Josir!")
st.write("Olá! Esse é o meu primeiro app Streamlit!")

nome = st.text_input("**Digite seu nome completo:**")

if nome:
    st.success(f"**Olá, {nome.split()[0].title()}!** Seu nome tem **{len(nome)}** caracteres.")
  
    st.header("🎨 Qual a sua Cor Favorita?")   
    cor_favorita = st.selectbox(
        "Selecione uma cor para personalizar a mensagem abaixo:",
        ("Azul", "Verde", "Vermelho", "Amarelo", "Roxo"))

    if cor_favorita == "Azul":
        st.info(f"Ótima escolha, {cor_favorita}! O azul é a cor do céu e da tranquilidade.")
    elif cor_favorita == "Verde":
        st.success(f"Que bom, {cor_favorita}! O verde representa a natureza e esperança.")
    elif cor_favorita == "Vermelho":
        st.error(f"Uau, {cor_favorita}! Uma cor de muita energia e amor.")
    else:
        st.warning(f"Você escolheu **{cor_favorita}**. Uma cor vibrante! ✨")

    st.markdown("---")
    
    
    st.header("Escala de felicidade")

    nivel_criatividade = st.slider(
        'Em uma escala de 1 a 10, quão feliz você está?',
        1, 10, 5)
    
    st.write(f"Você está **{nivel_criatividade}/10** feliz.")
    
    if st.button('Clique para uma surpresa!'):
        if nivel_criatividade >= 8:
            st.balloons()
            st.subheader("🎉 Parabéns pela sua criatividade!")
        else:
            st.snow() 
        
            
