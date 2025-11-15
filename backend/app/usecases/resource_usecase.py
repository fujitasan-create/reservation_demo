"""Resource関連のユースケース"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.resource import Resource
from app.repositories.resource_repository import ResourceRepository
from app.schemas.resource_schema import ResourceCreate, ResourceResponse, ResourceUpdate
from app.usecases.exceptions import ResourceNotFoundError


class ResourceUsecase:
    """Resource関連のユースケース"""

    def __init__(self, db: Session):
        """
        初期化

        Args:
            db: データベースセッション
        """
        self.repository = ResourceRepository(db)

    def create_resource(self, resource_data: ResourceCreate) -> ResourceResponse:
        """
        リソースを作成

        Args:
            resource_data: リソース作成データ

        Returns:
            作成されたリソース
        """
        resource = Resource(
            name=resource_data.name,
            type=resource_data.type,
            description=resource_data.description,
            availability_schedule=resource_data.availability_schedule,
            profile=resource_data.profile,
            photos=resource_data.photos,
            tags=resource_data.tags,
        )
        created_resource = self.repository.create(resource)
        return ResourceResponse.model_validate(created_resource)

    def get_resource(self, resource_id: int) -> ResourceResponse:
        """
        リソースを取得

        Args:
            resource_id: リソースID

        Returns:
            リソース

        Raises:
            ResourceNotFoundError: リソースが見つからない場合
        """
        resource = self.repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError(f"Resource with id {resource_id} not found")
        return ResourceResponse.model_validate(resource)

    def get_resources(
        self, skip: int = 0, limit: int = 100, type: Optional[str] = None
    ) -> List[ResourceResponse]:
        """
        リソース一覧を取得

        Args:
            skip: スキップする件数
            limit: 取得する最大件数
            type: リソースタイプでフィルタリング（オプション）

        Returns:
            リソースのリスト
        """
        if type:
            resources = self.repository.get_by_type(type, skip=skip, limit=limit)
        else:
            resources = self.repository.get_all(skip=skip, limit=limit)
        return [ResourceResponse.model_validate(resource) for resource in resources]

    def update_resource(
        self, resource_id: int, resource_data: ResourceUpdate
    ) -> ResourceResponse:
        """
        リソースを更新

        Args:
            resource_id: リソースID
            resource_data: リソース更新データ

        Returns:
            更新されたリソース

        Raises:
            ResourceNotFoundError: リソースが見つからない場合
        """
        update_dict = resource_data.model_dump(exclude_unset=True)
        updated_resource = self.repository.update(resource_id, update_dict)
        if updated_resource is None:
            raise ResourceNotFoundError(f"Resource with id {resource_id} not found")
        return ResourceResponse.model_validate(updated_resource)

    def delete_resource(self, resource_id: int) -> None:
        """
        リソースを削除

        Args:
            resource_id: リソースID

        Raises:
            ResourceNotFoundError: リソースが見つからない場合
        """
        success = self.repository.delete(resource_id)
        if not success:
            raise ResourceNotFoundError(f"Resource with id {resource_id} not found")

