"""Project paths, models, and credentials loaded from .env."""

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

DOMAINS = ("hr", "tech", "finance")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    pinecone_api_key: str
    pinecone_index: str
    pinecone_cloud: str
    pinecone_region: str
    chunk_size: int = 800
    chunk_overlap: int = 120
    retriever_k: int = 4
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    chat_model: str = "gpt-4o-mini"
    route_confidence_threshold: float = 0.6


def load_settings() -> Settings:
    load_dotenv(ROOT / ".env")
    missing = [
        name
        for name in ("OPENAI_API_KEY", "PINECONE_API_KEY")
        if not os.getenv(name)
    ]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Faltan variables en .env: {names}")

    return Settings(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        pinecone_api_key=os.environ["PINECONE_API_KEY"],
        pinecone_index=os.getenv("PINECONE_INDEX", "multi-agent-assistant"),
        pinecone_cloud=os.getenv("PINECONE_CLOUD", "aws"),
        pinecone_region=os.getenv("PINECONE_REGION", "us-east-1"),
    )


def domain_docs_dir(domain: str) -> Path:
    if domain not in DOMAINS:
        raise ValueError(f"Dominio desconocido: {domain}")
    return DATA_DIR / f"{domain}_docs"
