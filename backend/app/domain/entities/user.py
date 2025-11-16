"""Userエンティティ（ユーザー情報）"""
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, Enum):
    """ユーザーロール"""

    ADMIN = "admin"
    USER = "user"


class User(Base):
    """ユーザーエンティティ"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True, comment="メールアドレス")
    password_hash = Column(String(255), nullable=False, comment="パスワードハッシュ")
    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.USER,
        index=True,
        comment="ユーザーロール（admin/user）",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="作成日時",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新日時",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

