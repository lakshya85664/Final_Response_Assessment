import pytest

from evidence_filter import Evidence
from final_response import FinalResponse
from finalizer import FinalizationError, finalize


def test_completed_output_is_produced():
    response = finalize(
        result="Report ready.",
        status="completed",
        evidence=[
            Evidence(
                value="report:verified",
                accepted=True,
                source="report_service",
            )
        ],
        next_action="review",
    )

    assert isinstance(response, FinalResponse)
    assert response.status == "completed"
    assert response.message == "Report ready."
    assert response.evidence == ["report:verified"]
    assert response.next_action == "review"


def test_pending_output_is_actionable():
    response = finalize(
        result="Approval is pending.",
        status="pending",
        evidence=[
            Evidence(
                value="approval:pending",
                accepted=True,
                source="approval_service",
            )
        ],
        next_action="review",
    )

    assert response.status == "pending"
    assert response.next_action == "review"


def test_unaccepted_evidence_never_reaches_output():
    response = finalize(
        result="Report ready.",
        status="completed",
        evidence=[
            Evidence(
                value="report:verified",
                accepted=True,
                source="report_service",
            ),
            Evidence(
                value="model_guess:report_complete",
                accepted=False,
                source="model",
            ),
        ],
        next_action="review",
    )

    assert response.evidence == ["report:verified"]
    assert "model_guess:report_complete" not in response.evidence


def test_secret_is_redacted_in_final_output():
    response = finalize(
        result="Report ready. api_key=sk-test-example-12345",
        status="completed",
        evidence=[
            Evidence(
                value="api_key=sk-secret-example",
                accepted=True,
                source="internal_service",
            )
        ],
        next_action="review",
    )

    assert "sk-test-example-12345" not in response.message
    assert "sk-secret-example" not in response.evidence
    assert "[REDACTED]" in response.message
    assert "[REDACTED]" in response.evidence[0]


def test_missing_accepted_evidence_blocks_finalization():
    with pytest.raises(
        FinalizationError,
        match="without accepted evidence",
    ):
        finalize(
            result="Report ready.",
            status="completed",
            evidence=[
                Evidence(
                    value="model_guess:complete",
                    accepted=False,
                    source="model",
                )
            ],
            next_action="review",
        )