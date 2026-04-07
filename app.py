import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import yagmail
from PIL import Image

# --- CONFIGURAÇÕES ---
EMAIL_MEU = "supergamerlivept@gmail.com"
EMAIL_PASS = "vsekxbeanppigvzj" # Senha de App sem espaços

def enviar_email_completo(destinatario, cliente_nome, local, observacoes, checklist, imagem_assinatura):
    try:
        yag = yagmail.SMTP(EMAIL_MEU, EMAIL_PASS)
        
        # 1. Preparar o texto da Checklist
        texto_checklist = ""
        for item, status in checklist.items():
            icone = "✅" if status else "❌"
            texto_checklist += f"{icone} {item}\n"

        # 2. Montar o corpo do e-mail
        assunto = f"Relatório de Manutenção MAGILARMES - {cliente_nome}"
        conteudo = [
            f"""
            RELATÓRIO DE MANUTENÇÃO - SISTEMA DE INCÊNDIO
            ----------------------------------------------
            Cliente: {cliente_nome}
            Local: {local}

            CHECKLIST DE INSPEÇÃO:
            {texto_checklist}

            OBSERVAÇÕES TÉCNICAS:
            {observacoes}

            ----------------------------------------------
            Assinatura digital em anexo.
            """,
            imagem_assinatura # Envia a imagem como anexo
        ]
        
        yag.send(to=destinatario, subject=assunto, contents=conteudo)
        return True
    except Exception as e:
        st.error(f"Erro no envio: {e}")
        return False

# --- INTERFACE ---
st.set_page_config(page_title="MAGILARMES", layout="centered")
st.title("🛡️ MAGILARMES")
st.subheader("Relatório de Manutenção S.A.D.I.")

# Secção 1: Dados
with st.expander("📍 Dados do Cliente", expanded=True):
    cliente = st.text_input("Nome do Cliente / Empresa")
    email_cliente = st.text_input("E-mail do Cliente")
    col_l, col_d = st.columns(2)
    with col_l:
        localizacao = st.text_input("Local da Instalação")
    with col_d:
        data = st.date_input("Data da Intervenção")

# Secção 2: Checklist
st.markdown("### ✅ Checklist de Inspeção")
c1, c2 = st.columns(2)
with c1:
    v1 = st.checkbox("Central de Incêndio OK")
    v2 = st.checkbox("Detectores Testados")
with c2:
    v3 = st.checkbox("Sirenes Testadas")
    v4 = st.checkbox("Baterias Verificadas")

observacoes = st.text_area("Observações Técnicas")

# Secção 3: Assinatura
st.markdown("### ✍️ Assinatura Digital")
canvas_result = st_canvas(
    stroke_width=3,
    stroke_color="#000000",
    background_color="#eeeeee",
    height=150,
    drawing_mode="freedraw",
    key="canvas_final_magilarmes",
)

# --- BOTÃO DE ENVIO ---
if st.button("Finalizar e Enviar Relatório", use_container_width=True):
    assinou = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if cliente and email_cliente and assinou:
        with st.spinner("A gerar relatório e a enviar e-mails..."):
            
            # Processar a imagem da assinatura
            img_array = np.array(canvas_result.image_data)
            img = Image.fromarray(img_array.astype('uint8'), 'RGBA')
            img_path = "assinatura.png"
            img.save(img_path)
            
            # Dados para o email
            dados_check = {
                "Central de Incêndio": v1,
                "Detectores": v2,
                "Sirenes": v3,
                "Baterias": v4
            }
            
            # Enviar para o cliente e para a empresa
            sucesso = enviar_email_completo(email_cliente, cliente, localizacao, observacoes, dados_check, img_path)
            enviar_email_completo(EMAIL_MEU, cliente, localizacao, observacoes, dados_check, img_path)
            
            if sucesso:
                st.success(f"Relatório completo enviado para {cliente}!")
                st.balloons()
    else:
        st.error("Preencha o Nome, E-mail e assine o campo para continuar.")
