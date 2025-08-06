# backend/api/rag.py

from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel, Field
from ..rag_chain import query_rag_chain # Gerçek RAG zincirimizi import edelim

router = APIRouter()

class RagQueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="The user's question for the RAG chain.")

class RagQueryResponse(BaseModel):
    answer: str
    # source_info: list[str] # Şimdilik kaynak bilgisi olmadan devam edelim

@router.post(
    "/query",
    response_model=RagQueryResponse,
    summary="Query the RAG chain",
    description="Sends a question to the RAG chain and gets an answer based on the knowledge base."
)
async def query_rag(request: RagQueryRequest = Body(...)):
    """
    Kullanıcının sorusunu RAG zincirine gönderir ve bilgi bankasına dayalı bir cevap alır.
    """
    try:
        print(f"RAG zinciri için sorgu alındı: '{request.question}'")
        answer_text = await query_rag_chain(request.question)
        
        print(f"RAG zincirinden cevap alındı: '{answer_text[:100]}...'")
        
        return {"answer": answer_text}
    except Exception as e:
        print(f"RAG ENDPOINT HATASI: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while querying the RAG chain."
        )
