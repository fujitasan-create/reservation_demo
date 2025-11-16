"""管理者アカウント作成CLIツール（コマンドライン引数版）"""
import argparse
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
    parser = argparse.ArgumentParser(
        description="管理者アカウントを作成するスクリプト"
    )
    parser.add_argument(
        "--email", "-e", required=True, help="管理者のメールアドレス"
    )
    parser.add_argument(
        "--password", "-p", required=True, help="管理者のパスワード"
    )

    args = parser.parse_args()

    email = args.email.strip()
    password = args.password.strip()

    if not email:
        print("エラー: メールアドレスが入力されていません。")
        sys.exit(1)

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

    print(f"管理者アカウントを作成しています...")
    print(f"メールアドレス: {email}")

    # データベースセッションの取得
    db = SessionLocal()
    try:
        success, message = create_admin_user(email, password, db)
        if success:
            print(f"✓ {message}")
            print()
            print("管理者アカウントの作成が完了しました。")
            sys.exit(0)
        else:
            print(f"✗ {message}")
            sys.exit(1)
    except ValueError as e:
        # bcrypt関連のエラー（72バイト制限など）をキャッチ
        error_msg = str(e)
        if "72 bytes" in error_msg.lower() or "truncate" in error_msg.lower():
            print("✗ エラー: パスワードが長すぎます（72バイト以内）。")
            print("   パスワードを短くして再試行してください。")
        else:
            print(f"✗ エラーが発生しました: {error_msg}")
        db.rollback()
        sys.exit(1)
    except Exception as e:
        error_msg = str(e)
        if "72 bytes" in error_msg.lower() or "truncate" in error_msg.lower():
            print("✗ エラー: パスワードが長すぎます（72バイト以内）。")
            print("   パスワードを短くして再試行してください。")
        else:
            print(f"✗ エラーが発生しました: {error_msg}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

