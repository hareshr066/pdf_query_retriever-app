import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)  # 384 = vector dimension of MiniLM
doc_map = []

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_and_store(text, filename):
    chunks = chunk_text(text)
    vectors = model.encode(chunks)
    index.add(np.array(vectors))
    for i, chunk in enumerate(chunks):
        doc_map.append({"filename": filename, "chunk": chunk})
    return len(chunks)

def search_similar(query, top_k=3):
    q_vec = model.encode([query])
    distances, indices = index.search(np.array(q_vec), top_k)
    results = []
    for idx in indices[0]:
        if idx < len(doc_map):
            results.append(doc_map[idx])
    return results
