import streamlit as st
import os
from PIL import Image, ImageEnhance
from fpdf import FPDF
import io

# Criar pasta de documentos se não existir
if not os.path.exists("meus_documentos"):
    os.makedirs("meus_documentos")

st.set_page_config(page_title="Transportadora Pro", layout="wide")

st.title("🚚 Sistema de Documentos Digital")

# Menu Simples
aba = st.sidebar.radio("O que deseja fazer?", ["📤 Enviar e Receber", "📂 Ver Meus Arquivos", "🛠️ Melhorar Foto e Criar PDF"])

# --- ABA 1: ENVIO ---
if aba == "📤 Enviar e Receber":
    st.subheader("Enviar novo documento")
    u_files = st.file_uploader("Escolha os arquivos (Fotos ou PDF)", accept_multiple_files=True)
    
    if u_files:
        for f in u_files:
            with open(os.path.join("meus_documentos", f.name), "wb") as m:
                m.write(f.getbuffer())
        st.success("✅ Arquivos salvos no seu servidor!")

# --- ABA 2: GESTÃO ---
elif aba == "📂 Ver Meus Arquivos":
    st.subheader("Documentos na sua Nuvem")
    lista = os.listdir("meus_documentos")
    
    if not lista:
        st.info("Sua pasta está vazia.")
    
    for item in lista:
        col1, col2, col3 = st.columns([3, 1, 1])
        caminho = os.path.join("meus_documentos", item)
        
        col1.write(f"📄 {item}")
        
        with open(caminho, "rb") as file_data:
            col2.download_button("📥 Baixar", file_data, file_name=item, key=f"dl_{item}")
            
        if col3.button("🗑️ Apagar", key=f"del_{item}"):
            os.remove(caminho)
            st.rerun()
            
        # Botão WhatsApp
        msg = f"Olá, segue documento: {item}"
        st.markdown(f"[📲 Enviar pelo WhatsApp](https://wa.me/?text={msg})")
        st.divider()

# --- ABA 3: MELHORAR E PDF ---
elif aba == "🛠️ Melhorar Foto e Criar PDF":
    st.subheader("Transformar Foto em Documento Profissional")
    foto = st.file_uploader("Carregue a foto do canhoto ou nota", type=['jpg', 'jpeg', 'png'])
    
    if foto:
        img = Image.open(foto)
        
        # Ajustes automáticos de nitidez
        st.write("Ajuste a imagem para ficar legível:")
        n = st.slider("Nitidez (Foco)", 1.0, 5.0, 2.5)
        c = st.slider("Contraste (Fundo branco)", 1.0, 3.0, 1.5)
        
        img_edit = ImageEnhance.Sharpness(img).enhance(n)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
        
        st.image(img_edit, width=400)
        
        if st.button("Convertar para PDF e Salvar"):
            pdf = FPDF()
            pdf.add_page()
            # Salva temp para o PDF
            img_edit.save("temp.jpg")
            pdf.image("temp.jpg", 0, 0, 210, 297) # Tamanho A4
            
            nome_pdf = foto.name.split('.')[0] + ".pdf"
            pdf.output(os.path.join("meus_documentos", nome_pdf))
            st.success(f"✅ Convertido em PDF e salvo como {nome_pdf}!")
