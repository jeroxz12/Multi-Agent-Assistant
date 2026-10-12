"""Retrieval chain shared by the department agents."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

from src.config import load_settings
from src.vectorstore import get_store


def build_rag_chain(namespace: str, system_prompt: str, run_name: str) -> Runnable:
    settings = load_settings()
    store = get_store(namespace, settings)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}\n\nContexto recuperado:\n{context}"),
            ("human", "{question}"),
        ]
    )
    model = ChatOpenAI(
        model=settings.chat_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    generate = (prompt | model | StrOutputParser()).with_config({"run_name": "generation"})

    def retrieve(question: str) -> dict:
        pairs = store.similarity_search_with_score(question, k=settings.retriever_k)
        sources = []
        blocks = []
        for document, score in pairs:
            source = str(document.metadata.get("source", "desconocido"))
            sources.append(
                {
                    "source": source,
                    "excerpt": document.page_content[:500],
                    "score": round(float(score), 4),
                }
            )
            blocks.append(f"[{source}]\n{document.page_content}")
        context = "\n\n".join(blocks) if blocks else "(sin fragmentos relevantes)"
        return {
            "question": question,
            "system_prompt": system_prompt,
            "context": context,
            "sources": sources,
        }

    retrieve_step = RunnableLambda(retrieve).with_config({"run_name": "retriever"})
    return (retrieve_step | RunnablePassthrough.assign(answer=generate)).with_config(
        {"run_name": run_name}
    )
