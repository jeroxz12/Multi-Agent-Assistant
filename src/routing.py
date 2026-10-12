"""Open one department branch from the classifier decision."""

from langchain_core.runnables import (
    Runnable,
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)

from src.agents.finance_agent import SYSTEM_PROMPT as FINANCE_PROMPT
from src.agents.hr_agent import SYSTEM_PROMPT as HR_PROMPT
from src.agents.orchestrator import RouteDecision, build_classifier
from src.agents.tech_agent import SYSTEM_PROMPT as TECH_PROMPT
from src.config import load_settings
from src.rag import build_rag_chain

PROMPTS = {
    "hr": HR_PROMPT,
    "tech": TECH_PROMPT,
    "finance": FINANCE_PROMPT,
}


def apply_confidence_threshold(payload: dict) -> dict:
    decision: RouteDecision = payload["decision"]
    threshold = load_settings().route_confidence_threshold
    routed = decision.department
    reason = decision.reason
    if decision.confidence < threshold:
        routed = "out_of_scope"
        reason = (
            f"{decision.reason} "
            f"La confianza {decision.confidence:.2f} está por debajo de {threshold:.2f}, "
            "así que no se abre ninguna rama."
        )
    return {
        **payload,
        "decision": decision.model_copy(update={"reason": reason}),
        "routed_department": routed,
    }


def public_answer(payload: dict) -> dict:
    decision: RouteDecision = payload["decision"]
    rag = payload["rag"]
    return {
        "answer": rag["answer"],
        "department": payload["routed_department"],
        "confidence": decision.confidence,
        "reason": decision.reason,
        "sources": rag["sources"],
    }


def refuse(payload: dict) -> dict:
    decision: RouteDecision = payload["decision"]
    threshold = load_settings().route_confidence_threshold
    if decision.confidence < threshold:
        text = (
            "No estoy lo bastante seguro de a qué equipo corresponde. "
            "Reformulá la pregunta indicando si es de personas, de acceso a sistemas o de pagos."
        )
    else:
        text = (
            "No tengo un agente para esta consulta. "
            "Puedo ayudar con RR. HH., IT Support o Finance. "
            "Un tema legal, como una indemnización, queda fuera de este sistema."
        )
    return {
        "answer": text,
        "department": "out_of_scope",
        "confidence": decision.confidence,
        "reason": decision.reason,
        "sources": [],
    }


def department_branch(department: str) -> Runnable:
    rag_chain = build_rag_chain(department, PROMPTS[department], f"rag_{department}")
    with_retrieval = RunnablePassthrough.assign(
        rag=RunnableLambda(lambda payload: payload["question"]) | rag_chain
    )
    return with_retrieval | RunnableLambda(public_answer)


def is_department(department: str):
    def check(payload: dict) -> bool:
        return payload["routed_department"] == department

    return check


def build_router() -> Runnable:
    classifier = build_classifier()
    branch = RunnableBranch(
        (is_department("hr"), department_branch("hr")),
        (is_department("tech"), department_branch("tech")),
        (is_department("finance"), department_branch("finance")),
        RunnableLambda(refuse),
    )
    return (
        RunnableLambda(lambda question: {"question": question})
        | RunnablePassthrough.assign(
            decision=RunnableLambda(lambda payload: {"question": payload["question"]})
            | classifier
        )
        | RunnableLambda(apply_confidence_threshold)
        | branch
    ).with_config({"run_name": "router"})
