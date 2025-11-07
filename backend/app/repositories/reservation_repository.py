"""Reservationリポジトリ"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.domain.entities.reservation import Reservation, ReservationStatus
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """Reservationリポジトリ"""

    def __init__(self, db: Session):
        super().__init__(Reservation, db)

    def get_by_resource_id(
        self, resource_id: int, skip: int = 0, limit: int = 100
    ) -> List[Reservation]:
        """
        リソースIDで予約を取得

        Args:
            resource_id: リソースID
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            Reservationのリスト
        """
        return (
            self.db.query(Reservation)
            .filter(Reservation.resource_id == resource_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        resource_id: Optional[int] = None,
    ) -> List[Reservation]:
        """
        日付範囲で予約を取得

        Args:
            start_date: 開始日時
            end_date: 終了日時
            resource_id: リソースID（オプション）

        Returns:
            Reservationのリスト
        """
        query = self.db.query(Reservation).filter(
            or_(
                and_(
                    Reservation.start_time <= start_date,
                    Reservation.end_time > start_date,
                ),
                and_(
                    Reservation.start_time < end_date,
                    Reservation.end_time >= end_date,
                ),
                and_(
                    Reservation.start_time >= start_date,
                    Reservation.end_time <= end_date,
                ),
            )
        )

        if resource_id is not None:
            query = query.filter(Reservation.resource_id == resource_id)

        return query.all()

    def get_conflicting_reservations(
        self,
        resource_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None,
    ) -> List[Reservation]:
        """
        時間が重複する予約を取得

        Args:
            resource_id: リソースID
            start_time: 予約開始時刻
            end_time: 予約終了時刻
            exclude_id: 除外する予約ID（更新時に使用）

        Returns:
            重複するReservationのリスト
        """
        query = self.db.query(Reservation).filter(
            Reservation.resource_id == resource_id,
            Reservation.status != ReservationStatus.CANCELLED,
            or_(
                and_(
                    Reservation.start_time < end_time,
                    Reservation.end_time > start_time,
                ),
            ),
        )

        if exclude_id is not None:
            query = query.filter(Reservation.id != exclude_id)

        return query.all()

    def get_by_customer_email(
        self, email: str, skip: int = 0, limit: int = 100
    ) -> List[Reservation]:
        """
        顧客メールアドレスで予約を取得

        Args:
            email: 顧客メールアドレス
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            Reservationのリスト
        """
        return (
            self.db.query(Reservation)
            .filter(Reservation.customer_email == email)
            .offset(skip)
            .limit(limit)
            .all()
        )

