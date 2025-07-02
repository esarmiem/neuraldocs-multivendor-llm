# Aplicación RAG Backend

Una aplicación de Generación Aumentada por Recuperación (RAG) construida con FastAPI que soporta múltiples proveedores de LLM y capacidades de procesamiento de documentos.

## Características

- Soporte para Múltiples Proveedores LLM (OpenAI, Anthropic, Google Gemini, Ollama)
- Procesamiento de Documentos (.pdf, .txt, .json, .xlsx)
- Almacenamiento en Base de Datos Vectorial (ChromaDB)
- Autenticación JWT
- Soporte CORS
- Registro Estructurado

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- ChromaDB ejecutándose local o remotamente
- Uno de los proveedores LLM soportados:
  - Clave API de OpenAI
  - Clave API de Anthropic
  - Clave API de Google Gemini
  - Ollama ejecutándose localmente

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tuusuario/rag-app.git
   cd rag-app/backend
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usar: venv\Scripts\activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` en el directorio `backend` con tu configuración:

   ```env
   # Configuración de la Aplicación
   SECRET_KEY=tu_clave_secreta_aqui

   # Proveedor LLM (elegir uno: openai, anthropic, gemini, ollama)
   LLM_PROVIDER=openai

   # Claves API (completar según el proveedor elegido)
   OPENAI_API_KEY=tu_clave_api_openai
   ANTHROPIC_API_KEY=tu_clave_api_anthropic
   GEMINI_API_KEY=tu_clave_api_gemini

   # Configuración de Ollama (si se usa Ollama)
   OLLAMA_API_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```
5. `.env` de ejemplo:

      ```env
      # LLM Provider: openai, anthropic, gemini, ollama
      LLM_PROVIDER=ollama

      # API Keys (only required if using the corresponding provider)
      OPENAI_API_KEY="your-openai-api-key-here"  # Only needed if LLM_PROVIDER=openai
      ANTHROPIC_API_KEY="your-anthropic-api-key-here"  # Only needed if LLM_PROVIDER=anthropic
      GEMINI_API_KEY="your-gemini-api-key-here"  # Only needed if LLM_PROVIDER=gemini

      # Ollama (if used)
      OLLAMA_API_BASE_URL="http://localhost:11434"
      OLLAMA_MODEL="deepseek-r1:8b"

      # ChromaDB
      CHROMA_HOST="localhost"
      CHROMA_PORT=8000

      # Security
      SECRET_KEY="your_super_secret_key_for_jwt"
      ALGORITHM="HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Configurar la Base de Datos Vectorial (ChromaDB):
   - Si ChromaDB está ejecutándose localmente, no es necesario configurar nada adicional.
   - Si ChromaDB está ejecutándose en un servidor remoto, asegúrate de actualizar la URL en `.env`.
   - Si ChromaDB deseas ejecutarlo con docker usa el comando `docker run -d -p 8002:8000 chromadb/chroma`.

## Ejecutar la Aplicación

1. Iniciar el servidor FastAPI:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. La API estará disponible en:

   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc

## Endpoints de la API

### Autenticación

- `POST /api/v1/auth/token` : Obtener token de acceso

  ```bash
  curl -X POST "http://localhost:8000/api/v1/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=testpassword"
  ```

### Documentos

- `POST /api/v1/documents/upload` : Subir y procesar un documento

  ```bash
  curl -X POST "http://localhost:8000/api/v1/documents/upload" \
    -H "Authorization: Bearer tu_token" \
    -F "file=@ruta/a/tu/documento.pdf"
  ```

- `GET /api/v1/documents/database/stats` : Obtener estadísticas de la base de datos vectorial
  ```bash
  curl -X GET "http://localhost:8000/api/v1/documents/database/stats" \
  -H "Authorization: Bearer tu_token"
  ```
- `DELETE /api/v1/documents/database/clear` : Eliminar todos los documentos de la base de datos
  ```bash
  curl -X DELETE "http://localhost:8000/api/v1/documents/database/clear" \
  -H "Authorization: Bearer tu_token"
  ```
- `GET /api/v1/documents/list` : Listar todos los documentos subidos
  ```bash
  curl -X GET "http://localhost:8000/api/v1/documents/list" \
  -H "Authorization: Bearer tu_token"
  ```

### Chat

- `POST /api/v1/chat/query` : Consultar el sistema RAG

  ```bash
  curl -X POST "http://localhost:8000/api/v1/chat/query" \
    -H "Authorization: Bearer tu_token" \
    -H "Content-Type: application/json" \
    -d '{"query": "¿Qué información puedes encontrar sobre...?"}'
  ```

## Tipos de Documentos Soportados

- Archivos PDF (.pdf)
- Archivos de texto (.txt)
- Archivos JSON (.json)
- Archivos Excel (.xlsx)

## Desarrollo

### Estructura del Proyecto

```plaintext
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── rag/
│   ├── schemas/
│   └── utils/
├── requirements.txt
└── .env
```

### Agregar Nuevas Funcionalidades

1. Crear nuevos endpoints en `app/api/v1/endpoints/`
2. Agregar modelos en `app/schemas/`
3. Implementar lógica de negocio en los módulos apropiados
4. Actualizar el router de la API en `app/api/v1/api.py`

## Pruebas

Para ejecutar las pruebas (una vez implementadas):

```bash
pytest
```

## Solución de Problemas

### Problemas Comunes

1. **Error de Conexión con el Proveedor LLM**
   - Verificar las claves API en `.env`
   - Comprobar la conexión a internet
   - Asegurar que el proveedor elegido esté configurado correctamente

2. **Errores en el Procesamiento de Documentos**
   - Verificar que el formato del archivo sea soportado
   - Comprobar que el archivo no esté corrupto
   - Asegurar que las dependencias requeridas estén instaladas

3. **Problemas de Autenticación**
   - Verificar que el token JWT sea válido
   - Comprobar si el token ha expirado
   - Asegurar que se estén usando las credenciales correctas

## Consideraciones de Seguridad

- Las claves API nunca deben ser comprometidas en el control de versiones
- Usar variables de entorno para datos sensibles
- Mantener las dependencias actualizadas
- Implementar límites de tasa para producción
- Usar configuraciones CORS seguras en producción

## Contribuir

1. Hacer fork del repositorio
2. Crear una rama de funcionalidad
3. Realizar cambios
4. Hacer push a la rama
5. Crear un Pull Request
