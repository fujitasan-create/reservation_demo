"""ベースリポジトリ（共通CRUD操作）"""
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """リポジトリの基底クラス"""

    def __init__(self, model: Type[ModelType], db: Session):
        """
        初期化

        Args:
            model: SQLAlchemyモデルクラス
            db: データベースセッション
        """
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """
        IDでエンティティを取得

        Args:
            id: エンティティID

        Returns:
            エンティティ、存在しない場合はNone
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        全エンティティを取得（ページネーション対応）

        Args:
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            エンティティのリスト
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        """
        エンティティを作成

        Args:
            obj: 作成するエンティティ

        Returns:
            作成されたエンティティ
        """
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, update_data: dict) -> Optional[ModelType]:
        """
        エンティティを更新

        Args:
            id: エンティティID
            update_data: 更新データ

        Returns:
            更新されたエンティティ、存在しない場合はNone
        """
        obj = self.get(id)
        if obj is None:
            return None

        for key, value in update_data.items():
            if value is not None:
                setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        """
        エンティティを削除

        Args:
            id: エンティティID

        Returns:
            削除成功時True、存在しない場合はFalse
        """
        obj = self.get(id)
        if obj is None:
            return False

        self.db.delete(obj)
        self.db.commit()
        return True

