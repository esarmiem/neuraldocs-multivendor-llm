# Colección Postman - RAG App API

## Descripción General

Esta colección de Postman incluye todos los endpoints de la aplicación RAG con soporte para:

1. **RAG General** - Consultas generales sobre documentos
2. **DELIA** - Asistente especializado en EDSL PowerCurve™

## Configuración Inicial

### 1. Variables de Entorno

La colección utiliza las siguientes variables:

- **`base_url`**: URL base de la API (por defecto: `http://localhost:8000`)
- **`access_token`**: Token de autenticación (se establece automáticamente)

### 2. Autenticación

Antes de usar cualquier endpoint, debes obtener un token de acceso:

1. Ejecuta la petición **"Obtener Token"** en la carpeta **Autenticación**
2. El token se guardará automáticamente en la variable `access_token`
3. Todas las demás peticiones usarán este token automáticamente

## Estructura de la Colección

### 📁 Autenticación
- **Obtener Token**: Obtiene el token JWT para autenticación

### 📁 Documentos
- **Subir Documento**: Carga archivos para procesamiento RAG
- **Obtener Estado de Base de Datos**: Estadísticas de la base vectorial
- **Limpiar Base de Datos**: Elimina todos los documentos
- **Listar Documentos**: Lista documentos cargados

### 📁 Chat General
- **Realizar Consulta General**: Consultas generales sobre documentos
- **Consulta sobre Documentos Específicos**: Ejemplo de consulta específica

### 📁 DELIA - Asistente EDSL
- **Consulta Básica EDSL**: Explicaciones para principiantes
- **Validación de Código EDSL**: Revisión y corrección de código
- **Generación de Código EDSL**: Creación de scripts con buenas prácticas
- **Optimización Avanzada EDSL**: Optimizaciones para usuarios avanzados
- **Corrección de Errores EDSL**: Corrección de sintaxis
- **Consulta sobre Arrays EDSL**: Manejo de arrays dinámicos

## Uso de los Endpoints

### 🔍 Chat General

**Endpoint:** `POST /api/v1/chat/`

**Uso:** Para consultas generales sobre los documentos cargados en el sistema RAG.

**Ejemplo de petición:**
```json
{
    "question": "¿Qué información puedes encontrar sobre machine learning en los documentos?"
}
```

**Respuesta:**
```json
{
    "answer": "Basándome en los documentos disponibles, puedo encontrar información sobre..."
}
```

### 🤖 DELIA - Asistente EDSL

**Endpoint:** `POST /api/v1/chat/delia`

**Uso:** Para consultas especializadas sobre EDSL PowerCurve™ con validación y corrección de código.

**Parámetros:**
- `question`: La pregunta o código a revisar
- `user_level`: Nivel de usuario (`basic`, `intermediate`, `advanced`)

**Ejemplos de uso:**

#### 1. Consulta Básica
```json
{
    "question": "¿Qué es EDSL y para qué se usa?",
    "user_level": "basic"
}
```

#### 2. Validación de Código
```json
{
    "question": "Revisa este código EDSL: IF x > 10 THEN y = 20",
    "user_level": "intermediate"
}
```

#### 3. Generación de Código
```json
{
    "question": "Genera un script EDSL para validar si un campo es nulo antes de procesarlo",
    "user_level": "intermediate"
}
```

#### 4. Optimización Avanzada
```json
{
    "question": "Optimiza este script EDSL: IF IsNull(field1) THEN result = 0 ELSE result = field1 * 2",
    "user_level": "advanced"
}
```

**Respuesta de DELIA:**
```json
{
    "response": "Aquí está tu código EDSL corregido...",
    "validation_results": [
        {
            "is_valid": true,
            "errors": [],
            "warnings": ["Line 1: Consider adding semicolon at end"],
            "suggestions": []
        }
    ],
    "user_level": "intermediate",
    "has_edsl_code": true,
    "edsl_code_blocks_count": 1,
    "error": null
}
```

## Niveles de Usuario en DELIA

### 🟢 Basic
- Explicaciones detalladas y paso a paso
- Conceptos fundamentales explicados
- Ejemplos simples y claros
- Ideal para principiantes en EDSL

### 🟡 Intermediate
- Explicaciones balanceadas
- Ejemplos prácticos
- Buenas prácticas incluidas
- Nivel por defecto

### 🔴 Advanced
- Respuestas concisas
- Optimizaciones avanzadas
- Enfoque en rendimiento
- Para usuarios experimentados

## Flujo de Trabajo Recomendado

### 1. Configuración Inicial
1. Importa la colección en Postman
2. Ejecuta "Obtener Token" para autenticarte
3. Verifica que el token se haya guardado correctamente

### 2. Carga de Documentos
1. Usa "Subir Documento" para cargar archivos PDF, TXT, JSON o Excel
2. Verifica el estado con "Obtener Estado de Base de Datos"
3. Lista los documentos con "Listar Documentos"

### 3. Consultas RAG
1. **Para consultas generales**: Usa endpoints de "Chat General"
2. **Para consultas EDSL**: Usa endpoints de "DELIA - Asistente EDSL"

### 4. Ejemplos de Casos de Uso

#### Caso 1: Documentación General
```
1. Subir documento técnico
2. Usar "Realizar Consulta General" para preguntas sobre el contenido
3. Usar "Consulta sobre Documentos Específicos" para conceptos específicos
```

#### Caso 2: Desarrollo EDSL
```
1. Usar "Consulta Básica EDSL" para aprender conceptos
2. Usar "Validación de Código EDSL" para revisar scripts
3. Usar "Generación de Código EDSL" para crear nuevos scripts
4. Usar "Optimización Avanzada EDSL" para mejorar rendimiento
```

## Consejos de Uso

### ✅ Mejores Prácticas
- Siempre obtén un token antes de usar otros endpoints
- Usa el nivel de usuario apropiado en DELIA
- Incluye ejemplos específicos en tus preguntas
- Revisa las validaciones en las respuestas de DELIA

### ⚠️ Consideraciones
- Los tokens expiran después de 30 minutos
- Los documentos se procesan de forma asíncrona
- DELIA requiere contexto sobre EDSL para funcionar óptimamente

### 🔧 Troubleshooting
- **Error 401**: Renueva el token de autenticación
- **Error 422**: Verifica el formato JSON de la petición
- **Error 500**: Verifica que el servidor esté funcionando

## Personalización

### Modificar Variables
Puedes cambiar la URL base editando la variable `base_url` en la colección.

### Agregar Nuevos Ejemplos
Copia y modifica las peticiones existentes para crear nuevos casos de uso.

### Scripts de Prueba
Algunas peticiones incluyen scripts de prueba para validar respuestas automáticamente.

## Soporte

Para problemas con la API:
1. Verifica la documentación en `/docs` (Swagger)
2. Revisa los logs del servidor
3. Consulta el README principal del proyecto

Para problemas con Postman:
1. Verifica la configuración de variables
2. Asegúrate de que el token sea válido
3. Revisa la configuración de CORS si es necesario 