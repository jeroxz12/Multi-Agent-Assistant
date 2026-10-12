"""Shared run path for the department RAG agents."""

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from src.rag import build_rag_chain


def answer_department(department: str, system_prompt: str, question: str) -> dict:
    run_name = f"rag_{department}"
    result = build_rag_chain(department, system_prompt, run_name).invoke(
        question,
        config={"callbacks": [CallbackHandler()], "run_name": run_name},
    )
    get_client().flush()
    return {
        "answer": result["answer"],
        "department": department,
        "sources": result["sources"],
    }


def print_result(result: dict) -> None:
    print(result["answer"])
    print()
    print(f"departamento: {result['department']}")
    if "confidence" in result:
        print(f"confianza: {result['confidence']:.2f}")
        print(f"razon: {result['reason']}")
    for source in result["sources"]:
        print(f"- {source['source']} (score {source['score']})")
    scores = result.get("scores")
    if scores:
        print(
            "evaluacion: "
            f"calidad {scores['quality']}/10, "
            f"relevancia {scores['relevance']}, "
            f"completitud {scores['completeness']}, "
            f"exactitud {scores['accuracy']}"
        )
        print(scores["comment"])
