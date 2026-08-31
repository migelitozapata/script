#!/data/data/com.termux/files/usr/bin/bash

set -e

CFG_URL="https://mgproxy.site.je/3proxy.cfg"
BUILD_DIR="$HOME/.build_tmp"
CFG_FILE="$HOME/3proxy.cfg"
PROXY_LOG_DIR="$PREFIX/var/log/3proxy"

pkg update -y
pkg upgrade -y

pkg install -y git clang make python curl

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

cd "$BUILD_DIR"
git clone https://github.com/3proxy/3proxy.git
cd 3proxy
make -f Makefile.Linux CC=clang PREFIX=

install -m 755 bin/3proxy "$PREFIX/bin/3proxy-bin"

mkdir -p "$PROXY_LOG_DIR"

curl -fsSL "$CFG_URL" -o "$CFG_FILE"

sed -i "s|^log .*|log ${PROXY_LOG_DIR}/3proxy.log D|" "$CFG_FILE"

cat > "$PREFIX/bin/3proxy" <<EOF
#!$PREFIX/bin/bash
exec "$PREFIX/bin/3proxy-bin" "\${1:-$CFG_FILE}"
EOF
chmod 755 "$PREFIX/bin/3proxy"

cd "$BUILD_DIR"
git clone https://github.com/Yisus7u7/termux-ngrok
cd termux-ngrok
bash install.sh

NGROK_BIN=$(find "$BUILD_DIR" -maxdepth 3 -type f -iname "ngrok" 2>/dev/null | head -n1)
if [ -n "$NGROK_BIN" ]; then
    install -m 755 "$NGROK_BIN" "$PREFIX/bin/ngrok"
else
    echo "Aviso: no se encontró el binario de ngrok tras install.sh, revisa $BUILD_DIR/termux-ngrok" >&2
fi

cd "$HOME"
rm -rf "$BUILD_DIR"
