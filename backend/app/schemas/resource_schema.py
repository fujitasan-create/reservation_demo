"""Resource関連のPydanticスキーマ"""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ResourceBase(BaseModel):
    """Resourceの基底スキーマ"""

    name: str = Field(..., min_length=1, max_length=255, description="リソース名")
    type: str = Field(..., min_length=1, max_length=50, description="リソースタイプ")
    description: Optional[str] = Field(None, description="説明")
    availability_schedule: Any = Field(
        ...,
        description="リソースの空き時間（ホテルなら空室、人間なら空いている出勤時間）",
    )
    profile: str = Field(..., min_length=1, description="プロフィール")
    photos: Optional[List[str]] = Field(None, description="写真のURL配列")
    tags: Optional[List[str]] = Field(None, description="タグの配列")


class ResourceCreate(ResourceBase):
    """Resource作成用スキーマ"""

    pass


class ResourceUpdate(BaseModel):
    """Resource更新用スキーマ"""

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="リソース名")
    type: Optional[str] = Field(None, min_length=1, max_length=50, description="リソースタイプ")
    description: Optional[str] = Field(None, description="説明")
    availability_schedule: Optional[Any] = Field(
        None,
        description="リソースの空き時間（ホテルなら空室、人間なら空いている出勤時間）",
    )
    profile: Optional[str] = Field(None, min_length=1, description="プロフィール")
    photos: Optional[List[str]] = Field(None, description="写真のURL配列")
    tags: Optional[List[str]] = Field(None, description="タグの配列")


class ResourceResponse(ResourceBase):
    """Resourceレスポンス用スキーマ"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

