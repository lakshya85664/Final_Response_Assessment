import json
from pathlib import Path

from redaction import contains_secret, redact_text


TRACE = Path("traces/task4_redaction.jsonl")


def record(case: str, status: str, original: str, redacted: str) -> None:
    with TRACE.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "case": case,
                    "status": status,
                    "original_contains_secret": contains_secret(original),
                    "redacted_output": redacted,
                    "redacted_contains_secret": contains_secret(redacted),
                }
            )
            + "\n"
        )


def run_case(name: str, text: str) -> None:
    redacted = redact_text(text)
    safe = not contains_secret(redacted)

    print(f"\n{name}")
    print(f"original: {text}")
    print(f"redacted: {redacted}")
    print(f"secret removed: {safe}")

    record(
        name.lower().replace(" ", "_"),
        "passed" if safe else "failed",
        text,
        redacted,
    )


def main() -> None:
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    TRACE.write_text("", encoding="utf-8")

    print("=" * 60)
    print("Topic 9 — Task 4: Redaction")
    print("=" * 60)

    run_case(
        "CASE 1 — API KEY",
        "api_key=sk-test-example-12345",
    )

    run_case(
        "CASE 2 — BEARER TOKEN",
        "Authorization: Bearer abc123SECRET",
    )

    run_case(
        "CASE 3 — PASSWORD",
        "password=my-secret-password",
    )

    run_case(
        "CASE 4 — CARD NUMBER",
        "card_number=4111111111111111",
    )

    run_case(
        "CASE 5 — MULTIPLE SECRETS",
        (
            "api_key=sk-example123 "
            "password=super-secret "
            "card_number=4111111111111111"
        ),
    )

    print("\nSAFETY BOUNDARY")
    print("Sensitive values are replaced before public output.")

    print("\nTRACE")
    print(TRACE)

    print("\nTask 4 demonstration complete.")


if __name__ == "__main__":
    main()