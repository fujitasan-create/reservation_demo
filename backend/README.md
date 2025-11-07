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

## 使い方

```bash
make dev    # 開発サーバーを起動
make fmt    # コードフォーマット
make lint   # 静的解析
make help   # コマンド一覧を表示
```

