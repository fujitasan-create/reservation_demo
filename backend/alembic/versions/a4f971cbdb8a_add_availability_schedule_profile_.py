"""add_availability_schedule_profile_photos_tags_to_resources

Revision ID: a4f971cbdb8a
Revises: cbd83fdf5260
Create Date: 2025-11-16 08:39:50.653191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4f971cbdb8a'
down_revision: Union[str, Sequence[str], None] = 'cbd83fdf5260'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # availability_scheduleカラムを追加（まずnullable=Trueで追加）
    op.add_column(
        'resources',
        sa.Column(
            'availability_schedule',
            sa.JSON(),
            nullable=True,
            comment='リソースの空き時間（ホテルなら空室、人間なら空いている出勤時間）'
        )
    )
    
    # 既存データにデフォルト値を設定
    op.execute("UPDATE resources SET availability_schedule = '{}'::json WHERE availability_schedule IS NULL")
    
    # nullable=Falseに変更
    op.alter_column(
        'resources',
        'availability_schedule',
        nullable=False
    )
    
    # profileカラムを追加（まずnullable=Trueで追加）
    op.add_column(
        'resources',
        sa.Column(
            'profile',
            sa.Text(),
            nullable=True,
            comment='プロフィール'
        )
    )
    
    # 既存データにデフォルト値を設定
    op.execute("UPDATE resources SET profile = '' WHERE profile IS NULL")
    
    # nullable=Falseに変更
    op.alter_column(
        'resources',
        'profile',
        nullable=False
    )
    
    # photosカラムを追加（オプション）
    op.add_column(
        'resources',
        sa.Column(
            'photos',
            sa.JSON(),
            nullable=True,
            comment='写真のURL配列'
        )
    )
    
    # tagsカラムを追加（オプション）
    op.add_column(
        'resources',
        sa.Column(
            'tags',
            sa.JSON(),
            nullable=True,
            comment='タグの配列'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('resources', 'tags')
    op.drop_column('resources', 'photos')
    op.drop_column('resources', 'profile')
    op.drop_column('resources', 'availability_schedule')
