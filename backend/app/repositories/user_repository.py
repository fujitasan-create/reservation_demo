"""Userリポジトリ"""
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Userリポジトリ"""

    def __init__(self, db: Session):
        """初期化"""
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        メールアドレスでユーザーを取得

        Args:
            email: メールアドレス

        Returns:
            ユーザー、存在しない場合はNone
        """
        return self.db.query(User).filter(User.email == email).first()

    def exists_by_email(self, email: str) -> bool:
        """
        メールアドレスが既に存在するか確認

        Args:
            email: メールアドレス

        Returns:
            存在する場合True、存在しない場合False
        """
        user = self.get_by_email(email)
        return user is not None

