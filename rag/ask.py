
# rag/ask.py

from fastapi import FastAPI
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer

import chromadb

from openai import OpenAI

from dotenv import load_dotenv

import os

# =====================================================
# LOAD ENV VARIABLES
# =====================================================

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(

    title="FactoryMind AI Copilot",

    description="Industrial RAG AI System",

    version="1.0"
)

# =====================================================
# OPENROUTER CLIENT
# =====================================================

client_llm = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=OPENROUTER_API_KEY
)

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================================
# LOAD CHROMADB
# =====================================================

client_db = chromadb.PersistentClient(
    path="../vector_db"
)

collection = client_db.get_collection(
    name="factorymind_docs"
)

print("\n🏭 FactoryMind AI Copilot API Ready\n")

# =====================================================
# INPUT SCHEMA
# =====================================================

class QueryInput(BaseModel):

    question: str

# =====================================================
# HOME ROUTE
# =====================================================

@app.get("/")

def home():

    return {

        "message":
        "FactoryMind AI Copilot Running Successfully"
    }

# =====================================================
# ASK API
# =====================================================

@app.post("/ask")

def ask_question(data: QueryInput):

    query = data.question

    # =================================================
    # QUERY EMBEDDING
    # =================================================

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    # =================================================
    # SEARCH RELEVANT PDF CHUNKS
    # =================================================

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=5
    )

    retrieved_docs = results["documents"][0]

    # =================================================
    # COMBINE PDF CONTEXT
    # =================================================

    context = "\n\n".join(retrieved_docs)

    # =================================================
    # PROMPT
    # =================================================

    prompt = f"""
You are FactoryMind AI,
an Industrial Predictive Maintenance Expert.

Use the industrial PDF context below
to answer the user's question professionally.

IMPORTANT RULES:

1. Primarily use the PDF context.
2. If exact information is unavailable,
provide the best industrial reasoning.
3. Never say:
'Information not found in industrial documents.'
4. Always provide a useful technical answer.
5. Explain professionally.

INDUSTRIAL PDF CONTEXT:
{context}

USER QUESTION:
{query}

Provide answer in this format:

1. Problem Explanation
2. Possible Causes
3. Recommended Maintenance
4. Prevention Strategy
"""

    # =================================================
    # LLM RESPONSE
    # =================================================

    response = client_llm.chat.completions.create(

        model="meta-llama/llama-3-8b-instruct",

        messages=[

            {
                "role": "system",

                "content":
                "You are an industrial AI maintenance expert."
            },

            {
                "role": "user",

                "content": prompt
            }
        ],

        temperature=0.3,

        max_tokens=700
    )

    # =================================================
    # FINAL ANSWER
    # =================================================

    answer = response.choices[0].message.content

    print("\n" + "="*80)

    print("\nQUESTION:\n")

    print(query)

    print("\nANSWER:\n")

    print(answer)

    print("\n" + "="*80)

    # =================================================
    # RETURN RESPONSE
    # =================================================

    return {

        "question": query,

        "answer": answer,

        "retrieved_docs": retrieved_docs
    }

# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "ask:app",

        host="127.0.0.1",

        port=9000,

        reload=True
    )

