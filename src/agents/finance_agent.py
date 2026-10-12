"""Finance RAG agent. Answers only from the finance namespace in Pinecone."""

from src.agents.common import answer_department, print_result

SYSTEM_PROMPT = """Eres el agente de Finance de Nubiq.
Respondes en español, en prosa clara.

Reglas:
- Usá solamente el contexto recuperado.
- Si el contexto no alcanza, decí que la documentación de Finance no cubre la pregunta. No completes el hueco con conocimiento general.
- Cuando uses un dato, mencioná el archivo de donde salió.
- No informes días de vacaciones ni pasos para configurar la VPN.
"""


def answer_finance(question: str) -> dict:
    return answer_department("finance", SYSTEM_PROMPT, question)


if __name__ == "__main__":
    import sys

    question = (
        " ".join(sys.argv[1:]).strip()
        or "¿Cómo solicito el reembolso de un viaje de trabajo?"
    )
    print_result(answer_finance(question))
