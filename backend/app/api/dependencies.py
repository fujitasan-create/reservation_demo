"""API依存性注入モジュール"""
from sqlalchemy.orm import Session

from app.database import get_db


def get_database_session() -> Session:
    """
    データベースセッションを取得する依存性
    
    Returns:
        Session: データベースセッション
    """
    return next(get_db())

