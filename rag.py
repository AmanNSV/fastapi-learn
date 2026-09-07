from fastapi import FastAPI, File, UploadFile, HTTPException
from rag_utils.genChunks import chunk_pdf

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "RAG"}

@app.post("/chunk-pdf")
async def chunking_PDF(file: UploadFile = File(...)):
    try:
        got_chunks = await chunk_pdf(file)
        if not got_chunks:
            raise HTTPException(detail="Error in chunking")
        return got_chunks
    finally:
        pass