# from datetime import datetime, timedelta, timezone

# from passlib.context import CryptContext
# from jose import jwt, JWTError

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from sqlalchemy.orm import Session

# from app.config import SECRET_KEY, ALGORITHM
# from app.database import get_db
# from app import models


# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# security = HTTPBearer(auto_error=False)


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

#     return jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={
#             "WWW-Authenticate": "Bearer"
#         }
#     )

#     if credentials is None:
#         raise credentials_exception

#     token = credentials.credentials

#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception

#     user = (
#         db.query(models.User)
#         .filter(models.User.id == int(user_id))
#         .first()
#     )

#     if user is None:
#         raise credentials_exception

#     return user
# # ============================================================
# # OPTIONAL CURRENT USER
# # ============================================================

# def get_optional_current_user(
#     credentials: HTTPAuthorizationCredentials | None = Depends(security),
#     db: Session = Depends(get_db),
# ):

#     print("\n========== OPTIONAL AUTH DEBUG ==========")

#     # --------------------------------------------------------
#     # NO TOKEN
#     # --------------------------------------------------------

#     if credentials is None:

#         print("NO CREDENTIALS RECEIVED")
#         print("========================================\n")

#         return None

#     # --------------------------------------------------------
#     # TOKEN RECEIVED
#     # --------------------------------------------------------

#     token = credentials.credentials

#     print("TOKEN RECEIVED:", token[:30], "...")

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={
#             "WWW-Authenticate": "Bearer"
#         },
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

#             print("USER ID IS MISSING")

#             raise credentials_exception

#     except JWTError as e:

#         print("JWT ERROR:", repr(e))

#         raise credentials_exception

#     # --------------------------------------------------------
#     # DATABASE LOOKUP
#     # --------------------------------------------------------

#     try:

#         user_id = int(user_id)

#         print("SEARCHING USER ID:", user_id)

#         user = (
#             db.query(models.User)
#             .filter(
#                 models.User.id == user_id
#             )
#             .first()
#         )

#         print("DATABASE USER RESULT:", user)

#     except Exception as e:

#         print("DATABASE ERROR:", repr(e))

#         raise credentials_exception

#     # --------------------------------------------------------
#     # USER NOT FOUND
#     # --------------------------------------------------------

#     if user is None:

#         print("USER NOT FOUND")

#         raise credentials_exception

#     print(
#         "AUTH SUCCESS:",
#         user.username
#     )

#     print("========================================\n")

#     return user

from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM
from app.database import get_db
from app import models


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ============================================================
# JWT / BEARER AUTHENTICATION
# ============================================================

security = HTTPBearer(auto_error=False)


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# CREATE JWT ACCESS TOKEN
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ============================================================
# COMMON AUTHENTICATION EXCEPTION
# ============================================================

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
):

    auth_exception = credentials_exception()

    # --------------------------------------------------------
    # NO AUTHORIZATION HEADER
    # --------------------------------------------------------

    if credentials is None:

        print("\n========== AUTH DEBUG ==========")
        print("AUTH ERROR: NO CREDENTIALS RECEIVED")
        print("================================\n")

        raise auth_exception

    # --------------------------------------------------------
    # TOKEN RECEIVED
    # --------------------------------------------------------

    token = credentials.credentials

    print("\n========== AUTH DEBUG ==========")
    print(
        "TOKEN RECEIVED:",
        token[:30] + "..." if token else "EMPTY"
    )

    # --------------------------------------------------------
    # DECODE JWT
    # --------------------------------------------------------

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("JWT DECODE SUCCESS")
        print("JWT PAYLOAD:", payload)

        user_id = payload.get("sub")

        print("USER ID FROM TOKEN:", user_id)

        if user_id is None:

            print("AUTH ERROR: USER ID IS MISSING")
            print("================================\n")

            raise auth_exception

    except JWTError as e:

        print(
            "JWT VALIDATION ERROR:",
            repr(e)
        )

        print("================================\n")

        raise auth_exception

    # --------------------------------------------------------
    # CONVERT USER ID
    # --------------------------------------------------------

    try:

        user_id = int(user_id)

    except (ValueError, TypeError) as e:

        print(
            "AUTH ERROR: INVALID USER ID:",
            repr(e)
        )

        print("================================\n")

        raise auth_exception

    # --------------------------------------------------------
    # DATABASE USER LOOKUP
    # --------------------------------------------------------

    try:

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
            "DATABASE AUTH ERROR:",
            repr(e)
        )

        print("================================\n")

        raise auth_exception

    # --------------------------------------------------------
    # USER NOT FOUND
    # --------------------------------------------------------

    if user is None:

        print(
            "JWT USER NOT FOUND:",
            user_id
        )

        print("================================\n")

        raise auth_exception

    # --------------------------------------------------------
    # AUTHENTICATION SUCCESS
    # --------------------------------------------------------

    print(
        "AUTH SUCCESS:",
        user.username
    )

    print("================================\n")

    return user


# ============================================================
# OPTIONAL CURRENT USER
# ============================================================

def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    print("\n========== OPTIONAL AUTH DEBUG ==========")

    # ========================================================
    # CONDITION 1: NO CREDENTIALS
    # ========================================================

    if credentials is None:

        print("AUTH CONDITION 1 FAILED")
        print("REASON: NO AUTHORIZATION CREDENTIALS")
        print("========================================\n")

        return None

    print("CONDITION 1 PASSED: CREDENTIALS RECEIVED")

    # ========================================================
    # GET TOKEN
    # ========================================================

    token = credentials.credentials

    print(
        "TOKEN RECEIVED:",
        token[:30] + "..."
        if token
        else "EMPTY TOKEN"
    )

    # ========================================================
    # CONDITION 2: JWT DECODE
    # ========================================================

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        print("CONDITION 2 PASSED: JWT DECODE SUCCESS")
        print("JWT PAYLOAD:", payload)

    except JWTError as e:

        print("AUTH CONDITION 2 FAILED")
        print("REASON: JWT DECODE/VALIDATION FAILED")
        print("JWT ERROR:", repr(e))
        print("========================================\n")

        raise credentials_exception

    # ========================================================
    # CONDITION 3: SUB
    # ========================================================

    user_id = payload.get("sub")

    print("USER ID FROM TOKEN:", user_id)

    if user_id is None:

        print("AUTH CONDITION 3 FAILED")
        print("REASON: 'sub' IS MISSING FROM JWT")
        print("========================================\n")

        raise credentials_exception

    print("CONDITION 3 PASSED: SUB EXISTS")

    # ========================================================
    # CONVERT USER ID
    # ========================================================

    try:

        user_id = int(user_id)

    except (ValueError, TypeError) as e:

        print("AUTH CONDITION 3 FAILED")
        print("REASON: INVALID USER ID IN SUB")
        print("VALUE:", user_id)
        print("ERROR:", repr(e))
        print("========================================\n")

        raise credentials_exception

    print("USER ID:", user_id)

    # ========================================================
    # CONDITION 4: DATABASE USER
    # ========================================================

    try:

        print("SEARCHING USER ID:", user_id)

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

        print("AUTH CONDITION 4 FAILED")
        print("REASON: DATABASE ERROR")
        print("DATABASE ERROR:", repr(e))
        print("========================================\n")

        raise credentials_exception

    # ========================================================
    # USER NOT FOUND
    # ========================================================

    if user is None:

        print("AUTH CONDITION 4 FAILED")
        print("REASON: USER NOT FOUND")
        print("USER ID:", user_id)
        print("========================================\n")

        raise credentials_exception

    # ========================================================
    # EVERYTHING PASSED
    # ========================================================

    print("CONDITION 4 PASSED: USER FOUND")
    print("AUTH SUCCESS:", user.username)
    print("========================================\n")

    return user