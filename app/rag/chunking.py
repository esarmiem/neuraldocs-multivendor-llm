from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


def chunk_documents(documents: List[Document]) -> List[Document]:
    """Splits a list of Documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_documents(documents)
