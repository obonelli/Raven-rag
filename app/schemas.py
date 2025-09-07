from pydantic import BaseModel

class IngestBody(BaseModel):
    text: str
    title: str | None = None
    source: str = "manual"
    path: str | None = None

class SearchBody(BaseModel):
    query: str
    k: int = 6
