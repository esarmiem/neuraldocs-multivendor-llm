from typing import List
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    TextLoader,
    JSONLoader,
    UnstructuredExcelLoader,
)
from langchain.schema import Document

DOCUMENT_LOADERS = {
    ".pdf": UnstructuredPDFLoader,
    ".txt": TextLoader,
    ".json": JSONLoader,
    ".xlsx": UnstructuredExcelLoader,
}

def load_document(file_path: str) -> List[Document]:
    """Loads a document from a file path and returns a list of Documents."""
    extension = f".{file_path.split('.')[-1]}"
    if extension not in DOCUMENT_LOADERS:
        raise ValueError(f"Unsupported file extension: {extension}")

    loader = DOCUMENT_LOADERS[extension](file_path)
    return loader.load()
