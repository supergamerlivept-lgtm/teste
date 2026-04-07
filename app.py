import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

st.set_page_config(page_title="MAGILARMES - Manutenção", layout="centered")

st.title("🛡️ MAGILARMES")
st.subheader("Relatório de Manutenção: Sistema de Deteção de Incêndio")

# --- SECÇÃO 1: DADOS DO CLIENTE ---
with st.expander("📍 Dados do Cliente", expanded=True):
    cliente = st.text_input("Nome do Cliente / Empresa")
    localizacao = st.text_input("Local da Instalação")
    data = st.date_input("Data da Intervenção")

# --- SECÇÃO 2: CHECKLIST DE MANUTENÇÃO ---
st.markdown("### ✅ Checklist de Inspeção")
col1, col2 = st.columns(2)

with col1:
    central = st.checkbox("Central de Incêndio Operacional")
    detectores = st.checkbox("Detectores Limpos e Testados")
    baterias = st.checkbox("Baterias em Bom Estado")

with col2:
    sirenes = st.checkbox("Sirenes/Alarmes Testados")
    botoeiras = st.checkbox("Botoeiras de Emergência OK")
    comunicador = st.checkbox("Comunicador Rocha/GSM OK")

# --- SECÇÃO 3: OBSERVAÇÕES E ASSINATURA ---
st.markdown("---")
observacoes = st.text_area("Observações Técnicas / Peças Substituídas")

st.markdown("### ✍️ Assinatura Digital")
canvas_result = st_canvas(
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=150,
    drawing_mode="freedraw",
    key="canvas_magilarmes",
)

# --- BOTÃO DE SUBMISSÃO ---
if st.button("Finalizar Relatório"):
    if cliente and (canvas_result.image_data is not None):
        st.success(f"Relatório de {cliente} guardado com sucesso!")
        st.balloons()
        # Aqui o relatório estaria pronto para ser enviado ou impresso
    else:
        st.warning("Por favor, preencha o nome do cliente e assine o campo.")
