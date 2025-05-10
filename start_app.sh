#!/bin/bash

XMING_PATH="/mnt/c/Program Files (x86)/Xming/Xming.exe"

# Xmingが起動していなければ起動
if ! pgrep -f Xming.exe > /dev/null; then
  nohup "$XMING_PATH" :0 -ac > /dev/null 2>&1 &
  echo "Xmingを起動しました。"
  sleep 2
else
  echo "Xmingはすでに起動しています。"
fi

docker-compose up -d 