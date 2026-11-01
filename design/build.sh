#!/bin/sh
# 화면 다시 만들기: design/canvas (캔버스 원본) -> prototype/ (Vercel 배포용 정적 HTML)
set -e
cd "$(dirname "$0")/.."
python3 design/scripts/build_screens.py design/canvas design/data/v4_heights.json
python3 design/scripts/export_static.py design/canvas prototype
