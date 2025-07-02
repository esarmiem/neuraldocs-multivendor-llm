from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.db.vector_store import get_vector_store
from app.rag.llm_factory import llm

# Global variables for lazy initialization
_vectorstore = None
_retriever = None
_rag_chain = None

def get_retriever():
    """Get retriever with lazy initialization."""
    global _vectorstore, _retriever
    
    if _retriever is None:
        _vectorstore = get_vector_store()
        _retriever = _vectorstore.as_retriever()
    
    return _retriever

template = """
Answer the question based only on the following context:
{context}

Question: {question}

Answer in the original language of the question.
"""
prompt = ChatPromptTemplate.from_template(template)

def get_rag_chain():
    """Get RAG chain with lazy initialization."""
    global _rag_chain
    
    if _rag_chain is None:
        retriever = get_retriever()
        _rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    
    return _rag_chain

# For backward compatibility
rag_chain = get_rag_chain
