import streamlit as st
import os
from PIL import Image, ImageEnhance
from fpdf import FPDF
import io
from streamlit_drawable_canvas import st_canvas

if not os.path.exists("meus_documentos"):
    os.makedirs("meus_documentos")

st.set_page_config(page_title="Transportadora Pro", layout="wide")

# --- CONFIGURAÇÃO WHATSAPP ---
st.sidebar.header("Configurações")
tipo_zap = st.sidebar.radio("Enviar por onde?", ["WhatsApp Pessoal", "WhatsApp Business (Web)"])

# Ajuste para evitar múltiplas abas no navegador
target = "_self" if tipo_zap == "WhatsApp Business (Web)" else "_blank"
url_base = "https://web.whatsapp.com/send?text=" if "Business" in tipo_zap else "https://wa.me/?text="

aba = st.sidebar.radio("Navegação", ["📤 Enviar e Receber", "📂 Ver Meus Arquivos", "🛠️ Melhorar Foto/PDF", "✍️ Assinar Documento"])

# --- ABA 1 e 2 (Mantidas as funcionalidades anteriores) ---
if aba == "📤 Enviar e Receber":
    st.subheader("Enviar novo documento")
    u_files = st.file_uploader("Selecione os arquivos", accept_multiple_files=True)
    if u_files:
        for f in u_files:
            with open(os.path.join("meus_documentos", f.name), "wb") as m:
                m.write(f.getbuffer())
        st.success("✅ Salvo!")

elif aba == "📂 Ver Meus Arquivos":
    st.subheader("Documentos Armazenados")
    for item in os.listdir("meus_documentos"):
        with st.expander(f"📄 {item}"):
            caminho = os.path.join("meus_documentos", item)
            col1, col2 = st.columns([3, 1])
            with col1:
                if item.lower().endswith(('png', 'jpg', 'jpeg')): st.image(caminho, width=300)
                else: st.write("Visualização indisponível.")
            with col2:
                with open(caminho, "rb") as f:
                    st.download_button("📥 Baixar", f, file_name=item, key=f"dl_{item}")
                msg = f"Segue o documento: {item}"
                # O segredo para não abrir várias abas no Business Web é o target="_self"
                st.markdown(f'<a href="{url_base}{msg}" target="{target}"><button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%;">📲 Enviar Zap</button></a>', unsafe_allow_html=True)
                if st.button("🗑️ Apagar", key=f"del_{item}"):
                    os.remove(caminho)
                    st.rerun()

# --- ABA 3 (Melhorar Foto) ---
elif aba == "🛠️ Melhorar Foto/PDF":
    st.subheader("Tratamento de Documentos")
    foto = st.file_uploader("Carregue a foto", type=['jpg', 'jpeg', 'png'])
    if foto:
        img = Image.open(foto)
        n = st.slider("Nitidez", 1.0, 5.0, 2.0)
        c = st.slider("Contraste", 1.0, 3.0, 1.5)
        img_edit = ImageEnhance.Sharpness(img).enhance(n)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(c)
        st.image(img_edit, width=400)
        if st.button("Salvar como PDF"):
            pdf = FPDF(); pdf.add_page()
            img_edit.save("temp.jpg"); pdf.image("temp.jpg", 10, 10, 190)
            pdf.output(os.path.join("meus_documentos", foto.name.split('.')[0] + ".pdf"))
            st.success("✅ PDF Criado!")

# --- NOVA ABA: ASSINATURA ---
elif aba == "✍️ Assinar Documento":
    st.subheader("Assinatura Digital (Desenhe abaixo)")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#eeeeee",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("Salvar Assinatura"):
        if canvas_result.image_data is not None:
            img_as = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            img_as.save(os.path.join("meus_documentos", "assinatura.png"))
            st.success("✅ Assinatura salva como 'assinatura.png' em seus arquivos!")
