# DELIA Integration - Dual RAG System

## Overview

Este proyecto ahora soporta **dos modos de operación** para el sistema RAG:

1. **RAG General** - Funcionalidad original para consultas generales
2. **DELIA** - Asistente experto especializado en EDSL PowerCurve™

## Arquitectura

### Estructura de Cadenas RAG

```python
# Cadenas separadas para diferentes propósitos
_general_rag_chain = None  # Para consultas generales
_delia_chain = None        # Para consultas específicas de EDSL
```

### Prompts Separados

- **`general_template`**: Prompt simple para consultas generales
- **`delia_template`**: Prompt completo con instrucciones específicas de EDSL

## Endpoints Disponibles

### 1. Chat General (Backward Compatible)

**Endpoint:** `POST /api/v1/chat/`

**Uso:** Consultas generales sobre documentos cargados

```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué información puedes encontrar sobre...?"}'
```

**Respuesta:**
```json
{
  "answer": "Respuesta general basada en el contexto..."
}
```

### 2. DELIA - Asistente EDSL

**Endpoint:** `POST /api/v1/chat/delia`

**Uso:** Consultas específicas sobre EDSL PowerCurve™

```bash
curl -X POST "http://localhost:8000/api/v1/chat/delia" \
  -H "Authorization: Bearer tu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Revisa este código EDSL: IF x > 10 THEN y = 20",
    "user_level": "basic"
  }'
```

**Respuesta:**
```json
{
  "response": "Respuesta especializada de DELIA...",
  "validation_results": [
    {
      "is_valid": true,
      "errors": [],
      "warnings": ["Line 1: Consider adding semicolon at end"],
      "suggestions": []
    }
  ],
  "user_level": "basic",
  "has_edsl_code": true,
  "edsl_code_blocks_count": 1,
  "error": null
}
```

## Funciones Disponibles

### Para Uso General

```python
from app.rag.chain import get_rag_chain

# Obtener cadena RAG general
chain = get_rag_chain()
response = chain.invoke("Tu pregunta general")
```

### Para Uso con DELIA

```python
from app.rag.chain import query_delia

# Consulta especializada con DELIA
result = query_delia(
    question="Revisa este código EDSL...",
    user_level="intermediate"  # basic, intermediate, advanced
)

print(result["response"])
print(f"Validaciones: {result['validation_results']}")
```

## Configuración

### Configuración de DELIA

```python
DELIA_CONFIG = {
    "max_context_length": 4000,
    "temperature": 0.1,  # Respuestas consistentes
    "max_tokens": 2000,
    "retrieval_k": 5,  # Documentos a recuperar
}
```

### Niveles de Usuario

- **`basic`**: Explicaciones detalladas, conceptos fundamentales
- **`intermediate`**: Explicaciones balanceadas, ejemplos prácticos
- **`advanced`**: Respuestas concisas, optimizaciones avanzadas

## Características de DELIA

### ✅ Validación de Sintaxis EDSL
- Detección de palabras reservadas
- Verificación de estructura de código
- Sugerencias de mejora

### ✅ Formateo Automático
- Bloques de código etiquetados como `edsl`
- Estructura de respuesta consistente

### ✅ Manejo de Errores
- Logging detallado
- Respuestas de error amigables
- Validación de entrada

### ✅ Metadata Enriquecida
- Conteo de bloques de código EDSL
- Resultados de validación
- Nivel de usuario aplicado

## Migración y Compatibilidad

### ✅ Sin Cambios Requeridos
- El endpoint `/api/v1/chat/` funciona exactamente igual
- Todas las integraciones existentes siguen funcionando
- No hay breaking changes

### ✅ Nuevas Funcionalidades
- Endpoint `/api/v1/chat/delia` para consultas especializadas
- Funciones `query_delia()` para uso programático
- Schemas extendidos para respuestas enriquecidas

## Ejemplos de Uso

### Consulta General
```python
# Mantiene funcionalidad original
response = chain.invoke("¿Qué documentos tienes sobre machine learning?")
```

### Consulta EDSL Básica
```python
result = query_delia(
    "¿Qué es EDSL?",
    user_level="basic"
)
```

### Consulta EDSL Avanzada
```python
result = query_delia(
    "Optimiza este script EDSL: [código complejo]",
    user_level="advanced"
)
```

### Validación de Código
```python
result = query_delia(
    "Revisa la sintaxis de: IF x > 10 THEN y = 20",
    user_level="intermediate"
)

if result["validation_results"]:
    for validation in result["validation_results"]:
        if validation["warnings"]:
            print("Advertencias:", validation["warnings"])
```

## Ventajas de esta Arquitectura

1. **✅ Compatibilidad Total**: No rompe funcionalidad existente
2. **✅ Separación Clara**: Cada cadena tiene su propósito específico
3. **✅ Escalabilidad**: Fácil agregar más especializaciones
4. **✅ Mantenibilidad**: Código organizado y bien documentado
5. **✅ Flexibilidad**: Usuarios pueden elegir el nivel de especialización

## Próximos Pasos

1. **Testing**: Verificar que ambos endpoints funcionen correctamente
2. **Documentación**: Actualizar README con nuevos endpoints
3. **Frontend**: Integrar endpoint de DELIA en la interfaz de usuario
4. **Monitoreo**: Agregar métricas específicas para cada tipo de consulta 