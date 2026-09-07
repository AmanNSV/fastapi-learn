from fastapi import HTTPException
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("Not able to get the LLM key")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=gemini_api_key
)

async def gen_embedding(chunks: List) -> List[dict]:

    try:

        # Extract only text for embedding
        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        generated_embeddings = await embeddings_model.aembed_documents(texts)

        response_data = []

        for index, chunk in enumerate(chunks):

            response_data.append({
                "chunk_index": index,
                "page_content": chunk.page_content,
                "metadata": chunk.metadata,
                "embedding": generated_embeddings[index]
            })
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )