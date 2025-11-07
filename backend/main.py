"""FastAPIアプリケーションエントリーポイント"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import resources, reservations
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="汎用的な予約システムのデモAPI",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(
    resources.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    reservations.router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {
        "message": "Reservation Demo API",
        "version": "1.0.0",
        "docs": "/docs",
    }