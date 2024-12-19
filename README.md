# キログルメ

## クローン方法
リポジトリをクローンします。

```bash
git clone https://github.com/kikitetomoro/gourmet_search.git
cd gourmet_search
```

必要な環境変数を設定します。
プロジェクトのルートディレクトリに .env ファイルを作成し、必要な値を設定してください。：

```env
SECRET_KEY=your_secret_key
HOTPEPPER_API_KEY = your_api_key
DEBUG=True
```
## 実行方法
### 1. Docker コンテナの起動
Docker Compose を使用してアプリケーションを起動します。

```bash
docker-compose up --build
```
これにより、アプリケーションが http://localhost:8000 で起動します。

### 2. ngrok を使用して HTTPS 経由で公開 (オプション)
ngrok をインストールしていない場合は、以下のコマンドでインストールしてください：

```bash
sudo snap install ngrok
brew install nginx　#（mac）
```
その後、以下のコマンドを実行して ngrok を起動します：

```bash
ngrok http 8000
```
https://xxxxx.ngrok-free.app のような URL が表示されます。この URL を使用してアプリケーションにアクセスできます。

### 動作確認
ブラウザで以下の URL にアクセスしてください：
ローカル：http://localhost:8000
ngrok：https://xxxxx.ngrok-free.app

### 注意事項
Docker コンテナの停止
コンテナを停止する場合は、以下を実行してください：

```bash
docker-compose down
```
ngrok セッションは一時的ですので、ターミナルを閉じると公開 URL が無効になるため、再実行時には新しい URL を取得してください。


## ngrokを使用した理由
まず、ngrokとはローカルPC上で稼働しているネットワーク（TCP）サービスを外部公開できるサービスです。
なぜ、これを使用しようと思ったのかというとhttpsでの公開ができるということです。クラウドにあげなくても、ローカル環境をインターネットに公開するため外部ユーザーや検証用に HTTPS 経由でアクセスさせるときに便利です。
今回の課題では不要ですが、最近知ってとても便利だと思ったので使用してみました。

