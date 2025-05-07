# Character Chat App

キャラクターとのチャットアプリケーション。PySide6を使用したデスクトップアプリケーションです。

## 機能

- キャラクター画像の表示とリサイズ
- チャット履歴の表示
- AIモデルの選択
- 音声ON/OFF機能

## 必要条件

- Python 3.8以上
- Docker
- X11（Linuxの場合）

## セットアップ

1. リポジトリのクローン
```bash
git clone https://github.com/Hkobayashi-0415/Character_Chat_app.git
cd Character_Chat_app
```

2. Dockerイメージのビルド
```bash
docker build -t character-chat-app .
```

3. アプリケーションの起動
```bash
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $XAUTHORITY:/home/appuser/.Xauthority:ro -v $(pwd):/app character-chat-app
```

## 開発

- `main.py`: メインアプリケーションコード
- `Dockerfile`: Dockerビルド設定
- `requirements.txt`: Python依存関係
- `img/`: キャラクター画像ディレクトリ

## ライセンス

MIT License 