from fastapi import FastAPI
from .db import connect, disconnect
from .schemas import IngestBody, SearchBody
from .ingest import ingest_text
from .search import hybrid_search

app = FastAPI(title="Raven RAG API")

@app.on_event("startup")
async def _start():
    await connect()

@app.on_event("shutdown")
async def _stop():
    await disconnect()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/ingest")
async def ingest(b: IngestBody):
    return await ingest_text(b.text, b.title, b.source, b.path)

@app.post("/search")
async def search(b: SearchBody):
    return await hybrid_search(b.query, b.k)
