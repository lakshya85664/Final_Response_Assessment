from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


ALLOWED = {
    "completed",
    "pending",
    "needs_review",
    "not_found",
}


class FinalResponse(BaseModel):
    """
    Public response contract for the final-response layer.

    The finalizer is responsible for formatting already-verified
    workflow results. It does not independently decide whether
    the underlying workflow action actually happened.
    """

    model_config = ConfigDict(extra="forbid")

    status: str
    message: str = Field(min_length=1, max_length=300)
    evidence: list[str]
    next_action: str = Field(min_length=1)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ALLOWED:
            raise ValueError("invalid public status")
        return value

    @field_validator("evidence")
    @classmethod
    def validate_evidence(cls, value: list[str]) -> list[str]:
        if any(
            not isinstance(item, str) or not item.strip()
            for item in value
        ):
            raise ValueError(
                "evidence items must be non-empty strings"
            )

        return value


def build_response(
    result: str,
    status: str,
    evidence: list[str],
    next_action: str,
) -> FinalResponse:
    """
    Build a validated final response from already-verified
    workflow information.
    """

    return FinalResponse(
        status=status,
        message=result,
        evidence=evidence,
        next_action=next_action,
    )


if __name__ == "__main__":
    response = build_response(
        "Report ready.",
        "completed",
        ["report:verified"],
        "review",
    )

    print(response.model_dump_json(indent=2))