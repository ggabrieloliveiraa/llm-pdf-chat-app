import os, tempfile
import streamlit as st
from pathlib import Path
Path("docs").mkdir(exist_ok=True) 

from app.ingest import ingest
from app.chat_chain import make_chain
from app.settings import settings  # garante env vars

# --- Inicializa cadeia de chat ---
chain = make_chain()

st.set_page_config(page_title="PDF Chat (Gemini)")
st.title("Chat com seus PDFs")

# ----------------------- Upload --------------------------------------------
if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = set()   # guarda nomes já indexados

uploaded_file = st.file_uploader("Envie um PDF para indexar", type=["pdf"])
if uploaded_file is not None:
    if uploaded_file.name in st.session_state.ingested_files:
        st.info(f"**{uploaded_file.name}** já está indexado.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = Path(tmp.name)
        dest = Path("docs") / uploaded_file.name
        dest.write_bytes(tmp_path.read_bytes())
        ingest("docs")
        st.session_state.ingested_files.add(uploaded_file.name)
        st.success(f"**{uploaded_file.name}** indexado!")

st.divider()

# ----------------------- Chat ----------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # [(user, assistant), ...]

question = st.text_input("Pergunte algo sobre o(s) PDF(s):", key="chat_input")
if st.button("Enviar") or question:
    if question:
        # exibe pergunta no chat
        st.write(f"**Você:** {question}")
        # chama cadeia
        answer = chain({"question": question, "chat_history": st.session_state.history})["answer"]
        st.session_state.history.append((question, answer))
        st.write(f"**Bot:** {answer}")