import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DE ACESSO ---
EMAIL_MEU = "supergamerlivept@gmail.com"
# A chave deve ser escrita sem espaços
EMAIL_PASS = "vsekxbeanppigvzj" 

def enviar_email(destinatario, cliente_nome, local, observacoes):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_MEU
    msg['To'] = destinatario
    msg['Subject'] = f"Relatório de Manutenção MAGILARMES - {cliente_nome}"

    corpo = f"""
    Relatório de Manutenção de Incêndio
    ----------------------------------
    Cliente: {cliente_nome}
    Local: {local}
    Observações: {observacoes}
    
    Este é um relatório automático gerado pela MAGILARMES.
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # Resolve o IP para evitar o erro "Name or service not known"
        endereco_ip = socket.gethostbyname("://gmail.com")
        server = smtplib.SMTP(endereco_ip, 587, timeout=20)
        server.starttls()
        server.login(EMAIL_MEU, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        # Tentativa secundária caso o IP mude
        try:
            server = smtplib.SMTP("://gmail.com", 587, timeout=20)
            server.starttls()
            server.login(EMAIL_MEU, EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e2:
            st.error(f"Erro de rede persistente: {e2}")
            return False

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="MAGILARMES", layout="centered")

st.title("🛡️ MAGILARMES")
st.subheader("Relatório Serviço Manutenção S.A.D.I.")

with st.expander("📍 Dados do Cliente", expanded=True):
    cliente = st.text_input("Nome do Cliente / Empresa")
    email_cliente = st.text_input("E-mail do Cliente")
    
    col_local, col_data = st.columns(2)
    with col_local:
        localizacao = st.text_input("Local da Instalação")
    with col_data:
        data = st.date_input("Data da Intervenção")

st.markdown("### ✅ Checklist de Inspeção")
col1, col2 = st.columns(2)
with col1:
    st.checkbox("Central de Incêndio OK")
    st.checkbox("Detectores Testados")
with col2:
    st.checkbox("Sirenes Testadas")
    st.checkbox("Baterias Verificadas")

observacoes = st.text_area("Observações Técnicas / Peças Substituídas")

st.markdown("### ✍️ Assinatura Digital")
canvas_result = st_canvas(
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    drawing_mode="freedraw",
    key="canvas_final",
)

st.markdown("---")

if st.button("Finalizar e Enviar Relatório", use_container_width=True):
    # Verificar se há assinatura (se o canvas não está vazio)
    assinou = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if cliente and email_cliente and assinou:
        with st.spinner("A processar e enviar e-mails..."):
            sucesso_meu = enviar_email(EMAIL_MEU, cliente, localizacao, observacoes)
            sucesso_cliente = enviar_email(email_cliente, cliente, localizacao, observacoes)
            
            if sucesso_meu and sucesso_cliente:
                st.success(f"Relatório enviado com sucesso para {cliente} e para a central!")
                st.balloons()
    else:
        st.warning("Certifique-se de que preencheu o Nome, E-mail e que assinou o campo.")
