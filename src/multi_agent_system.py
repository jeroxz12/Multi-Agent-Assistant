"""Public entry: classify a question and answer with one department agent."""

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from src.agents.common import print_result
from src.routing import build_router


def answer(question: str) -> dict:
    result = build_router().invoke(
        question,
        config={"callbacks": [CallbackHandler()], "run_name": "multi_agent"},
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
