"""화면에 들어가는 데이터를 research/ 원본에서 다시 만든다. 결과는 design/data/*.json.

  policies.json    research/youth-policy/jobs_policies.json 중 서울시와 중앙부처 (fetch_policies.py 먼저)
  courses.json     research/sesac/courses.csv 210개
  posts2026.json   SNS 콘텐츠 마케팅 2026 신입, 인턴 공고 (sns_trend.py 분류 사용)
  jobs_other.json  다른 6개 직무 공고 (~/Documents/job-board-anu/daegieop/jobs.json, 팀원 PC에만 있음)

사용: python3 design/scripts/data_tools/build_data.py [policies courses posts jobs]  (인자 없으면 전부)
기준일은 오늘. 시연 화면을 바꾸지 않으려면 필요한 것만 다시 만든다.
"""
import collections, csv, datetime, json, os, re, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
OUT = os.path.join(REPO, 'design/data')
TODAY = datetime.date.today().strftime('%Y%m%d')


def policies():
    P = json.load(open(os.path.join(REPO, 'research/youth-policy/jobs_policies.json'), encoding='utf-8'))
    central = lambda n: n == '서울특별시' or (re.search(r'(부|처|청)$', n) and not re.search(r'(시청|도청|군청|구청)$', n))
    out = []
    for p in P:
        reg = p['rgtrHghrkInstCdNm'].strip()
        if not central(reg):
            continue
        m = re.findall(r'(\d{8})', (p.get('aplyYmd') or '').strip())
        # aplyPrdSeCd: 0057001 특정기간, 0057002 상시, 0057003 마감 (온통청년 API 코드 정의서). 마감 코드는 날짜가 없어도 마감
        closed = p.get('aplyPrdSeCd') == '0057003'
        st = '마감' if closed else (('신청 중' if m[0] <= TODAY <= m[-1] else ('예정' if m[0] > TODAY else '마감')) if m else '상시')
        per = f'{m[0][:4]}.{m[0][4:6]}.{m[0][6:]} ~ {m[-1][4:6]}.{m[-1][6:]}' if m else ('신청 마감' if closed else '상시 신청')
        desc = re.sub(r'\s+', ' ', p.get('plcyExplnCn') or '').strip()
        out.append({'id': 'pol-' + p['plcyNo'], 'n': p['plcyNm'].strip(), 'o': (p.get('sprvsnInstCdNm') or p.get('rgtrInstCdNm') or '').strip(),
                    'r': '서울' if reg == '서울특별시' else '중앙부처', 'c': p['mclsfNm'].split(',')[0], 'k': [k for k in (p.get('plcyKywdNm') or '').split(',') if k][:3],
                    'd': desc[:90] + ('…' if len(desc) > 90 else ''), 'st': st, 'per': per, 'end': m[-1] if m else '',
                    'u': 'https://www.youthcenter.go.kr/youthPolicy/ythPlcyTotalSearch/ythPlcyDetail/' + p['plcyNo'], 'v': int(p.get('inqCnt') or 0)})
    return out


GROUP = [('마케팅', r'마케팅|MD/BM|영상/광고|MICE|굿즈|엔터'), ('AI', r'AI|AICE'), ('데이터', r'데이터|빅데이터|웹크롤링|파이썬'), ('기획, PM', r'기획|PM'),
         ('개발', r'웹|앱|풀스택|프론트|안드로이드|퍼블리싱|임베디드|클라우드|보안|정보보호|핀테크|IOT|IoT|AIot|AIoT|모빌리티|AR/VR|바이브'), ('디자인', r'UI|UX|디자인|패션|스타일')]
STATUS = {'모집중': '모집 중', '모집예정': '모집 예정', '상시': '상시', '운영중': '진행 중', '운영대기': '진행 중', '과정종료': '종료'}


def courses():
    out = []
    for r in csv.DictReader(open(os.path.join(REPO, 'research/sesac/courses.csv'), encoding='utf-8-sig')):
        g = next((name for name, pat in GROUP if re.search(pat, r['분야'])), '기타')
        rec = r['모집기간'].split(' - ')
        url = (f"https://sesac.seoul.kr/sesac/course/offline/courseDetail.do?crsSn={r['crsSn']}" if r['유형'] == 'offline' else 'https://sesac.seoul.kr')
        out.append({'id': 'edu-' + r['crsSn'], 'n': r['과정명'].strip(), 'cp': r['캠퍼스'], 'f': r['분야'], 'g': g, 'st': STATUS[r['상태']],
                    'recEnd': rec[-1].strip() if len(rec) > 1 else '', 'edu': r['교육기간'].replace(' - ', ' ~ '), 'h': r['교육시간'], 'tags': r['해시태그'].split()[:3],
                    'rv': int(r['후기수'] or 0), 'u': url, 'on': r['유형'] == 'online'})
    return out


def posts():
    g = runpy.run_path(os.path.join(HERE, 'sns_trend.py'), run_name='lib')
    grp = {}
    for d in g['GROUPS'].values():
        grp.update(d)
    pat = {k: v for k, v in grp.items() if k in ('콘텐츠 기획', '데이터, 성과 분석', '디자인 툴 (포토샵, 피그마, 캔바)')}
    out, seen = [], set()
    for r in g['new']:
        if int(r['year']) != 2026:
            continue
        t, org = r['title'], r.get('org')
        m = re.match(r'\s*\[([^\]]+)\]\s*', t)
        if not org and m:
            org = m.group(1)
        title = re.sub(r'\s+', ' ', re.sub(r'^\s*\[[^\]]+\]\s*', '', t) if (m and org and m.group(1) == org) else t).strip()
        company = (org or '기업명 비공개').strip()
        if (company, title) in seen:
            continue
        seen.add((company, title))
        m2 = re.match(r'\s*\[([^\]]+)\]\s*', title)
        if m2 and (m2.group(1) in company or company in m2.group(1)):
            title = title[m2.end():]
        company = re.sub(r'^\(주\)|^주식회사\s*|\s*\(주\)$|\s*주식회사$', '', company).strip()
        ca, rid = r.get('closeAt'), str(r['id'])
        out.append({'company': company, 'title': title, 'type': '인턴' if ('INTERN' in str(r.get('jobTypes')) or '인턴' in t) else '신입',
                    'close': datetime.datetime.fromtimestamp(int(ca) / 1000).strftime('%Y-%m-%d') if ca else '',
                    'url': r.get('url') or (('https://linkareer.com/activity/' + rid.split('-')[-1]) if rid.startswith('linkareer') else ''),
                    'size': r.get('orgType') or '', 'ov': [k.split(' (')[0] for k, p in pat.items() if re.search(p, r['title'] + r['text'], re.I)],
                    'created': int(r.get('createdAt') or 0)})
    return out


JOBS = [('pm', '서비스 기획, PM', r'서비스 ?기획|프로덕트 ?(매니저|오너)|\bPM\b|\bPO\b|기획자'), ('data', '데이터 분석', r'데이터 ?(분석|사이언|애널)|\bDA\b|\bBI\b|Data Analy'),
        ('uiux', 'UI/UX 디자인', r'UI|UX|프로덕트 ?디자인|웹 ?디자인|BX'), ('web', '웹 개발', r'프론트|백엔드|웹 ?개발|풀스택|Front|Back-?end|서버 ?개발'),
        ('ai', 'AI 엔지니어', r'\bAI\b|인공지능|머신 ?러닝|딥 ?러닝|\bML\b|LLM'), ('cloud', '클라우드 엔지니어', r'클라우드|DevOps|\bSRE\b|인프라|AWS|Cloud')]


def jobs():
    J = json.load(open(os.path.expanduser('~/Documents/job-board-anu/daegieop/jobs.json'), encoding='utf-8'))['jobs']
    today = datetime.date.today().isoformat()
    out = {}
    for key, label, pat in JOBS:
        seen, L = set(), []
        for j in J:
            lv = str(j.get('level') or '')
            if not re.search(r'신입|인턴', lv) or not re.search(pat, j['title'], re.I) or (j['company'], j['title']) in seen:
                continue
            seen.add((j['company'], j['title']))
            d = str(j.get('deadline') or '')
            ct = str(j.get('company_type') or '')
            L.append({'id': 'post-' + str(j['id']).split('-')[-1], 'c': re.sub(r'^\(주\)|^주식회사\s*|\s*\(주\)$|㈜', '', str(j['company'])).strip(),
                      't': re.sub(r'^\s*\[[^\]]*\]\s*', '', j['title']).strip() or j['title'], 'ty': '인턴' if '인턴' in lv else '신입',
                      'd': d if re.match(r'\d{4}-\d{2}-\d{2}$', d) else '', 'u': j.get('detail_url') or j.get('apply_url') or '',
                      's': '' if ct in ('미상', 'None', '') else ct, 'ov': 0, 'cr': 0, 'demo': False})
        L.sort(key=lambda x: x['d'] or '9999')
        live = [x for x in L if not x['d'] or x['d'] >= today]
        out[key] = {'label': label, 'posts': live[:120], 'total': len(live)}
    return out


BUILD = {'policies': ('policies.json', policies), 'courses': ('courses.json', courses), 'posts': ('posts2026.json', posts), 'jobs': ('jobs_other.json', jobs)}

if __name__ == '__main__':
    for name in (sys.argv[1:] or BUILD):
        fname, fn = BUILD[name]
        data = fn()
        json.dump(data, open(os.path.join(OUT, fname), 'w', encoding='utf-8'), ensure_ascii=False, **({'indent': 0} if name == 'posts' else {}))
        print(fname, len(data))
