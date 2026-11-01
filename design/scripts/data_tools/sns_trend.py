import json, os, re, glob, collections

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../research/job-trend/')
H = os.path.expanduser('~/Documents/')  # 2026 채용 게시판 원본 (repo 밖, 팀원 PC에만 있음)

rows = []
for f in sorted(glob.glob(D + 'linkareer_marketing_*.json')):
    y = int(re.search(r'(\d{4})', f).group(1))
    for r in json.load(open(f)):
        r['year'] = y
        r['src'] = 'linkareer'
        rows.append(r)

MKT = re.compile(r'마케팅|마케터|광고|브랜드|홍보|PR|콘텐츠|컨텐츠|MD|CRM|그로스|퍼포먼스|SNS|캠페인', re.I)
seen = {('linkareer', str(r['id'])) for r in rows}
extra = []
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
        extra.append({'id': k, 'title': j['title'], 'jobTypes': ['NEW'] if re.search(r'신입|인턴', lv) else [],
                      'text': jd, 'year': 2026, 'src': 'board'})

# Same subtype rules as scripts/analyze_mk.py
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

body = [r for r in rows + extra if len(r['text']) > 200]
sns = [r for r in body if subtype(r) == '콘텐츠/SNS']
new = [r for r in sns if set(r.get('jobTypes') or []) & {'NEW', 'INTERN'}]

GROUPS = {
  '역량 (교육과정 탭)': {
    '디자인 툴 (포토샵, 피그마, 캔바)': r'포토샵|photoshop|일러스트|illustrator|피그마|figma|캔바|canva',
    '포트폴리오': r'포트폴리오|portfolio',
    '영상 툴 (프리미어, 캡컷 등)': r'프리미어|premiere|애프터 ?이펙트|after effects|캡컷|capcut|파이널 ?컷',
    '영상, 숏폼 제작 (릴스, 쇼츠)': r'숏폼|쇼츠|shorts|릴스|reels|영상 ?(제작|편집|기획|촬영)',
    '데이터, 성과 분석': r'데이터 ?분석|데이터 ?기반|지표|KPI|A/B|AB ?테스트|퍼널|성과 ?분석|성과 ?측정|리포트|보고서',
    '콘텐츠 기획': r'콘텐츠 ?기획|컨텐츠 ?기획|콘텐츠 ?(아이디어|전략)|기획력',
    'SNS 채널 운영': r'(SNS|인스타그램|인스타|유튜브|틱톡|채널|계정) ?(운영|관리)',
    '카피라이팅, 글쓰기': r'카피|카피라이팅|글쓰기|문장력|작문|에디팅',
    '트렌드 감각, 밈': r'트렌드|밈|meme',
    '인플루언서, 크리에이터 협업': r'인플루언서|크리에이터|KOL|협찬',
    '생성형 AI 툴': r'생성형|chatgpt|챗gpt|\bgpt|미드저니|midjourney|프롬프트|AI ?(툴|도구|활용)',
    '외국어': r'영어|english|중국어|일본어|토익|오픽|외국어|비즈니스 ?회화',
  },
  '자격증 탭': {
    '자격증 언급 (어떤 것이든)': r'자격증|자격 ?소지|GTQ|GAIQ|검색광고마케터|컴활|컴퓨터활용능력|사회조사분석사',
    'GTQ (그래픽기술자격)': r'GTQ',
    '컴퓨터활용능력': r'컴활|컴퓨터활용능력',
    'GAIQ, 구글 애널리틱스 자격': r'GAIQ|구글 ?애널리틱스 ?자격',
    '검색광고마케터': r'검색광고마케터',
    '운전면허': r'운전 ?면허',
  },
  '비교과 탭': {
    '관련 경험 (경력, 실무 경험)': r'관련 ?(경험|경력)|실무 ?경험|유관 ?(경험|경력|업무)',
    '개인 SNS, 채널 운영 경험': r'(개인|본인) ?(SNS|채널|계정|블로그|유튜브)|채널을? 운영(해|한) ?(본|보신)|운영 ?경험',
    '인턴 경험': r'인턴 ?(경험|경력)',
    '공모전, 수상': r'공모전|수상',
    '서포터즈, 기자단, 대외활동': r'서포터즈|기자단|대외 ?활동|앰배서더',
  },
}

def rate(group, pat):
    t = lambda r: r['title'] + '\n' + r['text']
    return sum(bool(re.search(pat, t(r), re.I)) for r in group)

print(f"콘텐츠/SNS 공고 (본문 있음): {len(sns)}건  = 링커리어 {sum(r['src']=='linkareer' for r in sns)} + 2026 게시판 {sum(r['src']=='board' for r in sns)}")
print(f"그중 신입/인턴: {len(new)}건")
print(f"연도: {dict(collections.Counter(r['year'] for r in sns))}")
for g, specs in GROUPS.items():
    print(f"\n== {g}  [전체 n={len(sns)} | 신입 n={len(new)}]")
    res = [(k, rate(sns, p), rate(new, p)) for k, p in specs.items()]
    for k, a, b in sorted(res, key=lambda x: -x[1]):
        print(f"{k:28} {100*a/len(sns):5.1f}% ({a:3d})   신입 {100*b/max(1,len(new)):5.1f}% ({b})")
