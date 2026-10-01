import pytest

from final_response import FinalResponse
from response_validation import validate_response


def test_valid_completed_response_passes():
    response = FinalResponse(
        status="completed",
        message="Report ready.",
        evidence=["report:verified"],
        next_action="review",
    )

    result = validate_response(response)

    assert result.valid is True
    assert result.errors == []


def test_empty_evidence_is_rejected():
    response = FinalResponse(
        status="completed",
        message="Report ready.",
        evidence=[],
        next_action="review",
    )

    result = validate_response(response)

    assert result.valid is False
    assert "at least one evidence item is required" in result.errors


def test_pending_requires_actionable_next_action():
    response = FinalResponse(
        status="pending",
        message="Approval is pending.",
        evidence=["approval:pending"],
        next_action="done",
    )

    result = validate_response(response)

    assert result.valid is False
    assert (
        "non-final response requires an actionable next_action"
        in result.errors
    )


def test_completed_response_rejects_invalid_action():
    response = FinalResponse(
        status="completed",
        message="Report ready.",
        evidence=["report:verified"],
        next_action="retry",
    )

    result = validate_response(response)

    assert result.valid is False
    assert (
        "completed response has invalid next_action"
        in result.errors
    )


def test_not_found_can_request_retry():
    response = FinalResponse(
        status="not_found",
        message="The requested report was not found.",
        evidence=["search:completed"],
        next_action="retry",
    )

    result = validate_response(response)

    assert result.valid is True
    assert result.errors == []