import streamlit as st

st.set_page_config(page_title="Formulário Cloud", page_icon="📝")

st.title("📝 Registo de Feedback")
st.markdown("Preencha os dados abaixo para nos enviar as suas informações.")

# Criar o formulário
with st.form("feedback_form", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    tipo_servico = st.selectbox("Tipo de Serviço", ["Consultoria", "Suporte", "Vendas"])
    mensagem = st.text_area("A sua mensagem")
    classificacao = st.slider("Avaliação (0 a 10)", 0, 10, 5)
    
    # Botão de submissão
    submetido = st.form_submit_button("Enviar Dados")

    if submetido:
        if nome and email:
            # Aqui pode adicionar lógica para guardar num Google Sheet ou Base de Dados
            st.success(f"Sucesso! Obrigado, {nome}. Recebemos o seu feedback.")
            st.balloons()
        else:
            st.error("Por favor, preencha o Nome e o E-mail.")