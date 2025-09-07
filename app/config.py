import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
DATABASE_URL = os.getenv("DATABASE_URL")  # mysql://raven:raven@db:3306/raven
ALPHA = float(os.getenv("HYBRID_ALPHA", "0.6"))  # peso del score vectorial
