"""画像アップロード関連のAPIルーター"""
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.api.dependencies import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/upload", tags=["upload"])

# アップロードディレクトリの設定
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 許可する画像形式
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def is_allowed_file(filename: str) -> bool:
    """
    ファイル拡張子が許可されているか確認

    Args:
        filename: ファイル名

    Returns:
        許可されている場合True、そうでない場合False
    """
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


@router.post("/image", summary="画像をアップロード")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    """
    画像をアップロードします。

    - **file**: アップロードする画像ファイル

    認証が必要です。アップロードされた画像のURLを返します。
    """
    # ファイル拡張子の確認
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"許可されていないファイル形式です。許可されている形式: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # ファイルを保存
    file_ext = Path(file.filename).suffix.lower()
    filename = f"{current_user.id}_{int(file.filename or '0')}{file_ext}"
    file_path = UPLOAD_DIR / filename

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # 画像URLを返す（実際の本番環境では、クラウドストレージのURLを返す）
        image_url = f"/uploads/{filename}"

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"url": image_url, "filename": filename},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"画像アップロード中にエラーが発生しました: {str(e)}",
        ) from e


@router.post("/images", summary="複数の画像をアップロード")
async def upload_images(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    """
    複数の画像をアップロードします。

    - **files**: アップロードする画像ファイルのリスト

    認証が必要です。アップロードされた画像のURLリストを返します。
    """
    uploaded_urls = []

    for file in files:
        # ファイル拡張子の確認
        if not is_allowed_file(file.filename):
            continue

        # ファイルを保存
        file_ext = Path(file.filename).suffix.lower()
        filename = f"{current_user.id}_{int(file.filename or '0')}{file_ext}"
        file_path = UPLOAD_DIR / filename

        try:
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            # 画像URLを返す
            image_url = f"/uploads/{filename}"
            uploaded_urls.append({"url": image_url, "filename": filename})
        except Exception:
            continue

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"urls": uploaded_urls},
    )

