"""アプリケーション設定管理モジュール"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""

    # データベース設定
    database_url: str
    
    # API設定
    api_v1_prefix: str = "/api/v1"
    
    # アプリケーション設定
    app_name: str = "Reservation Demo API"
    debug: bool = False
    
    # JWT設定
    secret_key: str = "your-secret-key-change-in-production"  # 本番環境では環境変数から取得
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24時間
    
    # 営業時間設定
    business_hours_start: int = 9  # 9時
    business_hours_end: int = 21  # 21時

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # 未定義の環境変数を無視
    )


settings = Settings()

