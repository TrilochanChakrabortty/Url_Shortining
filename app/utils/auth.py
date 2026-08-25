# from datetime import datetime, timedelta, timezone

# from passlib.context import CryptContext
# from jose import jwt, JWTError

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from sqlalchemy.orm import Session

# from app.config import SECRET_KEY, ALGORITHM
# from app.database import get_db
# from app import models


# # ============================================================
# # PASSWORD HASHING
# # ============================================================

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# # ============================================================
# # JWT / BEARER AUTHENTICATION
# # ============================================================

# security = HTTPBearer(auto_error=False)


# # ============================================================
# # PASSWORD FUNCTIONS
# # ============================================================

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)


# def verify_password(
#     plain_password: str,
#     hashed_password: str
# ) -> bool:
#     return pwd_context.verify(
#         plain_password,
#         hashed_password
#     )


# # ============================================================
# # CREATE JWT ACCESS TOKEN
# # ============================================================

# def create_access_token(
#     data: dict,
#     expires_delta: timedelta | None = None
# ):
#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=60)

#     to_encode.update({
#         "exp": expire
#     })

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# # ============================================================
# # COMMON AUTHENTICATION EXCEPTION
# # ============================================================

# def credentials_exception():
#     return HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={
#             "WWW-Authenticate": "Bearer"
#         }
#     )


# # ============================================================
# # GET CURRENT USER
# # ============================================================

# def get_current_user(
#     credentials: HTTPAuthorizationCredentials | None = Depends(security),
#     db: Session = Depends(get_db)
# ):

#     auth_exception = credentials_exception()

#     # --------------------------------------------------------
#     # NO AUTHORIZATION HEADER
#     # --------------------------------------------------------

#     if credentials is None:

#         print("\n========== AUTH DEBUG ==========")
#         print("AUTH ERROR: NO CREDENTIALS RECEIVED")
#         print("================================\n")

#         raise auth_exception

#     # --------------------------------------------------------
#     # TOKEN RECEIVED
#     # --------------------------------------------------------

#     token = credentials.credentials

#     print("\n========== AUTH DEBUG ==========")
#     print(
#         "TOKEN RECEIVED:",
#         token[:30] + "..." if token else "EMPTY"
#     )

#     # --------------------------------------------------------
#     # DECODE JWT
#     # --------------------------------------------------------

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         print("JWT DECODE SUCCESS")
#         print("JWT PAYLOAD:", payload)

#         user_id = payload.get("sub")

#         print("USER ID FROM TOKEN:", user_id)

#         if user_id is None:

#             print("AUTH ERROR: USER ID IS MISSING")
#             print("================================\n")

#             raise auth_exception

#     except JWTError as e:

#         print(
#             "JWT VALIDATION ERROR:",
#             repr(e)
#         )

#         print("================================\n")

#         raise auth_exception

#     # --------------------------------------------------------
#     # CONVERT USER ID
#     # --------------------------------------------------------

#     try:

#         user_id = int(user_id)

#     except (ValueError, TypeError) as e:

#         print(
#             "AUTH ERROR: INVALID USER ID:",
#             repr(e)
#         )

#         print("================================\n")

#         raise auth_exception

#     # --------------------------------------------------------
#     # DATABASE USER LOOKUP
#     # --------------------------------------------------------

#     try:

#         user = (
#             db.query(models.User)
#             .filter(
#                 models.User.id == user_id
#             )
#             .first()
#         )

#         print(
#             "DATABASE USER RESULT:",
#             user
#         )

#     except Exception as e:

#         print(
#             "DATABASE AUTH ERROR:",
#             repr(e)
#         )

#         print("================================\n")

#         raise auth_exception

#     # --------------------------------------------------------
#     # USER NOT FOUND
#     # --------------------------------------------------------

#     if user is None:

#         print(
#             "JWT USER NOT FOUND:",
#             user_id
#         )

#         print("================================\n")

#         raise auth_exception

#     # --------------------------------------------------------
#     # AUTHENTICATION SUCCESS
#     # --------------------------------------------------------

#     print(
#         "AUTH SUCCESS:",
#         user.username
#     )

#     print("================================\n")

#     return user


# # ============================================================
# # OPTIONAL CURRENT USER
# # ============================================================

# def get_optional_current_user(
#     credentials: HTTPAuthorizationCredentials | None = Depends(security),
#     db: Session = Depends(get_db),
# ):
#     print("\n========== OPTIONAL AUTH DEBUG ==========")

#     # ========================================================
#     # CONDITION 1: NO CREDENTIALS
#     # ========================================================

#     if credentials is None:

#         print("AUTH CONDITION 1 FAILED")
#         print("REASON: NO AUTHORIZATION CREDENTIALS")
#         print("========================================\n")

#         return None

#     print("CONDITION 1 PASSED: CREDENTIALS RECEIVED")

#     # ========================================================
#     # GET TOKEN
#     # ========================================================

#     token = credentials.credentials

#     print(
#         "TOKEN RECEIVED:",
#         token[:30] + "..."
#         if token
#         else "EMPTY TOKEN"
#     )

#     # ========================================================
#     # CONDITION 2: JWT DECODE
#     # ========================================================

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={
#             "WWW-Authenticate": "Bearer"
#         },
#     )

#     try:

#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#         )

#         print("CONDITION 2 PASSED: JWT DECODE SUCCESS")
#         print("JWT PAYLOAD:", payload)

#     except JWTError as e:

#         print("AUTH CONDITION 2 FAILED")
#         print("REASON: JWT DECODE/VALIDATION FAILED")
#         print("JWT ERROR:", repr(e))
#         print("========================================\n")

#         raise credentials_exception

#     # ========================================================
#     # CONDITION 3: SUB
#     # ========================================================

#     user_id = payload.get("sub")

#     print("USER ID FROM TOKEN:", user_id)

#     if user_id is None:

#         print("AUTH CONDITION 3 FAILED")
#         print("REASON: 'sub' IS MISSING FROM JWT")
#         print("========================================\n")

#         raise credentials_exception

#     print("CONDITION 3 PASSED: SUB EXISTS")

#     # ========================================================
#     # CONVERT USER ID
#     # ========================================================

#     try:

#         user_id = int(user_id)

#     except (ValueError, TypeError) as e:

#         print("AUTH CONDITION 3 FAILED")
#         print("REASON: INVALID USER ID IN SUB")
#         print("VALUE:", user_id)
#         print("ERROR:", repr(e))
#         print("========================================\n")

#         raise credentials_exception

#     print("USER ID:", user_id)

#     # ========================================================
#     # CONDITION 4: DATABASE USER
#     # ========================================================

#     try:

#         print("SEARCHING USER ID:", user_id)

#         user = (
#             db.query(models.User)
#             .filter(
#                 models.User.id == user_id
#             )
#             .first()
#         )

#         print(
#             "DATABASE USER RESULT:",
#             user
#         )

#     except Exception as e:

#         print("AUTH CONDITION 4 FAILED")
#         print("REASON: DATABASE ERROR")
#         print("DATABASE ERROR:", repr(e))
#         print("========================================\n")

#         raise credentials_exception

#     # ========================================================
#     # USER NOT FOUND
#     # ========================================================

#     if user is None:

#         print("AUTH CONDITION 4 FAILED")
#         print("REASON: USER NOT FOUND")
#         print("USER ID:", user_id)
#         print("========================================\n")

#         raise credentials_exception

#     # ========================================================
#     # EVERYTHING PASSED
#     # ========================================================

#     print("CONDITION 4 PASSED: USER FOUND")
#     print("AUTH SUCCESS:", user.username)
#     print("========================================\n")

#     return user

from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db
from app import models


# ============================================================
# BCRYPT
# ============================================================

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ============================================================
# ARGON2ID
# ============================================================

argon2_hasher = Argon2Hasher(
    memory_cost=32768,   # 32 MB
    time_cost=3,
    parallelism=4,
)

argon2_context = PasswordHash(
    (argon2_hasher,)
)


# ============================================================
# HTTP AUTHENTICATION
# ============================================================

security = HTTPBearer(
    auto_error=False
)


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash new passwords using Argon2id.

    New users will therefore receive Argon2id
    hashes instead of bcrypt hashes.
    """

    return argon2_context.hash(password)


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password against either:

    1. Existing bcrypt hash
    2. Argon2id hash

    This allows old users and new users
    to authenticate during migration.
    """

    # --------------------------------------------------------
    # Existing bcrypt user
    # --------------------------------------------------------

    if hashed_password.startswith(
        ("$2a$", "$2b$", "$2y$")
    ):

        return bcrypt_context.verify(
            plain_password,
            hashed_password,
        )

    # --------------------------------------------------------
    # Argon2id user
    # --------------------------------------------------------

    if hashed_password.startswith(
        "$argon2id$"
    ):

        try:

            return argon2_context.verify(
                plain_password,
                hashed_password,
            )

        except Exception:

            return False

    # --------------------------------------------------------
    # Unknown hash format
    # --------------------------------------------------------

    return False


# ============================================================
# CHECK WHETHER HASH NEEDS MIGRATION
# ============================================================

def needs_argon2_migration(
    hashed_password: str,
) -> bool:
    """
    Returns True when the stored password is
    still using bcrypt.
    """

    return hashed_password.startswith(
        ("$2a$", "$2b$", "$2y$")
    )


# ============================================================
# MIGRATE BCRYPT → ARGON2ID
# ============================================================

def migrate_password_to_argon2(
    plain_password: str,
) -> str:
    """
    Generate a new Argon2id hash from the
    user's verified plaintext password.

    This function is called only after
    successful bcrypt verification.
    """

    return argon2_context.hash(
        plain_password
    )


# ============================================================
# JWT CREATION
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    """
    Create JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:

        expire = (
            datetime.now(timezone.utc)
            + expires_delta
        )

    else:

        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=60)
        )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# REQUIRED CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):
    """
    Validate JWT and return the current user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    # --------------------------------------------------------
    # Missing credentials
    # --------------------------------------------------------

    if credentials is None:

        raise credentials_exception

    token = credentials.credentials

    # --------------------------------------------------------
    # Decode JWT
    # --------------------------------------------------------

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            
            print("JWT VALIDATED BUT SUB IS MISSING")

            raise credentials_exception

    except JWTError as e:

        print("========================================")
        print("JWT VALIDATION FAILED")
        print("JWT ERROR:", repr(e))
        print("========================================")

        raise credentials_exception

    # --------------------------------------------------------
    # Convert user ID
    # --------------------------------------------------------

    try:

        user_id = int(user_id)

    except (ValueError, TypeError):

        raise credentials_exception

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = (
        db.query(models.User)
        .filter(
            models.User.id == user_id
        )
        .first()
    )

    if user is None:

        raise credentials_exception

    return user


# ============================================================
# OPTIONAL CURRENT USER
# ============================================================

def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        security
    ),
    db: Session = Depends(get_db),
):
    """
    Validate JWT when supplied.

    Returns:

        User object
            if valid JWT is supplied.

        None
            if no JWT is supplied.

    Invalid JWT still results in 401.
    """

    print(
        "\n========== OPTIONAL AUTH DEBUG =========="
    )

    # ========================================================
    # CONDITION 1
    # ========================================================

    if credentials is None:

        print(
            "AUTH CONDITION 1 FAILED"
        )

        print(
            "REASON: NO AUTHORIZATION CREDENTIALS"
        )

        print(
            "========================================\n"
        )

        return None

    print(
        "CONDITION 1 PASSED: "
        "CREDENTIALS RECEIVED"
    )

    # ========================================================
    # TOKEN
    # ========================================================

    token = credentials.credentials

    print(
        "TOKEN RECEIVED:",
        (
            token[:30] + "..."
            if token
            else "EMPTY TOKEN"
        )
    )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    # ========================================================
    # CONDITION 2
    # JWT DECODE
    # ========================================================

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        print(
            "CONDITION 2 PASSED: "
            "JWT DECODE SUCCESS"
        )

        print(
            "JWT PAYLOAD:",
            payload
        )

    except JWTError as e:

        print(
            "AUTH CONDITION 2 FAILED"
        )

        print(
            "REASON: "
            "JWT DECODE/VALIDATION FAILED"
        )

        print(
            "JWT ERROR:",
            repr(e)
        )

        print(
            "========================================\n"
        )

        raise credentials_exception

    # ========================================================
    # CONDITION 3
    # SUB
    # ========================================================

    user_id = payload.get("sub")

    print(
        "USER ID FROM TOKEN:",
        user_id
    )

    if user_id is None:

        print(
            "AUTH CONDITION 3 FAILED"
        )

        print(
            "REASON: 'sub' IS MISSING FROM JWT"
        )

        print(
            "========================================\n"
        )

        raise credentials_exception

    print(
        "CONDITION 3 PASSED: SUB EXISTS"
    )

    # ========================================================
    # USER ID
    # ========================================================

    try:

        user_id = int(user_id)

    except (ValueError, TypeError) as e:

        print(
            "AUTH CONDITION 3 FAILED"
        )

        print(
            "REASON: INVALID USER ID"
        )

        print(
            "VALUE:",
            user_id
        )

        print(
            "ERROR:",
            repr(e)
        )

        print(
            "========================================\n"
        )

        raise credentials_exception

    print(
        "USER ID:",
        user_id
    )

    # ========================================================
    # CONDITION 4
    # DATABASE USER
    # ========================================================

    try:

        print(
            "SEARCHING USER ID:",
            user_id
        )

        user = (
            db.query(models.User)
            .filter(
                models.User.id == user_id
            )
            .first()
        )

        print(
            "DATABASE USER RESULT:",
            user
        )

    except Exception as e:

        print(
            "AUTH CONDITION 4 FAILED"
        )

        print(
            "REASON: DATABASE ERROR"
        )

        print(
            "DATABASE ERROR:",
            repr(e)
        )

        print(
            "========================================\n"
        )

        raise credentials_exception

    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if user is None:

        print(
            "AUTH CONDITION 4 FAILED"
        )

        print(
            "REASON: USER NOT FOUND"
        )

        print(
            "USER ID:",
            user_id
        )

        print(
            "========================================\n"
        )

        raise credentials_exception

    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "CONDITION 4 PASSED: USER FOUND"
    )

    print(
        "AUTH SUCCESS:",
        user.username
    )

    print(
        "========================================\n"
    )

    return user