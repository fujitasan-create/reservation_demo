"""サロン情報関連のAPIルーター"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user, get_database_session
from app.domain.entities.user import User

router = APIRouter(prefix="/salon", tags=["salon"])


class SalonInfo(BaseModel):
    """サロン情報スキーマ"""

    name: str = Field(..., description="サロン名")
    description: Optional[str] = Field(None, description="説明")
    business_hours_start: int = Field(9, ge=0, le=23, description="営業開始時間（時）")
    business_hours_end: int = Field(21, ge=0, le=23, description="営業終了時間（時）")
    interior_image_url: Optional[str] = Field(None, description="内装画像URL")


# 簡易的なサロン情報ストレージ（実際の本番環境では、データベースに保存することを推奨）
_salon_info: Optional[SalonInfo] = None


@router.get("/info", response_model=SalonInfo, summary="サロン情報を取得")
def get_salon_info() -> SalonInfo:
    """
    サロン情報を取得します。

    認証は不要です。
    """
    # デフォルト値
    if _salon_info is None:
        return SalonInfo(
            name="〇〇サロン",
            description="美容院のデモサイトです",
            business_hours_start=9,
            business_hours_end=21,
        )
    return _salon_info


@router.put("/info", response_model=SalonInfo, summary="サロン情報を更新（管理者専用）")
def update_salon_info(
    salon_info: SalonInfo,
    admin_user: User = Depends(get_current_admin_user),
) -> SalonInfo:
    """
    サロン情報を更新します（管理者専用）。

    - **name**: サロン名（必須）
    - **description**: 説明（オプション）
    - **business_hours_start**: 営業開始時間（時、デフォルト: 9）
    - **business_hours_end**: 営業終了時間（時、デフォルト: 21）
    - **interior_image_url**: 内装画像URL（オプション）
    """
    global _salon_info
    _salon_info = salon_info
    return _salon_info

