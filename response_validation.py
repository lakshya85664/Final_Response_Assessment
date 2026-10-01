from __future__ import annotations

from dataclasses import dataclass

from final_response import ALLOWED, FinalResponse


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]


def validate_response(response: FinalResponse) -> ValidationResult:
    """
    Validate semantic rules for a response that has already
    passed the FinalResponse schema.

    This layer checks consistency and actionability rather
    than replacing the Pydantic schema.
    """

    errors: list[str] = []

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    if response.status not in ALLOWED:
        errors.append("invalid public status")

    # ---------------------------------------------------------
    # MESSAGE
    # ---------------------------------------------------------

    if not response.message.strip():
        errors.append("message cannot be empty")

    if len(response.message) > 300:
        errors.append("message exceeds 300 characters")

    # ---------------------------------------------------------
    # EVIDENCE
    # ---------------------------------------------------------

    if not response.evidence:
        errors.append("at least one evidence item is required")

    # ---------------------------------------------------------
    # NEXT ACTION
    # ---------------------------------------------------------

    if not response.next_action.strip():
        errors.append("next_action cannot be empty")

    # ---------------------------------------------------------
    # STATUS / ACTION CONSISTENCY
    # ---------------------------------------------------------

    if response.status == "completed":
        if response.next_action not in {
            "continue",
            "review",
            "none",
        }:
            errors.append(
                "completed response has invalid next_action"
            )

    elif response.status in {
        "pending",
        "needs_review",
    }:
        if response.next_action not in {
            "review",
            "wait",
            "continue",
        }:
            errors.append(
                "non-final response requires an actionable next_action"
            )

    elif response.status == "not_found":
        if response.next_action not in {
            "review",
            "retry",
            "none",
        }:
            errors.append(
                "not_found response has invalid next_action"
            )

    return ValidationResult(
        valid=not errors,
        errors=errors,
    )