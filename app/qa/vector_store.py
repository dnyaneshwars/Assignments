# app/qa/vector_store.py
from openai import OpenAI
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from typing import List
import os

openai_client = OpenAI(api_key="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")

chroma_client = chromadb.Client()
embedding_function = OpenAIEmbeddingFunction(
    api_key="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",
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    name="qa_chunks",
    embedding_function=embedding_function
)

def split_text(text: str, max_tokens=200) -> List[str]:
    return [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]

def create_vector_store(text: str):
    chunks = split_text(text)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)

def query_vector_store(question: str) -> str:
    results = collection.query(query_texts=[question], n_results=3)
    top_chunks = results["documents"][0]

    prompt = f"Answer this question: {question}\n\nContext:\n" + "\n".join(top_chunks)
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You answer questions from context."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
