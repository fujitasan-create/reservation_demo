"""Resourceリポジトリ"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.resource import Resource
from app.repositories.base import BaseRepository


class ResourceRepository(BaseRepository[Resource]):
    """Resourceリポジトリ"""

    def __init__(self, db: Session):
        super().__init__(Resource, db)

    def get_by_name(self, name: str) -> Optional[Resource]:
        """
        名前でResourceを取得

        Args:
            name: リソース名

        Returns:
            Resource、存在しない場合はNone
        """
        return self.db.query(Resource).filter(Resource.name == name).first()

    def get_by_type(self, type: str, skip: int = 0, limit: int = 100) -> List[Resource]:
        """
        タイプでResourceを取得

        Args:
            type: リソースタイプ
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            Resourceのリスト
        """
        return (
            self.db.query(Resource)
            .filter(Resource.type == type)
            .offset(skip)
            .limit(limit)
            .all()
        )

