import json, re, glob, collections, sys

D = '/Users/anubilegdemberel/ddp-hackathon/research/job-trend/'
rows = []
for f in sorted(glob.glob(D + 'linkareer_marketing_*.json')):
    y = int(re.search(r'(\d{4})', f).group(1))
    for r in json.load(open(f)):
        r['year'] = y
        r['src'] = 'linkareer'
        rows.append(r)

# Extra 2026 postings with full JD (boards), used only for the subtype x spec comparison
MKT = re.compile(r'마케팅|마케터|광고|브랜드|홍보|PR|콘텐츠|컨텐츠|MD|CRM|그로스|퍼포먼스|SNS|캠페인', re.I)
extra = []
H = '/Users/anubilegdemberel/Documents/'
seen = {('linkareer', str(r['id'])) for r in rows}
for jf, df in [('job-board-anu/daegieop/jobs.json', 'job-board-anu/daegieop/details.json'),
               ('job-board-anu/jobs.json', 'job-board-anu/details.json')]:
    J = {j['id']: j for j in json.load(open(H + jf))['jobs']}
    for k, v in json.load(open(H + df)).items():
        j = J.get(k)
        jd = str(v.get('jd') or '')
        if not j or not MKT.search(j['title']) or len(jd) < 200:
            continue
        key = (j['source'], k.split('-')[-1])
        if key in seen:
            continue
        seen.add(key)
        lv = str(j.get('level') or '')
        extra.append({'id': k, 'title': j['title'], 'org': j.get('company'), 'orgType': j.get('company_type'),
                      'jobTypes': ['NEW'] if re.search(r'신입|인턴', lv) else [], 'text': jd, 'year': 2026, 'src': 'board'})

# Subtype: first match on title, then on body
SUB = [
    ('퍼포먼스/그로스', r'퍼포먼스|그로스|growth|퍼마|광고 ?운영|매체|디지털 ?광고|검색광고|SA|DA|ROAS|UA'),
    ('CRM/리텐션', r'CRM|리텐션|retention|LMS|앱푸시|고객관계'),
    ('콘텐츠/SNS', r'콘텐츠|컨텐츠|SNS|인스타|유튜브|숏폼|에디터|영상'),
    ('브랜드', r'브랜드|브랜딩|BM|brand'),
    ('PR/홍보', r'PR|홍보|언론|보도자료|대외협력'),
    ('커머스/MD', r'MD|커머스|이커머스|상품기획|머천'),
    ('B2B/영업 마케팅', r'B2B|영업 ?마케팅|세일즈|파트너'),
    ('마케팅 기획/전략', r'마케팅 ?기획|마케팅 ?전략|캠페인 ?기획|마케팅'),
]
def subtype(r):
    for name, p in SUB:
        if re.search(p, r['title'], re.I):
            return name
    for name, p in SUB:
        if re.search(p, r['text'][:1500], re.I):
            return name
    return '기타'

# Specs: label -> regex (searched in body + title)
SPEC = {
    'GA/GA4': r'\bGA4?\b|구글 ?애널리틱스|google analytics',
    'SQL': r'\bSQL\b',
    '엑셀': r'엑셀|excel|스프레드시트|구글 ?시트',
    'Python/R': r'python|파이썬|\bR\b',
    'BI(태블로 등)': r'tableau|태블로|power ?bi|루커|looker|데이터 ?스튜디오',
    '광고 매체(메타·구글애즈·네이버)': r'메타 ?광고|페이스북 ?광고|facebook ads|구글 ?애즈|google ads|네이버 ?(검색)?광고|카카오 ?모먼트|틱톡 ?광고',
    '앱 분석(앱스플라이어 등)': r'appsflyer|앱스플라이어|애드저스트|adjust|amplitude|앰플리튜드|브레이즈|braze|믹스패널|mixpanel',
    '디자인 툴(포토샵·피그마)': r'포토샵|photoshop|일러스트|illustrator|피그마|figma|캔바|canva',
    '영상 툴(프리미어 등)': r'프리미어|premiere|애프터 ?이펙트|after effects|캡컷|capcut|파이널 ?컷',
    '생성형 AI': r'생성형|chatgpt|챗gpt|\bgpt|미드저니|midjourney|프롬프트|AI ?(툴|도구|활용|프롬프트)|gemini|제미나이|클로드|claude',
    '데이터 분석 역량': r'데이터 ?분석|데이터 ?기반|지표|KPI|A/B|AB ?테스트|퍼널',
    '외국어': r'영어|english|중국어|일본어|토익|오픽|외국어|비즈니스 ?회화',
    '자격증': r'자격증|GAIQ|구글 ?애널리틱스 ?자격|검색광고마케터|사회조사분석사|컴활|컴퓨터활용능력',
    '포트폴리오': r'포트폴리오|portfolio',
    '운전면허': r'운전 ?면허',
    '커뮤니케이션/협업': r'커뮤니케이션|협업|소통',
}
def specs(r):
    t = r['title'] + '\n' + r['text']
    return {k for k, p in SPEC.items() if re.search(p, t, re.I)}

for r in rows + extra:
    r['sub'] = subtype(r)
    r['specs'] = specs(r)
    r['new'] = bool(set(r.get('jobTypes') or []) & {'NEW', 'INTERN'})

years = sorted({r['year'] for r in rows})
C = collections.Counter

out = {'n_by_year': {y: sum(1 for r in rows if r['year'] == y) for y in years}}
print('posts per year', out['n_by_year'])
print('with body text', sum(1 for r in rows if len(r['text']) > 200), 'of', len(rows))

print('\n== subtype share by year (%)')
subs = [s for s, _ in SUB] + ['기타']
for s in subs:
    line = []
    for y in years:
        ys = [r for r in rows if r['year'] == y]
        line.append(f"{100*sum(r['sub']==s for r in ys)/max(1,len(ys)):5.1f}")
    print(f'{s:16}', ' '.join(line))

print('\n== spec mention rate by year (%)  [' + ' '.join(map(str, years)) + ']')
for k in SPEC:
    line = []
    for y in years:
        ys = [r for r in rows if r['year'] == y and len(r['text']) > 200]
        line.append(f"{100*sum(k in r['specs'] for r in ys)/max(1,len(ys)):5.1f}")
    print(f'{k:24}', ' '.join(line))

print('\n== spec mention rate by subtype (%, all years, body text only)')
body = [r for r in rows + extra if len(r['text']) > 200]
print('linkareer with body', sum(r['src'] == 'linkareer' for r in body), '+ 2026 boards', len(extra))
cnt = C(r['sub'] for r in body)
print('n:', dict(cnt))
for s in subs:
    g = [r for r in body if r['sub'] == s]
    if len(g) < 5:
        continue
    top = C(x for r in g for x in r['specs']).most_common(8)
    print(f'{s} (n={len(g)}):', ', '.join(f'{k} {100*v/len(g):.0f}%' for k, v in top))

print('\n== level and org type by year')
for y in years:
    ys = [r for r in rows if r['year'] == y]
    print(y, '신입/인턴', f"{100*sum(r['new'] for r in ys)/max(1,len(ys)):.0f}%", C(r.get('orgType') for r in ys).most_common(4))

json.dump([{k: (sorted(v) if isinstance(v, set) else v) for k, v in r.items() if k != 'text'} for r in rows],
          open(D + 'coded.json', 'w'), ensure_ascii=False, indent=1)
