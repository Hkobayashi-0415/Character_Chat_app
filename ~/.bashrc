# WSLでX11転送用DISPLAY自動設定
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0 