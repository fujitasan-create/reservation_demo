# 予約サイトのデモ
予約サイトのデモです。こちらは一例ですので、予約したいもの・スケール・UIなどは拡張性を持たせており柔軟に変えることが可能です。
このリポジトリでは、一例として美容院の予約サイトにしております。
他にも、ホテル・旅館、居酒屋・カフェ、水・風など、様々な業種にあったものに変えていくことができます。
ご依頼がありましたらblackokayu@yahoo.co.jpまでお願いいたします。

## 使用技術

主要なものに関してのみまとめます。

### バックエンド(概説)
#### **Python3.11**
- FastAPI(API構築)
- uv(パッケージ管理)
- Makefile(開発効率化)
- Alembic(データベースの管理)
- SQLAlchemy(ORM)
- PostgreSQL(データベース)

#### **APIエンドポイント**

1. リソース管理API(予約可能な対象:人物・建物など)
   - `GET /api/resources` リソース一覧取得(ページネーション対応)
   - `GET /api/resources/{resource_id}` リソース詳細取得
   - `POST /api/resources` リソース作成
   - `PUT /api/resources/{resource_id}` リソース更新
   - `DELETE /api/resources/{resource_id}` リソース削除
2. 予約管理API
   - `GET /api/reservations` 予約一覧取得(resource_id, date でフィルタリング可能)
   - `GET /api/reservations/{reservation_id}` 予約詳細取得
   - `POST /api/reservations` 予約作成(顧客情報含む)
   - `PUT /api/reservations/{reservation_id}` 予約更新
   - `DELETE /api/reservations/{reservation_id}` 予約削除

#### ディレクトリ構成の概要

```
backend/
├── app/
│   ├── domain/              # ドメイン層（ビジネスロジックの中核）
│   │   ├── entities/        # エンティティ（SQLAlchemyモデル）
│   │   │   ├── resource.py
│   │   │   └── reservation.py
│   │   └── value_objects/   # 値オブジェクト（オプション）
│   │
│   ├── schemas/             # スキーマ層（DTO: データ転送オブジェクト）
│   │   ├── resource_schema.py
│   │   └── reservation_schema.py
│   │
│   ├── repositories/        # リポジトリ層（データアクセス）
│   │   ├── base.py          # ベースリポジトリ
│   │   ├── resource_repository.py
│   │   └── reservation_repository.py
│   │
│   ├── usecases/            # ユースケース層（アプリケーションロジック）
│   │   ├── resource_usecase.py
│   │   └── reservation_usecase.py
│   │
│   └── api/                 # プレゼンテーション層（HTTP API）
│       ├── dependencies.py  # 依存性注入
│       └── routers/
│           ├── resources.py
│           └── reservations.py
```
上記のような概略になっており、ドメイン・スキーマ・リポジトリ・ユースケース・APIの層で構成されています。
保守性・可読性・拡張性を重視しております。


### その他各種ツール類
- DBeaver(DBをUIで管理)
- Git/GitHub(バージョン管理)
- VScode(エディタ)
- Cursor(開発効率化AIエディタ)
- Notion(要件管理)
- DockerDesktop(Dockerコンテナを管理)
