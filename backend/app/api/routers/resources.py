"""Resource関連のAPIルーター"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.schemas.resource_schema import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from app.usecases.exceptions import ResourceNotFoundError
from app.usecases.resource_usecase import ResourceUsecase

router = APIRouter(prefix="/resources", tags=["resources"])


def get_resource_usecase(db: Session = Depends(get_database_session)) -> ResourceUsecase:
    """
    ResourceUsecaseの依存性注入

    Args:
        db: データベースセッション

    Returns:
        ResourceUsecaseインスタンス
    """
    return ResourceUsecase(db)


@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="リソースを作成",
)
def create_resource(
    resource_data: ResourceCreate,
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    リソースを作成します。

    - **name**: リソース名（必須）
    - **type**: リソースタイプ（必須）
    - **description**: 説明（オプション）
    - **availability_schedule**: リソースの空き時間（必須、JSON形式）
    - **profile**: プロフィール（必須）
    - **photos**: 写真のURL配列（オプション）
    - **tags**: タグの配列（オプション）
    """
    return usecase.create_resource(resource_data)


@router.get(
    "",
    response_model=List[ResourceResponse],
    summary="リソース一覧を取得",
)
def get_resources(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    type: Optional[str] = Query(None, description="リソースタイプでフィルタリング"),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> List[ResourceResponse]:
    """
    リソース一覧を取得します。

    - **skip**: スキップする件数（デフォルト: 0）
    - **limit**: 取得する最大件数（デフォルト: 100、最大: 1000）
    - **type**: リソースタイプでフィルタリング（オプション）
    """
    return usecase.get_resources(skip=skip, limit=limit, type=type)


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="リソースを取得",
)
def get_resource(
    resource_id: int,
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    指定されたIDのリソースを取得します。

    - **resource_id**: リソースID
    """
    try:
        return usecase.get_resource(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="リソースを更新",
)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    指定されたIDのリソースを更新します。

    - **resource_id**: リソースID
    - 更新したいフィールドのみを指定してください
    """
    try:
        return usecase.update_resource(resource_id, resource_data)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="リソースを削除",
)
def delete_resource(
    resource_id: int,
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> None:
    """
    指定されたIDのリソースを削除します。

    - **resource_id**: リソースID
    """
    try:
        usecase.delete_resource(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

