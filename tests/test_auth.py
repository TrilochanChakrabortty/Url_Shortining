from app.utils.auth import (
    hash_password,
    verify_password,
)

from datetime import timedelta

from jose import jwt

from app.config import SECRET_KEY, ALGORITHM
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

# ============================================================
# TEST PASSWORD HASH RETURNS STRING
# ============================================================

def test_hash_password_returns_string():

    password = "mypassword123"

    hashed_password = hash_password(password)

    assert isinstance(hashed_password, str)


# ============================================================
# TEST PASSWORD IS ACTUALLY HASHED
# ============================================================

def test_hash_password_is_not_plain_password():

    password = "mypassword123"

    hashed_password = hash_password(password)

    assert hashed_password != password


# ============================================================
# TEST PASSWORD HASH IS NOT EMPTY
# ============================================================

def test_hash_password_is_not_empty():

    password = "mypassword123"

    hashed_password = hash_password(password)

    assert hashed_password != ""


# ============================================================
# POSITIVE TEST: CORRECT PASSWORD
# ============================================================

def test_verify_correct_password():

    password = "mypassword123"

    # First create the hash
    hashed_password = hash_password(password)

    # Verify the original password
    result = verify_password(
        password,
        hashed_password
    )

    assert result is True


# ============================================================
# NEGATIVE TEST: WRONG PASSWORD
# ============================================================

def test_verify_wrong_password():

    correct_password = "mypassword123"
    wrong_password = "wrongpassword"

    # Create hash using the correct password
    hashed_password = hash_password(
        correct_password
    )

    # Try verifying with the wrong password
    result = verify_password(
        wrong_password,
        hashed_password
    )

    assert result is False
    
# ============================================================
# TEST ACCESS TOKEN CREATION
# ============================================================

def test_create_access_token_returns_string():

    data = {
        "sub": "1"
    }

    token = create_access_token(data)

    assert isinstance(token, str)
    assert token != ""
    
# ============================================================
# TEST ACCESS TOKEN CONTAINS USER DATA
# ============================================================

def test_create_access_token_contains_payload():

    data = {
        "sub": "1"
    }

    token = create_access_token(data)

    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert decoded_token["sub"] == "1"
    
# ============================================================
# TEST ACCESS TOKEN HAS EXPIRATION
# ============================================================

def test_create_access_token_has_expiration():

    data = {
        "sub": "1"
    }

    token = create_access_token(data)

    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert "exp" in decoded_token