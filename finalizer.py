from __future__ import annotations

from evidence_filter import Evidence, filter_evidence
from final_response import FinalResponse, build_response
from redaction import redact_text
from response_validation import validate_response


class FinalizationError(ValueError):
    """Raised when a final response cannot safely be produced."""


def finalize(
    result: str,
    status: str,
    evidence: list[Evidence],
    next_action: str,
) -> FinalResponse:
    """
    Convert verified workflow information into a safe public response.

    Pipeline:
        evidence filter
        -> response construction
        -> semantic validation
        -> redaction
        -> final response validation
    """

    # ---------------------------------------------------------
    # 1. FILTER EVIDENCE
    # ---------------------------------------------------------

    accepted_evidence = filter_evidence(evidence)

    if not accepted_evidence:
        raise FinalizationError(
            "cannot produce final response without accepted evidence"
        )

    # ---------------------------------------------------------
    # 2. BUILD RESPONSE
    # ---------------------------------------------------------

    response = build_response(
        result=result,
        status=status,
        evidence=accepted_evidence,
        next_action=next_action,
    )

    # ---------------------------------------------------------
    # 3. VALIDATE RESPONSE
    # ---------------------------------------------------------

    validation = validate_response(response)

    if not validation.valid:
        raise FinalizationError(
            "; ".join(validation.errors)
        )

    # ---------------------------------------------------------
    # 4. REDACT PUBLIC FIELDS
    # ---------------------------------------------------------

    redacted_message = redact_text(response.message)

    redacted_evidence = [
        redact_text(item)
        for item in response.evidence
    ]

    redacted_next_action = redact_text(
        response.next_action
    )

    # ---------------------------------------------------------
    # 5. FINAL SAFETY VALIDATION
    # ---------------------------------------------------------

    final_response = FinalResponse(
        status=response.status,
        message=redacted_message,
        evidence=redacted_evidence,
        next_action=redacted_next_action,
    )

    final_validation = validate_response(final_response)

    if not final_validation.valid:
        raise FinalizationError(
            "; ".join(final_validation.errors)
        )

    return final_response