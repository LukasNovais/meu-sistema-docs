import streamlit as st
import os
from PIL import Image, ImageEnhance
from fpdf import FPDF
import io

# Configuração da pasta e página
if not os.path.exists("meus_documentos"):
    os.makedirs("meus_documentos")

st.set_page_config(page_title="Transportadora Pro", layout="wide")

st.title("🚚 Sistema de Documentos Digital")

# Escolha do WhatsApp na barra lateral
st.sidebar.header("Configurações")
tipo_zap = st.sidebar.radio("Usar qual WhatsApp?", ["Normal", "Business"])
url_base_zap = "https://wa.me/" if tipo_zap == "Normal" else "https://api.whatsapp.com/send?phone="

aba = st.sidebar.radio("Navegação", ["📤 Enviar e Receber", "📂 Ver Meus Arquivos", "🛠️ Melhorar Foto e PDF"])

# --- ABA 1: ENVIO ---
if aba == "📤 Enviar e Receber":
    st.subheader("Enviar novo documento")
    u_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)
    
    if u_files:
        for f in u_files:
            # Salva o arquivo
            caminho_salvamento = os.path.join("meus_documentos", f.name)
            with open(caminho_salvamento, "wb") as m:
                m.write(f.getbuffer())
            
            # VISUALIZAÇÃO IMEDIATA
            st.write(f"✅ Arquivo: {f.name}")
            if f.type.startswith('image'):
                st.image(f, width=250)
            elif f.type == 'application/pdf':
                st.info("Arquivo PDF salvo com sucesso.")
        st.success("Tudo salvo na nuvem!")

# --- ABA 2: GESTÃO ---
elif aba == "📂 Ver Meus Arquivos":
    st.subheader("Documentos Armazenados")
    lista = os.listdir("meus_documentos")
    
    for item in lista:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            caminho = os.path.join("meus_documentos", item)
            extensao = item.split('.')[-1].lower()

            with col1:
                st.write(f"**{item}**")
                # MOSTRAR MINIATURA SE FOR IMAGEM
                if extensao in ['jpg', 'jpeg', 'png']:
                    st.image(caminho, width=150)
            
            with col2:
                # Botões de ação
                with open(caminho, "rb") as f_data:
                    st.download_button("📥 Baixar", f_data, file_name=item, key=f"dl_{item}")
                
                # Link do WhatsApp Dinâmico
                msg = f"Olá, segue o documento: {item}"
                link_final = f"{url_base_zap}&text={msg}"
                st.markdown(f"[📲 Enviar via Zap {tipo_zap}]({link_final})")
            
            with col3:
                if st.button("🗑️ Apagar", key=f"del_{item}"):
                    os.remove(caminho)
                    st.rerun()
            st.divider()

# --- ABA 3: MELHORAR E PDF ---
elif aba == "🛠️ Melhorar Foto e PDF":
    st.subheader("Tratamento de Documentos")
    foto = st.file_uploader("Carregue a foto do canhoto", type=['jpg', 'jpeg', 'png'])
    
    if foto:
        img = Image.open(foto)
        st.write("### Ajuste a Visualização:")
        
        c1, c2 = st.columns(2)
        with c1:
            n = st.slider("Nitidez (Deixar letras claras)", 1.0, 5.0, 2.0)
            c = st.slider("Contraste (Fundo Branco)", 1.0, 3.0, 1.5)
            # Mostrar a imagem enquanto ajusta
            img_edit = ImageEnhance.Sharpness(img).enhance(n)
            img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
            st.image(img_edit, caption="Prévia do Ajuste", use_container_width=True)
            
        with c2:
            if st.button("Converter para PDF e Salvar"):
                pdf
