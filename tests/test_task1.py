import pytest
from pydantic import ValidationError

from final_response import ALLOWED, FinalResponse, build_response


def test_success_response_matches_contract():
    response = build_response(
        "Report ready.",
        "completed",
        ["report:verified"],
        "review",
    )

    assert response.status == "completed"
    assert response.message == "Report ready."
    assert response.evidence == ["report:verified"]
    assert response.next_action == "review"


def test_all_public_statuses_are_allowed():
    for status in ALLOWED:
        response = FinalResponse(
            status=status,
            message="Status recorded.",
            evidence=["run:verified"],
            next_action="continue",
        )

        assert response.status == status


def test_invalid_status_is_rejected():
    with pytest.raises(
        ValidationError,
        match="invalid public status",
    ):
        FinalResponse(
            status="success",
            message="Done.",
            evidence=["run:verified"],
            next_action="continue",
        )


def test_message_over_300_characters_is_rejected():
    with pytest.raises(ValidationError):
        FinalResponse(
            status="completed",
            message="x" * 301,
            evidence=["run:verified"],
            next_action="continue",
        )


def test_required_fields_are_enforced():
    with pytest.raises(ValidationError):
        FinalResponse(
            status="completed",
            message="Done.",
            evidence=["run:verified"],
        )