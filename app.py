import streamlit as st
import fitz  # PyMuPDF
from pdf_extractor import extract_text_from_pdf
from chunker import chunk_text
from embedder import store_chunk_in_chroma
from qa_engine import get_qa_chain
import io

st.set_page_config(page_title="📄 PDF Chatbot", layout="wide")

# Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# Sidebar for file upload
with st.sidebar:
    st.markdown("## 📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and st.session_state.qa_chain is None:
        file_bytes = uploaded_file.read()  # ✅ Read once and reuse
        with st.spinner("Processing PDF..."):
            text = extract_text_from_pdf(io.BytesIO(file_bytes))
            if text.strip():
                chunks = chunk_text(text)
                vectordb = store_chunk_in_chroma(chunks)
                st.session_state.qa_chain = get_qa_chain(vectordb)
                st.success("PDF indexed! Start chatting below.")
            else:
                st.error("No text found in this PDF.")

# Full-width layout for chat UI
st.markdown("## 🤖 ASK ANYTHING TO YOUR PDF")
chat_container = st.container()

with chat_container:
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"<div style='text-align:right;   padding:8px; border-radius:10px; margin:5px 0;'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;  padding:8px; border-radius:10px; margin:5px 0;'><strong>Bot:</strong> {message}</div>", unsafe_allow_html=True)

# Bottom input area pinned using empty space
st.markdown("""
    <style>
        div.block-container { padding-top: 1rem; padding-bottom: 0rem; }
        .stTextInput > div > input {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

if st.session_state.qa_chain:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask something about the PDF:", key="input")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            with st.spinner("Thinking..."):
                response = st.session_state.qa_chain.invoke(user_input)
                answer = response["result"]

                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("AI", answer))
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Summarize this PDF"):
            st.session_state.chat_history.append(("You", "Summarize this document."))
            response = st.session_state.qa_chain.invoke("Summarize this document.")
            st.session_state.chat_history.append(("AI", response["result"]))
            st.rerun()
    with col2:
        if st.button("📌 What are the key points?"):
            st.session_state.chat_history.append(("You", "What are the key points in this document?"))
            response = st.session_state.qa_chain.invoke("What are the key points in this document?")
            st.session_state.chat_history.append(("AI", response["result"]))
            st.rerun()