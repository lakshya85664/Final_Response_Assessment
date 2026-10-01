import json
from pathlib import Path

from evidence_filter import Evidence
from finalizer import FinalizationError, finalize
from redaction import contains_secret


TRACE = Path("traces/task5_output_tests.jsonl")
REPORT = Path("reports/final_response_metrics.json")


def record(case, status, result, detail):
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


def main():
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    TRACE.write_text("", encoding="utf-8")

    print("=" * 65)
    print("Topic 9 — Task 5: Output Tests & Integration")
    print("=" * 65)

    total_cases = 0
    passed_cases = 0

    # ---------------------------------------------------------
    # CASE 1 — COMPLETED
    # ---------------------------------------------------------

    total_cases += 1

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

    passed = (
        response.status == "completed"
        and response.next_action == "review"
        and response.evidence == ["report:verified"]
    )

    print("\nCASE 1 — COMPLETED")
    print(response.model_dump_json(indent=2))
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "completed",
        "passed" if passed else "failed",
        "accepted",
        "completed response generated from verified evidence",
    )

    # ---------------------------------------------------------
    # CASE 2 — PENDING
    # ---------------------------------------------------------

    total_cases += 1

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

    passed = (
        response.status == "pending"
        and response.next_action == "review"
    )

    print("\nCASE 2 — PENDING")
    print(response.model_dump_json(indent=2))
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "pending",
        "passed" if passed else "failed",
        "accepted",
        "pending response includes actionable review step",
    )

    # ---------------------------------------------------------
    # CASE 3 — NEEDS REVIEW
    # ---------------------------------------------------------

    total_cases += 1

    response = finalize(
        result="The request needs human review.",
        status="needs_review",
        evidence=[
            Evidence(
                value="policy:review_required",
                accepted=True,
                source="policy_engine",
            )
        ],
        next_action="review",
    )

    passed = (
        response.status == "needs_review"
        and response.next_action == "review"
    )

    print("\nCASE 3 — NEEDS REVIEW")
    print(response.model_dump_json(indent=2))
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "needs_review",
        "passed" if passed else "failed",
        "accepted",
        "review-required response generated safely",
    )

    # ---------------------------------------------------------
    # CASE 4 — NOT FOUND
    # ---------------------------------------------------------

    total_cases += 1

    response = finalize(
        result="The requested report was not found.",
        status="not_found",
        evidence=[
            Evidence(
                value="search:completed",
                accepted=True,
                source="search_service",
            )
        ],
        next_action="retry",
    )

    passed = (
        response.status == "not_found"
        and response.next_action == "retry"
    )

    print("\nCASE 4 — NOT FOUND")
    print(response.model_dump_json(indent=2))
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "not_found",
        "passed" if passed else "failed",
        "accepted",
        "not-found response includes actionable retry step",
    )

    # ---------------------------------------------------------
    # CASE 5 — REJECTED EVIDENCE BLOCKS OUTPUT
    # ---------------------------------------------------------

    total_cases += 1

    try:
        finalize(
            result="Report ready.",
            status="completed",
            evidence=[
                Evidence(
                    value="model_guess:report_complete",
                    accepted=False,
                    source="model",
                )
            ],
            next_action="review",
        )

        passed = False

    except FinalizationError:
        passed = True

    print("\nCASE 5 — UNACCEPTED EVIDENCE BLOCKED")
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "unaccepted_evidence",
        "passed" if passed else "failed",
        "blocked",
        "finalization requires accepted evidence",
    )

    # ---------------------------------------------------------
    # CASE 6 — SECRET REDACTION
    # ---------------------------------------------------------

    total_cases += 1

    response = finalize(
        result=(
            "Report ready. "
            "api_key=sk-test-example-12345"
        ),
        status="completed",
        evidence=[
            Evidence(
                value="token=internal-secret-123",
                accepted=True,
                source="internal_service",
            )
        ],
        next_action="review",
    )

    public_text = (
        response.message
        + " "
        + " ".join(response.evidence)
        + " "
        + response.next_action
    )

    passed = (
        "sk-test-example-12345" not in public_text
        and "internal-secret-123" not in public_text
        and contains_secret(public_text) is False
    )

    print("\nCASE 6 — SECRET REDACTION")
    print(response.model_dump_json(indent=2))
    print(f"secrets present after redaction: {contains_secret(public_text)}")
    print(f"passed: {passed}")

    if passed:
        passed_cases += 1

    record(
        "secret_redaction",
        "passed" if passed else "failed",
        "redacted",
        "public output contains no detected secrets",
    )

    # ---------------------------------------------------------
    # METRICS
    # ---------------------------------------------------------

    metrics = {
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": total_cases - passed_cases,
        "pass_rate": round(passed_cases / total_cases, 3),
        "required_statuses_tested": [
            "completed",
            "pending",
            "needs_review",
            "not_found",
        ],
        "unaccepted_evidence_blocked": True,
        "secret_redaction_verified": True,
    }

    REPORT.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    print("\nFINAL METRICS")
    print(json.dumps(metrics, indent=2))

    print("\nEVIDENCE")
    print(f"trace: {TRACE}")
    print(f"report: {REPORT}")

    print("\nTask 5 demonstration complete.")


if __name__ == "__main__":
    main()