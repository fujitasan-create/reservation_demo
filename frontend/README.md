# Frontend - Reservation Demo

Next.js + TypeScript + TailwindCSS で構築された予約システムのフロントエンド

## セットアップ

### 1. 依存関係のインストール

```bash
npm install
```

### 2. 環境変数の設定

`.env.local`ファイルを作成し、以下の内容を設定してください：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. APIクライアントの生成

バックエンドAPIが起動している状態で、以下のコマンドを実行：

```bash
npm run generate:api
```

### 4. 開発サーバーの起動

```bash
npm run dev
```

## スクリプト

- `npm run dev` - 開発サーバーを起動
- `npm run build` - プロダクションビルド
- `npm run start` - プロダクションサーバーを起動
- `npm run lint` - ESLintでコードをチェック
- `npm run generate:api` - APIクライアントを生成
- `npm run generate:api:watch` - APIクライアントを監視モードで生成

## 技術スタック

- **Next.js 16** - Reactフレームワーク
- **TypeScript** - 型安全性
- **Tailwind CSS v4** - スタイリング
- **Orval** - APIクライアント自動生成
- **TanStack Query** - データフェッチング
- **Axios** - HTTPクライアント
