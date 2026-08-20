from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    original_url = Column(String(2048), nullable=False)
    
    original_url_hash = Column(String(64), nullable=False)

    short_code = Column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    click_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
    
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )