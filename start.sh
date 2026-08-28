#!/usr/bin/env bash
set -euo pipefail

DISPLAY_NUM="${DISPLAY_NUM:-99}"
SCREEN="${SCREEN:-1280x720x24}"
VNC_PORT="${VNC_PORT:-5900}"
NOVNC_PORT="${NOVNC_PORT:-6080}"
URL="${URL:-https://google.com}"

export DISPLAY=":${DISPLAY_NUM}"

cleanup() {
  pkill -f "Xvfb :${DISPLAY_NUM}" || true
  pkill -f "x11vnc" || true
  pkill -f "websockify" || true
  pkill -f "google-chrome" || true
  pkill -f "google-chrome-stable" || true
}
trap cleanup EXIT

echo "🖥️ Starting virtual display..."
Xvfb ":${DISPLAY_NUM}" \
  -screen 0 "${SCREEN}" \
  -ac +extension RANDR &

sleep 2

# فقط Google Chrome واقعی
CHROME_BIN="/usr/bin/google-chrome"

if [ ! -x "${CHROME_BIN}" ]; then
  echo "❌ Google Chrome not found at ${CHROME_BIN}"
  exit 1
fi

echo "✅ Google Chrome found:"
"${CHROME_BIN}" --version

echo "🖥️ Starting VNC server..."
x11vnc \
  -display ":${DISPLAY_NUM}" \
  -rfbport "${VNC_PORT}" \
  -forever \
  -shared \
  -nopw \
  -xkb \
  -noxrecord \
  -noxfixes \
  -noxdamage &

sleep 1

# پیدا کردن فایل‌های noVNC
NOVNC_WEB=""

for p in \
  /usr/share/novnc \
  /usr/share/novnc/www \
  /usr/share/novnc/novnc
do
  if [ -d "$p" ]; then
    NOVNC_WEB="$p"
    break
  fi
done

if [ -z "${NOVNC_WEB}" ]; then
  echo "❌ noVNC web directory not found"
  exit 1
fi

echo "✅ noVNC directory: ${NOVNC_WEB}"

echo "🌐 Starting noVNC..."
websockify \
  --web="${NOVNC_WEB}" \
  "${NOVNC_PORT}" \
  "localhost:${VNC_PORT}" &

sleep 2

echo "🚀 Starting Google Chrome..."

"${CHROME_BIN}" \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --disable-extensions \
  --disable-background-networking \
  --disable-default-apps \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/tmp/chrome-profile \
  --window-size=1280,720 \
  --start-maximized \
  "${URL}" &

echo ""
echo "======================================"
echo "✅ Google Chrome is running"
echo "🌐 noVNC: http://localhost:${NOVNC_PORT}/vnc.html"
echo "======================================"
echo ""

wait
