"""Reservation関連のPydanticスキーマ"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.entities.reservation import ReservationStatus


class ReservationBase(BaseModel):
    """Reservationの基底スキーマ"""

    resource_id: int = Field(..., description="リソースID")
    customer_name: str = Field(..., min_length=1, max_length=255, description="顧客名")
    customer_email: EmailStr = Field(..., description="顧客メールアドレス")
    customer_phone: Optional[str] = Field(None, max_length=50, description="顧客電話番号")
    start_time: datetime = Field(..., description="予約開始時刻")
    end_time: datetime = Field(..., description="予約終了時刻")
    status: ReservationStatus = Field(
        default=ReservationStatus.PENDING,
        description="予約ステータス",
    )


class ReservationCreate(ReservationBase):
    """Reservation作成用スキーマ"""

    pass


class ReservationUpdate(BaseModel):
    """Reservation更新用スキーマ"""

    resource_id: Optional[int] = Field(None, description="リソースID")
    customer_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="顧客名"
    )
    customer_email: Optional[EmailStr] = Field(None, description="顧客メールアドレス")
    customer_phone: Optional[str] = Field(None, max_length=50, description="顧客電話番号")
    start_time: Optional[datetime] = Field(None, description="予約開始時刻")
    end_time: Optional[datetime] = Field(None, description="予約終了時刻")
    status: Optional[ReservationStatus] = Field(None, description="予約ステータス")


class ReservationResponse(ReservationBase):
    """Reservationレスポンス用スキーマ"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

