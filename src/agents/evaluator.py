"""Score a RAG answer and attach the grades to its Langfuse trace."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel, Field, field_validator

from src.config import load_settings

EVALUATOR_PROMPT = """Evaluá la respuesta de un agente de soporte interno de Nubiq.
Mirá la consulta, la respuesta y los fragmentos recuperados. No reescribas la respuesta.

Puntuá cada dimensión del 1 al 10:
- relevance: la respuesta contesta lo que se preguntó.
- completeness: incluye los datos importantes que sí estaban en los fragmentos.
- accuracy: los datos coinciden con los fragmentos y no agrega hechos que no están ahí.
- quality: nota general.

Si los fragmentos no alcanzan y la respuesta lo dice, accuracy puede ser alta.
comment es una sola frase, en español, que justifica la nota general.
"""


class QualityScores(BaseModel):
    relevance: int = Field(ge=1, le=10)
    completeness: int = Field(ge=1, le=10)
    accuracy: int = Field(ge=1, le=10)
    quality: int = Field(ge=1, le=10)
    comment: str

    @field_validator("relevance", "completeness", "accuracy", "quality", mode="before")
    @classmethod
    def whole_number(cls, value: object) -> int:
        return int(round(float(value)))


def build_evaluator() -> Runnable:
    settings = load_settings()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", EVALUATOR_PROMPT),
            (
                "human",
                "Consulta:\n{question}\n\nRespuesta:\n{answer}\n\nFragmentos:\n{context}",
            ),
        ]
    )
    model = ChatOpenAI(
        model=settings.chat_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    structured = model.with_structured_output(QualityScores)
    return (prompt | structured).with_config({"run_name": "evaluator"})


def evaluate_answer(
    question: str,
    answer: str,
    sources: list[dict],
    trace_id: str | None,
) -> dict:
    context = "\n\n".join(
        f"[{source.get('source', 'desconocido')}]\n{source.get('excerpt', '')}"
        for source in sources
    ) or "(sin fragmentos)"
    handler = (
        CallbackHandler(trace_context={"trace_id": trace_id})
        if trace_id
        else CallbackHandler()
    )
    scores = build_evaluator().invoke(
        {"question": question, "answer": answer, "context": context},
        config={"callbacks": [handler], "run_name": "evaluator"},
    )
    payload = scores.model_dump()
    target_trace = trace_id or handler.last_trace_id
    if target_trace:
        client = get_client()
        client.create_score(
            name="quality",
            value=float(payload["quality"]),
            trace_id=target_trace,
            data_type="NUMERIC",
            comment=payload["comment"],
        )
        for name in ("relevance", "completeness", "accuracy"):
            client.create_score(
                name=name,
                value=float(payload[name]),
                trace_id=target_trace,
                data_type="NUMERIC",
            )
    return payload
