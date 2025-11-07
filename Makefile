# ============================
# Root Makefile - すべてのコマンドをbackend/Makefileに委譲
# ============================

.PHONY: install dev fmt lint clean help db

# すべてのターゲットをbackendディレクトリで実行
install dev fmt lint clean help db:
	@$(MAKE) -C backend $@

# デフォルトはhelp
.DEFAULT_GOAL := help

