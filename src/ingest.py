"""Embed domain documents and upsert them into a Pinecone namespace."""

import hashlib

from langchain_core.documents import Document

from src.config import load_settings
from src.documents import load_domain_documents, split_documents
from src.vectorstore import clear_namespace, ensure_index, get_store, namespace_vector_count


def chunk_id(domain: str, document: Document, position: int) -> str:
    raw = "|".join(
        [
            domain,
            str(document.metadata.get("source", "")),
            str(document.metadata.get("start_index", position)),
            str(position),
        ]
    )
    return hashlib.sha1(raw.encode()).hexdigest()[:32]


def ingest_domain(domain: str) -> int:
    settings = load_settings()
    documents = load_domain_documents(domain)
    chunks = split_documents(documents, domain)
    ensure_index(settings)
    clear_namespace(domain, settings)
    store = get_store(domain, settings)
    store.add_documents(
        chunks,
        ids=[chunk_id(domain, chunk, index) for index, chunk in enumerate(chunks)],
        namespace=domain,
        async_req=False,
    )
    stored = namespace_vector_count(domain, settings)
    print(f"dominio: {domain}")
    print(f"chunks preparados: {len(chunks)}")
    print(f"vectores en el namespace: {stored}")
    print(f"indice: {settings.pinecone_index}")
    return len(chunks)


if __name__ == "__main__":
    import sys

    ingest_domain(sys.argv[1] if len(sys.argv) > 1 else "hr")
