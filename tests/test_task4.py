import pytest

from redaction import RedactionError, contains_secret, redact_text


def test_api_key_is_redacted():
    text = "api_key=sk-test-example-12345"

    result = redact_text(text)

    assert "[REDACTED]" in result
    assert "sk-test-example-12345" not in result
    assert contains_secret(result) is False


def test_bearer_token_is_redacted():
    text = "Authorization: Bearer abc123SECRET"

    result = redact_text(text)

    assert "[REDACTED]" in result
    assert "abc123SECRET" not in result
    assert contains_secret(result) is False


def test_password_is_redacted():
    text = "password=my-secret-password"

    result = redact_text(text)

    assert "[REDACTED]" in result
    assert "my-secret-password" not in result
    assert contains_secret(result) is False


def test_card_number_is_redacted():
    text = "card_number=4111111111111111"

    result = redact_text(text)

    assert "[REDACTED]" in result
    assert "4111111111111111" not in result
    assert contains_secret(result) is False


def test_non_string_input_is_rejected():
    with pytest.raises(
        RedactionError,
        match="redaction input must be a string",
    ):
        redact_text(12345)