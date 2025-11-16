"""User関連のPydanticスキーマ"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.entities.user import UserRole


class UserBase(BaseModel):
    """Userの基底スキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    role: UserRole = Field(default=UserRole.USER, description="ユーザーロール")


class UserCreate(UserBase):
    """User作成用スキーマ"""

    password: str = Field(..., min_length=4, description="パスワード")


class UserRegister(BaseModel):
    """ユーザー登録用スキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=4, description="パスワード")


class UserLogin(BaseModel):
    """ログイン用スキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., description="パスワード")


class UserResponse(UserBase):
    """Userレスポンス用スキーマ"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """User更新用スキーマ"""

    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    password: Optional[str] = Field(None, min_length=4, description="パスワード")
    role: Optional[UserRole] = Field(None, description="ユーザーロール")


class Token(BaseModel):
    """JWTトークンレスポンス用スキーマ"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse

