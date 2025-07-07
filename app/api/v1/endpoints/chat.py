from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.user import User
from app.schemas.chat import ChatRequest, ChatResponse, DeliaRequest, DeliaResponse
from app.rag.chain import get_rag_chain, query_delia

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    General chat endpoint to interact with the RAG chain.
    This endpoint maintains backward compatibility and provides general RAG functionality.
    """
    chain = get_rag_chain()
    answer = chain.invoke(request.question)
    return {"answer": answer}

@router.post("/delia", response_model=DeliaResponse)
def delia_endpoint(
    request: DeliaRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    DELIA-specific endpoint for EDSL PowerCurve™ expert assistance.
    This endpoint provides specialized EDSL validation, correction, and guidance.
    """
    result = query_delia(
        question=request.question,
        user_level=request.user_level
    )
    return DeliaResponse(**result)
