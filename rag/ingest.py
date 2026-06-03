from PyPDF2 import PdfReader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from sentence_transformers import SentenceTransformer

import chromadb

import os
# =========================================
# READ PDFS
# =========================================

folder_path = "../knowledge_base"

all_text = ""

for file in os.listdir(folder_path):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(
            folder_path,
            file
        )

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            text = page.extract_text()

            if text:

                all_text += text

# =========================================
# CHUNK TEXT
# =========================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50
)

chunks = splitter.split_text(all_text)

print(f"Total Chunks: {len(chunks)}")

# =========================================
# CREATE EMBEDDINGS
# =========================================

embedding_model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

# =========================================
# CHROMADB
# =========================================

client = chromadb.PersistentClient(
    path="../vector_db"
)

collection = client.get_or_create_collection(
    name="factorymind_docs"
)

# =========================================
# STORE CHUNKS
# =========================================

for i, chunk in enumerate(chunks):

    embedding = embedding_model.encode(
        chunk
    ).tolist()

    collection.add(

        ids=[str(i)],

        embeddings=[embedding],

        documents=[chunk]
    )

print("✅ PDFs converted into AI knowledge base")