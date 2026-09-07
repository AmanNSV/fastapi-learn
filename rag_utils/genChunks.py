from fastapi import HTTPException

import shutil
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_utils.genEmbed import gen_embedding

async def chunk_pdf(file):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDFs are allowed."
        )

    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Load PDF
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()

        # 2. Chunk PDF
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        chunks = text_splitter.split_documents(docs)

        print("Successfully Created Chunks")

        # 3. Generate embeddings
        embeds = await gen_embedding(chunks)

        if not embeds:
            raise HTTPException(detail="Not able to gen embeds")

        return {
            "filename": file.filename,
            "total_chunks": len(chunks),
            # "embeds": embeds
        }

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

