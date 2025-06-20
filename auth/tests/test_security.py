import re
import hashlib
import pytest
from modules.api.auth.security import (
    anonymize,
    hash_token,
    hash_password,
    verify_password,
)


def test_anonymize():
    name = "John"
    hashed = anonymize(name)
    expected = hashlib.sha256(name.encode("utf-8")).hexdigest()
    assert hashed == expected
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 hex string length


def test_hash_token():
    token = "sensitive_refresh_token"
    hashed = hash_token(token)
    expected = hashlib.sha256(token.encode("utf-8")).hexdigest()
    assert hashed == expected
    assert isinstance(hashed, str)
    assert len(hashed) == 64


def test_hash_password_and_verify():
    password = "MySecurePassword123!"
    hashed = hash_password(password)

    # The hashed password should look like a bcrypt hash
    assert isinstance(hashed, str)
    assert re.match(r"^\$2[aby]?\$[0-9]{2}\$.{53}$", hashed)

    # verify_password should return True with the correct password
    assert verify_password(password, hashed)

    # and False with an incorrect password
    assert not verify_password("WrongPassword", hashed)


def test_verify_password_with_invalid_hash():
    with pytest.raises(ValueError):
        # Invalid bcrypt hash format
        verify_password("password", "not_a_valid_bcrypt_hash")
