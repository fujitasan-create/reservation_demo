"""セキュリティ関連ユーティリティ"""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.config import settings

# bcryptの設定
BCRYPT_ROUNDS = 12  # bcryptのラウンド数（セキュリティとパフォーマンスのバランス）


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを検証

    Args:
        plain_password: 平文パスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        検証成功時True、失敗時False

    Note:
        bcryptの制限により、72バイトを超えるパスワードは自動的に切り詰めて検証します
    """
    # bcryptの制限: 72バイトを超えるパスワードは切り詰める
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > 72:
        plain_password = password_bytes[:72].decode("utf-8", errors="ignore")
    
    # bcryptでパスワードを検証
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化

    Args:
        password: 平文パスワード

    Returns:
        ハッシュ化されたパスワード

    Note:
        bcryptの制限により、72バイトを超えるパスワードは自動的に切り詰めます
    """
    # bcryptの制限: 72バイトを超えるパスワードは切り詰める
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")
    
    # bcryptでパスワードをハッシュ化
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWTアクセストークンを作成

    Args:
        data: トークンに含めるデータ
        expires_delta: 有効期限（指定しない場合は設定値を使用）

    Returns:
        JWTトークン文字列
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    JWTアクセストークンをデコード

    Args:
        token: JWTトークン文字列

    Returns:
        デコードされたデータ、失敗時はNone
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

