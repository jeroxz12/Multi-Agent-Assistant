"""HTTP entry for the router. Translates JSON into answer() and back."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.multi_agent_system import answer

UI_DIR = Path(__file__).resolve().parents[1] / "ui"

app = FastAPI(title="Nubiq multi-agent router")
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)


class SourceChunk(BaseModel):
    source: str
    excerpt: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    department: str
    confidence: float
    reason: str
    sources: list[SourceChunk]


@app.get("/")
def home() -> FileResponse:
    return FileResponse(UI_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/query", response_model=QueryResponse)
def query(body: QueryRequest) -> QueryResponse:
    return QueryResponse(**answer(body.query))
