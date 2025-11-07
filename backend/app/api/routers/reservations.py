"""Reservation関連のAPIルーター"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session
from app.schemas.reservation_schema import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from app.usecases.exceptions import (
    InvalidReservationTimeError,
    ReservationConflictError,
    ReservationNotFoundError,
    ResourceNotFoundError,
)
from app.usecases.reservation_usecase import ReservationUsecase

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_usecase(
    db: Session = Depends(get_database_session),
) -> ReservationUsecase:
    """
    ReservationUsecaseの依存性注入

    Args:
        db: データベースセッション

    Returns:
        ReservationUsecaseインスタンス
    """
    return ReservationUsecase(db)


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="予約を作成",
)
def create_reservation(
    reservation_data: ReservationCreate,
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> ReservationResponse:
    """
    予約を作成します。

    - **resource_id**: リソースID（必須）
    - **customer_name**: 顧客名（必須）
    - **customer_email**: 顧客メールアドレス（必須）
    - **customer_phone**: 顧客電話番号（オプション）
    - **start_time**: 予約開始時刻（必須）
    - **end_time**: 予約終了時刻（必須）
    - **status**: 予約ステータス（デフォルト: pending）

    時間が重複している場合や、リソースが存在しない場合はエラーになります。
    """
    try:
        return usecase.create_reservation(reservation_data)
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidReservationTimeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ReservationConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=List[ReservationResponse],
    summary="予約一覧を取得",
)
def get_reservations(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    resource_id: Optional[int] = Query(None, description="リソースIDでフィルタリング"),
    customer_email: Optional[str] = Query(
        None, description="顧客メールアドレスでフィルタリング"
    ),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> List[ReservationResponse]:
    """
    予約一覧を取得します。

    - **skip**: スキップする件数（デフォルト: 0）
    - **limit**: 取得する最大件数（デフォルト: 100、最大: 1000）
    - **resource_id**: リソースIDでフィルタリング（オプション）
    - **customer_email**: 顧客メールアドレスでフィルタリング（オプション）
    """
    return usecase.get_reservations(
        skip=skip, limit=limit, resource_id=resource_id, customer_email=customer_email
    )


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
    summary="予約を取得",
)
def get_reservation(
    reservation_id: int,
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> ReservationResponse:
    """
    指定されたIDの予約を取得します。

    - **reservation_id**: 予約ID
    """
    try:
        return usecase.get_reservation(reservation_id)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{reservation_id}",
    response_model=ReservationResponse,
    summary="予約を更新",
)
def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> ReservationResponse:
    """
    指定されたIDの予約を更新します。

    - **reservation_id**: 予約ID
    - 更新したいフィールドのみを指定してください

    時間が重複している場合や、リソースが存在しない場合はエラーになります。
    """
    try:
        return usecase.update_reservation(reservation_id, reservation_data)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidReservationTimeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ReservationConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="予約を削除",
)
def delete_reservation(
    reservation_id: int,
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> None:
    """
    指定されたIDの予約を削除します。

    - **reservation_id**: 予約ID
    """
    try:
        usecase.delete_reservation(reservation_id)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get(
    "/resources/{resource_id}/availability",
    summary="リソースの利用可能性を確認",
)
def check_resource_availability(
    resource_id: int,
    start_time: datetime = Query(..., description="確認開始時刻"),
    end_time: datetime = Query(..., description="確認終了時刻"),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> dict:
    """
    指定されたリソースの指定時間帯の利用可能性を確認します。

    - **resource_id**: リソースID
    - **start_time**: 確認開始時刻
    - **end_time**: 確認終了時刻

    利用可能な場合、`{"available": true}` を返します。
    利用不可能な場合、`{"available": false}` を返します。
    """
    try:
        available = usecase.check_availability(resource_id, start_time, end_time)
        return {"available": available}
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidReservationTimeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post(
    "/check-availability",
    summary="予約時間の利用可能性を確認",
)
def check_reservation_availability(
    resource_id: int = Query(..., description="リソースID"),
    start_time: datetime = Query(..., description="確認開始時刻"),
    end_time: datetime = Query(..., description="確認終了時刻"),
    usecase: ReservationUsecase = Depends(get_reservation_usecase),
) -> dict:
    """
    指定されたリソースの指定時間帯の利用可能性を確認します。

    - **resource_id**: リソースID
    - **start_time**: 確認開始時刻
    - **end_time**: 確認終了時刻

    利用可能な場合、`{"available": true}` を返します。
    利用不可能な場合、`{"available": false}` を返します。
    """
    try:
        available = usecase.check_availability(resource_id, start_time, end_time)
        return {"available": available}
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidReservationTimeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

