from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.chain import get_rag_chain

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Chat endpoint to interact with the RAG chain.
    """
    chain = get_rag_chain()
    answer = chain.invoke(request.question)
    return {"answer": answer}
