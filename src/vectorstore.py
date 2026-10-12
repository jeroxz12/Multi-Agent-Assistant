"""Pinecone index and per-department namespaces."""

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.config import Settings, load_settings


def pinecone_client(settings: Settings | None = None) -> Pinecone:
    settings = settings or load_settings()
    return Pinecone(api_key=settings.pinecone_api_key)


def ensure_index(settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    client = pinecone_client(settings)
    if client.has_index(settings.pinecone_index):
        return
    client.create_index(
        name=settings.pinecone_index,
        dimension=settings.embedding_dimensions,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=settings.pinecone_cloud,
            region=settings.pinecone_region,
        ),
        timeout=180,
    )


def clear_namespace(namespace: str, settings: Settings | None = None) -> None:
    settings = settings or load_settings()
    client = pinecone_client(settings)
    description = client.describe_index(settings.pinecone_index)
    index = client.Index(host=description.host)
    try:
        index.delete(delete_all=True, namespace=namespace)
    except Exception as error:
        message = str(error).lower()
        if "namespace" in message and "not found" in message:
            return
        raise


def get_store(namespace: str, settings: Settings | None = None) -> PineconeVectorStore:
    settings = settings or load_settings()
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
    return PineconeVectorStore(
        index_name=settings.pinecone_index,
        embedding=embeddings,
        namespace=namespace,
        pinecone_api_key=settings.pinecone_api_key,
    )


def namespace_vector_count(namespace: str, settings: Settings | None = None) -> int:
    settings = settings or load_settings()
    client = pinecone_client(settings)
    description = client.describe_index(settings.pinecone_index)
    index = client.Index(host=description.host)
    stats = index.describe_index_stats()
    namespaces = stats.namespaces or {}
    summary = namespaces.get(namespace)
    if summary is None:
        return 0
    return int(summary.vector_count or 0)
