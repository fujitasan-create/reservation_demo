"""Reservation関連のユースケース"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.resource_repository import ResourceRepository
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


class ReservationUsecase:
    """Reservation関連のユースケース"""

    def __init__(self, db: Session):
        """
        初期化

        Args:
            db: データベースセッション
        """
        self.reservation_repository = ReservationRepository(db)
        self.resource_repository = ResourceRepository(db)

    def _validate_reservation_time(
        self, start_time: datetime, end_time: datetime
    ) -> None:
        """
        予約時間の妥当性を検証

        Args:
            start_time: 予約開始時刻
            end_time: 予約終了時刻

        Raises:
            InvalidReservationTimeError: 予約時間が無効な場合
        """
        if start_time >= end_time:
            raise InvalidReservationTimeError(
                "Start time must be before end time"
            )

        if start_time < datetime.now(start_time.tzinfo):
            raise InvalidReservationTimeError(
                "Start time must be in the future"
            )

    def _check_reservation_conflict(
        self,
        resource_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None,
    ) -> None:
        """
        予約の時間重複をチェック

        Args:
            resource_id: リソースID
            start_time: 予約開始時刻
            end_time: 予約終了時刻
            exclude_id: 除外する予約ID（更新時に使用）

        Raises:
            ReservationConflictError: 予約が重複している場合
        """
        conflicting = self.reservation_repository.get_conflicting_reservations(
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            exclude_id=exclude_id,
        )
        if conflicting:
            raise ReservationConflictError(
                f"Reservation conflicts with existing reservation(s)"
            )

    def create_reservation(
        self, reservation_data: ReservationCreate
    ) -> ReservationResponse:
        """
        予約を作成

        Args:
            reservation_data: 予約作成データ

        Returns:
            作成された予約

        Raises:
            ResourceNotFoundError: リソースが見つからない場合
            InvalidReservationTimeError: 予約時間が無効な場合
            ReservationConflictError: 予約が重複している場合
        """
        # リソースの存在確認
        resource = self.resource_repository.get(reservation_data.resource_id)
        if resource is None:
            raise ResourceNotFoundError(
                f"Resource with id {reservation_data.resource_id} not found"
            )

        # 予約時間の妥当性検証
        self._validate_reservation_time(
            reservation_data.start_time, reservation_data.end_time
        )

        # 時間重複チェック
        self._check_reservation_conflict(
            resource_id=reservation_data.resource_id,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
        )

        # 予約作成
        reservation = Reservation(
            resource_id=reservation_data.resource_id,
            customer_name=reservation_data.customer_name,
            customer_email=reservation_data.customer_email,
            customer_phone=reservation_data.customer_phone,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
            status=reservation_data.status,
        )
        created_reservation = self.reservation_repository.create(reservation)
        return ReservationResponse.model_validate(created_reservation)

    def get_reservation(self, reservation_id: int) -> ReservationResponse:
        """
        予約を取得

        Args:
            reservation_id: 予約ID

        Returns:
            予約

        Raises:
            ReservationNotFoundError: 予約が見つからない場合
        """
        reservation = self.reservation_repository.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError(
                f"Reservation with id {reservation_id} not found"
            )
        return ReservationResponse.model_validate(reservation)

    def get_reservations(
        self,
        skip: int = 0,
        limit: int = 100,
        resource_id: Optional[int] = None,
        customer_email: Optional[str] = None,
    ) -> List[ReservationResponse]:
        """
        予約一覧を取得

        Args:
            skip: スキップする件数
            limit: 取得する最大件数
            resource_id: リソースIDでフィルタリング（オプション）
            customer_email: 顧客メールアドレスでフィルタリング（オプション）

        Returns:
            予約のリスト
        """
        if resource_id:
            reservations = self.reservation_repository.get_by_resource_id(
                resource_id, skip=skip, limit=limit
            )
        elif customer_email:
            reservations = self.reservation_repository.get_by_customer_email(
                customer_email, skip=skip, limit=limit
            )
        else:
            reservations = self.reservation_repository.get_all(skip=skip, limit=limit)
        return [
            ReservationResponse.model_validate(reservation)
            for reservation in reservations
        ]

    def update_reservation(
        self, reservation_id: int, reservation_data: ReservationUpdate
    ) -> ReservationResponse:
        """
        予約を更新

        Args:
            reservation_id: 予約ID
            reservation_data: 予約更新データ

        Returns:
            更新された予約

        Raises:
            ReservationNotFoundError: 予約が見つからない場合
            ResourceNotFoundError: リソースが見つからない場合
            InvalidReservationTimeError: 予約時間が無効な場合
            ReservationConflictError: 予約が重複している場合
        """
        # 既存の予約を取得
        existing_reservation = self.reservation_repository.get(reservation_id)
        if existing_reservation is None:
            raise ReservationNotFoundError(
                f"Reservation with id {reservation_id} not found"
            )

        update_dict = reservation_data.model_dump(exclude_unset=True)

        # リソースIDが変更される場合、存在確認
        if "resource_id" in update_dict:
            resource = self.resource_repository.get(update_dict["resource_id"])
            if resource is None:
                raise ResourceNotFoundError(
                    f"Resource with id {update_dict['resource_id']} not found"
                )

        # 予約時間が変更される場合、妥当性検証と重複チェック
        start_time = update_dict.get("start_time", existing_reservation.start_time)
        end_time = update_dict.get("end_time", existing_reservation.end_time)
        resource_id = update_dict.get("resource_id", existing_reservation.resource_id)

        if "start_time" in update_dict or "end_time" in update_dict:
            self._validate_reservation_time(start_time, end_time)
            self._check_reservation_conflict(
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time,
                exclude_id=reservation_id,
            )

        # 予約更新
        updated_reservation = self.reservation_repository.update(
            reservation_id, update_dict
        )
        return ReservationResponse.model_validate(updated_reservation)

    def delete_reservation(self, reservation_id: int) -> None:
        """
        予約を削除

        Args:
            reservation_id: 予約ID

        Raises:
            ReservationNotFoundError: 予約が見つからない場合
        """
        success = self.reservation_repository.delete(reservation_id)
        if not success:
            raise ReservationNotFoundError(
                f"Reservation with id {reservation_id} not found"
            )

    def check_availability(
        self,
        resource_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> bool:
        """
        指定された時間帯の利用可能性を確認

        Args:
            resource_id: リソースID
            start_time: 確認開始時刻
            end_time: 確認終了時刻

        Returns:
            利用可能な場合True、利用不可能な場合False

        Raises:
            ResourceNotFoundError: リソースが見つからない場合
            InvalidReservationTimeError: 予約時間が無効な場合
        """
        # リソースの存在確認
        resource = self.resource_repository.get(resource_id)
        if resource is None:
            raise ResourceNotFoundError(
                f"Resource with id {resource_id} not found"
            )

        # 時間の妥当性検証
        if start_time >= end_time:
            raise InvalidReservationTimeError(
                "Start time must be before end time"
            )

        # 重複チェック
        try:
            self._check_reservation_conflict(
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time,
            )
            return True
        except ReservationConflictError:
            return False

