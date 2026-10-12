"""Confirm that OpenAI, Langfuse, and Pinecone accept the keys in .env."""

from langfuse import get_client
from openai import OpenAI
from pinecone import Pinecone

from src.config import load_settings


def main() -> None:
    settings = load_settings()

    OpenAI(api_key=settings.openai_api_key).models.list()
    print("OpenAI: ok")

    langfuse_ok = get_client().auth_check()
    print(f"Langfuse: {'ok' if langfuse_ok else 'rechazó las claves'}")
    if not langfuse_ok:
        raise SystemExit(1)

    client = Pinecone(api_key=settings.pinecone_api_key)
    names = [item.name for item in client.list_indexes()]
    print("Pinecone: ok")
    print("indices: " + (", ".join(names) if names else "(ninguno todavía)"))


if __name__ == "__main__":
    main()
