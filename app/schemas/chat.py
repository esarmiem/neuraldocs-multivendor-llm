from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    # sources: list[dict] # To be added later

class DeliaRequest(BaseModel):
    question: str
    user_level: str = "intermediate"  # basic, intermediate, advanced

class DeliaResponse(BaseModel):
    response: str
    validation_results: List[Dict[str, Any]]
    user_level: str
    has_edsl_code: bool
    edsl_code_blocks_count: int
    error: Optional[str] = None
