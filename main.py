import streamlit as st
import tempfile

from app.agent import create_agent
from app.models.embeddings import get_embeddings
from app.utils.rag_utils import load_pdf, create_vectorstore

st.set_page_config(layout="wide")

st.title("LexBot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload PDF
uploaded_file = st.file_uploader("Upload Legal PDF", type="pdf")

vectorstore = None

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    docs = load_pdf(file_path)
    embeddings = get_embeddings()
    vectorstore = create_vectorstore(docs, embeddings)

# Create agent
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(vectorstore)

# ONLY ONE INPUT (IMPORTANT)
user_input = st.chat_input("Ask your legal question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    response = st.session_state.agent.run(user_input)

    st.session_state.messages.append(("bot", response))

# Display chat
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)