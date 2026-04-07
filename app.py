import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DE E-MAIL (MUITO IMPORTANTE) ---
# Dica: Na Cloud, usa st.secrets para não expor a tua pass no código
EMAIL_MEU = "supergamerlivept@gmail.com"
EMAIL_PASS = "vsekxbeanppigvzj" # Não é a senha normal, é a "App Password"

def enviar_email(destinatario, cliente_nome, local, observacoes):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_MEU
    msg['To'] = destinatario
    msg['Subject'] = f"Relatório de Manutenção - {cliente_nome}"

    corpo = f"""
    Olá,
    Segue o resumo da manutenção de incêndio:
    
    Cliente: {cliente_nome}
    Local: {local}
    Observações: {observacoes}
    
    Relatório gerado automaticamente pela MAGILARMES.
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smpt.gmail.com', 587) # Se for Outlook use: ://office365.com
        server.starttls()
        server.login(EMAIL_MEU, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")
        return False

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="MAGILARMES", layout="centered")
st.title("🛡️ MAGILARMES")

with st.expander("📍 Dados do Cliente", expanded=True):
    cliente = st.text_input("Nome do Cliente / Empresa")
    email_cliente = st.text_input("E-mail do Cliente") # Campo novo
    col_local, col_data = st.columns(2)
    with col_local:
        localizacao = st.text_input("Local da Instalação")
    with col_data:
        data = st.date_input("Data da Intervenção")

st.markdown("### ✅ Checklist")
# ... (Checkboxes aqui como no código anterior)
observacoes = st.text_area("Observações Técnicas")

st.markdown("### ✍️ Assinatura")
canvas_result = st_canvas(stroke_width=3, background_color="#eeeeee", height=150, key="canvas")

if st.button("Finalizar e Enviar por E-mail", use_container_width=True):
    assinou = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if cliente and email_cliente and assinou:
        with st.spinner("A enviar relatórios..."):
            # Envia para ti e para o cliente
            ok_meu = enviar_email(EMAIL_MEU, cliente, localizacao, observacoes)
            ok_cliente = enviar_email(email_cliente, cliente, localizacao, observacoes)
            
            if ok_meu and ok_cliente:
                st.success("Relatórios enviados com sucesso para ambos!")
                st.balloons()
    else:
        st.error("Preencha o nome, e-mail do cliente e assine.")
