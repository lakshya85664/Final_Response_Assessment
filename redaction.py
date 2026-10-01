from __future__ import annotations

import re


class RedactionError(ValueError):
    """Raised when redaction input is invalid."""


# Patterns are ordered from more specific to more general.
REDACTION_PATTERNS = [
    (
        re.compile(
            r"(?i)(authorization\s*[:=]\s*)(Bearer\s+[A-Za-z0-9_\-\.]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(api[_-]?key\s*[:=]\s*)(?!\[REDACTED\])([A-Za-z0-9_\-\.]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(bearer\s+)(?!\[REDACTED\])([A-Za-z0-9_\-\.]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(authorization\s*[:=]\s*)(?!\[REDACTED\])([^\s,;]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(password\s*[:=]\s*)(?!\[REDACTED\])([^\s,;]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(token\s*[:=]\s*)(?!\[REDACTED\])([A-Za-z0-9_\-\.]+)"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(
            r"(?i)(card[_\s-]?number\s*[:=]\s*)(?!\[REDACTED\])(\d{12,19})"
        ),
        r"\1[REDACTED]",
    ),
]


def redact_text(text: str) -> str:
    """
    Remove known secret patterns from user-facing text.

    Redaction is deterministic and preserves the field name
    while replacing the sensitive value.
    """

    if not isinstance(text, str):
        raise RedactionError("redaction input must be a string")

    redacted = text

    for pattern, replacement in REDACTION_PATTERNS:
        redacted = pattern.sub(replacement, redacted)

    return redacted


def contains_secret(text: str) -> bool:
    """
    Return True if a known secret value is still present.

    The standard [REDACTED] placeholder is explicitly treated
    as safe and is not considered a secret.
    """

    if not isinstance(text, str):
        raise RedactionError("secret check input must be a string")

    for pattern, _ in REDACTION_PATTERNS:
        if pattern.search(text):
            return True

    return False