from __future__ import annotations

from dataclasses import dataclass


class EvidenceError(ValueError):
    """Raised when evidence is invalid or unsafe."""


@dataclass(frozen=True)
class Evidence:
    """
    A piece of workflow evidence.

    accepted=True means the workflow has explicitly verified
    this evidence for use by the final-response layer.
    """

    value: str
    accepted: bool
    source: str


def filter_evidence(evidence: list[Evidence]) -> list[str]:
    """
    Return only accepted, non-empty evidence.

    The finalizer must not expose rejected or unverified evidence.
    """

    accepted: list[str] = []

    for item in evidence:
        if not isinstance(item, Evidence):
            raise EvidenceError("invalid evidence object")

        if not item.value.strip():
            raise EvidenceError("evidence value cannot be empty")

        if not item.source.strip():
            raise EvidenceError("evidence source cannot be empty")

        if item.accepted:
            accepted.append(item.value)

    return accepted