"""Load markdown policies and split them into retrieval chunks."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import domain_docs_dir, load_settings


def load_domain_documents(domain: str) -> list[Document]:
    folder = domain_docs_dir(domain)
    if not folder.exists():
        raise FileNotFoundError(f"No existe la carpeta de documentos: {folder}")

    paths = sorted(folder.glob("*.md"))
    if not paths:
        raise RuntimeError(f"No hay archivos .md en {folder}")

    return [
        Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.name},
        )
        for path in paths
    ]


def split_documents(documents: list[Document], domain: str) -> list[Document]:
    settings = load_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    prepared: list[Document] = []
    for chunk in chunks:
        text = chunk.page_content.strip()
        if not text:
            continue
        source = chunk.metadata.get("source", "")
        chunk.metadata = {
            "source": source,
            "domain": domain,
            "start_index": int(chunk.metadata.get("start_index", 0)),
        }
        chunk.page_content = text
        prepared.append(chunk)
    return prepared


def describe_chunks(domain: str) -> None:
    documents = load_domain_documents(domain)
    chunks = split_documents(documents, domain)
    print(f"dominio: {domain}")
    print(f"archivos: {len(documents)}")
    print(f"chunks: {len(chunks)}")
    if chunks:
        sample = chunks[0]
        print(f"ejemplo: {sample.metadata['source']} @ {sample.metadata['start_index']}")
        print(sample.page_content[:400])


if __name__ == "__main__":
    import sys

    describe_chunks(sys.argv[1] if len(sys.argv) > 1 else "hr")
