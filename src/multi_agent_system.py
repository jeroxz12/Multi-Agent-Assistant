"""Public entry: classify a question and answer with one department agent."""

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from src.agents.common import print_result
from src.agents.evaluator import evaluate_answer
from src.routing import build_router


def answer(question: str) -> dict:
    router = build_router()
    handler = CallbackHandler()
    result = router.invoke(
        question,
        config={"callbacks": [handler], "run_name": "multi_agent"},
    )
    if result["department"] == "out_of_scope":
        result["scores"] = None
    else:
        result["scores"] = evaluate_answer(
            question=question,
            answer=result["answer"],
            sources=result["sources"],
            trace_id=handler.last_trace_id,
        )
    get_client().flush()
    return result


if __name__ == "__main__":
    import sys

    question = (
        " ".join(sys.argv[1:]).strip()
        or "¿Cuántos días de vacaciones corresponden después de 2 años en la empresa?"
    )
    print_result(answer(question))
