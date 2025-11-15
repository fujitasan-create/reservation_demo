"""Resourceエンティティ（予約可能な対象：人物・建物など）"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Resource(Base):
    """予約可能なリソースエンティティ"""

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, comment="リソース名")
    type = Column(
        String(50),
        nullable=False,
        index=True,
        comment="リソースタイプ（person/building/etc）",
    )
    description = Column(Text, nullable=True, comment="説明")
    availability_schedule = Column(
        JSON,
        nullable=False,
        comment="リソースの空き時間（ホテルなら空室、人間なら空いている出勤時間）",
    )
    profile = Column(Text, nullable=False, comment="プロフィール")
    photos = Column(JSON, nullable=True, comment="写真のURL配列")
    tags = Column(JSON, nullable=True, comment="タグの配列")
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
    reservations = relationship(
        "Reservation",
        back_populates="resource",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Resource(id={self.id}, name='{self.name}', type='{self.type}')>"

