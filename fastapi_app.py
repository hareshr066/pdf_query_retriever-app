from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pdf_parser import extract_text_from_pdf, embed_and_store, search_similar
import os

app = FastAPI()

# Enable CORS for frontend (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    content = extract_text_from_pdf(file_path)
    chunks_stored = embed_and_store(content, file.filename)
    return {"message": f"{file.filename} uploaded.", "chunks": chunks_stored}

@app.post("/ask-question")
async def ask_question(request: Request):
    body = await request.json()
    query = body.get("query")
    results = search_similar(query)
    return {"results": results}
