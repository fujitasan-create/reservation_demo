"""管理者用APIルーター"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user, get_database_session
from app.domain.entities.user import User
from app.schemas.resource_schema import ResourceCreate, ResourceResponse, ResourceUpdate
from app.schemas.reservation_schema import ReservationResponse
from app.usecases.exceptions import ResourceNotFoundError
from app.usecases.reservation_usecase import ReservationUsecase
from app.usecases.resource_usecase import ResourceUsecase

router = APIRouter(prefix="/admin", tags=["admin"])


def get_resource_usecase(db: Session = Depends(get_database_session)) -> ResourceUsecase:
    """ResourceUsecaseの依存性注入"""
    return ResourceUsecase(db)


def get_reservation_usecase(
    db: Session = Depends(get_database_session),
) -> ReservationUsecase:
    """ReservationUsecaseの依存性注入"""
    return ReservationUsecase(db)


# リソース管理（管理者専用）
@router.post(
    "/resources",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="リソースを作成（管理者専用）",
)
def create_resource(
    resource_data: ResourceCreate,
    admin_user: User = Depends(get_current_admin_user),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    リソースを作成します（管理者専用）。

    - **name**: リソース名（必須）
    - **type**: リソースタイプ（必須）
    - **description**: 説明（オプション）
    - **availability_schedule**: リソースの空き時間（必須、JSON形式）
    - **profile**: プロフィール（必須）
    - **photos**: 写真のURL配列（オプション）
    - **tags**: タグの配列（オプション）
    - **menu_services**: メニュー・サービス情報（オプション）
    """
    return usecase.create_resource(resource_data)


@router.get(
    "/resources",
    response_model=List[ResourceResponse],
    summary="リソース一覧を取得（管理者専用）",
)
def get_resources(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    type: Optional[str] = Query(None, description="リソースタイプでフィルタリング"),
    admin_user: User = Depends(get_current_admin_user),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> List[ResourceResponse]:
    """
    リソース一覧を取得します（管理者専用）。
    """
    return usecase.get_resources(skip=skip, limit=limit, type=type)


@router.get(
    "/resources/{resource_id}",
    response_model=ResourceResponse,
    summary="リソースを取得（管理者専用）",
)
def get_resource(
    resource_id: int,
    admin_user: User = Depends(get_current_admin_user),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    指定されたIDのリソースを取得します（管理者専用）。
    """
    try:
        return usecase.get_resource(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/resources/{resource_id}",
    response_model=ResourceResponse,
    summary="リソースを更新（管理者専用）",
)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    admin_user: User = Depends(get_current_admin_user),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> ResourceResponse:
    """
    指定されたIDのリソースを更新します（管理者専用）。
    """
    try:
        return usecase.update_resource(resource_id, resource_data)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/resources/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="リソースを削除（管理者専用）",
)
def delete_resource(
    resource_id: int,
    admin_user: User = Depends(get_current_admin_user),
    usecase: ResourceUsecase = Depends(get_resource_usecase),
) -> None:
    """
    指定されたIDのリソースを削除します（管理者専用）。
    """
    try:
        usecase.delete_resource(resource_id)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


# 予約管理（管理者専用）
@router.get(
    "/reservations",
    response_model=List[ReservationResponse],
    summary="全予約一覧を取得（管理者専用）",
)
def get_all_reservations(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    admin_user: User = Depends(get_current_admin_user),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> List[ReservationResponse]:
    """
    全予約一覧を取得します（管理者専用）。
    """
    return usecase.get_reservations(skip=skip, limit=limit)


@router.get(
    "/reservations/by-user",
    response_model=List[ReservationResponse],
    summary="ユーザー別予約一覧を取得（管理者専用）",
)
def get_reservations_by_user(
    customer_email: str = Query(..., description="顧客メールアドレス"),
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    admin_user: User = Depends(get_current_admin_user),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> List[ReservationResponse]:
    """
    指定されたユーザーの予約一覧を取得します（管理者専用）。
    """
    return usecase.get_reservations(
        skip=skip, limit=limit, customer_email=customer_email
    )


@router.get(
    "/reservations/by-resource",
    response_model=List[ReservationResponse],
    summary="リソース別予約一覧を取得（管理者専用）",
)
def get_reservations_by_resource(
    resource_id: int = Query(..., description="リソースID"),
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    admin_user: User = Depends(get_current_admin_user),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> List[ReservationResponse]:
    """
    指定されたリソースの予約一覧を取得します（管理者専用）。
    """
    return usecase.get_reservations(
        skip=skip, limit=limit, resource_id=resource_id
    )

