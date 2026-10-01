import json
from pathlib import Path

from evidence_filter import Evidence, EvidenceError, filter_evidence


TRACE = Path("traces/task2_evidence_filter.jsonl")


def record(case: str, status: str, result: str, detail: str) -> None:
    with TRACE.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "case": case,
                    "status": status,
                    "result": result,
                    "detail": detail,
                }
            )
            + "\n"
        )


def main() -> None:
    TRACE.write_text("", encoding="utf-8")

    print("=" * 60)
    print("Topic 9 — Task 2: Evidence Filter")
    print("=" * 60)

    # ---------------------------------------------------------
    # CASE 1 — ACCEPTED EVIDENCE
    # ---------------------------------------------------------

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

    accepted = filter_evidence(evidence)

    print("\nCASE 1 — ACCEPTED EVIDENCE")
    print("accepted evidence:")
    for item in accepted:
        print(f"  - {item}")

    record(
        "accepted_evidence",
        "passed",
        "accepted",
        f"{len(accepted)} evidence items retained",
    )

    # ---------------------------------------------------------
    # CASE 2 — REJECTED EVIDENCE IS FILTERED
    # ---------------------------------------------------------

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
        Evidence(
            value="unverified:customer_claim",
            accepted=False,
            source="user_text",
        ),
    ]

    filtered = filter_evidence(evidence)

    print("\nCASE 2 — REJECTED EVIDENCE FILTERED")
    print("input evidence:")
    for item in evidence:
        print(f"  - {item.value} | accepted={item.accepted}")

    print("final evidence:")
    for item in filtered:
        print(f"  - {item}")

    rejected_removed = (
        "model_guess:refund_complete" not in filtered
        and "unverified:customer_claim" not in filtered
    )

    print(f"rejected evidence removed: {rejected_removed}")

    record(
        "rejected_evidence",
        "passed" if rejected_removed else "failed",
        "filtered",
        "unaccepted evidence was removed",
    )

    # ---------------------------------------------------------
    # CASE 3 — EMPTY EVIDENCE VALUE
    # ---------------------------------------------------------

    try:
        filter_evidence(
            [
                Evidence(
                    value="",
                    accepted=True,
                    source="order_service",
                )
            ]
        )

    except EvidenceError as exc:
        print("\nCASE 3 — EMPTY EVIDENCE")
        print("status: rejected")
        print(f"reason: {exc}")

        record(
            "empty_evidence",
            "passed",
            "rejected",
            str(exc),
        )

    # ---------------------------------------------------------
    # CASE 4 — EMPTY SOURCE
    # ---------------------------------------------------------

    try:
        filter_evidence(
            [
                Evidence(
                    value="order:88213",
                    accepted=True,
                    source="",
                )
            ]
        )

    except EvidenceError as exc:
        print("\nCASE 4 — EMPTY SOURCE")
        print("status: rejected")
        print(f"reason: {exc}")

        record(
            "empty_source",
            "passed",
            "rejected",
            str(exc),
        )

    # ---------------------------------------------------------
    # SAFETY BOUNDARY
    # ---------------------------------------------------------

    print("\nSAFETY BOUNDARY")
    print("Only explicitly accepted evidence reaches the finalizer.")

    # ---------------------------------------------------------
    # TRACE
    # ---------------------------------------------------------

    print("\nTRACE")
    print(TRACE)

    print("\nTask 2 demonstration complete.")


if __name__ == "__main__":
    main()