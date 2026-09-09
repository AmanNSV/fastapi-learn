from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from rag_utils.genChunks import chunk_pdf
from rag_utils.dbConnect import db_connection
from rag_utils.genAIRes import gen_ai_res
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "RAG"}

@app.post("/chunk-pdf")
async def chunking_PDF(file: UploadFile = File(...), db: Session = Depends(db_connection)):
    try:
        got_chunks = await chunk_pdf(file, db)
        if not got_chunks:
            raise HTTPException(detail="Error in chunking")
        return got_chunks
    finally:
        pass

@app.post("/ask")
async def user_query(query: str):

    ai_res = await gen_ai_res(query)

    if not ai_res:
        raise HTTPException(
            detail="Not able to get gen_ai_res",
            status_code=500
        )

    return ai_res