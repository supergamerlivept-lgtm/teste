import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import yagmail
from PIL import Image
from fpdf import FPDF
import os

# --- CONFIGURAÇÕES ---
EMAIL_MEU = "supergamerlivept@gmail.com"
EMAIL_PASS = "vsekxbeanppigvzj"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "MAGILARMES", ln=True, align="C")
        self.cell(0, 10, "Relatório Serviço Manutenção do Sistema Automático de Deteção de Incendio", ln=True, align="C")
        self.ln(10)

def gerar_pdf(cliente, email, local, data, hora, checklist, obs, assinatura_path):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Dados do Cliente
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Cliente: {cliente}", ln=True)
    pdf.cell(0, 8, f"Local: {local}", ln=True)
    pdf.cell(0, 8, f"Data: {data}" f"Hora: {hora}", ln=True)
    pdf.ln(5)

    # Checklist
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Checklist de Inspeção:", ln=True)
    pdf.set_font("Arial", size=11)
    for item, status in checklist.items():
        res = "OK" if status else "NÃO VERIFICADO / FALHA"
        pdf.cell(0, 8, f"- {item}: {res}", ln=True)
    
    # Observações
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Observações Técnicas:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, obs)
    
    # Assinatura
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Assinatura Digital:", ln=True)
    pdf.image(assinatura_path, x=10, w=60)
    
    pdf_path = f"Relatorio_{cliente.replace(' ', '_')}.pdf"
    pdf.output(pdf_path)
    return pdf_path

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="MAGILARMES PDF", layout="centered")
st.title("🛡️ MAGILARMES")
st.subheader("Gerador de Relatório S.A.D.I. (PDF)")

with st.expander("📍 Informações Gerais", expanded=True):
    cliente = st.text_input("Nome do Cliente")
    email_cliente = st.text_input("E-mail do Cliente")
    col1, col2, col3 = st.columns(3)
    with col1: localizacao = st.text_input("Local")
    with col2: data_servico = st.date_input("Data")
    with col3: hora_servico = st.time_input("Hora")        

st.markdown("### ✅ Checklist")
c1, c2 = st.columns(2)
with c1:
    v1 = st.checkbox("Central OK")
    v2 = st.checkbox("Detectores OK")
with c2:
    v3 = st.checkbox("Sirenes OK")
    v4 = st.checkbox("Baterias OK")

observacoes = st.text_area("Notas Técnicas")

st.markdown("### ✍️ Assinatura")
canvas_result = st_canvas(stroke_width=3, background_color="#eeeeee", height=150, key="pdf_canvas")

if st.button("Gerar PDF e Enviar", use_container_width=True):
    assinou = canvas_result.image_data is not None and np.any(canvas_result.image_data > 0)
    
    if cliente and email_cliente and assinou:
        with st.spinner("A criar PDF e a enviar..."):
            # 1. Guardar Imagem da Assinatura
            img_array = np.array(canvas_result.image_data)
            img = Image.fromarray(img_array.astype('uint8'), 'RGBA')
            # Converter para RGB para o PDF (tira o fundo transparente)
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img_path = "temp_assinatura.jpg"
            bg.save(img_path, "JPEG")
            
            # 2. Gerar PDF
            dados_check = {"Central": v1, "Detectores": v2, "Sirenes": v3, "Baterias": v4}
            pdf_final = gerar_pdf(cliente, email_cliente, localizacao, data_servico, hora_servico, dados_check, observacoes, img_path)
            
            # 3. Enviar Email
            try:
                yag = yagmail.SMTP(EMAIL_MEU, EMAIL_PASS)
                assunto = f"Relatório Técnico - {cliente}"
                corpo = "Segue em anexo o relatório oficial de manutenção da MAGILARMES."
                yag.send(to=[email_cliente, EMAIL_MEU], subject=assunto, contents=corpo, attachments=pdf_final)
                st.success("PDF enviado com sucesso para todos!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro no envio: {e}")
    else:
        st.error("Preencha os dados e assine.")
