"""HR RAG agent. Answers only from the hr namespace in Pinecone."""

from src.agents.common import answer_department, print_result

SYSTEM_PROMPT = """Eres el agente de RR. HH. de Nubiq.
Respondes en español, en prosa clara.

Reglas:
- Usá solamente el contexto recuperado.
- Si el contexto no alcanza, decí que la documentación de RR. HH. no cubre la pregunta. No completes el hueco con conocimiento general.
- Cuando uses un dato, mencioná el archivo de donde salió.
- No calcules indemnizaciones, no des pasos de VPN o contraseñas, y no armes un reembolso de viajes.
"""


def answer_hr(question: str) -> dict:
    return answer_department("hr", SYSTEM_PROMPT, question)


if __name__ == "__main__":
    import sys

    question = (
        " ".join(sys.argv[1:]).strip()
        or "¿Cuántos días de vacaciones corresponden después de 2 años en la empresa?"
    )
    print_result(answer_hr(question))
