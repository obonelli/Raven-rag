# Raven RAG — Private AI Search (Python + MySQL)

Raven RAG is a lightweight **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**, **Prisma**, **MySQL**, and **LangChain**.
It ingests text into chunks, stores embeddings directly in MySQL, and performs **hybrid search** (FULLTEXT + vector similarity).
Designed to integrate seamlessly with frontends such as **Next.js**.

---

## Features

- 🚀 **FastAPI** — modern, async Python backend.
- 🗄️ **Prisma ORM** — type-safe database access for MySQL.
- 🔎 **Hybrid search** — combines keyword (FULLTEXT) and semantic (vector) search.
- 🧩 **LangChain integration** — easy to extend with LLM pipelines.
- ⚡ **Docker Compose** setup — ready to run with a single command.

---

## Environment Variables (.env)

> **Do not commit your `.env` file.** Use placeholders and keep secrets out of git.

Create a file named `.env` at the project root with the following keys **(replace placeholders with your own values)**:

```env
# Database (Docker Compose service name is 'db')
DATABASE_URL="mysql://raven:raven@db:3306/raven"

# OpenAI (example provider) — put YOUR key here
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# Embeddings model (you can change it in code too)
EMBEDDINGS_MODEL="text-embedding-3-small"

# Hybrid search weight: 0..1 (vector vs. keyword)
HYBRID_ALPHA="0.6"
```

> If you accidentally pushed a real key in any commit, **revoke/rotate it immediately** in your provider dashboard and rewrite your git history to remove the secret.

You can also provide a public-safe template file named `.env.example` using placeholders (this one **can** be committed):

```env
DATABASE_URL="mysql://raven:raven@db:3306/raven"
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
EMBEDDINGS_MODEL="text-embedding-3-small"
HYBRID_ALPHA="0.6"
```

---

## Quick Start

```bash
# 1) Copy env file
cp .env.example .env   # or create .env manually with your secrets

# 2) Start the database
docker compose up -d db
# wait ~10s for MySQL to be ready

# 3) Push schema & generate Prisma client
prisma db push
prisma generate

# 4) Build and run the API
docker compose up --build
```

API will be available at `http://localhost:8000` by default (configured in `docker-compose.yml`).

---

## API Endpoints

- `GET /health` — health check.
- `POST /ingest` — ingest documents.
  ```json
  { "text": "...", "title": "?", "source": "?", "path": "?" }
  ```
- `POST /search` — hybrid search.
  ```json
  { "query": "...", "k": 5 }
  ```

---

## Configuration

- **Hybrid weight**: adjust `HYBRID_ALPHA` (`0..1`) in `.env` to control the balance between vector score and keyword score.
- **Embeddings provider**: change or swap the embedding model/provider in `app/ingest.py` and `app/search.py`.
- **Schema**: database schema is defined in `prisma/schema.prisma`.

---

## Deployment (AWS Lightsail — minimal)

1. Create a Lightsail Linux instance (free trial eligible).
2. SSH into the instance and install Docker & Docker Compose.
3. Clone this repository and set your `.env` on the server.
4. Run `docker compose up -d db`, then `prisma db push && prisma generate`.
5. Run `docker compose up --build -d` to start the API.
6. Optionally put Nginx in front and add HTTPS with Let's Encrypt.

> For truly “scale-to-zero” cost patterns, consider a serverless approach (API Gateway + Lambda + DynamoDB), but it requires adapting the container/app packaging.

---

## Development Tips

- Use `uvicorn` hot-reload locally if not running in Docker:
  ```bash
  uvicorn app.main:app --reload --port 8000
  ```
- Lint/format (optional): `ruff`, `black`, `mypy`.
- Tests: add `pytest` and create fixtures for the DB.

---

## License

MIT (update as needed).
