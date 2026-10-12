"""Classify a question into one department before any retrieval happens."""

from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, field_validator

from src.config import load_settings

Department = Literal["hr", "tech", "finance", "out_of_scope"]

CLASSIFIER_PROMPT = """Clasificá la consulta de una persona que trabaja en Nubiq.
Elegí un solo departamento. No respondas la consulta.

hr: vacaciones, licencias, beneficios, onboarding de personas, desempeño, conducta, jornada, legajo, People Operations.
tech: VPN, contraseñas, autenticador, laptop, Wi-Fi, credencial, correo sospechoso, tickets de acceso, un portal que no abre.
finance: reembolsos, viáticos, anticipos, facturas, tarjeta corporativa, presupuestos, recibos, fecha de pago del sueldo, topes de hotel y de gastos de un viaje de trabajo.
out_of_scope: temas legales (indemnización, contratos, despido), preguntas ajenas a la empresa, o una consulta que no encaja en los tres departamentos.

Si la pregunta mezcla un acceso con una política, gana el acceso.
"No puedo entrar al portal de nómina" es tech.
"¿Cuándo se paga la nómina?" es finance.
"¿Cuál es el tope de hotel por noche en un viaje de trabajo?" es finance.
"¿Cuántos días de vacaciones tengo?" es hr.

confidence es un número entre 0 y 1.
reason es una sola frase, en español, que dice por qué elegiste ese departamento.
"""


class RouteDecision(BaseModel):
    department: Department
    confidence: float = Field(ge=0, le=1)
    reason: str

    @field_validator("confidence", mode="before")
    @classmethod
    def confidence_as_fraction(cls, value: object) -> float:
        number = float(value)
        if number > 1:
            number = number / 100
        return max(0.0, min(1.0, number))


def build_classifier() -> Runnable:
    settings = load_settings()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CLASSIFIER_PROMPT),
            ("human", "{question}"),
        ]
    )
    model = ChatOpenAI(
        model=settings.chat_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    structured = model.with_structured_output(RouteDecision)
    return (prompt | structured).with_config({"run_name": "orchestrator"})
