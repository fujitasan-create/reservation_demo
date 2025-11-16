"""認証関連のAPIルーター"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_database_session
from app.config import settings
from app.core.security import create_access_token
from app.domain.entities.user import User, UserRole
from app.schemas.user_schema import Token, UserLogin, UserRegister, UserResponse
from app.usecases.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from app.usecases.user_usecase import UserUsecase

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_usecase(db: Session = Depends(get_database_session)) -> UserUsecase:
    """
    UserUsecaseの依存性注入

    Args:
        db: データベースセッション

    Returns:
        UserUsecaseインスタンス
    """
    return UserUsecase(db)


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="ユーザー登録",
)
def register(
    register_data: UserRegister,
    usecase: UserUsecase = Depends(get_user_usecase),
) -> Token:
    """
    新規ユーザーを登録します（一般ユーザーとして登録されます）。

    - **email**: メールアドレス（必須）
    - **password**: パスワード（必須、4文字以上）

    登録成功時に自動的にログインされ、JWTトークンを返します。
    """
    from app.schemas.user_schema import UserCreate

    try:
        # 一般ユーザーとして登録（role=user）
        user_create = UserCreate(
            email=register_data.email,
            password=register_data.password,
            role=UserRole.USER,  # 一般ユーザーとして登録
        )
        created_user = usecase.create_user(user_create)

        # 登録後、自動的にログインしてトークンを返す
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(created_user.id)}, expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(created_user),
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/login", response_model=Token, summary="ログイン")
def login(
    login_data: UserLogin,
    usecase: UserUsecase = Depends(get_user_usecase),
) -> Token:
    """
    ログインしてアクセストークンを取得します。

    - **email**: メールアドレス（必須）
    - **password**: パスワード（必須）

    認証成功時にJWTトークンを返します。
    """
    try:
        user = usecase.authenticate_user(login_data.email, login_data.password)

        # アクセストークンの作成
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.get("/me", response_model=UserResponse, summary="現在のユーザー情報を取得")
def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    現在ログインしているユーザーの情報を取得します。

    認証が必要です。
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout", summary="ログアウト")
def logout(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    ログアウトします。

    注意: JWTトークンはステートレスなので、実際のログアウト処理は
    クライアント側でトークンを削除することで行われます。
    このエンドポイントは主に将来の拡張（トークンブラックリストなど）のために用意されています。
    """
    return {"message": "ログアウトしました"}

