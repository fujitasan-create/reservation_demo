# Backend - FastAPI Reservation Demo

## セットアップ

### 依存関係のインストール

```bash
make install
```

### MSYS環境でのuvコマンドの設定

MSYS環境で`make dev`を実行する際に`uv: No such file or directory`エラーが発生する場合は、以下のいずれかの方法で解決できます：

#### 方法1: 自動検出（推奨・direnv不要）

Makefileが自動的に`uv`のパスを検出します。特別な設定は不要です。もし見つからない場合は、方法2または3を試してください。

#### 方法2: 環境変数を手動で設定

プロジェクトルートの`.envrc`ファイルをsourceして環境変数を設定：

```bash
source .envrc
# または
. .envrc

# これで環境変数が設定されます
make dev
```

#### 方法3: direnvを使用（オプション）

`direnv`がインストールされている場合：

```bash
# direnvがインストールされていることを確認
direnv version

# .envrcファイルを許可（初回のみ）
direnv allow

# これ以降、ディレクトリに入ると自動的に環境変数が設定されます
```

#### 方法4: PATHに追加（恒久的な解決策）

MSYS環境のシェル初期化ファイル（`~/.bashrc`など）に以下を追加：

```bash
export PATH="/c/Users/black/AppData/Local/Programs/Python/Python310/Scripts:$PATH"
```

その後、シェルを再起動するか、`source ~/.bashrc`を実行してください。

## データベースマイグレーション

マイグレーションを実行してデータベースをセットアップ：

```bash
# マイグレーションファイルの生成（モデル変更時）
alembic revision --autogenerate -m "description"

# マイグレーションの適用
alembic upgrade head
```

## 管理者アカウントの作成

マイグレーション完了後、管理者アカウントを作成します。

### 方法1: インタラクティブ（推奨）

```bash
make create-admin
```

実行すると、メールアドレスとパスワードの入力を求められます。

### 方法2: コマンドライン引数

```bash
make create-admin-cli EMAIL=admin@example.com PASSWORD=password123
```

### 方法3: Pythonスクリプトを直接実行

```bash
# インタラクティブ版
uv run python scripts/create_admin.py

# CLI版
uv run python scripts/create_admin_cli.py --email admin@example.com --password password123
```

**注意**:
- パスワードは4文字以上である必要があります
- bcryptの制限により、72バイトを超えるパスワードは自動的に切り詰められます
- 通常のASCII文字の場合は最大72文字まで使用可能です

## 使い方

```bash
make dev    # 開発サーバーを起動
make fmt    # コードフォーマット
make lint   # 静的解析
make help   # コマンド一覧を表示
```

