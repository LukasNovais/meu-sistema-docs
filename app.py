import streamlit as st
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image, ImageEnhance
import io

# Configuração de Acesso com correção de erro
try:
    google_json_str = st.secrets["GOOGLE_JSON"]
    info = json.loads(google_json_str)
    creds = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=creds)
except Exception as e:
    st.error(f"Erro nas Credenciais: Verifique os Secrets no Streamlit. Erro: {e}")
    st.stop()

st.set_page_config(page_title="DOC-PRO Transportadora", layout="wide")

st.title("🚚 Gestão de Documentos Digital")

aba = st.sidebar.radio("Navegação", ["📦 Receber e Enviar", "📂 Gestão do Drive", "🖼️ Melhorar Imagem"])

# --- ABA 1: RECEBER E ENVIAR ---
if aba == "📦 Receber e Enviar":
    st.subheader("📤 Envio Rápido")
    arquivos = st.file_uploader("Selecione os documentos", accept_multiple_files=True)
    
    if arquivos:
        for arq in arquivos:
            with st.spinner(f"Enviando {arq.name}..."):
                file_metadata = {'name': arq.name}
                media = MediaIoBaseUpload(io.BytesIO(arq.getbuffer()), mimetype=arq.type)
                drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                st.success(f"✅ {arq.name} salvo no Google Drive!")
                
                # Link WhatsApp
                msg = f"Documento enviado para o Drive: {arq.name}"
                st.markdown(f"[📲 Avisar no WhatsApp](https://wa.me/?text={msg})")

# --- ABA 2: GESTÃO DO DRIVE ---
elif aba == "📂 Gestão do Drive":
    st.subheader("📋 Arquivos no Google Drive")
    results = drive_service.files().list(pageSize=20, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        st.info("Nenhum arquivo encontrado no Drive.")
    else:
        for item in items:
            col1, col2 = st.columns([4, 1])
            col1.write(f"📄 {item['name']}")
            if col2.button("🗑️ Excluir", key=item['id']):
                drive_service.files().delete(fileId=item['id']).execute()
                st.rerun()

# --- ABA 3: EDITOR ---
elif aba == "🖼️ Melhorar Imagem":
    st.subheader("🖼️ Editor de Nitidez (Fotos Ruins)")
    foto = st.file_uploader("Carregar foto do celular", type=['jpg', 'png', 'jpeg'])
    if foto:
        img = Image.open(foto)
        col1, col2 = st.columns(2)
        with col1:
            n = st.slider("Aumentar Nitidez", 1.0, 5.0, 2.0)
            c = st.slider("Melhorar Contraste", 1.0, 3.0, 1.5)
            b = st.slider("Ajustar Brilho", 0.5, 2.0, 1.0)
        
        img_edit = ImageEnhance.Sharpness(img).enhance(n)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
        img_edit = ImageEnhance.Brightness(img_edit).enhance(b)
        
        with col2:
            st.image(img_edit, use_container_width=True)
            buf = io.BytesIO()
            img_edit.save(buf, format="JPEG")
            st.download_button("📥 Baixar para enviar", data=buf.getvalue(), file_name="corrigido.jpg")
