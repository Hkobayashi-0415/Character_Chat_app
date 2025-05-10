#!/bin/bash

# 共通イメージのビルド
docker build -f Dockerfile.common -t character_chat_app:common .

# デスクトップ用イメージ
if [ "$1" = "desktop" ]; then
  docker build -f Dockerfile.desktop -t character_chat_app:desktop .
  echo "デスクトップ用イメージをビルドしました"
# WSL用イメージ
elif [ "$1" = "wsl" ]; then
  docker build -f Dockerfile.wsl -t character_chat_app:wsl .
  echo "WSL用イメージをビルドしました"
else
  echo "Usage: ./build.sh [desktop|wsl]"
fi 