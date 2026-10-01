import pytest

from evidence_filter import Evidence, EvidenceError, filter_evidence


def test_accepted_evidence_is_returned():
    evidence = [
        Evidence(
            value="order:88213",
            accepted=True,
            source="order_service",
        )
    ]

    assert filter_evidence(evidence) == ["order:88213"]


def test_rejected_evidence_is_removed():
    evidence = [
        Evidence(
            value="order:88213",
            accepted=True,
            source="order_service",
        ),
        Evidence(
            value="model_guess:refund_complete",
            accepted=False,
            source="model",
        ),
    ]

    assert filter_evidence(evidence) == ["order:88213"]


def test_multiple_accepted_evidence_items_are_preserved():
    evidence = [
        Evidence(
            value="order:88213",
            accepted=True,
            source="order_service",
        ),
        Evidence(
            value="status:verified",
            accepted=True,
            source="workflow_validator",
        ),
    ]

    assert filter_evidence(evidence) == [
        "order:88213",
        "status:verified",
    ]


def test_empty_evidence_value_is_rejected():
    evidence = [
        Evidence(
            value="",
            accepted=True,
            source="order_service",
        )
    ]

    with pytest.raises(
        EvidenceError,
        match="evidence value cannot be empty",
    ):
        filter_evidence(evidence)


def test_empty_source_is_rejected():
    evidence = [
        Evidence(
            value="order:88213",
            accepted=True,
            source="",
        )
    ]

    with pytest.raises(
        EvidenceError,
        match="evidence source cannot be empty",
    ):
        filter_evidence(evidence)