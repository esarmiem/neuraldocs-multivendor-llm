import chromadb
from langchain_chroma import Chroma

from app.core.config import settings
from app.rag.embeddings_factory import get_embeddings

# Global variable to store the vector store instance
_vector_store = None

def get_vector_store() -> Chroma:
    """Returns the Chroma vector store instance using lazy initialization."""
    global _vector_store
    
    if _vector_store is None:
        # Initialize ChromaDB client - using PersistentClient to avoid timeout issues
        try:
            # Use PersistentClient for local storage instead of HttpClient
            client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=chromadb.Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            
            # Initialize embeddings using the factory
            embeddings = get_embeddings()
            
            # Initialize Chroma vector store
            _vector_store = Chroma(
                client=client,
                collection_name="rag_collection",
                embedding_function=embeddings,
            )
        except Exception as e:
            print(f"Failed to connect to ChromaDB: {e}")
            print(f"Trying to connect to {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
            raise
    
    return _vector_store
