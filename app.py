import streamlit as st
import os

st.set_page_config(page_title="Sistema Transportadora", layout="wide")

st.title("📂 Meus Documentos")

# Pasta para salvar
if not os.path.exists("docs"):
    os.makedirs("docs")

# Envio rápido
arquivo = st.file_uploader("Enviar Arquivo", type=['pdf', 'png', 'jpg', 'csv', 'xml', 'xlsx'])
if arquivo:
    with open(os.path.join("docs", arquivo.name), "wb") as f:
        f.write(arquivo.getbuffer())
    st.success("Salvo!")

st.divider()

# Lista de arquivos
for item in os.listdir("docs"):
    col1, col2 = st.columns([4, 1])
    col1.write(f"📄 {item}")
    
    # Botão WhatsApp
    link_zap = f"https://wa.me/?text=Segue+documento:+{item}"
    col2.markdown(f"[📲 Zap]({link_zap})")
