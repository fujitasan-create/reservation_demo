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

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # 未定義の環境変数を無視
    )


settings = Settings()

