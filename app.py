import streamlit as st
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from PIL import Image, ImageEnhance
import io

# Configuração de Acesso Simplificada
try:
    cred_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    creds = service_account.Credentials.from_service_account_info(cred_dict, scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=creds)
except Exception as e:
    st.error(f"Erro na configuração: {e}")
    st.stop()

st.set_page_config(page_title="DOC-PRO Transportadora", layout="wide")

st.title("🚚 Sistema de Documentos")

menu = st.sidebar.radio("Navegação", ["📦 Enviar/Receber", "📂 Gestão do Drive", "🖼️ Editor de Nitidez"])

if menu == "📦 Enviar/Receber":
    st.subheader("📤 Enviar Documentos")
    uploads = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)
    if uploads:
        for arq in uploads:
            with st.spinner(f"Enviando {arq.name}..."):
                meta = {'name': arq.name}
                media = MediaIoBaseUpload(io.BytesIO(arq.getbuffer()), mimetype=arq.type)
                drive_service.files().create(body=meta, media_body=media).execute()
                st.success(f"✅ {arq.name} salvo!")
                st.markdown(f"[📲 Enviar via Zap](https://wa.me/?text=Documento+{arq.name}+recebido)")

elif menu == "📂 Gestão do Drive":
    st.subheader("📋 Arquivos na Nuvem")
    res = drive_service.files().list(pageSize=15, fields="files(id, name)").execute()
    arquivos = res.get('files', [])
    for a in arquivos:
        col1, col2 = st.columns([4, 1])
        col1.write(f"📄 {a['name']}")
        if col2.button("🗑️ Apagar", key=a['id']):
            drive_service.files().delete(fileId=a['id']).execute()
            st.rerun()

elif menu == "🖼️ Editor de Nitidez":
    st.subheader("🖼️ Melhorar Documento Embaçado")
    foto = st.file_uploader("Suba a foto", type=['jpg', 'jpeg', 'png'])
    if foto:
        img = Image.open(foto)
        n = st.slider("Nitidez", 1.0, 5.0, 2.5)
        c = st.slider("Contraste", 1.0, 3.0, 1.5)
        
        img_edit = ImageEnhance.Sharpness(img).enhance(n)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
        
        st.image(img_edit, use_container_width=True)
        buf = io.BytesIO()
        img_edit.save(buf, format="JPEG")
        st.download_button("📥 Baixar Imagem Limpa", data=buf.getvalue(), file_name="corrigido.jpg")
