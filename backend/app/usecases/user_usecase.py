"""User関連のユースケース"""
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.domain.entities.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.usecases.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserUsecase:
    """User関連のユースケース"""

    def __init__(self, db: Session):
        """
        初期化

        Args:
            db: データベースセッション
        """
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        ユーザーを作成

        Args:
            user_data: ユーザー作成データ

        Returns:
            作成されたユーザー

        Raises:
            UserAlreadyExistsError: メールアドレスが既に存在する場合
        """
        if self.repository.exists_by_email(user_data.email):
            raise UserAlreadyExistsError(f"メールアドレス {user_data.email} は既に登録されています")

        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role,
        )
        created_user = self.repository.create(user)
        return UserResponse.model_validate(created_user)

    def get_user(self, user_id: int) -> UserResponse:
        """
        ユーザーを取得

        Args:
            user_id: ユーザーID

        Returns:
            ユーザー

        Raises:
            UserNotFoundError: ユーザーが見つからない場合
        """
        user = self.repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f"ユーザーID {user_id} は存在しません")
        return UserResponse.model_validate(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        メールアドレスでユーザーを取得

        Args:
            email: メールアドレス

        Returns:
            ユーザー、存在しない場合はNone
        """
        return self.repository.get_by_email(email)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        ユーザーを認証

        Args:
            email: メールアドレス
            password: パスワード

        Returns:
            認証成功時はユーザー、失敗時はNone

        Raises:
            InvalidCredentialsError: 認証情報が無効な場合
        """
        user = self.repository.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError("メールアドレスまたはパスワードが正しくありません")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("メールアドレスまたはパスワードが正しくありません")

        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """
        ユーザーを更新

        Args:
            user_id: ユーザーID
            user_data: ユーザー更新データ

        Returns:
            更新されたユーザー

        Raises:
            UserNotFoundError: ユーザーが見つからない場合
            UserAlreadyExistsError: メールアドレスが既に存在する場合
        """
        user = self.repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f"ユーザーID {user_id} は存在しません")

        update_dict = user_data.model_dump(exclude_unset=True)

        # メールアドレスの重複チェック
        if "email" in update_dict and update_dict["email"] != user.email:
            if self.repository.exists_by_email(update_dict["email"]):
                raise UserAlreadyExistsError(
                    f"メールアドレス {update_dict['email']} は既に登録されています"
                )

        # パスワードのハッシュ化
        if "password" in update_dict:
            update_dict["password_hash"] = get_password_hash(update_dict.pop("password"))

        updated_user = self.repository.update(user_id, update_dict)
        if updated_user is None:
            raise UserNotFoundError(f"ユーザーID {user_id} は存在しません")

        return UserResponse.model_validate(updated_user)

    def is_admin(self, user: User) -> bool:
        """
        ユーザーが管理者かどうかを確認

        Args:
            user: ユーザー

        Returns:
            管理者の場合True、そうでない場合False
        """
        return user.role == UserRole.ADMIN

