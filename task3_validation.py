import json
from pathlib import Path

from final_response import FinalResponse
from response_validation import validate_response


TRACE = Path("traces/task3_validation.jsonl")


def record(case: str, status: str, result: str, errors: list[str]) -> None:
    with TRACE.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "case": case,
                    "status": status,
                    "result": result,
                    "errors": errors,
                }
            )
            + "\n"
        )


def run_case(
    name: str,
    response: FinalResponse,
) -> None:
    result = validate_response(response)

    print(f"\n{name}")
    print(f"valid: {result.valid}")

    if result.errors:
        print("errors:")
        for error in result.errors:
            print(f"  - {error}")
    else:
        print("errors: none")

    record(
        name.lower().replace(" ", "_"),
        "passed",
        "accepted" if result.valid else "rejected",
        result.errors,
    )


def main() -> None:
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")

    print("=" * 60)
    print("Topic 9 — Task 3: Response Validation")
    print("=" * 60)

    # ---------------------------------------------------------
    # CASE 1 — VALID COMPLETED RESPONSE
    # ---------------------------------------------------------

    run_case(
        "CASE 1 — VALID COMPLETED RESPONSE",
        FinalResponse(
            status="completed",
            message="Report ready.",
            evidence=["report:verified"],
            next_action="review",
        ),
    )

    # ---------------------------------------------------------
    # CASE 2 — EMPTY EVIDENCE
    # ---------------------------------------------------------

    run_case(
        "CASE 2 — EMPTY EVIDENCE",
        FinalResponse(
            status="completed",
            message="Report ready.",
            evidence=[],
            next_action="review",
        ),
    )

    # ---------------------------------------------------------
    # CASE 3 — INVALID PENDING ACTION
    # ---------------------------------------------------------

    run_case(
        "CASE 3 — INVALID PENDING ACTION",
        FinalResponse(
            status="pending",
            message="Approval is pending.",
            evidence=["approval:pending"],
            next_action="done",
        ),
    )

    # ---------------------------------------------------------
    # CASE 4 — INVALID COMPLETED ACTION
    # ---------------------------------------------------------

    run_case(
        "CASE 4 — INVALID COMPLETED ACTION",
        FinalResponse(
            status="completed",
            message="Report ready.",
            evidence=["report:verified"],
            next_action="retry",
        ),
    )

    # ---------------------------------------------------------
    # CASE 5 — VALID NOT FOUND RESPONSE
    # ---------------------------------------------------------

    run_case(
        "CASE 5 — VALID NOT FOUND RESPONSE",
        FinalResponse(
            status="not_found",
            message="The requested report was not found.",
            evidence=["search:completed"],
            next_action="retry",
        ),
    )

    # ---------------------------------------------------------
    # TRACE
    # ---------------------------------------------------------

    print("\nTRACE")
    print(TRACE)

    print("\nTask 3 demonstration complete.")


if __name__ == "__main__":
    main()