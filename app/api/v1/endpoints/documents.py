import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.api import deps
from app.schemas.user import User
from app.rag.loader import load_document
from app.rag.chunking import chunk_documents
from app.db.vector_store import get_vector_store
from typing import List
from app.schemas.document_info import DatabaseStats

router = APIRouter()

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Upload a document, process it, and store it in the vector database.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    # Create a temporary directory
    temp_dir = Path("temp_docs")
    temp_dir.mkdir(exist_ok=True)
    
    # Create unique temporary file path
    import uuid
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_file_path = temp_dir / unique_filename

    try:
        # Save the uploaded file temporarily
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Load the document
        docs = load_document(str(temp_file_path))
        if not docs:
            raise HTTPException(status_code=400, detail="Could not load document.")

        # 2. Chunk the document
        chunks = chunk_documents(docs)

        # 3. Store in vector database
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)

        return {"message": f"Document '{file.filename}' uploaded and processed successfully."}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and raise HTTP exception
        print(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up the temporary file
        try:
            if temp_file_path.exists() and temp_file_path.is_file():
                os.remove(temp_file_path)
        except Exception as cleanup_error:
            print(f"Warning: Could not clean up temporary file {temp_file_path}: {cleanup_error}")

@router.get("/database/stats", response_model=DatabaseStats)
def get_database_stats(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get relevant information about the vector database state.
    """
    vector_store = get_vector_store()
    
    # Get the underlying collection from ChromaDB
    collection = vector_store._collection
    
    # Get all documents from the collection
    try:
        documents = collection.get()
        total_chunks = len(documents["ids"]) if documents["ids"] else 0
        
        # Get embedding dimension if there are any embeddings
        embedding_dimension = 0
        if documents["embeddings"] and len(documents["embeddings"]) > 0:
            embedding_dimension = len(documents["embeddings"][0])
        
        # Count unique documents based on metadata source
        unique_sources = set()
        if documents["metadatas"]:
            for metadata in documents["metadatas"]:
                if metadata and "source" in metadata:
                    unique_sources.add(metadata["source"])
        
        stats = {
            "total_documents": len(unique_sources),
            "total_chunks": total_chunks,
            "embedding_dimension": embedding_dimension,
        }
    except Exception as e:
        # Handle empty collection or other errors
        stats = {
            "total_documents": 0,
            "total_chunks": 0,
            "embedding_dimension": 0,
        }
    
    return DatabaseStats(**stats)

@router.delete("/database/clear")
def clear_database(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Clear all documents from the vector database.
    """
    vector_store = get_vector_store()
    
    # Get the underlying collection and delete all documents
    collection = vector_store._collection
    try:
        # Get all document IDs first
        documents = collection.get()
        if documents["ids"]:
            # Delete all documents by their IDs
            collection.delete(ids=documents["ids"])
    except Exception as e:
        # Collection might be empty or not exist
        pass
    
    return {"message": "Vector database cleared successfully"}

@router.get("/list", response_model=List[str])
def list_documents(
    current_user: User = Depends(deps.get_current_user)
):
    """
    List all document names that have been uploaded.
    """
    vector_store = get_vector_store()
    
    # Get the underlying collection from ChromaDB
    collection = vector_store._collection
    document_names = set()
    
    try:
        # Get all documents from the collection
        documents = collection.get()
        
        if documents["metadatas"]:
            for metadata in documents["metadatas"]:
                if metadata and "source" in metadata:
                    # Extract just the filename from the path
                    filename = os.path.basename(metadata["source"])
                    document_names.add(filename)
    except Exception as e:
        # Handle empty collection or other errors
        pass
    
    return sorted(list(document_names))
