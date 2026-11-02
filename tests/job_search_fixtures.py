"""Build synthetic P02 pages outside the product for registered-state QA."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
from test_compare import load_screens, ROOT

out = Path(sys.argv[1])
ns = load_screens()
out.mkdir(parents=True, exist_ok=True)
(out/'jobs.json').write_text(json.dumps(ns['JOB_KEYS'], ensure_ascii=False))
for mode in ('registered', 'pending', 'empty'):
    data = {}
    for key, label in ns['JOB_KEYS']:
        posts=[]
        for i in range(13):
            skills = None if mode == 'pending' or i == 12 else ['a'] * 2 + ['b', 'c'] if i == 1 else [] if i == 11 else ['a', 'b'] if i == 2 else ['a']
            posts.append(dict(id=f'{key}-{i}', c=f'회사{i}', t=f'테스트 공고{i}', ty='인턴' if i%2 else '신입', d=f'2099-12-{13-i:02}', u='https://example.com/posting', s='', ov=999, cr=1000+i, demo=i==0, postingSkillIds=skills))
        data[key]={'label':label,'src':'검증 전용 가상 자료','posts':posts}
    profile=json.dumps(dict(resumeContent=[] if mode == 'empty' else ['작성된 경험'],resumeSkillIds=['a','a','b','c']))
    canvas=out/(mode+'-canvas');canvas.mkdir(exist_ok=True)
    for name in ('S1-list.dc.html','m-S1-list.dc.html'):
        html=ns['boards'][name][1].replace(ns['JOBS_JSON'],json.dumps(data,ensure_ascii=False)).replace(ns['PROFILE_JSON'],profile)
        (canvas/name).write_text(html)
    subprocess.run([sys.executable,str(ROOT/'design/scripts/export_static.py'),str(canvas),str(out/mode)],check=True)
    shutil.copyfile(ROOT/'design/scripts/dc-lite.js',out/mode/'dc-lite.js')
