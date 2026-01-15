import streamlit as st
import os
import pandas as pd
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from io import BytesIO

# Configuração Base
st.set_page_config(page_title="DOC-PRO Transportadora", layout="wide")
if not os.path.exists("arquivos"):
    os.makedirs("arquivos")

st.sidebar.title("🛠️ Ferramentas")
aba = st.sidebar.radio("Navegação", ["Portaria (Envio/Recebimento)", "Gestão de Arquivos", "Editor de Documentos"])

# --- FUNÇÕES DE PROCESSAMENTO ---
def melhorar_imagem(img, nitidez, contraste, brilho):
    img = ImageEnhance.Sharpness(img).enhance(nitidez)
    img = ImageEnhance.Contrast(img).enhance(contraste)
    img = ImageEnhance.Brightness(img).enhance(brilho)
    return img

# --- ABA 1: ENVIO E RECEBIMENTO ---
if aba == "Portaria (Envio/Recebimento)":
    st.header("📤 Envio Rápido de Documentos")
    upload = st.file_uploader("Arraste ou Tire Foto (PDF, JPG, PNG, XML, CSV, XLSX)", type=None, accept_multiple_files=True)
    
    if upload:
        for file in upload:
            with open(os.path.join("arquivos", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success("✅ Arquivos salvos com sucesso!")

# --- ABA 2: GESTÃO DE ARQUIVOS ---
elif aba == "Gestão de Arquivos":
    st.header("📋 Gestão de Pastas")
    arquivos = os.listdir("arquivos")
    
    for arq in arquivos:
        with st.expander(f"📄 {arq}"):
            col1, col2, col3 = st.columns(3)
            ext = arq.split('.')[-1].lower()
            path = os.path.join("arquivos", arq)
            
            with col1:
                if ext in ['jpg', 'jpeg', 'png']:
                    st.image(path, width=200)
                st.write(f"Tipo: {ext.upper()}")
            
            with col2:
                with open(path, "rb") as f:
                    st.download_button("📥 Baixar", f, file_name=arq, key=f"dl_{arq}")
                if st.button("🗑️ Excluir", key=f"del_{arq}"):
                    os.remove(path)
                    st.rerun()
            
            with col3:
                msg = f"Segue documento da Transportadora: {arq}"
                st.markdown(f"[📲 Enviar via WhatsApp](https://wa.me/?text={msg})")

# --- ABA 3: EDITOR DE DOCUMENTOS ---
elif aba == "Editor de Documentos":
    st.header("🖼️ Melhorar Nitidez e Enquadramento")
    arquivos_img = [f for f in os.listdir("arquivos") if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    if arquivos_img:
        selecionado = st.selectbox("Selecione a imagem para tratar", arquivos_img)
        img_path = os.path.join("arquivos", selecionado)
        image = Image.open(img_path)
        
        col_ed1, col_ed2 = st.columns(2)
        
        with col_ed1:
            st.write("Ajustes Finais")
            nitidez = st.slider("Nitidez", 0.0, 5.0, 1.0)
            contraste = st.slider("Contraste (Melhora fundo branco)", 0.0, 3.0, 1.2)
            brilho = st.slider("Brilho", 0.0, 2.0, 1.0)
            giro = st.selectbox("Girar Imagem", [0, 90, 180, 270])
            
        img_editada = melhorar_imagem(image, nitidez, contraste, brilho)
        img_editada = img_editada.rotate(giro, expand=True)
        
        with col_ed2:
            st.image(img_editada, caption="Prévia do Documento", use_container_width=True)
            
        if st.button("💾 Salvar Versão Editada"):
            img_editada.save(os.path.join("arquivos", f"EDITADO_{selecionado}"))
            st.success("Salvo como 'EDITADO_...' na pasta de gestão!")
    else:
        st.info("Suba uma imagem (JPG/PNG) na aba de Envio para usar o editor.")
