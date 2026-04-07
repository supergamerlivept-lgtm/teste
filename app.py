import streamlit as st

st.set_page_config(page_title="Formulário Cloud", page_icon="📝")

st.title("MAGILARMES")
st.markdown("Relatório Serviço Manutenção do Sistema Automático de Deteção de Incendio")

# Criar o formulário
with st.form("feedback_form", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    tipo_servico = st.selectbox("Tipo de Serviço", ["Consultoria", "Suporte", "Vendas"])
    mensagem = st.text_area("A sua mensagem")
    classificacao = st.slider("Avaliação (0 a 10)", 0, 10, 5)
    nome = st.text_input("Nome do Signatário")
    
    st.markdown("### Assine aqui (use o dedo ou rato):")
    
    # Criar o componente de desenho (Canvas)
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Cor de preenchimento
        stroke_width=3,                       # Espessura do traço
        stroke_color="#000000",               # Cor do traço (preto)
        background_color="#eeeeee",           # Cor de fundo da área
        height=150,                           # Altura da área de assinatura
        drawing_mode="freedraw",              # Modo desenho livre
        key="canvas",
    )
    
    # Botão de submissão
    submetido = st.form_submit_button("Enviar Dados")

    if submetido:
        if nome and email:
            # Aqui pode adicionar lógica para guardar num Google Sheet ou Base de Dados
            st.success(f"Sucesso! Obrigado, {nome}. Recebemos o seu feedback.")
            st.balloons()
        else:
            st.error("Por favor, preencha o Nome e o E-mail.")
