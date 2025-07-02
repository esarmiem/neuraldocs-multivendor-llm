from pydantic import BaseModel

class DatabaseStats(BaseModel):
    total_documents: int
    total_chunks: int
    embedding_dimension: int