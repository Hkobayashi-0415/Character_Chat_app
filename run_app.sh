#!/bin/bash
# WSLのX11 DISPLAYを自動取得してdocker-compose upを実行
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
docker-compose up 