from .db import db
from .config import ALPHA, OPENAI_API_KEY, EMBEDDINGS_MODEL
from .utils import any_to_floats, cosine
from langchain_openai import OpenAIEmbeddings

emb = OpenAIEmbeddings(model=EMBEDDINGS_MODEL, api_key=OPENAI_API_KEY)


async def hybrid_search(query: str, k: int = 6):
    rows = await db.query_raw(
        """
        SELECT id, docId, text, embedding,
               MATCH(text) AGAINST(? IN NATURAL LANGUAGE MODE) AS kw_score
        FROM Chunk
        WHERE MATCH(text) AGAINST(? IN NATURAL LANGUAGE MODE)
        ORDER BY kw_score DESC
        LIMIT 100
        """,
        query,
        query,
    )

    qv = emb.embed_query(query)
    results = []
    for r in rows:
        vec = any_to_floats(r["embedding"])
        vscore = cosine(vec, qv)
        score = ALPHA * vscore + (1.0 - ALPHA) * float(r["kw_score"])
        results.append(
            {
                "chunkId": r["id"],
                "docId": r["docId"],
                "text": r["text"],
                "kw_score": float(r["kw_score"]),
                "vec_score": vscore,
                "score": score,
            }
        )
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]
