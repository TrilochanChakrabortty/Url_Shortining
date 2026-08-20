import pytest

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.auth import get_current_user


# ============================================================
# PHASE 6.9.1
# INVALID JWT TOKEN SHOULD BE REJECTED
# ============================================================

def test_get_current_user_rejects_invalid_token(db):

    class FakeCredentials:

        credentials = "this.is.an.invalid.token"

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=FakeCredentials(),
            db=db
        )

    assert exc_info.value.status_code == 401

    assert (
        exc_info.value.detail
        == "Could not validate credentials"
    )
    
import pytest

from fastapi import HTTPException
from jose import jwt

from app.utils.auth import get_current_user
from app.config import SECRET_KEY, ALGORITHM


# ============================================================
# PHASE 6.9.2
# JWT WITHOUT SUB CLAIM SHOULD BE REJECTED
# ============================================================

def test_get_current_user_rejects_token_without_sub(db):

    # Create a valid JWT but without "sub"
    token = jwt.encode(
        {
            "role": "user"
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    class FakeCredentials:
        credentials = token

    # The function should raise HTTPException
    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=FakeCredentials(),
            db=db
        )

    # Verify response
    assert exc_info.value.status_code == 401

    assert (
        exc_info.value.detail
        == "Could not validate credentials"
    )
    
# ============================================================
# PHASE 6.9.3
# TOKEN WITH NONEXISTENT USER SHOULD BE REJECTED
# ============================================================

def test_get_current_user_rejects_nonexistent_user(db):

    # Create a valid JWT with a user ID
    # that does not exist in the test database
    token = jwt.encode(
        {
            "sub": "999999999"
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    class FakeCredentials:
        credentials = token

    # Function should reject the token because
    # the user does not exist
    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            credentials=FakeCredentials(),
            db=db
        )

    # Verify unauthorized response
    assert exc_info.value.status_code == 401

    assert (
        exc_info.value.detail
        == "Could not validate credentials"
    )
    
from app import models


# ============================================================
# TEST 4
# VALID TOKEN SHOULD RETURN THE CORRECT USER
# ============================================================

def test_get_current_user_returns_valid_user(db):

    # ========================================================
    # STEP 1: CREATE A USER IN TEST DATABASE
    # ========================================================

    user = models.User(
        username="validtokenuser",
        email="validtoken@example.com",
        password_hash="hashed_password"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # ========================================================
    # STEP 2: CREATE JWT WITH USER ID
    # ========================================================

    token = jwt.encode(
        {
            "sub": str(user.id)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    # ========================================================
    # STEP 3: CREATE FAKE CREDENTIALS
    # ========================================================

    class FakeCredentials:
        credentials = token

    # ========================================================
    # STEP 4: CALL get_current_user()
    # ========================================================

    current_user = get_current_user(
        credentials=FakeCredentials(),
        db=db
    )

    # ========================================================
    # STEP 5: VERIFY CORRECT USER IS RETURNED
    # ========================================================

    assert current_user is not None

    assert current_user.id == user.id

    assert current_user.username == "validtokenuser"

    assert current_user.email == "validtoken@example.com"
    
# ============================================================
# PHASE 6.10.1
# INVALID URL SHOULD BE REJECTED
# ============================================================

def test_shorten_invalid_url_returns_422(client):

    response = client.post(
        "/shorten",
        json={
            "url": "this-is-not-a-valid-url"
        }
    )

    assert response.status_code == 422
    
# ============================================================
# PHASE 6.10.2
# EMPTY URL SHOULD BE REJECTED
# ============================================================

def test_shorten_empty_url_returns_422(client):

    response = client.post(
        "/shorten",
        json={
            "url": ""
        }
    )

    assert response.status_code == 422
    
# ============================================================
# PHASE 6.10.3
# MISSING URL FIELD SHOULD BE REJECTED
# ============================================================

def test_shorten_without_url_returns_422(client):

    response = client.post(
        "/shorten",
        json={}
    )

    assert response.status_code == 422
    
# ============================================================
# PHASE 6.10.4
# NULL URL SHOULD BE REJECTED
# ============================================================

def test_shorten_null_url_returns_422(client):

    response = client.post(
        "/shorten",
        json={
            "url": None
        }
    )

    assert response.status_code == 422