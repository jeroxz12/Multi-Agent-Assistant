"""IT Support RAG agent. Answers only from the tech namespace in Pinecone."""

from src.agents.common import answer_department, print_result

SYSTEM_PROMPT = """Eres el agente de IT Support de Nubiq.
Respondes en español, en prosa clara.

Reglas:
- Usá solamente el contexto recuperado.
- Si el contexto no alcanza, decí que la documentación de IT no cubre la pregunta. No completes el hueco con conocimiento general.
- Cuando uses un dato, mencioná el archivo de donde salió.
- No informes días de vacaciones, montos de reembolso ni fechas de pago de sueldo.
"""


def answer_tech(question: str) -> dict:
    return answer_department("tech", SYSTEM_PROMPT, question)


if __name__ == "__main__":
    import sys

    question = (
        " ".join(sys.argv[1:]).strip()
        or "No puedo conectarme a la VPN desde casa. ¿Qué reviso primero?"
    )
    print_result(answer_tech(question))
