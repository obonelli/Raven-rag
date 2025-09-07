from .textsplit import split_text
from .db import db
from .config import OPENAI_API_KEY, EMBEDDINGS_MODEL
from .utils import floats_to_b64
from langchain_openai import OpenAIEmbeddings

emb = OpenAIEmbeddings(model=EMBEDDINGS_MODEL, api_key=OPENAI_API_KEY)


async def ingest_text(text: str, title: str | None, source: str, path: str | None):
    chunks = split_text(text)
    doc = await db.document.create(
        data={"source": source, "path": path, "title": title}
    )
    vecs = emb.embed_documents(chunks)
    data = []
    for i, (t, v) in enumerate(zip(chunks, vecs)):
        data.append(
            {
                "docId": doc.id,
                "index": i,
                "text": t,
                "embedding": floats_to_b64(v),  # base64 string
            }
        )
    if data:
        await db.chunk.create_many(data=data)
    return {"documentId": doc.id, "chunks": len(chunks)}
