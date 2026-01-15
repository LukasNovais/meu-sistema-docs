import streamlit as st
import os
import pandas as pd
from PIL import Image, ImageEnhance
from fpdf import FPDF
import io

if not os.path.exists("meus_documentos"):
    os.makedirs("meus_documentos")

st.set_page_config(page_title="Transportadora Pro", layout="wide")

# --- CONFIGURAÇÃO WHATSAPP ---
st.sidebar.header("Configurações")
tipo_zap = st.sidebar.radio("Enviar por onde?", ["WhatsApp Pessoal", "WhatsApp Business (Web)"])

# Define o link correto para Business Web ou Pessoal
if tipo_zap == "WhatsApp Business (Web)":
    url_base_zap = "https://web.whatsapp.com/send?text="
else:
    url_base_zap = "https://wa.me/?text="

aba = st.sidebar.radio("Navegação", ["📤 Enviar e Receber", "📂 Ver Meus Arquivos", "🛠️ Melhorar Foto e PDF"])

# --- ABA 1: ENVIO ---
if aba == "📤 Enviar e Receber":
    st.subheader("Enviar novo documento")
    u_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)
    
    if u_files:
        for f in u_files:
            caminho = os.path.join("meus_documentos", f.name)
            with open(caminho, "wb") as m:
                m.write(f.getbuffer())
            st.success(f"✅ {f.name} salvo!")

# --- ABA 2: GESTÃO E VISUALIZAÇÃO ---
elif aba == "📂 Ver Meus Arquivos":
    st.subheader("Documentos Armazenados")
    lista = os.listdir("meus_documentos")
    
    for item in lista:
        with st.expander(f"📄 Ver Arquivo: {item}"):
            caminho = os.path.join("meus_documentos", item)
            ext = item.split('.')[-1].lower()
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # VISUALIZADOR POR TIPO DE ARQUIVO
                if ext in ['jpg', 'jpeg', 'png']:
                    st.image(caminho, width=400)
                elif ext == 'pdf':
                    st.info("Arquivo PDF (Clique em baixar para abrir)")
                elif ext in ['csv', 'xml', 'txt']:
                    try:
                        with open(caminho, 'r', encoding='utf-8') as f:
                            st.code(f.read(), language='xml' if ext == 'xml' else 'text')
                    except:
                        st.warning("Não foi possível pré-visualizar o texto deste arquivo.")

            with col2:
                with open(caminho, "rb") as f_data:
                    st.download_button("📥 Baixar", f_data, file_name=item, key=f"dl_{item}")
                
                # Link WhatsApp com texto pronto
                msg = f"Segue o documento: {item}"
                link_final = f"{url_base_zap}{msg}"
                st.markdown(f'<a href="{link_final}" target="_blank" style="text-decoration:none;"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">📲 Abrir no WhatsApp</button></a>', unsafe_allow_html=True)
                
                if st.button("🗑️ Apagar", key=f"del_{item}"):
                    os.remove(caminho)
                    st.rerun()

# --- ABA 3: MELHORAR E PDF ---
elif aba == "🛠️ Melhorar Foto e PDF":
    st.subheader("Tratamento de Documentos")
    foto = st.file_uploader("Carregue a foto do canhoto", type=['jpg', 'jpeg', 'png'])
    
    if foto:
        img = Image.open(foto)
        c1, c2 = st.columns(2)
        with c1:
            n = st.slider("Nitidez", 1.0, 5.0, 2.0)
            c = st.slider("Contraste", 1.0, 3.0, 1.5)
            img_edit = ImageEnhance.Sharpness(img).enhance(n)
            img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
            st.image(img_edit, caption="Prévia", use_container_width=True)
            
        with c2:
            if st.button("Salvar como PDF"):
                pdf = FPDF()
                pdf.add_page()
                img_edit.save("temp.jpg")
                pdf.image("temp.jpg", 10, 10, 190)
                nome_pdf = foto.name.split('.')[0] + ".pdf"
                pdf.output(os.path.join("meus_documentos", nome_pdf))
                st.success(f"✅ PDF '{nome_pdf}' criado!")
