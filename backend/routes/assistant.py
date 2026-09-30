from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.assistant_scope import validate_question
from services.assistant_intents import (
    classify_question,
    is_unsupported_prediction,
)
from services.assistant_query import query_approved_evidence
from services.assistant_response import compose_response
from services.assistant_grounding import validate_grounded_response
from services.assistant_llm import LLMService
from services.assistant_llm_validation import validate_llm_output


assistant_router = APIRouter(
    prefix="/api/assistant",
    tags=["Grounded Assistant"],
)


class AssistantQuery(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )


def _missing_parameter_response(
    intent_name: str,
) -> dict[str, Any]:
    return {
        "answer_id": "ANS-POC88-MISSING-PARAMETER",
        "status": "missing_parameter",
        "intent": intent_name,
        "answer": (
            "A metric name or approved result ID is required "
            "to answer this question."
        ),
        "evidence_references": [],
        "key_values": [],
        "metadata": {},
        "limitation": (
            "The assistant only answers from approved "
            "Track A comparative evidence."
        ),
        "suggested_follow_ups": [
            "What is the baseline for transaction count?",
            "What is the range for block size?",
            "What is the finding for POC88-COMP-0003?",
        ],
        "answer_mode": "deterministic_fallback",
    }


def _comparison_disabled_response() -> dict[str, Any]:
    return {
        "answer_id": "ANS-POC88-COMPARISON-DISABLED",
        "status": "unsupported",
        "intent": "compare_record_to_baseline",
        "answer": (
            "Record-to-baseline comparison is currently disabled "
            "because no genuine observation or record was supplied."
        ),
        "evidence_references": [],
        "key_values": [],
        "metadata": {},
        "limitation": (
            "The approved Track A comparative evidence does not "
            "support comparison against an assumed or internally "
            "selected observation."
        ),
        "suggested_follow_ups": [
            "What is the baseline for transaction count?",
            "What is the range for block size?",
            "What is the finding for POC88-COMP-0003?",
        ],
        "answer_mode": "deterministic_fallback",
    }


@assistant_router.post("/query")
def query_assistant(payload: AssistantQuery) -> dict[str, Any]:

    question = payload.question.strip()

    # --------------------------------------------------
    # Safety / scope validation
    # --------------------------------------------------

    safe, reason = validate_question(question)

    if not safe:
        return {
            "answer_id": "ANS-POC88-UNSAFE",
            "status": "unsafe",
            "intent": None,
            "answer": reason,
            "evidence_references": [],
            "key_values": [],
            "metadata": {},
            "limitation": (
                "The assistant only supports bounded questions "
                "over approved Phase 3 intelligence outputs."
            ),
            "suggested_follow_ups": [],
            "answer_mode": "deterministic_fallback",
        }

    # --------------------------------------------------
    # Prediction / forecasting hard stop
    # --------------------------------------------------

    if is_unsupported_prediction(question):
        return {
            "answer_id": "ANS-POC88-PREDICTION-REJECTED",
            "status": "unsupported",
            "intent": None,
            "answer": (
                "This question requests forecasting or prediction, "
                "which is outside the approved Track A comparative "
                "analysis."
            ),
            "evidence_references": [],
            "key_values": [],
            "metadata": {},
            "limitation": (
                "The approved comparative analysis does not establish "
                "temporal trends, forecasting, or predictive capability."
            ),
            "suggested_follow_ups": [
                "What is the approved comparative method?",
                "What is the baseline for transaction count?",
                "What is the range for block size?",
            ],
            "answer_mode": "deterministic_fallback",
        }

    # --------------------------------------------------
    # Intent classification
    # --------------------------------------------------

    intent = classify_question(question)

    if intent is None:
        return {
            "answer_id": "ANS-POC88-UNSUPPORTED",
            "status": "unsupported",
            "intent": None,
            "answer": (
                "This question is outside the approved "
                "Grounded Data Assistant scope."
            ),
            "evidence_references": [],
            "key_values": [],
            "metadata": {},
            "limitation": (
                "The assistant cannot perform forecasting, "
                "new analytical tracks, arbitrary computation, "
                "or unrestricted dataset access."
            ),
            "suggested_follow_ups": [
                "What is the baseline for transaction count?",
                "What is the range for block size?",
                "What is the approved comparative method?",
            ],
            "answer_mode": "deterministic_fallback",
        }

    # --------------------------------------------------
    # Post #5: comparison hard stop
    #
    # Do not compare an approved result against itself or
    # against an assumed observation. A genuine observation
    # or record must be supplied first.
    # --------------------------------------------------

    if intent.name == "compare_record_to_baseline":
        return _comparison_disabled_response()

    # --------------------------------------------------
    # Post #5: required metric/result validation
    #
    # Do not silently select the first available result when
    # the user asks an underspecified baseline/range/result
    # question.
    # --------------------------------------------------

    metric_required_intents = {
        "get_group_baseline",
        "get_group_range",
        "get_group_extreme",
        "explain_result",
    }

    if (
        intent.name in metric_required_intents
        and not intent.metric_name
        and not intent.result_id
    ):
        return _missing_parameter_response(
            intent_name=intent.name,
        )

    # --------------------------------------------------
    # Deterministic approved query
    # --------------------------------------------------

    try:
        evidence = query_approved_evidence(intent)

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail=(
                "Approved Phase 3 intelligence package "
                "is unavailable."
            ),
        )

    except ValueError as exc:
        return {
            "answer_id": "ANS-POC88-UNAVAILABLE",
            "status": "unavailable",
            "intent": intent.name,
            "answer": str(exc),
            "evidence_references": [],
            "key_values": [],
            "metadata": {},
            "limitation": (
                "The assistant can only answer from "
                "approved deterministic evidence."
            ),
            "suggested_follow_ups": [],
            "answer_mode": "deterministic_fallback",
        }

    # --------------------------------------------------
    # Deterministic response composition
    # --------------------------------------------------

    response = compose_response(
        intent_name=intent.name,
        evidence=evidence,
    )

    # --------------------------------------------------
    # Deterministic grounding validation
    # --------------------------------------------------

    response = validate_grounded_response(
        response=response,
        evidence=evidence,
    )

    # --------------------------------------------------
    # Optional grounded LLM explanation
    # --------------------------------------------------

    # The deterministic response remains authoritative.
    #
    # The LLM receives only:
    # - scoped question
    # - intent
    # - approved evidence
    # - approved metadata
    #
    # It does NOT receive the canonical dataset.
    #
    # If the LLM is disabled, unavailable, fails, or produces
    # unsupported content, the deterministic answer remains active.

    llm_service = LLMService()

    llm_result = llm_service.explain(
        question=question,
        intent_name=intent.name,
        evidence=evidence,
    )

    llm_answer = validate_llm_output(
        llm_result=llm_result,
        evidence=evidence,
        deterministic_response=response,
    )

    if llm_answer:
        response["answer"] = llm_answer
        response["answer_mode"] = "llm_grounded"
    else:
        response["answer_mode"] = "deterministic_fallback"

    return response