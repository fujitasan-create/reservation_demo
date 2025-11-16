# ============================
# FastAPI Reservation Demo Makefile
# ============================

# Python環境設定
PYTHON = uv run python
# MSYS環境でも動作するようにuvコマンドを自動検出
# 1. 環境変数UV_PATHが設定されている場合はそれを使用
# 2. そうでなければ、uvコマンドがPATHにあるか確認
# 3. 見つからない場合は、よくあるパスを順番に試す
ifeq ($(UV_PATH),)
  # まずuvコマンドがPATHにあるか確認
  UV_TEST := $(shell which uv 2>/dev/null || type uv 2>/dev/null || echo "")
  ifneq ($(UV_TEST),)
    UV = uv
  else
    # Windowsのよくあるuvパスを順番に試す（ユーザー名は環境変数から取得、なければblackをデフォルトに）
    USER_NAME := $(shell echo $$USER)
    ifeq ($(USER_NAME),)
      USER_NAME := black
    endif
    # 各パスを順番に確認
    UV_PYTHON310 := /c/Users/$(USER_NAME)/AppData/Local/Programs/Python/Python310/Scripts/uv.exe
    UV_PYTHON311 := /c/Users/$(USER_NAME)/AppData/Local/Programs/Python/Python311/Scripts/uv.exe
    UV_PYTHON312 := /c/Users/$(USER_NAME)/AppData/Local/Programs/Python/Python312/Scripts/uv.exe
    UV_CARGO := /c/Users/$(USER_NAME)/.cargo/bin/uv.exe
    # 存在するパスを探す
    UV := $(shell [ -f "$(UV_PYTHON310)" ] && echo "$(UV_PYTHON310)" || \
                  [ -f "$(UV_PYTHON311)" ] && echo "$(UV_PYTHON311)" || \
                  [ -f "$(UV_PYTHON312)" ] && echo "$(UV_PYTHON312)" || \
                  [ -f "$(UV_CARGO)" ] && echo "$(UV_CARGO)" || \
                  echo "")
    ifeq ($(UV),)
      $(warning uvコマンドが見つかりません。以下のいずれかを試してください:)
      $(warning 1. export UV_PATH=/c/Users/black/AppData/Local/Programs/Python/Python310/Scripts/uv.exe)
      $(warning 2. source .envrc (direnvを使用している場合))
      $(error uvコマンドが見つかりません。上記の方法で環境変数を設定してください)
    endif
  endif
else
  UV = $(UV_PATH)
endif
APP = main:app

# デフォルトタスク
.DEFAULT_GOAL := help

# ============================
# Commands
# ============================

## install : 依存関係をインストール
install:
	$(UV) sync

## run : 開発サーバを起動
dev:
	$(UV) run uvicorn $(APP) --reload --port 8000

## fmt : コードフォーマット (black, isort)
fmt:
	$(UV) run black . && $(UV) run isort .

## lint : 静的解析 (ruff)
lint:
	$(UV) run ruff check .

## db : SQLiteの中身確認（DBeaverで開く場合はパスを使う）
db:
	@echo "Database file: ./test.db"

## create-admin : 管理者アカウントを作成（インタラクティブ）
create-admin:
	$(PYTHON) scripts/create_admin.py

## create-admin-cli : 管理者アカウントを作成（コマンドライン引数版）
create-admin-cli:
	@echo "使用方法: make create-admin-cli EMAIL=admin@example.com PASSWORD=password123"
	@if [ -z "$(EMAIL)" ] || [ -z "$(PASSWORD)" ]; then \
		echo "エラー: EMAILとPASSWORDを指定してください"; \
		exit 1; \
	fi
	$(PYTHON) scripts/create_admin_cli.py --email "$(EMAIL)" --password "$(PASSWORD)"

## clean : キャッシュ削除
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f .coverage

## help : コマンド一覧を表示
help:
	@echo "Usage:"
	@grep -E '^##' $(MAKEFILE_LIST) | sed 's/## //'
