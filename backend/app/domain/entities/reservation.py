"""Reservationエンティティ（予約情報）"""
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ReservationStatus(str, Enum):
    """予約ステータス"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Reservation(Base):
    """予約エンティティ"""

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(
        Integer,
        ForeignKey("resources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="リソースID",
    )
    customer_name = Column(String(255), nullable=False, comment="顧客名")
    customer_email = Column(String(255), nullable=False, index=True, comment="顧客メールアドレス")
    customer_phone = Column(String(50), nullable=True, comment="顧客電話番号")
    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="予約開始時刻",
    )
    end_time = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="予約終了時刻",
    )
    status = Column(
        SQLEnum(ReservationStatus),
        nullable=False,
        default=ReservationStatus.PENDING,
        index=True,
        comment="予約ステータス",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="作成日時",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新日時",
    )

    # リレーション
    resource = relationship("Resource", back_populates="reservations")

    def __repr__(self) -> str:
        return (
            f"<Reservation(id={self.id}, resource_id={self.resource_id}, "
            f"start_time={self.start_time}, status='{self.status}')>"
        )

