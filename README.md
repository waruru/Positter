# Positter
## 本番環境

デプロイ先: [PythonAnywhere](https://www.pythonanywhere.com/)

url: [https://waruru.pythonanywhere.com/](https://waruru.pythonanywhere.com/)

## ローカルでのサーバー起動
前提条件
- `Docker` のインストール・設定が行われている

1. 環境変数の設定
  - .envファイル生成
```:ターミナル
touch .env
```
  - 環境変数の設定
```:.env
DB_USER='postgres'
DB_PASSWORD='postgres'

TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

GOOGLE_API_KEY=
```
※ `Twitter API`と`Google API`のKeyは各自で取得すること。
※ `GOOGLE_API`は`Natural Language API`を使用できるようにする必要がある。

2. 以下のコマンドをターミナルで実行
```
docker-compose build
docker-compose up
```

3. `localhost:8000`にアクセスする。

## バージョン情報
Python: 3.9

Django: 3.2
