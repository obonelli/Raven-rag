# Raven RAG — Private AI Search (Python + MySQL)

FastAPI + Prisma (Python) + MySQL + LangChain. Ingesta de texto en *chunks*, embeddings en MySQL y **búsqueda híbrida** (FULLTEXT + similitud vectorial). Listo para integrarse con Next.js.

## Quick start

```bash
cp .env.example .env
docker compose up -d db
# espera ~10s a que MySQL arranque
prisma db push
prisma generate
docker compose up --build
```

Endpoints:

- `GET /health`
- `POST /ingest` → `{ text, title?, source?, path? }`
- `POST /search` → `{ query, k? }`

## Notas
- Ajusta `HYBRID_ALPHA` (0..1) para el peso del score vectorial vs. keyword.
- Puedes cambiar el proveedor de embeddings en `app/ingest.py` y `app/search.py`.
