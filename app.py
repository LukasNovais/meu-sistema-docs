import streamlit as st
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image, ImageEnhance
import io

# Configuração de Acesso
if "GOOGLE_CREDENTIALS" in st.secrets:
    info = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(info)
    drive_service = build('drive', 'v3', credentials=creds)
else:
    st.error("Configure as Credenciais no Streamlit/GitHub primeiro.")

st.set_page_config(page_title="DOC-PRO Transportadora", layout="wide")

# Interface
st.title("🚚 Sistema de Documentos Digital")

aba = st.sidebar.radio("Navegação", ["Enviar/Receber", "Editor de Imagem"])

if aba == "Enviar/Receber":
    st.subheader("📤 Enviar para Google Drive")
    arquivos = st.file_uploader("Selecione os documentos", accept_multiple_files=True)
    
    if arquivos:
        for arq in arquivos:
            file_metadata = {'name': arq.name}
            media = MediaIoBaseUpload(io.BytesIO(arq.getbuffer()), mimetype=arq.type)
            drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            st.success(f"✅ {arq.name} enviado!")
            
            # Botão Zap rápido
            st.markdown(f"[📲 Enviar aviso de {arq.name} via Zap](https://wa.me/?text=Documento+{arq.name}+enviado+para+o+Drive)")

elif aba == "Editor de Imagem":
    st.subheader("🖼️ Melhorar Qualidade do Documento")
    foto = st.file_uploader("Carregar imagem", type=['jpg', 'png', 'jpeg'])
    if foto:
        img = Image.open(foto)
        col1, col2 = st.columns(2)
        with col1:
            n = st.slider("Nitidez (Foco)", 1.0, 5.0, 2.0)
            c = st.slider("Contraste (Fundo Branco)", 1.0, 3.0, 1.5)
            b = st.slider("Brilho", 0.5, 2.0, 1.0)
        
        # Processamento
        img_edit = ImageEnhance.Sharpness(img).enhance(n)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
        img_edit = ImageEnhance.Brightness(img_edit).enhance(b)
        
        with col2:
            st.image(img_edit, caption="Resultado", use_container_width=True)
            buf = io.BytesIO()
            img_edit.save(buf, format="JPEG")
            st.download_button("📥 Baixar Imagem Melhorada", data=buf.getvalue(), file_name="doc_corrigido.jpg")
