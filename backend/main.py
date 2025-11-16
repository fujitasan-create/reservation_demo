"""FastAPIアプリケーションエントリーポイント"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routers import admin, auth, resources, reservations, salon, upload
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
    auth.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    resources.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    reservations.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    admin.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    upload.router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    salon.router,
    prefix=settings.api_v1_prefix,
)

# 静的ファイル配信（画像アップロード用）
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {
        "message": "Reservation Demo API",
        "version": "1.0.0",
        "docs": "/docs",
    }