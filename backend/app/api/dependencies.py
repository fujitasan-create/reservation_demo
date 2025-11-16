"""API依存性注入モジュール"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.domain.entities.user import User
from app.repositories.user_repository import UserRepository

# HTTP Bearer認証スキーマ
security = HTTPBearer()


def get_database_session() -> Session:
    """
    データベースセッションを取得する依存性

    Returns:
        Session: データベースセッション
    """
    return next(get_db())


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database_session),
) -> User:
    """
    現在ログインしているユーザーを取得する依存性

    Args:
        credentials: HTTP Bearer認証情報
        db: データベースセッション

    Returns:
        User: 現在ログインしているユーザー

    Raises:
        HTTPException: 認証失敗時（401 Unauthorized）
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効な認証トークンです",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証トークンが無効です",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repository = UserRepository(db)
    user = repository.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーが見つかりません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    現在ログインしている管理者ユーザーを取得する依存性

    Args:
        current_user: 現在ログインしているユーザー

    Returns:
        User: 現在ログインしている管理者ユーザー

    Raises:
        HTTPException: 管理者権限がない場合（403 Forbidden）
    """
    from app.domain.entities.user import UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作には管理者権限が必要です",
        )

    return current_user

