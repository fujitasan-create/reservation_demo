"""管理者アカウント作成スクリプト"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database import SessionLocal
from app.domain.entities.user import User, UserRole
from app.repositories.user_repository import UserRepository


def create_admin_user(
    email: str, password: str, db: Session
) -> tuple[bool, str]:
    """
    管理者アカウントを作成

    Args:
        email: メールアドレス
        password: パスワード
        db: データベースセッション

    Returns:
        (成功フラグ, メッセージ)のタプル
    """
    repository = UserRepository(db)

    # 既存のユーザーを確認
    if repository.exists_by_email(email):
        existing_user = repository.get_by_email(email)
        if existing_user.role == UserRole.ADMIN:
            return False, f"管理者アカウント {email} は既に存在します。"
        else:
            # 既存のユーザーを管理者に変更
            repository.update(
                existing_user.id,
                {"role": UserRole.ADMIN, "password_hash": get_password_hash(password)},
            )
            db.commit()
            return True, f"既存のユーザー {email} を管理者アカウントに変更しました。"

    # 新しい管理者アカウントを作成
    admin_user = User(
        email=email,
        password_hash=get_password_hash(password),
        role=UserRole.ADMIN,
    )
    repository.create(admin_user)
    return True, f"管理者アカウント {email} を作成しました。"


def main():
    """メイン処理"""
    print("=" * 50)
    print("管理者アカウント作成スクリプト")
    print("=" * 50)
    print()

    # メールアドレスの入力
    email = input("メールアドレスを入力してください: ").strip()
    if not email:
        print("エラー: メールアドレスが入力されていません。")
        sys.exit(1)

    # パスワードの入力（表示されるように変更）
    password = input("パスワードを入力してください（数字4桁でも可）: ").strip()
    if not password:
        print("エラー: パスワードが入力されていません。")
        sys.exit(1)

    # 最小文字数チェック（緩和: 4文字以上、数字のみでも可）
    if len(password) < 4:
        print("エラー: パスワードは4文字以上である必要があります。")
        sys.exit(1)

    # bcryptの制限: パスワードは72バイト以内である必要がある
    # 72バイトを超える場合は自動的に切り詰める
    password_bytes = password.encode("utf-8")
    original_password_length = len(password_bytes)
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")
        print(f"注意: パスワードが72バイト（{original_password_length}バイト）を超えていたため、自動的に切り詰めました。")

    # パスワードの確認（表示されるように変更）
    password_confirm = input("パスワード（確認）: ").strip()
    # 確認パスワードも72バイトに切り詰める（元のパスワードと同じように処理）
    password_confirm_bytes = password_confirm.encode("utf-8")
    original_confirm_length = len(password_confirm_bytes)
    if len(password_confirm_bytes) > 72:
        password_confirm = password_confirm_bytes[:72].decode("utf-8", errors="ignore")
        if original_confirm_length != original_password_length:
            print(f"注意: 確認パスワードも72バイト（{original_confirm_length}バイト）を超えていたため、自動的に切り詰めました。")
    
    if password != password_confirm:
        print("エラー: パスワードが一致しません。")
        sys.exit(1)

    print()
    print("管理者アカウントを作成しています...")

    # データベースセッションの取得
    db = SessionLocal()
    try:
        success, message = create_admin_user(email, password, db)
        if success:
            print(f"✓ {message}")
            print()
            print("管理者アカウントの作成が完了しました。")
            print(f"メールアドレス: {email}")
        else:
            print(f"✗ {message}")
            sys.exit(1)
    except Exception as e:
        error_msg = str(e)
        print(f"✗ エラーが発生しました: {error_msg}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

