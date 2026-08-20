import hashlib
from datetime import timedelta

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
    status,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from starlette.middleware.sessions import SessionMiddleware

from authlib.integrations.starlette_client import OAuth

from sqlalchemy.orm import Session


# ============================================================
# DATABASE
# ============================================================

from app.database import engine, Base, get_db


# ============================================================
# MODELS
# ============================================================

from app import models


# ============================================================
# SCHEMAS
# ============================================================

from app.schemas import (
    URLCreate,
    URLResponse,
    UserCreate,
    UserLogin,
)


# ============================================================
# CONFIG
# ============================================================

from app.config import (
    SESSION_SECRET_KEY,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


# ============================================================
# UTILITIES
# ============================================================

from app.utils.shortener import generate_short_code

from app.utils.rate_limiter import (
    check_rate_limit,
    check_guest_limit,
)

from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_optional_current_user,
)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI()


# ============================================================
# CORS MIDDLEWARE
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SESSION MIDDLEWARE
# Required for Google OAuth state handling
# ============================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)


# ============================================================
# GOOGLE OAUTH CONFIGURATION
# ============================================================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=(
        "https://accounts.google.com/"
        ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile"
    },
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "URL Shortener API is running"
    }


# ============================================================
# REGISTER USER
# ============================================================

@app.post("/auth/register")
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    # Check existing username
    existing_username = (
        db.query(models.User)
        .filter(
            models.User.username == user_data.username
        )
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    # Check existing email
    existing_email = (
        db.query(models.User)
        .filter(
            models.User.email == user_data.email
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    # Create new user
    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        },
    }


# ============================================================
# LOGIN USER
# Username + Password
# ============================================================

@app.post("/auth/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):

    # Find user using username
    user = (
        db.query(models.User)
        .filter(
            models.User.username == user_data.username
        )
        .first()
    )

    # Check username
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Check password
    if not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": str(user.id)
        },
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


# ============================================================
# GOOGLE LOGIN
# ============================================================

@app.get("/auth/google/login")
async def google_login(
    request: Request,
):

    redirect_uri = request.url_for(
        "google_callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


# ============================================================
# GOOGLE CALLBACK
# ============================================================

@app.get(
    "/auth/google/callback",
    name="google_callback",
)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):

    try:

        # Get Google access token
        token = await oauth.google.authorize_access_token(
            request
        )

        # Get user information
        user_info = token.get("userinfo")

        if not user_info:

            user_info = await oauth.google.userinfo(
                token=token
            )

        email = user_info.get("email")
        name = user_info.get("name")
        google_sub = user_info.get("sub")

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Google account email not found",
            )

        # ----------------------------------------------------
        # Check if user already exists
        # ----------------------------------------------------

        user = (
            db.query(models.User)
            .filter(
                models.User.email == email
            )
            .first()
        )

        # ----------------------------------------------------
        # Create user if not found
        # ----------------------------------------------------

        if not user:

            # Generate a base username
            base_username = (
                email.split("@")[0]
            )

            username = base_username

            counter = 1

            # Ensure username is unique
            while (
                db.query(models.User)
                .filter(
                    models.User.username == username
                )
                .first()
            ):

                username = (
                    f"{base_username}{counter}"
                )

                counter += 1

            # Google OAuth users don't use password login
            user = models.User(
                username=username,
                email=email,
                password_hash=None,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        # ----------------------------------------------------
        # Create JWT Token
        # ----------------------------------------------------

        access_token = create_access_token(
            data={
                "sub": str(user.id)
            },
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        # ----------------------------------------------------
        # Redirect to React frontend
        # ----------------------------------------------------

        frontend_url = (
            "http://localhost:5173/"
            "oauth-success"
        )

        redirect_url = (
            f"{frontend_url}"
            f"?token={access_token}"
        )

        return RedirectResponse(
            url=redirect_url
        )

    except Exception as e:

        print(
            "GOOGLE OAUTH ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Google authentication failed",
        )


# ============================================================
# GET CURRENT USER
# ============================================================

@app.get("/auth/me")
def get_me(
    current_user: models.User = Depends(
        get_current_user
    ),
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }


# ============================================================
# SHORTEN URL
# Supports:
#
# Guest user     → 5 URLs per IP
# Registered user → unlimited based on current logic
#
# General rate limit:
# 60 requests/minute/IP
# ============================================================

@app.post(
    "/shorten",
    response_model=URLResponse,
)
def shorten_url(
    url_data: URLCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(
        get_optional_current_user
    ),
):

    # --------------------------------------------------------
    # GET CLIENT IP
    # --------------------------------------------------------

    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    # --------------------------------------------------------
    # GENERAL RATE LIMIT
    # 60 requests/minute/IP
    # --------------------------------------------------------

    allowed, current_count = check_rate_limit(
        identifier=f"ip:{client_ip}",
        limit=60,
        window_seconds=60,
    )

    if not allowed:

        raise HTTPException(
            status_code=429,
            detail=(
                "Too many requests. "
                "Please try again later."
            ),
        )

    # --------------------------------------------------------
    # GUEST USER LIMIT
    # 5 URL shorten attempts
    # --------------------------------------------------------

    if current_user is None:

        allowed_guest, guest_count = check_guest_limit(
            client_ip=client_ip,
            limit=5,
        )

        if not allowed_guest:

            raise HTTPException(
                status_code=403,
                detail=(
                    "Guest limit reached. "
                    "Please register or login "
                    "to shorten more URLs."
                ),
            )

    # --------------------------------------------------------
    # CONVERT URL TO STRING
    # --------------------------------------------------------

    original_url = str(
        url_data.url
    )

    # --------------------------------------------------------
    # CREATE SHA-256 HASH
    # --------------------------------------------------------

    original_url_hash = hashlib.sha256(
        original_url.encode("utf-8")
    ).hexdigest()

    # --------------------------------------------------------
    # CHECK EXISTING URL
    #
    # Only for registered users.
    # --------------------------------------------------------

    if current_user:

        existing_url = (
            db.query(models.URL)
            .filter(
                models.URL.original_url_hash
                == original_url_hash,

                models.URL.user_id
                == current_user.id,
            )
            .first()
        )

        if existing_url:

            return {
                "id": existing_url.id,
                "original_url": (
                    existing_url.original_url
                ),
                "short_code": (
                    existing_url.short_code
                ),
                "short_url": (
                    f"http://localhost:8000/"
                    f"{existing_url.short_code}"
                ),
                "click_count": (
                    existing_url.click_count
                ),
            }

    # --------------------------------------------------------
    # GENERATE UNIQUE SHORT CODE
    # --------------------------------------------------------

    while True:

        short_code = generate_short_code()

        existing_code = (
            db.query(models.URL)
            .filter(
                models.URL.short_code
                == short_code
            )
            .first()
        )

        if not existing_code:
            break

    # --------------------------------------------------------
    # CREATE URL RECORD
    # --------------------------------------------------------

    new_url = models.URL(
        original_url=original_url,
        original_url_hash=original_url_hash,
        short_code=short_code,

        # Registered user ID
        # Guest user → None
        user_id=(
            current_user.id
            if current_user
            else None
        ),
    )

    # --------------------------------------------------------
    # SAVE TO DATABASE
    # --------------------------------------------------------

    try:

        db.add(new_url)
        db.commit()
        db.refresh(new_url)

    except Exception as e:

        db.rollback()

        print(
            "SHORTEN URL ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to create shortened URL",
        )

    # --------------------------------------------------------
    # RETURN RESPONSE
    # --------------------------------------------------------

    return {
        "id": new_url.id,
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "short_url": (
            f"http://localhost:8000/"
            f"{new_url.short_code}"
        ),
        "click_count": new_url.click_count,
    }


# ============================================================
# REDIRECT SHORT URL
# ============================================================

@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db),
):

    url = (
        db.query(models.URL)
        .filter(
            models.URL.short_code
            == short_code
        )
        .first()
    )

    if not url:

        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    # Increase click count
    url.click_count += 1

    db.commit()

    # Redirect user
    return RedirectResponse(
        url=url.original_url,
        status_code=307,
    )
    
# ============================================================
# USER DASHBOARD STATS
# ============================================================

@app.get("/dashboard/stats")
def get_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Get all URLs created by the logged-in user
    urls = (
        db.query(models.URL)
        .filter(
            models.URL.user_id == current_user.id
        )
        .all()
    )

    # Total URLs
    total_urls = len(urls)

    # Total clicks across all URLs
    total_clicks = sum(
        url.click_count for url in urls
    )

    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks,
        "account_status": "Active",
    }