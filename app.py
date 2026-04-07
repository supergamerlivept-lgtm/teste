import streamlit as st
from streamlit_drawable_canvas import st_canvas # Importação necessária
import numpy as np

st.set_page_config(page_title="MAGILARMES - Relatório", page_icon="📝")

st.title("MAGILARMES")
st.subheader("Relatório Serviço Manutenção do Sistema Automático de Deteção de Incendio")

# 1. CAMPOS DE TEXTO E SELEÇÃO
nome = st.text_input("Nome Completo")
email = st.text_input("E-mail")
tipo_servico = st.selectbox("Tipo de Serviço", ["Manutenção Preventiva", "Manutenção Corretiva", "Instalação"])
mensagem = st.text_area("Observações Técnicas")
classificacao = st.slider("Estado Geral do Sistema (0 a 10)", 0, 10, 5)

st.markdown("---")
st.markdown("### Assinatura do Técnico/Cliente (use o dedo ou rato):")

# 2. O CANVAS (Tem de estar fora do 'st.form')
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    drawing_mode="freedraw",
    key="canvas_assinatura",
)

# 3. BOTÃO DE SUBMISSÃO MANUAL
if st.button("Finalizar e Enviar Relatório"):
    # Validação simples
    tem_assinatura = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if nome and email and tem_assinatura:
        st.success(f"Relatório de {nome} enviado com sucesso!")
        st.balloons()
        
        # Opcional: Mostrar a assinatura processada
        st.image(canvas_result.image_data, caption="Assinatura Digitalizada", width=300)
    else:
        st.error("Por favor, preencha todos os campos e certifique-se de que assinou o documento.")
