from operator import itemgetter
import logging
from typing import Dict, Any, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.db.vector_store import get_vector_store
from app.rag.llm_factory import llm

# Configure logging
logger = logging.getLogger(__name__)

# Global variables for lazy initialization
_vectorstore = None
_retriever = None
_general_rag_chain = None
_delia_chain = None

# Configuration for DELIA agent
DELIA_CONFIG = {
    "max_context_length": 4000,
    "temperature": 0.1,  # Low temperature for consistent EDSL responses
    "max_tokens": 2000,
    "retrieval_k": 5,  # Number of documents to retrieve
}

def get_retriever():
    """Get retriever with lazy initialization."""
    global _vectorstore, _retriever
    
    if _retriever is None:
        try:
            _vectorstore = get_vector_store()
            _retriever = _vectorstore.as_retriever(
                search_kwargs={"k": DELIA_CONFIG["retrieval_k"]}
            )
            logger.info("Retriever initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize retriever: {e}")
            raise
    
    return _retriever

def validate_edsl_syntax(code: str) -> Dict[str, Any]:
    """
    Basic validation for EDSL syntax patterns.
    Returns validation results with suggestions.
    """
    validation_result = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    # Basic EDSL keyword validation
    edsl_keywords = [
        "IF", "THEN", "ELSE", "EVALUATE", "WHEN", "WHILE", "DO", 
        "REPEAT", "UNTIL", "IsNull", "Add", "element", "Set", "size",
        "Clear", "elements", "Size"
    ]
    
    # Check for common syntax issues
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//'):
            continue
            
        # Check for missing semicolons (common EDSL requirement)
        if line and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
            validation_result["warnings"].append(f"Line {i}: Consider adding semicolon at end")
    
    return validation_result

def format_edsl_response(response: str) -> str:
    """
    Format the response to ensure proper EDSL code blocks and structure.
    """
    # Ensure EDSL code blocks are properly formatted
    if "```edsl" not in response and "```" in response:
        # Replace generic code blocks with EDSL-specific ones
        response = response.replace("```", "```edsl")
    
    return response

# General RAG template (original functionality)
general_template = """
Answer the question based only on the following context:
{context}

Question: {question}

Answer in the original language of the question.
"""

# DELIA-specific template
delia_template = """
# DELIA - Asistente Experto en EDSL PowerCurve™

## 🔹 Situación
Eres DELIA (Delivery + IA), un asistente especializado en EDSL (Experian Domain Specific Language) dentro del ecosistema PowerCurve™, con enfoque principal en Strategy Management Design Studio (SDS) y Customer Management Design Studio (CMDS).

## 🔹 Tarea
Proporcionar asistencia experta en:
- Interpretación y explicación de sintaxis y funcionalidades de EDSL
- Validación y revisión de scripts EDSL existentes
- Generación de nuevos scripts conforme a los estándares
- Corrección y mejora de código entregado por los usuarios
- Sugerencias de parametrización y buenas prácticas de implementación

## 🔹 Objetivo
Garantizar máxima precisión, conformidad y claridad en la implementación de scripts EDSL, facilitando la comprensión, la calidad y el desarrollo de soluciones dentro del framework PowerCurve™.

## 🔹 Conocimientos Clave
Aplica estos conocimientos en tus respuestas:
- **Tipos de datos**: Numeric, Date, String, Boolean, Arrays (fijos y dinámicos), Logical Data Models (LDMs)
- **Operadores**: Aritméticos, Lógicos, Comparación, con atención a su precedencia:
  - Aritméticos: Brackets > Multiply > Divide > Percent > Add > Subtract
  - Lógicos: Not > And > Or
- **Estructuras de control**: IF, IF THEN ELSE, EVALUATE WHEN, WHILE DO, REPEAT UNTIL
- **Funciones**: Arrays, matemáticas, estadísticas, fechas, texto y otras
- **Sintaxis**: Reglas de sintaxis, notación punto ('LDS.Child.Characteristic') y manejo de índices en arrays
- **Arrays dinámicos**: Add element, Set size, Clear elements, Size
- **Validación**: Control de errores, comprobación con IsNull antes de operar sobre datos potencialmente nulos

## 🔹 Instrucciones Críticas
1. **Validar rigurosamente** la sintaxis y estructura de cualquier script recibido
2. **Detectar errores** o inconsistencias y proponer correcciones detalladas
3. **Reescribir scripts** corregidos manteniendo el propósito original cuando corresponda
4. **Proporcionar sugerencias** de mejora y optimización técnica:
   - Validación de valores nulos
   - Parametrización de longitud de campos y arrays
   - Claridad en precedencia de operadores
   - Comentarios explicativos
5. **Solicitar aclaraciones** ante ambigüedades o información incompleta
6. **Adaptar el nivel** de explicación según el conocimiento del usuario (básico, intermedio, avanzado)
7. **Usar bloques de código** etiquetados con 'edsl'
8. **Referenciar secciones** del EDSL User Guide cuando aplique

## 🔹 Validación de Sintaxis y Terminología
- **Verificar que todas las palabras reservadas** coincidan textualmente con la documentación oficial
- **No adaptar, traducir, inventar o modificar** palabras reservadas
- **Mostrar referencias exactas** de la sección del documento donde se valida la sintaxis
- **Evitar confusiones** con sintaxis de otros lenguajes

## 🔹 Restricciones
- No asumir información no proporcionada por el usuario
- Mantener estricta adherencia a las especificaciones oficiales de EDSL
- Priorizar claridad, precisión técnica y consistencia
- Evitar incluir sintaxis de otros lenguajes de programación

## 🔹 Formato de Respuesta
- Código EDSL corregido dentro de bloques etiquetados 'edsl'
- Explicaciones claras y concisas de cada cambio o mejora
- Viñetas con sugerencias de parametrización o buenas prácticas
- Referencias al documento guía si corresponde
- Opción de solicitar confirmación antes de aplicar cambios mayores

## 🔹 Contexto Disponible
{context}

## 🔹 Pregunta del Usuario
{question}

Responde en el idioma original de la pregunta, aplicando todas las instrucciones anteriores.
"""

# Create prompts
general_prompt = ChatPromptTemplate.from_template(general_template)
delia_prompt = ChatPromptTemplate.from_template(delia_template)

def get_general_rag_chain():
    """Get general RAG chain with lazy initialization."""
    global _general_rag_chain
    
    if _general_rag_chain is None:
        try:
            retriever = get_retriever()
            _general_rag_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | general_prompt
                | llm
                | StrOutputParser()
            )
            logger.info("General RAG chain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize general RAG chain: {e}")
            raise
    
    return _general_rag_chain

def get_delia_chain():
    """Get DELIA-specific chain with lazy initialization."""
    global _delia_chain
    
    if _delia_chain is None:
        try:
            retriever = get_retriever()
            _delia_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | delia_prompt
                | llm
                | StrOutputParser()
            )
            logger.info("DELIA chain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DELIA chain: {e}")
            raise
    
    return _delia_chain

def query_delia(question: str, user_level: str = "intermediate") -> Dict[str, Any]:
    """
    Enhanced query function for DELIA with additional context and validation.
    
    Args:
        question: User's question about EDSL
        user_level: User's expertise level (basic, intermediate, advanced)
    
    Returns:
        Dictionary containing response, validation results, and metadata
    """
    try:
        # Get the DELIA chain
        chain = get_delia_chain()
        
        # Add user level context to the question
        enhanced_question = f"[User Level: {user_level}] {question}"
        
        # Get response
        response = chain.invoke(enhanced_question)
        
        # Format response
        formatted_response = format_edsl_response(response)
        
        # Extract EDSL code from response for validation
        import re
        edsl_code_blocks = re.findall(r'```edsl\n(.*?)\n```', formatted_response, re.DOTALL)
        
        validation_results = []
        for code_block in edsl_code_blocks:
            validation_results.append(validate_edsl_syntax(code_block))
        
        return {
            "response": formatted_response,
            "validation_results": validation_results,
            "user_level": user_level,
            "has_edsl_code": len(edsl_code_blocks) > 0,
            "edsl_code_blocks_count": len(edsl_code_blocks)
        }
        
    except Exception as e:
        logger.error(f"Error in DELIA query: {e}")
        return {
            "error": str(e),
            "response": "Lo siento, hubo un error procesando tu consulta. Por favor, intenta de nuevo.",
            "validation_results": [],
            "user_level": user_level,
            "has_edsl_code": False,
            "edsl_code_blocks_count": 0
        }

# For backward compatibility - this now returns the GENERAL RAG chain
def get_rag_chain():
    """Get general RAG chain (backward compatibility)."""
    return get_general_rag_chain()

# For backward compatibility
rag_chain = get_rag_chain
