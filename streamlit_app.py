import streamlit as st
import os
from pdf_parser import extract_text_from_pdf, embed_and_store, search_similar
import shutil

# File & folder paths
UPLOAD_FOLDER = "uploads"
INDEX_FILE = "vector.index"
DOC_MAP_FILE = "doc_map.pkl"

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set Streamlit page config
st.set_page_config(page_title="📄 PDF Query System", layout="centered")
st.title("📄 PDF Query Retrieval System (Free + Local)")

# Sidebar menu
menu = st.sidebar.radio("Choose Action", ["Upload PDF", "Ask a Question", "View Uploaded PDFs", "Reset App"])

# 1️⃣ Upload PDF
if menu == "Upload PDF":
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process and embed
        text = extract_text_from_pdf(file_path)
        num_chunks = embed_and_store(text, uploaded_file.name)
        st.success(f"✅ Uploaded and embedded: {uploaded_file.name} ({num_chunks} chunks)")

# 2️⃣ Ask Question
elif menu == "Ask a Question":
    query = st.text_input("Type your question")
    if st.button("Search"):
        if not query.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            results = search_similar(query)
            if results:
                st.subheader("🔍 Top Matches:")
                for i, res in enumerate(results):
                    st.markdown(f"**{i+1}. File:** `{res['filename']}`")
                    st.write(res['chunk'])
            else:
                st.warning("❌ No relevant chunks found.")

# 3️⃣ View Uploaded PDFs
elif menu == "View Uploaded PDFs":
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        st.info("ℹ️ No files uploaded yet.")
    else:
        st.subheader("📁 Uploaded Files:")
        for f in files:
            st.markdown(f"- `{f}`")

# 4️⃣ Reset App (Safe deletion)
elif menu == "Reset App":
    st.warning("⚠️ This will delete all uploaded files and embedded data.")
    if st.button("🔁 Reset Everything"):
        try:
            # Remove index and metadata
            if os.path.exists(INDEX_FILE):
                os.remove(INDEX_FILE)
            if os.path.exists(DOC_MAP_FILE):
                os.remove(DOC_MAP_FILE)

            # Safely delete files in uploads/
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    os.remove(file_path)
                except Exception as e:
                    st.warning(f"Could not delete {filename}: {e}")

            st.success("✅ All data has been reset.")
        except Exception as e:
            st.error(f"Error during reset: {e}")
