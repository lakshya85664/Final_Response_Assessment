import json
from pathlib import Path

from pydantic import ValidationError

from final_response import FinalResponse, build_response


TRACE = Path("traces/task1_response_schema.jsonl")


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
    print("Topic 9 — Task 1: Response Schema")
    print("=" * 60)

    # ---------------------------------------------------------
    # CASE 1 — VALID SUCCESS RESPONSE
    # ---------------------------------------------------------

    response = build_response(
        "Report ready.",
        "completed",
        ["report:verified"],
        "review",
    )

    print("\nCASE 1 — VALID SUCCESS RESPONSE")
    print(response.model_dump_json(indent=2))

    record(
        "valid_success",
        "passed",
        "accepted",
        "valid completed response",
    )

    # ---------------------------------------------------------
    # CASE 2 — INVALID PUBLIC STATUS
    # ---------------------------------------------------------

    try:
        FinalResponse(
            status="success",
            message="Done.",
            evidence=["run:verified"],
            next_action="continue",
        )

    except ValidationError as exc:
        print("\nCASE 2 — INVALID STATUS")
        print("status: rejected")
        print("reason: invalid public status")

        record(
            "invalid_status",
            "passed",
            "rejected",
            str(exc.errors()[0]["msg"]),
        )

    # ---------------------------------------------------------
    # CASE 3 — MESSAGE TOO LONG
    # ---------------------------------------------------------

    try:
        FinalResponse(
            status="completed",
            message="x" * 301,
            evidence=["run:verified"],
            next_action="continue",
        )

    except ValidationError:
        print("\nCASE 3 — MESSAGE LENGTH")
        print("status: rejected")
        print("reason: message exceeds 300 characters")

        record(
            "message_length",
            "passed",
            "rejected",
            "max_length=300",
        )

    # ---------------------------------------------------------
    # CASE 4 — MISSING REQUIRED FIELD
    # ---------------------------------------------------------

    try:
        FinalResponse(
            status="completed",
            message="Done.",
            evidence=["run:verified"],
        )

    except ValidationError:
        print("\nCASE 4 — MISSING REQUIRED FIELD")
        print("status: rejected")
        print("reason: next_action is required")

        record(
            "missing_field",
            "passed",
            "rejected",
            "next_action is required",
        )

    # ---------------------------------------------------------
    # PUBLIC STATUS VOCABULARY
    # ---------------------------------------------------------

    print("\nPUBLIC STATUS VOCABULARY")
    print("completed")
    print("pending")
    print("needs_review")
    print("not_found")

    # ---------------------------------------------------------
    # TRACE
    # ---------------------------------------------------------

    print("\nTRACE")
    print(TRACE)

    print("\nTask 1 demonstration complete.")


if __name__ == "__main__":
    main()