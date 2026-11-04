"""P05 마이페이지: 한눈에 보기, 저장함, 이력서 등록, 취업 수기."""

# 14 sections like a job-board resume (P05-F04). Filled ones show the persona, empty optional ones fold into one line.
# 취업 우대·병역은 묻지 않는다. 생년월일, 주소, 사진은 팀 결정으로 다시 받되 비교 요청에는 넣지 않는다 (PRD v1.3).
RSEC = [('basic', '인적사항', True, True), ('job', '희망 직무', True, True), ('skill', '스킬', True, False), ('school', '학력', True, True),
        ('career', '경력', True, False), ('act', '인턴, 대외활동', True, False), ('train', '교육', False, False), ('cert', '자격증', True, False),
        ('award', '수상', False, False), ('abroad', '해외 경험', False, False), ('lang', '어학', True, False), ('pf', '포트폴리오', True, False),
        ('intro', '자기소개서', True, False), ('cond', '희망 근무 조건', True, False)]
FOLD = [k for k, _, filled, _ in RSEC if not filled]
R_TOTAL, R_DONE = len(RSEC), sum(1 for _, _, filled, _ in RSEC if filled)
R_PCT = round(R_DONE * 100 / R_TOTAL)
R_COUNT = f'{R_TOTAL}개 중 {R_DONE}개 작성'

# --- S5 마이페이지 (내 경험 + 내 경로) ---
# P05-F17~F19 내 취업 경로: 목표 공고 하나 + 비교한 다른 공고 목록 + 목표로 정하기.
# 11/6은 P03이 비교 기록을 남기지 않아서, 처음에는 예시 기록 3개를 넣어 둔다 (예시 데이터 라벨). 브라우저 illo-path에 저장.
PATH_SEED = {'target': 'post-327326', 'items': [
    {'id': 'post-327326', 't': '[올리브인터내셔널] 성분에디터 콘텐츠 마케팅 인턴', 's': '채용연계형 인턴', 'u': POSTING, 'd': '2026-11-03',
     'total': 6, 'ok': 1, 'part': 1, 'miss': '숏폼 발행, 영상 툴, 트렌드, 실무 경험', 'demo': True,
     'next': 'SeSAC (강북5기) AI 활용 SNS 마케터 양성 과정', 'nextSub': '11/25 개강 · 모집 마감 11/8', 'nextU': SESAC + '1421', 'nextL': '과정 페이지'},
    {'id': 'post-358108', 't': '[카카오] 숏폼 서비스 영상 콘텐츠 제작 및 운영_어시스턴트', 's': '신입', 'u': 'https://linkareer.com/activity/358108', 'd': '2026-11-02',
     'total': 7, 'ok': 2, 'part': 1, 'miss': '영상 편집 툴, 숏폼 기획, 데이터 분석, 협업 경험', 'demo': False,
     'next': '', 'nextSub': '', 'nextU': '', 'nextL': ''},
    {'id': 'post-327328', 't': '[클래스101] [인턴] 콘텐츠 마케터', 's': '인턴', 'u': 'https://linkareer.com/activity/327328', 'd': '2026-10-31',
     'total': 5, 'ok': 2, 'part': 2, 'miss': '콘텐츠 성과 분석', 'demo': False,
     'next': '대외활동: 브랜드 SNS 서포터즈', 'nextSub': '포트폴리오에 올릴 결과물 만들기', 'nextU': 'https://linkareer.com/list/activity', 'nextL': '활동 찾기'}]}
MY_SCRIPT = ("  pageVals() {\n"
             "    const P = this.illoGet('illo-path', __PATH__) || { items: [] }, items = Array.isArray(P.items) ? P.items : [];\n"
             "    const sorted = items.slice().sort((a, b) => String(b.d).localeCompare(String(a.d)));\n"
             "    const tid = items.some((x) => x.id === P.target) ? P.target : (sorted[0] || {}).id;\n"
             "    const dec = (x) => Object.assign({}, x, { hasNext: !!x.next, noNext: !x.next, notDemo: !x.demo, date: String(x.d).slice(5).replace('-', '.'),\n"
             "      pick: () => this.illoSet('illo-path', { target: x.id, items: items }) });\n"
             "    const t = items.find((x) => x.id === tid);\n"
             "    const others = sorted.filter((x) => x.id !== tid).map(dec);\n"
             "    return { hasPath: !!t, noPath: !t, pt: t ? dec(t) : {}, others, hasOthers: others.length > 0 };\n"
             "  }").replace('__PATH__', json.dumps(PATH_SEED, ensure_ascii=False))


def mytabs(active, mobile=False):
    pre = 'm-' if mobile else ''
    out = ''
    for k, label, href in [('home', '한눈에 보기', 'S5-path.dc.html'), ('saved', '저장함 @@savedCount@@', 'S5-saved.dc.html'), ('resume', '이력서 등록', 'S5-resume.dc.html')]:
        on = k == active
        st = (f'background: #FFFFFF; color: {INK}; font-weight: 600; box-shadow: 0 1px 3px rgba(0,23,51,0.08);' if on else f'color: {SUB};')
        cur = ' aria-current="page"' if on else ''
        out += f'<a href="{pre}{href}"{cur} style="{"flex: 1 1 0; text-align: center; " if mobile else ""}padding: 9px 18px; border-radius: 9px; font-size: 14px; {st} text-decoration: none;">{label}</a>'
    return f'<nav aria-label="마이페이지 메뉴" style="display: {"flex" if mobile else "inline-flex"}; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06); {"" if mobile else "align-self: flex-start;"}">{out}</nav>'

def my_exp(mobile):
    p = 'm-' if mobile else ''
    rows = ''.join(f'<div style="display: flex; gap: 12px; padding: 12px 0; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.5;"><span style="width: 72px; flex-shrink: 0; color: {MUTE};">{k}</span><span>{v}</span></div>'
                   for k, v in [('학력', '미디어커뮤니케이션학과 · 2026.02 졸업 예정'), ('활동', '학생회 홍보부 인스타그램 운영 1년'), ('자격증', '컴퓨터활용능력 2급'), ('어학', 'OPIc IM2'), ('스킬', '캔바, 인스타그램 운영, 엑셀')])
    bar = f'<span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: {R_PCT}%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span>'
    return f'''    <section aria-labelledby="{p}cv" style="display: flex; flex-direction: column; gap: 12px; padding: {'20px' if mobile else '28px'}; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: baseline;"><h2 id="{p}cv" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">내 이력서</h2><span style="font-size: 13px; color: {SUB};">{R_TOTAL}개 항목 중 {R_DONE}개 작성</span></div>
      {bar}
      <div style="display: flex; flex-direction: column; margin-top: 4px;">{rows}</div>
      <a href="{p}S5-resume.dc.html" style="height: 48px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: {FILL}; color: {INK}; font-size: 15px; font-weight: 600; text-decoration: none;">이력서 등록, 수정하기</a>
      <span style="font-size: 12px; color: {MUTE};">이 이력서가 공고 비교에 자동으로 쓰여요</span>
    </section>
'''


def path_step(n, label, title, sub, on=True):
    c = BLUE if on else '#D1D6DB'
    return (f'<li style="display: flex; gap: 14px;"><span style="width: 28px; height: 28px; flex-shrink: 0; border-radius: 50%; background: {c}; color: #FFFFFF; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{n}</span>'
            f'<span style="display: flex; flex-direction: column; gap: 3px; padding-bottom: 6px;"><span style="font-size: 12px; color: {MUTE};">{label}</span><span style="font-size: 15px; font-weight: 600; line-height: 1.45;">{title}</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">{sub}</span></span></li>')


def my_path(mobile):
    p = 'm-' if mobile else ''
    iff = lambda v, body, d='false': f'<sc-if value="@@{v}@@" hint-placeholder-val="@@{d}@@">{body}</sc-if>'
    steps = (path_step(1, '목표 공고', '@@pt.t@@', f'@@pt.s@@ · <a href="@@pt.u@@" {EXT} style="text-decoration: none;">원문 공고 ↗</a>')
             + path_step(2, 'AI 비교 결과', '공고 요구 @@pt.total@@개 중 맞음 @@pt.ok@@개, 일부 @@pt.part@@개',
                         '찾지 못함: @@pt.miss@@' + iff('pt.demo', f' · <a href="{p}S3-compare.dc.html#result" style="text-decoration: none;">다시 보기</a>', 'true'))
             + path_step(3, '다음 행동 (내가 고름)', iff('pt.hasNext', '@@pt.next@@', 'true') + iff('pt.noNext', '아직 고르지 않았어요'),
                         iff('pt.hasNext', f'@@pt.nextSub@@ · <a href="@@pt.nextU@@" {EXT} style="text-decoration: none;">@@pt.nextL@@ ↗</a>', 'true') + iff('pt.noNext', '비교 결과에서 다음 행동을 골라 보세요'))
             + path_step('·', '그다음', '과정을 마치면 같은 공고와 다시 비교해 보세요', f'<a href="{p}S1-list.dc.html" style="text-decoration: none;">다른 공고와도 비교하기 ›</a>', False))
    row = (f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 10px; padding: 14px 0; border-top: 1px solid {LINE};">'
           f'<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 15px; font-weight: 600; line-height: 1.4;">@@o.t@@</span>'
           f'<span style="font-size: 13px; color: {SUB};">요구 @@o.total@@개 중 맞음 @@o.ok@@개, 일부 @@o.part@@개 · @@o.date@@ 비교</span></span>'
           f'<button type="button" onClick="@@o.pick@@" style="flex-shrink: 0; height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; cursor: pointer; font-family: inherit;">목표로 정하기</button></div>')
    others = iff('hasOthers', f'<div style="display: flex; flex-direction: column;"><h3 style="margin: 0 0 4px; font-size: 15px; font-weight: 700;">비교한 다른 공고</h3><sc-for list="@@others@@" as="o" hint-placeholder-count="2">{row}</sc-for></div>', 'true')
    empty = (f'<div style="display: flex; flex-direction: column; align-items: flex-start; gap: 10px;"><span style="font-size: 15px; font-weight: 600;">아직 비교한 공고가 없어요</span>'
             f'<a href="{p}S1-list.dc.html" style="height: 40px; padding: 0 16px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;">직무 찾기</a></div>')
    return f'''    <section aria-labelledby="{p}path" style="display: flex; flex-direction: column; gap: 16px; padding: {'20px' if mobile else '28px'}; {CARD}">
      <div style="display: flex; flex-direction: column; gap: 6px;"><div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap;"><h2 id="{p}path" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">내 취업 경로</h2><span style="padding: 4px 8px; border: 1.5px dashed #D1D6DB; border-radius: 6px; font-size: 11px; color: {SUB};">예시 데이터 · 비교 기록은 아직 예시예요</span></div>
      <span style="font-size: 13px; line-height: 1.5; color: {SUB};">비교해 본 공고 중 목표를 하나 정하고, 고른 다음 행동을 이어 가요. 공고 한 건의 자세한 비교는 비교 결과 화면에서 봐요</span></div>
      {iff('hasPath', f'<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px;">{steps}</ol>', 'true')}
      {iff('noPath', empty)}
      {others}
    </section>
'''


def my_profile(mobile):
    p = 'm-' if mobile else ''
    return f'''    <section style="display: flex; flex-direction: column; gap: 14px; padding: {'20px' if mobile else '24px'}; {CARD}">
      <div style="display: flex; align-items: center; gap: 14px;">{AVATAR_IMG(52) if not mobile else '<span aria-hidden="true" style="width: 52px; height: 52px; border-radius: 50%; background: ' + BLUE_BG + '; display: flex; align-items: center; justify-content: center;"><svg width="26" height="26" viewBox="0 0 24 24">' + ICON_ON['my'] + '</svg></span>'}<span style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 17px; font-weight: 700;">@@profileName@@</span><span style="font-size: 13px; color: {SUB};">취업 준비생 · 미디어커뮤니케이션학과</span></span></div>
      <div style="display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 12px; color: {SUB};">관심 직무</span><div style="display: flex; gap: 6px; flex-wrap: wrap;">{chip('SNS 콘텐츠 마케팅', True)}{ADD}</div></div>
    </section>
    <a href="{p}S5-saved.dc.html" style="display: flex; align-items: center; gap: 14px; padding: {'18px 20px' if mobile else '20px 24px'}; {CARD} color: {INK}; text-decoration: none;"><span aria-hidden="true" style="width: 44px; height: 44px; border-radius: 12px; background: {BLUE_BG}; display: flex; align-items: center; justify-content: center;"><svg width="22" height="22" viewBox="0 0 24 24" fill="{BLUE}" stroke="{BLUE}" stroke-width="1.6" stroke-linejoin="round">{BOOK}</svg></span><span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 16px; font-weight: 700;">저장함 @@savedCount@@개</span><span style="font-size: 13px; color: {SUB};">공고, 교육과정, 정책</span></span><span style="color: {MUTE};">›</span></a>
    <a href="{p}S6-story.dc.html" style="display: flex; flex-direction: column; gap: 8px; padding: {'20px' if mobile else '24px'}; {CARD} color: {INK}; text-decoration: none;"><span style="font-size: 16px; font-weight: 700;">취업하셨나요?</span><span style="font-size: 13px; line-height: 1.55; color: {SUB};">어떤 경험과 과정이 도움이 됐는지 남겨 주시면, 같은 공고를 보는 다음 청년의 추천 근거가 돼요</span><span style="font-size: 14px; font-weight: 600; color: {BLUE};">취업 수기 남기기 ›</span></a>
'''


s5_body = f'''  <div style="padding: 24px 56px 0; display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 15px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아도 돼요</span><div style="margin-top: 12px;">{mytabs('home')}</div></div>
  <div style="display: grid; grid-template-columns: 360px minmax(0, 1fr); gap: 24px; padding: 24px 56px 56px; align-items: start;">
    <div style="display: flex; flex-direction: column; gap: 16px;">
{my_profile(False)}    </div>
    <div style="display: flex; flex-direction: column; gap: 16px;">
{my_exp(False)}{my_path(False)}    </div>
  </div>
'''
boards['S5-path.dc.html'] = ('S5 마이페이지 (내 경험, 내 경로)', dpage('S5-path.dc.html', '마이페이지', 'my', s5_body, MY_SCRIPT))

# --- mobile ---
m_s5 = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 13px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아요</span></div>
    {mytabs('home', True)}
{my_profile(True).split('    <a href=')[0]}{my_exp(True)}{my_path(True)}    <a href={my_profile(True).split('    <a href=')[1]}'''
boards['m-S5-path.dc.html'] = ('M5 마이페이지 (모바일)', mpage('m-S5-path.dc.html', 'M5 마이페이지 (모바일)', topbar_logo(auth_mobile()), m_s5, 'my', MY_SCRIPT))

# --- S5b 이력서 등록 (마이페이지 두 번째 탭) ---
INTRO = ('학생회 홍보부에서 1년 동안 인스타그램 계정을 맡았습니다. 매주 카드뉴스를 캔바로 만들어 올렸고, 팔로워는 300명에서 1,200명으로 늘었습니다. '
         '반응이 좋았던 게시물의 공통점을 정리해 다음 기획에 반영했던 경험을 살려, 숫자로 이야기하는 콘텐츠 마케터가 되고 싶습니다.')


RDEF = {}       # 칸 키 -> 예시 이력서 값. 데스크톱과 모바일이 같은 순서로 그려서 키가 같다
_rk = [0]


def _rkey(val):
    _rk[0] += 1
    k = f'f{_rk[0]}'
    RDEF[k] = val
    return k


def rf(label, val='', ph='', span=1, req=False, kind='text'):
    star = f' <span style="color: {RED};">*</span>' if req else ''
    k = _rkey(val)
    return (f'<label style="grid-column: span {span}; display: flex; flex-direction: column; gap: 6px; min-width: 0;"><span style="font-size: 13px; color: {SUB};">{label}{star}</span>'
            f'<input type="{kind}" data-rk="{k}" value="@@rv.{k}@@" placeholder="{ph}" style="{INP_D} font-size: 15px;"></label>')


def rta(label, val='', ph='', h=96, span=2, count=''):
    c = f'<span style="align-self: flex-end; font-size: 12px; color: {MUTE};">{count}</span>' if count else ''
    k = _rkey(val)
    return (f'<label style="grid-column: span {span}; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 13px; color: {SUB};">{label}</span>'
            f'<textarea data-rk="{k}" placeholder="{ph}" style="{TA_D} height: {h}px; font-size: 15px;">@@rv.{k}@@</textarea>{c}</label>')


def rgrid(cols, *fields):
    return f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;">{"".join(fields)}</div>'


def rentry(*rows):
    return f'<div style="display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: 14px; background: #F9FAFB;">{"".join(rows)}</div>'


def radd(label):
    return f'<button type="button" style="height: 44px; border: 1.5px dashed #D1D6DB; border-radius: 12px; background: #FFFFFF; color: {SUB}; font-size: 14px; cursor: pointer;">+ {label} 추가</button>'


def rchips(items, on=True):
    x = '<span aria-hidden="true" style="margin-left: 4px; opacity: 0.6;">✕</span>'
    return ''.join(f'<span style="display: inline-flex; align-items: center; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG if on else FILL}; color: {BLUE_D if on else "#4E5968"}; font-size: 14px;">{t}{x if on else ""}</span>' for t in items)


def rcard(key, title, body, sub='', mobile=False, ai=True):
    if ai:
        title = f'<span style="display: inline-flex; align-items: center; gap: 8px;">{title}<sc-if value="@@aiDone@@" hint-placeholder-val="@@false@@">{AI}</sc-if></span>'
    return (f'    <section id="{"m-" if mobile else ""}r-{key}" aria-labelledby="{"m-" if mobile else ""}rh-{key}" style="display: flex; flex-direction: column; gap: 16px; padding: {"20px 18px" if mobile else "26px 28px"}; {CARD} scroll-margin-top: 16px;">\n'
            f'      <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px;"><h2 id="{"m-" if mobile else ""}rh-{key}" style="margin: 0; font-size: {17 if mobile else 19}px; font-weight: 700;">{title}</h2><span style="font-size: 12px; color: {MUTE}; text-align: right;">{sub}</span></div>\n'
            f'      {body}\n    </section>\n')


def rfold(key, title, hint, body, mobile=False):
    """Empty optional section: one line until opened."""
    return (f'    <sc-if value="@@shut.{key}@@" hint-placeholder-val="@@true@@">\n'
            f'    <div id="{"m-" if mobile else ""}r-{key}" style="display: flex; align-items: center; gap: 12px; padding: {"16px 18px" if mobile else "18px 28px"}; {CARD}"><span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 16px; font-weight: 700;">{title}</span><span style="font-size: 12px; color: {MUTE};">{hint}</span></span>'
            f'<button type="button" onClick="@@toggle.{key}@@" style="flex-shrink: 0; height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">+ 추가</button></div>\n'
            f'    </sc-if>\n    <sc-if value="@@open.{key}@@" hint-placeholder-val="@@false@@">\n'
            + rcard(key, title, body + f'<button type="button" onClick="@@toggle.{key}@@" style="align-self: flex-start; border: none; background: none; padding: 0; font-size: 13px; color: {MUTE}; cursor: pointer;">접기</button>', '선택', mobile, ai=False)
            + '    </sc-if>\n')


def resume_sections(mobile):
    _rk[0] = 0
    c2, c3, c4 = (2, 2, 2) if mobile else (2, 3, 4)
    tools = '<span style="font-size: 12px; color: {}; ">공고에서 많이 찾는 툴</span>'.format(SUB)
    sugg = ''.join(f'<span style="padding: 7px 12px; border-radius: 999px; border: 1px solid #E5E8EB; font-size: 13px; color: #4E5968;">+ {t} <span style="color: {MUTE};">{n}건</span></span>' for t, n in [('프리미어', 30), ('포토샵', 28), ('피그마', 19), ('캡컷', 10)])
    photo = (f'<span aria-hidden="true" style="width: 96px; height: 120px; flex-shrink: 0; border-radius: 12px; border: 1.5px dashed #D1D6DB; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: {MUTE}; font-size: 12px;">'
             f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="9" r="3.5"/><path d="M5 20c1-3.5 3.8-5 7-5s6 1.5 7 5"/></svg>사진 · 선택</span>')
    basic = (rgrid(c3, rf('이름', '김하늘', req=True), rf('생년월일', '2002.03.14', req=True), rf('성별', '여', 'ex. 여'), rf('이메일', '', 'name@example.com', req=True, kind='email'), rf('휴대폰', '', '010-0000-0000', req=True, kind='tel'), rf('주소', '서울 성북구', '시, 구까지만'))
             + rgrid(1, rf('홈페이지, SNS', '', 'https://')))
    basic = basic if mobile else f'<div style="display: flex; gap: 20px; align-items: flex-start;"><div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 12px;">{basic}</div>{photo}</div>'
    out = ''
    out += rcard('basic', '인적사항', basic, '비교에는 쓰지 않아요', mobile)
    out += rcard('job', '희망 직무', f'<div style="display: flex; gap: 6px; flex-wrap: wrap;">{rchips(["SNS 콘텐츠 마케팅", "콘텐츠 마케터"])}</div>{radd("직무")}', '최대 5개', mobile)
    out += rcard('skill', '스킬', f'<div style="display: flex; gap: 6px; flex-wrap: wrap;">{rchips(["캔바", "인스타그램 운영", "엑셀"])}</div><div style="display: flex; flex-direction: column; gap: 8px;">{tools}<div style="display: flex; gap: 6px; flex-wrap: wrap;">{sugg}</div></div>', 'SNS 콘텐츠 마케팅 공고 104건 기준 추천', mobile)
    out += rcard('school', '학력', rentry(rgrid(c3, rf('학교 구분', '대학교 (4년제)', req=True), rf('학교명', '', '학교 이름', req=True), rf('전공', '미디어커뮤니케이션학과', req=True)),
                                           rgrid(c4, rf('입학', '2021.03'), rf('졸업', '2026.02'), rf('상태', '졸업 예정'), rf('학점', '3.83 / 4.5'))) + radd('학력'), '최종 학력부터', mobile)
    out += rcard('career', '경력', f'<label style="display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-radius: 14px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 15px; font-weight: 600; cursor: pointer;"><input type="checkbox" checked style="width: 18px; height: 18px; accent-color: {BLUE};">신입이에요</label><span style="font-size: 13px; color: {SUB};">경력이 생기면 체크를 풀고 회사, 기간, 담당 업무를 적어요</span>', '', mobile)
    out += rcard('act', '인턴, 대외활동', rentry(rgrid(c3, rf('구분', '교내 활동'), rf('기관, 단체', '학생회 홍보부'), rf('기간', '2024.03 ~ 2025.02')),
                                                rta('활동 내용', '인스타그램 계정 운영 1년\n카드뉴스 주 1회 제작 (캔바)\n팔로워 300명에서 1,200명', h=104)) + radd('활동'), '공고 비교에 가장 많이 쓰여요', mobile)
    out += rfold('train', '교육', '부트캠프, 직무 교육, SeSAC 과정', rentry(rgrid(c3, rf('교육명', '', '과정 이름'), rf('기관', '', 'ex. SeSAC'), rf('기간', '', '2026.11 ~ 2027.03')), rta('내용', '', '배운 것과 만든 결과물', h=80)), mobile)
    out += rcard('cert', '자격증', rentry(rgrid(c3, rf('자격증명', '컴퓨터활용능력 2급'), rf('발행처', '대한상공회의소'), rf('취득일', '2024.08'))) + radd('자격증'), '이 직무 공고는 3%만 자격증을 적어요', mobile)
    out += rfold('award', '수상', '공모전, 대회 수상', rentry(rgrid(c3, rf('수상명', '', '대회와 상 이름'), rf('수여 기관'), rf('수상일', '', '2025.11'))), mobile)
    out += rfold('abroad', '해외 경험', '어학연수, 교환학생, 워홀', rentry(rgrid(c3, rf('국가', '', 'ex. 캐나다'), rf('기간', '', '2024.01 ~ 2024.03'), rf('구분', '', '어학연수')), rta('내용', '', '무엇을 했는지 한두 줄', h=72)), mobile)
    out += rcard('lang', '어학', rentry(rgrid(c4, rf('외국어', '영어'), rf('시험', 'OPIc'), rf('등급, 점수', 'IM2'), rf('취득일', '2025.06'))) + radd('어학'), '외국어를 적은 공고 14%', mobile)
    out += rcard('pf', '포트폴리오', rgrid(1, rf('링크', '', 'https://instagram.com/학생회 계정', kind='url'))
                 + f'<label style="display: flex; align-items: center; gap: 10px; height: 48px; padding: 0 14px; border-radius: 12px; border: 1.5px dashed #D1D6DB; cursor: pointer;"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4"/><path d="M7 9l5-5 5 5"/><path d="M5 20h14"/></svg><span style="font-size: 15px;">파일 올리기</span><span style="margin-left: auto; font-size: 12px; color: {MUTE};">PDF, 이미지 · 20MB</span><input type="file" style="display: none;"></label>',
                 '링크나 파일', mobile)
    out += rcard('intro', '자기소개서', rgrid(1, rf('제목', '숫자로 이야기하는 콘텐츠 마케터')) + rta('내용', INTRO, h=150 if mobile else 128, span=1, count=f'{len(INTRO)} / 1,000자'),
                 '', mobile)
    cond = (rgrid(c3, rf('고용 형태', '인턴, 정규직'), rf('근무 지역', '서울'), rf('희망 연봉', '회사 내규에 따름')))
    out += rcard('cond', '희망 근무 조건', cond, '', mobile)
    return out


def resume_nav():
    items = ''
    for k, name, filled, req in RSEC:
        dot = (f'<span style="width: 18px; height: 18px; border-radius: 50%; background: {BLUE}; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
               if filled else '<span style="width: 18px; height: 18px; border-radius: 50%; border: 1.5px solid #D1D6DB; box-sizing: border-box;"></span>')
        star = f'<span style="color: {RED}; font-size: 12px;">*</span>' if req else ''
        items += f'<a href="#r-{k}" style="display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 10px; color: {INK if filled else SUB}; font-size: 14px; text-decoration: none;">{dot}{name}{star}</a>'
    return f'''    <aside style="position: sticky; top: 24px; display: flex; flex-direction: column; gap: 14px; padding: 22px 16px; {CARD}">
      <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 6px;"><span style="font-size: 15px; font-weight: 700;">{R_COUNT}</span><span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: {R_PCT}%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span></div>
      <nav aria-label="이력서 항목" style="display: flex; flex-direction: column;">{items}</nav>
      <button type="button" onClick="@@save@@" style="height: 52px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; cursor: pointer;">이력서 저장</button>
      <sc-if value="@@saved@@" hint-placeholder-val="@@false@@"><span style="padding: 0 6px; font-size: 12px; line-height: 1.5; color: {BLUE_D};">저장했어요 · 이 기기 브라우저에만 저장돼요</span></sc-if>
    </aside>
'''


LOCK = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'


def resume_note(mobile):
    """P05-F24 폼 위 저장 위치 안내."""
    return f'    <p style="display: flex; align-items: center; gap: 6px; margin: 0; padding: 0 4px; font-size: 13px; color: {SUB};">{LOCK}이 정보는 이 기기에만 저장돼요</p>\n'


PDF_ICON = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 17v-6M9.5 13.5L12 11l2.5 2.5"/></svg>'
CHECK_ICON = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#166534" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'


def resume_ai_desk():
    """P05-F12 데스크톱: 한 카드, 두 상태. 올린 뒤에는 올리기 버튼을 회색 보조 버튼으로 낮춘다 (주요 행동은 이력서 저장)."""
    btn = 'height: 44px; padding: 0 18px; display: inline-flex; align-items: center; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit; white-space: nowrap;'
    file_in = '<input type="file" accept="application/pdf,.pdf" onChange="@@pickPdf@@" style="display: none;">'
    err = f'<sc-if value="@@pdfErr@@" hint-placeholder-val="@@false@@"><span role="alert" style="font-size: 13px; color: {RED};">PDF 파일만 올릴 수 있어요. 다른 파일이면 PDF로 저장한 뒤 올려 주세요</span></sc-if>'
    empty = (f'<div style="display: flex; flex-direction: column; gap: 12px; padding: 20px 24px; border-radius: 20px; background: #F4F9FF;">'
             f'<div style="display: flex; align-items: center; gap: 16px;">'
             f'<span style="width: 44px; height: 44px; flex-shrink: 0; border-radius: 12px; background: #FFFFFF; color: {BLUE_D}; display: flex; align-items: center; justify-content: center;">{PDF_ICON}</span>'
             f'<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;"><span style="display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 700;">이력서 PDF가 있나요?{AI}</span>'
             f'<span style="font-size: 13px; line-height: 1.5; color: {SUB};">올리면 AI가 항목을 나눠 채워요 · PDF 파일만</span></span>'
             f'<div style="display: flex; gap: 8px; flex-shrink: 0;"><label style="{btn} background: {BLUE}; color: #FFFFFF;">PDF 올리기{file_in}</label>'
             f'<button type="button" onClick="@@tryAi@@" style="{btn} background: #FFFFFF; color: {BLUE_D};">예시 PDF로 해 보기</button></div></div>{err}</div>')
    done = (f'<div role="status" style="display: flex; flex-direction: column; gap: 14px; padding: 20px 24px; border-radius: 20px; background: #FFFFFF;">'
            f'<div style="display: flex; align-items: center; gap: 16px;">'
            f'<span style="width: 44px; height: 44px; flex-shrink: 0; border-radius: 50%; background: #E8F5EC; display: flex; align-items: center; justify-content: center;">{CHECK_ICON}</span>'
            f'<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;">'
            f'<span style="display: flex; align-items: center; gap: 8px; min-width: 0;"><span style="min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 16px; font-weight: 700;">@@pdf@@</span>{AI}</span>'
            f'<span style="font-size: 13px; line-height: 1.5; color: {SUB};">{R_DONE}개 항목을 채웠어요 · 비어 있는 {R_TOTAL - R_DONE}개는 접어 두었어요</span></span>'
            f'<label style="{btn} background: {FILL}; color: {INK};">다시 올리기{file_in}</label></div>'
            f'<span style="padding-top: 12px; border-top: 1px solid {LINE}; font-size: 13px; line-height: 1.5; color: {SUB};">AI 표시가 붙은 항목이 맞는지 확인하고 저장해 주세요'
            f'<span style="color: {MUTE};"> · 시연이라 PDF 내용 대신 예시 이력서 값으로 채워요</span></span>{err}</div>')
    return (f'    <sc-if value="@@aiNot@@" hint-placeholder-val="@@true@@">{empty}</sc-if>\n'
            f'    <sc-if value="@@aiDone@@" hint-placeholder-val="@@false@@">{done}</sc-if>\n')


def resume_ai(mobile):
    """P05-F12 PDF로 채우기. 11/6은 프론트 시연이라 PDF 내용 대신 예시 이력서 값으로 채운다.
    데스크톱은 카드 하나가 상태를 바꾼다 (올리기 전 안내 -> 올린 뒤 결과). 모바일은 이전 구조 유지."""
    if not mobile:
        return resume_ai_desk()
    btn = f'height: 44px; padding: 0 18px; display: inline-flex; align-items: center; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; font-family: inherit; white-space: nowrap;'
    return f'''    <div style="display: flex; flex-direction: column; gap: 12px; padding: {"16px 18px" if mobile else "18px 24px"}; border-radius: 20px; background: #F4F9FF;">
      <div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 12px;">
      <span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 4px;"><span style="display: flex; align-items: center; gap: 6px; font-size: 15px; font-weight: 700;">{AI}이력서 PDF가 있나요?</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">올리면 AI가 항목을 나눠 채워요. 채운 뒤 맞는지만 확인하면 돼요</span></span>
      <div style="display: flex; gap: 8px; flex-shrink: 0;"><label style="{btn} background: {BLUE}; color: #FFFFFF;">@@aiLabel@@<input type="file" accept="application/pdf,.pdf" onChange="@@pickPdf@@" style="display: none;"></label><button type="button" onClick="@@tryAi@@" style="{btn} background: #FFFFFF; color: {BLUE_D};">예시 PDF로 해 보기</button></div>
      </div>
      <sc-if value="@@pdfErr@@" hint-placeholder-val="@@false@@"><span role="alert" style="font-size: 13px; color: {RED};">PDF 파일만 올릴 수 있어요</span></sc-if>
    </div>
    <sc-if value="@@aiDone@@" hint-placeholder-val="@@false@@"><div role="status" style="display: flex; flex-direction: column; gap: 4px; padding: 12px 16px; border-radius: 14px; background: #F0EBFF; font-size: 14px; line-height: 1.5; color: #4B36B5;"><span style="display: flex; align-items: center; gap: 8px;">{AI}<span><b>@@pdf@@</b>에서 {R_DONE}개 항목을 채웠어요. 비어 있는 {R_TOTAL - R_DONE}개는 접어 두었어요</span></span><span style="font-size: 12px; color: #6B4EE6;">AI 표시가 붙은 항목이 맞는지 확인하고 저장해 주세요 · 시연이라 PDF 내용 대신 예시 이력서 값으로 채워요</span></div></sc-if>
'''


_fold_js = ', '.join(f'{k}: false' for k in FOLD)
RESUME_SCRIPT = ("  constructor(props) { super(props); this.state = { open: { " + _fold_js + " }, ai: false, pdf: '', pdfErr: false, saved: false, draft: null }; }\n"
                 # 다시 그리기 전에 입력 중인 값을 잡아 둔다 (화면 전체를 다시 그리므로)
                 "  snap() { const o = {}; try { document.querySelectorAll('[data-rk]').forEach((el) => { o[el.getAttribute('data-rk')] = el.value; }); } catch (e) {} return o; }\n"
                 "  renderVals() {\n    const o = this.state.open, toggle = {}, shut = {};\n"
                 "    Object.keys(o).forEach(k => { shut[k] = !o[k]; toggle[k] = () => this.setState({ open: Object.assign({}, o, { [k]: !o[k] }), draft: this.snap() }); });\n"
                 "    const a = this.state.ai, rv = Object.assign({}, __RDEF__, this.illoGet('illo-resume', null) || {}, this.state.draft || {});\n"
                 "    const pickPdf = (e) => { const f = e && e.target && e.target.files && e.target.files[0]; if (!f) return; if (f.name.toLowerCase().endsWith('.pdf')) this.setState({ ai: true, pdf: f.name, pdfErr: false, draft: this.snap() }); else this.setState({ pdfErr: true, draft: this.snap() }); };\n"
                 "    const save = () => { const v = this.snap(); this.state.saved = true; this.state.draft = v; this.illoSet('illo-resume', v); };\n"
                 "    return { open: o, shut, toggle, rv, aiDone: a, aiNot: !a, pdf: this.state.pdf, pdfErr: this.state.pdfErr, aiLabel: a ? '다시 올리기' : 'PDF 올리기', pickPdf, tryAi: () => this.setState({ ai: true, pdf: '김하늘_이력서.pdf (예시)', pdfErr: false, draft: this.snap() }), saved: this.state.saved, save };\n  }")


resume_body = f'''  <div style="padding: 24px 56px 0; display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 15px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아도 돼요</span><div style="margin-top: 12px;">{mytabs('resume')}</div></div>
  <div style="display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 24px; padding: 24px 56px 56px; align-items: start;">
{resume_nav()}    <div style="display: flex; flex-direction: column; gap: 14px; min-width: 0;">
{resume_note(False)}{resume_ai(False)}{resume_sections(False)}    </div>
  </div>
'''
boards['S5-resume.dc.html'] = ('S5b 마이페이지 · 이력서 등록', dpage('S5-resume.dc.html', '이력서 등록', 'my', resume_body, RESUME_SCRIPT.replace('__RDEF__', json.dumps(RDEF, ensure_ascii=False))))

m_jump = ''.join(f'<a href="#m-r-{k}" style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG if f else "#FFFFFF"}; color: {BLUE_D if f else SUB}; font-size: 13px; text-decoration: none;">{n}</a>' for k, n, f, _ in RSEC)
m_resume = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 13px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아요</span></div>
    {mytabs('resume', True)}
    <div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 18px; {CARD}"><span style="font-size: 15px; font-weight: 700;">{R_COUNT}</span><span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: {R_PCT}%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span>
      <nav aria-label="이력서 항목" class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -18px; padding: 2px 18px;">{m_jump}</nav></div>
{resume_note(True)}{resume_ai(True)}{resume_sections(True)}    <button type="button" onClick="@@save@@" style="height: 54px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; cursor: pointer;">이력서 저장</button>
    <sc-if value="@@saved@@" hint-placeholder-val="@@false@@"><span style="text-align: center; font-size: 12px; color: {BLUE_D};">저장했어요 · 이 기기 브라우저에만 저장돼요</span></sc-if>
'''
boards['m-S5-resume.dc.html'] = ('M5b 이력서 등록 (모바일)', mpage('m-S5-resume.dc.html', 'M5b 이력서 등록 (모바일)', topbar_logo(auth_mobile()), m_resume, 'my', RESUME_SCRIPT.replace('__RDEF__', json.dumps(RDEF, ensure_ascii=False))))

# --- 저장함 ---
SAVED_JS = '''  constructor(props) { super(props); this.state = { f: 'all' }; }
  pageVals() {
    const S = this.illoSaved(), f = this.state.f, pre = '__PRE__';
    const pill = (on) => on ? '__PON__' : '__POFF__';
    const KC = { '공고': ['#E8F3FF', '#1B64DA'], '교육': ['#FFF4E5', '#C26A00'], '정책': ['#E6F7F1', '#0E8A63'] };
    const F = ['all', '공고', '교육', '정책'].map((k) => ({ label: (k === 'all' ? '전체' : k) + ' ' + S.filter((x) => k === 'all' || x.kind === k).length, style: pill(f === k), go: () => this.setState({ f: k }) }));
    const L = S.filter((x) => f === 'all' || x.kind === f).map((x) => ({ kind: x.kind, t: x.t, s: x.s, kindStyle: 'padding: 3px 9px; border-radius: 6px; background: ' + KC[x.kind][0] + '; color: ' + KC[x.kind][1] + '; font-size: 12px; font-weight: 700;',
      internal: !!x.h, external: !x.h, href: x.h ? pre + x.h : x.u, isPost: x.kind === '공고' && !!x.h, inApp: x.kind !== '공고' && !!x.h, sv: this.sv(x) }));
    return { filters: F, items: L, none: L.length === 0, some: L.length > 0, total: S.length };
  }'''


def saved_page(mobile):
    pre = 'm-' if mobile else ''
    row = (f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 12px; padding: 18px 0; border-top: 1px solid {LINE};">'
           f'<div style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 6px;"><span style="align-self: flex-start; @@x.kindStyle@@">@@x.kind@@</span><span style="font-size: 16px; font-weight: 700; line-height: 1.4;">@@x.t@@</span><span style="font-size: 13px; color: {SUB};">@@x.s@@</span></div>'
           f'<div style="display: flex; gap: 8px; align-items: center;">'
           f'<sc-if value="@@x.isPost@@" hint-placeholder-val="@@false@@"><a href="@@x.href@@" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">내 경험과 비교</a></sc-if>'
           f'<sc-if value="@@x.inApp@@" hint-placeholder-val="@@false@@"><a href="@@x.href@@" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">자세히 보기</a></sc-if>'
           f'<sc-if value="@@x.external@@" hint-placeholder-val="@@true@@"><a href="@@x.href@@" {EXT} style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">열기 ↗</a></sc-if>'
           f'{save_btn("x.sv", 38)}</div></div>')
    chips = f'<sc-for list="@@filters@@" as="g" hint-placeholder-count="4"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.label@@</button></sc-for>'
    empty = (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 48px 0; border-top: 1px solid {LINE}; text-align: center;">'
             f'<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#D1D6DB" stroke-width="1.6" stroke-linejoin="round">{BOOK}</svg>'
             f'<span style="font-size: 16px; font-weight: 700;">아직 저장한 게 없어요</span><span style="font-size: 13px; color: {SUB};">공고, 교육과정, 정책 카드의 저장 버튼을 누르면 여기에 모여요</span>'
             f'<div style="display: flex; gap: 8px;"><a href="{pre}S1-list.dc.html" style="height: 40px; padding: 0 16px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;">공고 보기</a><a href="{pre}E1-edu.dc.html" style="height: 40px; padding: 0 16px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;">교육과정 보기</a></div></div>')
    sc = ' class="illo-scroll"' if mobile else ''
    card = (f'<section aria-labelledby="{pre}sv" style="display: flex; flex-direction: column; gap: 14px; padding: {"18px 18px 8px" if mobile else "26px 28px 12px"}; {CARD}">'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline;"><h2 id="{pre}sv" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">저장함</h2><span style="font-size: 13px; color: {MUTE};">이 기기에 저장돼요</span></div>'
            f'<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -18px; padding: 0 18px;" if mobile else ""}">{chips}</div>'
            f'<div><sc-if value="@@some@@" hint-placeholder-val="@@true@@"><sc-for list="@@items@@" as="x" hint-placeholder-count="3">{row}</sc-for></sc-if><sc-if value="@@none@@" hint-placeholder-val="@@false@@">{empty}</sc-if></div></section>')
    if mobile:
        return (f'    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 13px; color: {SUB};">저장한 공고, 교육과정, 정책을 한곳에서 봐요</span></div>\n'
                f'    {mytabs("saved", True)}\n    {card}\n')
    return (f'  <div style="padding: 24px 56px 0; display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 15px; color: {SUB};">저장한 공고, 교육과정, 정책을 한곳에서 봐요</span><div style="margin-top: 12px;">{mytabs("saved")}</div></div>\n'
            f'  <div style="padding: 24px 56px 56px;">{card}</div>\n')


def saved_js(mobile):
    return SAVED_JS.replace('__PRE__', 'm-' if mobile else '').replace('__PON__', PILL_ON).replace('__POFF__', PILL_OFF)


boards['S5-saved.dc.html'] = ('S5a 마이페이지 · 저장함', dpage('S5-saved.dc.html', '저장함', 'my', saved_page(False), saved_js(False)))
boards['m-S5-saved.dc.html'] = ('M5a 저장함 (모바일)', mpage('m-S5-saved.dc.html', 'M5a 저장함 (모바일)', topbar_logo(auth_mobile()), saved_page(True), 'my', saved_js(True)))

# --- S6 취업 수기 ---
LINKS = [('S2-input.dc.html', 'S3-compare.dc.html'), ('P1-trend.dc.html', 'S1-list.dc.html#trend'),
         ('내 경로에 저장', '마이페이지에 저장'), ('내 경로에 추가', '마이페이지에 추가'), ('경험 입력의 "링크" 칸', '마이페이지의 "포트폴리오 링크" 칸')]


def relink(s, mobile):
    for a, b in LINKS:
        if a.endswith('.html') and mobile:
            a, b = 'm-' + a, 'm-' + b
        s = s.replace(a, b)
    pre = 'm-' if mobile else ''
    s = s.replace(f'href="{pre}S3-compare.dc.html">‹ 비교 결과', f'href="{pre}S3-compare.dc.html#result">‹ 비교 결과')
    s = s.replace(f'href="{pre}S3-compare.dc.html" aria-label="뒤로"', f'href="{pre}S3-compare.dc.html#result" aria-label="뒤로"')
    return s


KEEP = {'S6-story.dc.html': 'my'}  # 원본 화면을 받아 메뉴, 링크, 로그인 값만 바꾼다
for name, active in KEEP.items():
    s = open(os.path.join(DATA, 'source', name), encoding='utf-8').read()  # 원본에서 매번 새로 만듦
    s = re.sub(r'  <header .*?</header>\n', lambda m: dheader(active), s, count=1, flags=re.S)
    s = relink(s, False).replace('‹ 내 경로', '‹ 마이페이지')
    s = re.sub(r'(class Component extends DCLogic \{\n)(.*?)(\n\}\n</script>)', lambda m: m.group(1) + inject(m.group(2)) + m.group(3), s, count=1, flags=re.S)
    s = holes(s)
    if name in HEIGHTS:
        s = re.sub(r'width: 1280px; height: \d+px', f'width: 1280px; height: {HEIGHTS[name]}px', s, count=1)
        s = re.sub(r'"height":\d+\}', f'"height":{HEIGHTS[name]}}}', s, count=1)
    boards[name] = (None, s)
    m = 'm-' + name
    s = open(os.path.join(DATA, 'source', m), encoding='utf-8').read()
    s = re.sub(r'  <nav aria-label="주요 메뉴" style="position: sticky; bottom: 0;.*?</nav>\n', lambda _: tabbar(active), s, count=1, flags=re.S)
    s = relink(s, True).replace('‹ 내 경로', '‹ 마이페이지')
    s = re.sub(r'(class Component extends DCLogic \{\n)(.*?)(\n\}\n</script>)', lambda m: m.group(1) + inject(m.group(2)) + m.group(3), s, count=1, flags=re.S)
    s = s.replace('<span style="text-align: center; font-size: 17px; font-weight: 700;">내 취업 경로</span>', '<span style="text-align: center; font-size: 17px; font-weight: 700;">마이페이지</span>')
    boards[m] = (None, s)
