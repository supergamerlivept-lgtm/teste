import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import yagmail # Biblioteca mais robusta para Gmail

# --- CONFIGURAÇÃO ---
EMAIL_MEU = "supergamerlivept@gmail.com"
EMAIL_PASS = "vsekxbeanppigvzj" # Confirma que não tem espaços

def enviar_email_yag(destinatario, cliente_nome, local, observacoes):
    try:
        # Configura o cliente de email
        yag = yagmail.SMTP(EMAIL_MEU, EMAIL_PASS)
        
        assunto = f"Relatório MAGILARMES - {cliente_nome}"
        conteudo = f"""
        Olá, segue o resumo da manutenção:
        
        Cliente: {cliente_nome}
        Local: {local}
        Observações: {observacoes}
        
        Relatório gerado pela MAGILARMES.
        """
        
        yag.send(to=destinatario, subject=assunto, contents=conteudo)
        return True
    except Exception as e:
        st.error(f"Erro no envio: {e}")
        return False

# --- INTERFACE ---
st.set_page_config(page_title="MAGILARMES", layout="centered")
st.title("🛡️ MAGILARMES")

with st.expander("📍 Dados do Cliente", expanded=True):
    cliente = st.text_input("Nome do Cliente / Empresa")
    email_cliente = st.text_input("E-mail do Cliente")
    col_local, col_data = st.columns(2)
    with col_local:
        localizacao = st.text_input("Local da Instalação")
    with col_data:
        data = st.date_input("Data da Intervenção")

st.markdown("### ✅ Checklist Rápida")
c1, c2 = st.columns(2)
with c1:
    central = st.checkbox("Central OK")
    detectores = st.checkbox("Detectores OK")
with c2:
    sirenes = st.checkbox("Sirenes OK")
    baterias = st.checkbox("Baterias OK")

observacoes = st.text_area("Observações Técnicas")

st.markdown("### ✍️ Assinatura")
canvas_result = st_canvas(stroke_width=3, background_color="#eeeeee", height=150, key="canvas_v3")

if st.button("Finalizar e Enviar", use_container_width=True):
    assinou = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if cliente and email_cliente and assinou:
        with st.spinner("A enviar..."):
            # Envia para a empresa e para o cliente
            envio1 = enviar_email_yag(EMAIL_MEU, cliente, localizacao, observacoes)
            envio2 = enviar_email_yag(email_cliente, cliente, localizacao, observacoes)
            
            if envio1 and envio2:
                st.success("Relatórios enviados com sucesso!")
                st.balloons()
    else:
        st.error("Preencha todos os campos e assine.")
