# Asistente multiagente de soporte interno

Sistema de routing para consultas internas de Nubiq, una empresa SaaS ficticia. Una pregunta entra por `answer()`. El orquestador elige RR. HH., IT, Finance o fuera de alcance, y el router abre una sola rama RAG.

## Qué hay ahora

1. Las políticas viven en `data/hr_docs/`, `data/tech_docs/` y `data/finance_docs/`.
2. Cada carpeta se parte en chunks y se convierte en embeddings.
3. Los vectores quedan en los namespaces `hr`, `tech` y `finance` del índice de Pinecone.
4. El clasificador devuelve departamento, confianza y una razón.
5. Si la confianza es menor a 0,6, no se abre ninguna rama.
6. El agente elegido recupera 4 chunks de su namespace y redacta solo con eso.
7. Langfuse registra la clasificación, la búsqueda y la generación en la misma ejecución.

El endpoint, la interfaz y el evaluador vienen después. El repaso del código es antes del evaluador.

## Requisitos

- Python 3.11
- Cuentas de OpenAI, Langfuse y Pinecone

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Completá `.env` con tus claves. No lo subas al repositorio.

## Primer recorrido

Desde la raíz del proyecto, con el entorno activo:

```bash
python -m src.check_credentials
python -m src.documents hr
python -m src.ingest hr
python -m src.ingest tech
python -m src.ingest finance
python -m src.multi_agent_system "¿Cuántos días de vacaciones corresponden después de 2 años en la empresa?"
```

`src.documents` solo muestra cómo quedó partido el texto. `src.ingest` crea el índice si no existe y carga el namespace que se le pasa (`hr`, `tech` o `finance`). Volver a correr la ingesta borra ese namespace y lo carga de nuevo.

## Configuración

| Variable | Uso |
| --- | --- |
| `OPENAI_API_KEY` | Embeddings `text-embedding-3-small` y respuestas `gpt-4o-mini` |
| `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL` | Trazas en Langfuse Cloud |
| `PINECONE_API_KEY` | Base vectorial |
| `PINECONE_INDEX` | Nombre del índice. Por defecto `multi-agent-assistant` |
| `PINECONE_CLOUD`, `PINECONE_REGION` | Dónde se crea el índice si todavía no existe. Por defecto `aws` / `us-east-1` |

Los Markdown de `data/` son la fuente. Pinecone guarda el índice derivado.

## Límites de esta etapa

- El router elige el departamento. Los comandos `hr_agent`, `tech_agent` y `finance_agent` siguen sirviendo para hablarle a un solo agente.
- Una confianza menor a 0,6 no abre rama.
- No hay memoria de la conversación anterior.
- Cada ingesta y cada pregunta consumen créditos de OpenAI. Pinecone almacena los vectores.
