"""Generate isolated empty/long-content pages for browser QA; no production data edits."""
from pathlib import Path
import subprocess
import shutil
import sys
from screen_loader import ROOT, load_screens

output = Path(sys.argv[1])
for kind in ('empty', 'long'):
    ns = load_screens()
    if kind == 'empty':
        ns.update(DUTIES=[], POST_REQ=[], PROCEDURE='')
    else:
        text = '긴문장검증' * 80
        ns['DUTIES'] = [text]
        ns['POST_REQ'] = [(title, [(text, 'no')], [('no', text, '프로젝트', 'S4-activity.dc.html')])
                          for title in ('자격요건', '우대사항')]
        ns['PROCEDURE'] = text
    body = ns['side_panel'](True) + ns['posting_card'](True)
    if kind == 'long':
        body = body.replace('학생회 홍보부 인스타그램 운영 1년', '긴 경험 요약 검증 ' * 80)
    html = ns['mpage']('m-S3-compare.dc.html', '테스트 공고', ns['topbar_back']('m-S1-list.dc.html', '공고와 비교'),
                       body + ns['compare_trend_popup'](True), 'find', ns['V6_SCRIPT'], saves=('olive',))
    canvas = output / (kind + '-canvas')
    canvas.mkdir(parents=True, exist_ok=True)
    (canvas / 'm-S3-compare.dc.html').write_text(html)
    subprocess.run([sys.executable, str(ROOT / 'design/scripts/export_static.py'), str(canvas), str(output / kind)], check=True)

    shutil.copyfile(ROOT / 'design/scripts/dc-lite.js', output / kind / 'dc-lite.js')
