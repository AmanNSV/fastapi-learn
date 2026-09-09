import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

from langchain_postgres import PGVector
from rag_utils.genEmbed import embeddings_model
from rag_utils.dbConnect import db_url

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


async def retrieve_documents(query: str):

    vector_store = PGVector(
        embeddings=embeddings_model,
        collection_name="documents",
        connection=db_url,
        use_jsonb=True,
    )

    results = vector_store.similarity_search(
        query,
        k=5
    )

    return results


async def gen_ai_res(query: str):

    # --------------------------------
    # 1. Retrieve relevant documents
    # --------------------------------

    retrieved_docs = await retrieve_documents(query)

    if not retrieved_docs:
        return None

    # --------------------------------
    # 2. Build context
    # --------------------------------

    context_parts = []

    for index, doc in enumerate(retrieved_docs):

        page = doc.metadata.get("page", "Unknown")

        context_parts.append(
            f"""
            SOURCE {index + 1}
            PAGE: {page}

            {doc.page_content}
            """
        )

    context = "\n".join(context_parts)

    # --------------------------------
    # 3. Build prompt
    # --------------------------------

    prompt = f"""
            You are a helpful question-answering assistant.

            Answer the user's question using ONLY the information provided
            in the context below.

            If the answer cannot be found in the context, say:
            "I could not find the answer in the provided documents."

            Do not make up information.

            USER QUESTION:
            {query}

            CONTEXT:
            {context}

            ANSWER:
            """

    # --------------------------------
    # 4. Send to Gemini
    # --------------------------------

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    # --------------------------------
    # 5. Return Gemini answer
    # --------------------------------

    return {
        "question": query,
        "answer": response.text,
        "sources": [
            {
                "page": doc.metadata.get("page"),
                "content": doc.page_content
            }
            for doc in retrieved_docs
        ]
    }