# import os

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base


# # ============================================================
# # DATABASE URL
# # ============================================================

# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mysql+pymysql://root:trilochan@localhost:3306/url_shortener"
# )


# # ============================================================
# # DATABASE ENGINE
# # ============================================================

# engine = create_engine(
#     DATABASE_URL,
#     pool_size=10,
#     max_overflow=20,
#     pool_timeout=30,
#     pool_recycle=1800,
# )


# # ============================================================
# # SESSION
# # ============================================================

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )


# # ============================================================
# # BASE
# # ============================================================

# Base = declarative_base()


# # ============================================================
# # DATABASE DEPENDENCY
# # ============================================================

# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.utils.encryption import decrypt_value


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_USER = os.getenv("DB_USER", "root")

DB_PASSWORD_ENCRYPTED = os.getenv(
    "DB_PASSWORD_ENCRYPTED"
)

DB_ENCRYPTION_KEY = os.getenv(
    "DB_ENCRYPTION_KEY"
)

DB_HOST = os.getenv(
    "DB_HOST",
    "host.docker.internal"
)

DB_PORT = os.getenv(
    "DB_PORT",
    "3306"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "url_shortener"
)


# ============================================================
# VALIDATE ENCRYPTED DATABASE CREDENTIALS
# ============================================================

if not DB_PASSWORD_ENCRYPTED:
    raise RuntimeError(
        "DB_PASSWORD_ENCRYPTED environment variable is missing."
    )

if not DB_ENCRYPTION_KEY:
    raise RuntimeError(
        "DB_ENCRYPTION_KEY environment variable is missing."
    )


# ============================================================
# DECRYPT DATABASE PASSWORD
# ============================================================

DB_PASSWORD = decrypt_value(
    DB_PASSWORD_ENCRYPTED,
    DB_ENCRYPTION_KEY,
)


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()