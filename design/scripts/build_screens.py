"""캔버스 화면 만들기.

design/screens/ 의 파일을 이름 순서대로 하나의 이름 공간에서 실행한다.
  00_mobile_parts.py  모바일 공통 부품
  01_base.py          공통 토큰, 로그인과 저장, 메뉴, 페이지 틀
  10~70             페이지별 화면 (P01~P06)
  90_canvas.py      파일 쓰기와 canvas.json

사용: python3 design/scripts/build_screens.py design/canvas design/data/board_heights.json
보통은 ./design/build.sh 를 쓴다.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
DATA = os.path.join(DESIGN, 'data')
ROOT = sys.argv[1]

ns = {'__name__': 'illo_screens', 'json': json, 'os': os, 're': re, 'sys': sys, 'HERE': HERE, 'DATA': DATA, 'ROOT': ROOT}
for path in sorted(glob.glob(os.path.join(DESIGN, 'screens', '*.py'))):
    exec(compile(open(path, encoding='utf-8').read(), path, 'exec'), ns)
