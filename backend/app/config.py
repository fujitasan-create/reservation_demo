"""アプリケーション設定管理モジュール"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""

    # データベース設定
    database_url: str = "postgresql://user:password@localhost:5432/reservation_db"
    
    # API設定
    api_v1_prefix: str = "/api/v1"
    
    # アプリケーション設定
    app_name: str = "Reservation Demo API"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

