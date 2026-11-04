"""P03 다음 행동 4가지: 교육 (관련 과정 목록, 강북5기 상세), 자격증과 어학, 대외활동, 지원 준비."""

# --- S3a~d 다음 행동: four sibling screens, rebuilt in the v4 style ---
NEXT_TABS = [('edu', '교육으로 배우기', 'S4-next.dc.html', 'edu'), ('cert', '자격증, 어학', 'S4-cert.dc.html', 'cert'),
             ('act', '대외활동, 프로젝트', 'S4-activity.dc.html', 'act'), ('apply', '지원 준비', 'S4-apply.dc.html', 'apply')]
GAPS = [('short', '숏폼 발행 경험'), ('tool', 'Premiere Pro, Photoshop으로 직접 구현'), ('trend', '최신 콘텐츠 트렌드와 밈에 관심'), ('work', '학회, 공모전, 인턴십 등 실무 경험')]
FILLS = {'edu': {'short', 'tool'}, 'cert': {'tool'}, 'act': {'short', 'work'}, 'apply': set()}
NEXT_SCRIPT = "  constructor(props) { super(props); this.state = { saved: false }; }\n  renderVals() { return { saved: this.state.saved, notSaved: !this.state.saved, save: () => this.setState({ saved: true }) }; }"
SRC_POST = f'출처: SNS 콘텐츠 마케팅 {SRC104}. 퍼센트는 해당 단어가 나온 공고 비율'


def next_tabs(active, mobile):
    pre = 'm-' if mobile else ''
    out = ''
    for k, label, href, ic in NEXT_TABS:
        on = k == active
        st = (f'background: {INK}; color: #FFFFFF; font-weight: 600;' if on else f'background: #FFFFFF; color: #4E5968;')
        icon = f'<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{CICON[ic]}</svg>'
        cur = ' aria-current="page"' if on else ''
        out += f'<a href="{pre}{href}"{cur} style="flex-shrink: 0; display: flex; align-items: center; gap: 6px; height: 40px; padding: 0 16px; border-radius: 999px; {st} font-size: 14px; text-decoration: none; white-space: nowrap;">{icon}{label}</a>'
    cls = ' class="illo-scroll"' if mobile else ''
    sp = 'overflow-x: auto; margin: 0 -16px; padding: 0 16px;' if mobile else ''
    return f'<nav aria-label="다음 행동 4가지"{cls} style="display: flex; gap: 8px; {sp}">{out}</nav>'


def gap_card(active, mobile):
    rows = ''
    for g, label in GAPS:
        on = g in FILLS[active]
        mark_ = (f'<span style="flex-shrink: 0; padding: 2px 8px; border-radius: 6px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 11px; font-weight: 700;">여기서 채움</span>' if on else '')
        rows += f'<div style="display: flex; align-items: center; gap: 10px; padding: 11px 0; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.45; color: {INK if on else MUTE};"><span style="flex: 1 1 0;">{label}</span>{mark_}</div>'
    save = (f'<sc-if value="@@notSaved@@" hint-placeholder-val="@@true@@"><button type="button" onClick="@@save@@" style="height: 48px; border: none; border-radius: 12px; background: {FILL}; color: {INK}; font-size: 15px; font-weight: 600; cursor: pointer;">내 경로에 저장</button></sc-if>'
            f'<sc-if value="@@saved@@" hint-placeholder-val="@@false@@"><a href="{"m-" if mobile else ""}S5-path.dc.html" style="height: 48px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 15px; font-weight: 600; text-decoration: none;">저장했어요 · 마이페이지에서 보기 ›</a></sc-if>')
    sticky = '' if mobile else 'position: sticky; top: 24px;'
    return (f'<aside style="{sticky} display: flex; flex-direction: column; gap: 12px; padding: {"18px" if mobile else "22px"}; {CARD}">'
            f'<div style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 12px; color: {MUTE};">올리브인터내셔널 · 성분에디터 콘텐츠 마케팅 인턴</span><span style="font-size: 16px; font-weight: 700;">아직 비어 있는 것 4</span></div>'
            f'<div>{rows}</div>{save}</aside>')


def next_page(active, title, lead, content, mobile):
    pre = 'm-' if mobile else ''
    head = (f'<div style="display: flex; flex-direction: column; gap: {12 if mobile else 16}px; {"padding: 4px 0 0;" if mobile else "padding: 20px 56px 0;"}">'
            + ('' if mobile else f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 16px;"><a href="S3-compare.dc.html#result" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 비교 결과</a>{flow_steps(3)}</div>')
            + f'{next_tabs(active, mobile)}<div style="display: flex; flex-direction: column; gap: 6px; {"padding: 4px 4px 0;" if mobile else ""}"><h1 style="margin: 0; font-size: {22 if mobile else 30}px; font-weight: 700; line-height: 1.35; letter-spacing: -0.02em;">{title}</h1>'
            f'<span style="font-size: {14 if mobile else 15}px; line-height: 1.55; color: {SUB};">{lead}</span></div></div>')
    if mobile:
        return f'    {head}\n{content}    {gap_card(active, True)}\n'
    return (f'  {head}\n  <div style="display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 24px; padding: 24px 56px 56px; align-items: start;">\n'
            f'    <div style="display: flex; flex-direction: column; gap: 16px; min-width: 0;">\n{content}    </div>\n    {gap_card(active, False)}\n  </div>\n')


def sec(title, body, sub='', mobile=False):
    return (f'    <section style="display: flex; flex-direction: column; gap: 14px; padding: {"18px" if mobile else "26px 28px"}; {CARD}">'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px;"><h2 style="margin: 0; font-size: {17 if mobile else 19}px; font-weight: 700;">{title}</h2><span style="font-size: 12px; color: {MUTE}; text-align: right;">{sub}</span></div>{body}</section>\n')


def bars(items, total=104, mobile=False):
    mx = max(n for _, n, _ in items) or 1
    out = ''
    for label, n, note in items:
        w = max(2, round(n / mx * 100)) if n else 0
        nt = f'<span style="padding: 2px 7px; border-radius: 6px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 11px; font-weight: 600;">{note}</span>' if note else ''
        out += (f'<div style="display: grid; grid-template-columns: {"110px" if mobile else "200px"} minmax(0, 1fr) 52px; gap: 12px; align-items: center; font-size: 14px;"><span style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">{label}{nt}</span>'
                f'<span style="height: 8px; border-radius: 999px; background: {FILL};"><span style="display: block; width: {w}%; height: 8px; border-radius: 999px; background: {BLUE if n else FILL};"></span></span><span style="text-align: right; font-weight: 600;">{n}건</span></div>')
    return f'<div style="display: flex; flex-direction: column; gap: 12px;">{out}</div>'


def quote(t):
    return f'<p style="margin: 0; padding: 12px 14px; border-left: 3px solid #D1D6DB; background: #F9FAFB; border-radius: 0 10px 10px 0; font-size: 14px; line-height: 1.55; color: #333D4B;">"{t}"</p>'


def stat_tiles(items, mobile):
    t = ''.join(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 16px; border-radius: 14px; background: #F9FAFB;"><span style="font-size: 12px; color: {SUB};">{k}</span><span style="font-size: {22 if mobile else 26}px; font-weight: 700; letter-spacing: -0.02em;">{v}</span><span style="font-size: 12px; color: {MUTE};">{n}</span></div>' for k, v, n in items)
    return f'<div style="display: grid; grid-template-columns: repeat({1 if mobile else len(items)}, minmax(0, 1fr)); gap: 10px;">{t}</div>'


def btnrow(*b):
    return f'<div style="display: flex; gap: 8px; flex-wrap: wrap;">{"".join(b)}</div>'


def pbtn(href, label, primary=True, ext=False):
    st = f'background: {BLUE}; color: #FFFFFF;' if primary else f'background: {FILL}; color: {INK};'
    return f'<a href="{href}"{" " + EXT if ext else ""} style="height: 46px; padding: 0 18px; display: inline-flex; align-items: center; border-radius: 12px; {st} font-size: 15px; font-weight: 600; text-decoration: none;">{label}</a>'




def next_cert(mobile):
    certs = bars([('컴퓨터활용능력', 0, '내 자격증'), ('GTQ', 0, ''), ('GAIQ', 0, ''), ('검색광고마케터', 0, '')], mobile=mobile)
    tools = bars([('프리미어', 30, ''), ('포토샵', 28, ''), ('피그마', 19, ''), ('캡컷', 10, '')], mobile=mobile)
    a = (stat_tiles([('자격증을 적은 공고', '3%', '104건 중 3건'), ('아래 4개 자격증', '0건', '어느 공고에도 없음')], mobile) + certs)
    b = (f'<span style="font-size: 14px; line-height: 1.55; color: #333D4B;">공고는 자격증 대신 툴 이름을 직접 적어요. 이 툴로 만든 결과물을 보여주는 쪽이 공고 문장과 이어져요</span>' + tools
         + btnrow(pbtn(('m-' if mobile else '') + 'S4-next.dc.html', '툴 실습 과정 보기')))
    c = (stat_tiles([('외국어를 적은 공고', '14%', '104건 중 15건'), ('내 어학', 'OPIc IM2', '이력서에 저장됨')], mobile)
         + quote('영어로 커뮤니케이션이 원활한 분') + quote('중급 이상의 일본어 활용 능력 (SNS, 밈, 트렌드를 이해할 수 있는 수준)')
         + f'<span style="font-size: 13px; color: {SUB};">필요한 공고는 언어와 수준을 직접 적어요. 지원할 공고 원문에 어학 문장이 있는지만 확인하면 돼요</span>')
    return (sec('자격증은 거의 보지 않아요', a, '', mobile) + sec('대신 공고가 적은 툴', b, '104건 중 언급 건수', mobile) + sec('어학', c, '', mobile)
            + f'    <span style="font-size: 12px; color: {MUTE};">{SRC_POST}</span>\n')


def next_act(mobile):
    a = stat_tiles([('개인 SNS, 채널 운영', '15%', '16건'), ('공모전, 수상', '9%', '9건'), ('서포터즈, 기자단', '2%', '2건')], mobile)
    a += f'<span style="font-size: 14px; color: #333D4B;">대외활동 이름보다 직접 채널을 운영해 본 경험을 더 많이 적어요</span>'
    steps = [('1주차', '레퍼런스 10개 모으기', '지원할 브랜드 계정의 릴스, 쇼츠에서 훅과 길이 기록'), ('2주차', '숏폼 3개 발행', '캡컷이나 프리미어로 편집해 학생회 계정이나 개인 계정에'),
             ('3주차', '훅 바꿔서 3개 더', '조회수가 낮았던 영상의 첫 3초만 바꿔 다시 올리기'), ('4주차', '결과 한 장으로', '조회수, 저장 수 비교와 다음에 바꿀 점을 링크로 정리')]
    tl = ''.join(f'<li style="display: flex; gap: 14px;"><span style="width: 30px; height: 30px; flex-shrink: 0; border-radius: 50%; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span>'
                 f'<span style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 12px; color: {MUTE};">{w}</span><span style="font-size: 15px; font-weight: 700;">{t}</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">{d}</span></span></li>' for i, (w, t, d) in enumerate(steps, 1))
    b = (f'<span style="font-size: 14px; color: #333D4B;">비어 있는 "숏폼 발행 경험"을 4주 안에 채워요</span><ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 16px;">{tl}</ol>'
         f'<span style="font-size: 13px; color: {SUB};">결과 링크를 이력서 포트폴리오 칸에 넣으면 다음 비교에 반영돼요</span>')
    c = quote('콘텐츠 기획 및 제작 경험을 보유하신 분 (개인 SNS 채널도 무관)') + quote('팀 프로젝트, 공모전, SNS 개인 콘텐츠 등 어떤 형태든 상관없어요') + quote('SNS 운영 경험이 있는 경우 URL 기재')
    c += btnrow(pbtn('https://linkareer.com/list/contest', '링커리어에서 공모전 찾기 ↗', False, True))
    return (sec('공고가 적은 경험', a, '104건 기준', mobile) + sec('일로 제안 · 4주 숏폼 프로젝트', b, '', mobile) + sec('공고가 실제로 적은 문장', c, '', mobile)
            + f'    <span style="font-size: 12px; color: {MUTE};">{SRC_POST}</span>\n')


def next_apply(mobile):
    m1 = d_match('맞음', BLUE_D, BLUE_BG, '채널을 직접 운영하며 고객 반응을 이끌어낸', '우대 · SNS 채널 운영', '학생회 홍보부 인스타그램 운영 1년, 팔로워 300명에서 1,200명')
    m2 = d_match('일부', OR, OR_BG, '콘텐츠 성과를 수치로 분석하고 다음 액션 제안', '자격요건 · 성과 분석', '팔로워 300명에서 1,200명', '무엇을 보고 무엇을 바꿨는지 한 문장 더하기')
    a = f'<span style="font-size: 14px; color: #333D4B;">이어지는 2개를 지원서 앞에 두세요</span><div>{m1}{m2}</div>'
    b = (f'<div style="display: grid; grid-template-columns: {"1fr" if mobile else "1fr 1fr"}; gap: 12px;">'
         f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 14px; border-radius: 12px; background: #F9FAFB;"><span style="font-size: 12px; color: {MUTE};">지금 이력서</span><span style="font-size: 14px; line-height: 1.6;">학생회 홍보부 인스타그램 운영 1년. 카드뉴스 주 1회 제작 (캔바). 팔로워 300명에서 1,200명</span></div>'
         f'<div style="display: flex; flex-direction: column; gap: 6px; padding: 14px; border-radius: 12px; background: #F4F9FF;"><span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: {BLUE_D};">{AI}공고 문장에 맞춰서</span><span style="font-size: 14px; line-height: 1.6;">학생회 인스타그램을 1년간 직접 운영하며 카드뉴스를 매주 발행해 팔로워를 300명에서 1,200명으로 늘렸습니다</span></div></div>'
         f'<span style="font-size: 12px; color: {MUTE};">입력한 사실만 순서를 바꿨어요. 없는 숫자나 경험은 넣지 않아요</span>')
    chk = [('인스타그램 계정 링크 첨부', '"SNS 운영 경험이 있는 경우 URL 기재" 같은 문장이 많아요'), ('없는 숏폼, 툴 경험은 쓰지 않기', '없는 경험은 면접에서 드러나요'), ('원문 공고에서 마감일 확인', '수집 데이터에는 마감일이 없을 수 있어요')]
    c = ''.join(f'<label style="display: flex; gap: 12px; padding: 12px 0; border-top: 1px solid {LINE}; cursor: pointer;"><input type="checkbox" style="width: 18px; height: 18px; margin-top: 2px; accent-color: {BLUE};"><span style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 15px; font-weight: 600;">{t}</span><span style="font-size: 13px; color: {SUB};">{d}</span></span></label>' for t, d in chk)
    c = f'<div>{c}</div>' + btnrow(pbtn(POSTING, '원문 공고에서 지원하기 ↗', True, True))
    return sec('앞에 둘 경험', a, '', mobile) + sec('문장 다듬기', b, '', mobile) + sec('지원 전에 확인', c, '', mobile)

NEXT_PAGES = [('S4-cert.dc.html', 'cert', 'S3b 자격증, 어학', '자격증보다 툴로 만든 결과물을 봐요', '이 직무 공고 104건에서 자격증, 툴, 어학을 얼마나 적었는지 세어 봤어요', next_cert),
              ('S4-activity.dc.html', 'act', 'S3c 대외활동, 프로젝트', '숏폼을 직접 발행해 본 경험을 만들어요', '비어 있는 "숏폼 발행"과 "실무 경험"을 프로젝트로 채워요', next_act),
              ('S4-apply.dc.html', 'apply', 'S3d 지원 준비', '지금 경험으로 지원해 볼 수 있어요', '맞는 경험을 앞에 두고, 빈 것은 솔직하게 두고 가요', next_apply)]
for fname, key, btitle, title, lead, fn in NEXT_PAGES:
    boards[fname] = (btitle, dpage(fname, title, 'find', next_page(key, title, lead, fn(False), False), NEXT_SCRIPT))
    mname = 'm-' + fname
    body = next_page(key, title, lead, fn(True).replace('href="S4-', 'href="m-S4-'), True)
    boards[mname] = ('M' + btitle[1:] + ' (모바일)', mpage(mname, btitle + ' (모바일)', topbar_back('m-S3-compare.dc.html#result', '다음 행동'), body, 'find', NEXT_SCRIPT))

# ===== v8: 교육으로 배우기 = matched SeSAC course grid; 강북5기 gets its own detail page =====
import re as _re8
MATCH = r'숏폼|영상|콘텐츠|SNS|마케팅|마케터|프리미어|편집'
SHORT = r'숏폼|릴스|쇼츠|영상'
TOOL = r'영상 ?편집|영상제작|프리미어|포토샵|디자인'
CD_ID = 'edu-1421'
MC = []
for c in COURSES_ALL:
    blob = c['n'] + ' ' + c['f'] + ' ' + ' '.join(c['tags'])
    if not _re8.search(MATCH, blob):
        continue
    fills = []
    if _re8.search(SHORT, blob): fills.append('숏폼 발행')
    if _re8.search(TOOL, blob): fills.append('디자인, 영상 툴')
    MC.append(dict(c, fills=fills))
MC_LIVE = sum(1 for c in MC if c['st'] in ('모집 중', '모집 예정', '상시'))
MC_JSON = json.dumps(MC, ensure_ascii=False)

EDU_GRID_JS = '''  constructor(props) { super(props); this.state = { all: false, page: 1, saved: false }; }
  pageVals() {
    const C = __MC__, TH = __TH__, GC = __GC__, SC = __SC__, s = this.state, set = (o) => this.setState(o);
    const live = (c) => c.st === '모집 중' || c.st === '모집 예정' || c.st === '상시';
    const rank = (c) => ({ '모집 중': 0, '모집 예정': 1, '상시': 2, '진행 중': 3, '종료': 4 })[c.st];
    const L = C.filter((c) => s.all || live(c)).slice().sort((a, b) => (b.fills.length - a.fills.length) || (rank(a) - rank(b)) || ((b.id === '__CD__') - (a.id === '__CD__')) || (b.rv - a.rv));
    const per = 6, pages = Math.max(1, Math.ceil(L.length / per)), page = Math.min(s.page, pages);
    const pg = (on) => on ? '__GON__' : '__GOFF__';
    const nums = []; for (let i = 1; i <= pages; i++) nums.push({ n: i, style: pg(i === page), cur: i === page ? 'page' : 'false', go: () => set({ page: i }) });
    const badge = (st) => 'padding: 3px 9px; border-radius: 999px; background: ' + (SC[st] || SC['종료'])[0] + '; color: ' + (SC[st] || SC['종료'])[1] + '; font-size: 12px; font-weight: 600;';
    const cards = L.slice((page - 1) * per, page * per).map((c) => {
      const col = GC[c.g] || GC['기타'];
      return { n: c.n, cp: c.cp, f: c.f, st: c.st, stStyle: badge(c.st), edu: c.edu, h: c.h, tags: c.tags.map((t) => '#' + t.replace(/^#/, '')), u: c.u,
        due: c.st === '모집 중' && c.recEnd ? c.recEnd.slice(5) + ' 마감' : '', hasDue: c.st === '모집 중' && !!c.recEnd,
        thumb: TH[c.id] || '', hasThumb: !!TH[c.id], noThumb: !TH[c.id], band: 'background: ' + col[0] + '; color: ' + col[1] + ';', g: c.g,
        fills: c.fills.map((x) => x + ' 채움'), direct: c.fills.length > 0, related: c.fills.length === 0,
        detail: c.id === '__CD__', noDetail: c.id !== '__CD__', dhref: '__PRE__C2-course.dc.html',
        sv: this.sv({ id: c.id, kind: '교육', t: c.n, s: 'SeSAC ' + c.cp + ' · ' + c.st, u: c.u, h: c.id === '__CD__' ? 'C2-course.dc.html' : '' }) };
    });
    const tog = (on) => on ? '__PON__' : '__POFF__';
    return { cards, total: L.length, nums, hasPages: pages > 1, liveTab: { style: tog(!s.all), go: () => set({ all: false, page: 1 }) }, allTab: { style: tog(s.all), go: () => set({ all: true, page: 1 }) },
      saved: s.saved, notSaved: !s.saved, save: () => set({ saved: true }) };
  }'''


def edu_grid_js(mobile):
    return (EDU_GRID_JS.replace('__MC__', MC_JSON).replace('__TH__', json.dumps(THUMBS)).replace('__GC__', json.dumps(GCOL, ensure_ascii=False)).replace('__SC__', json.dumps(STC, ensure_ascii=False))
            .replace('__CD__', CD_ID).replace('__PRE__', 'm-' if mobile else '').replace('__GON__', PG_ON).replace('__GOFF__', PG_OFF).replace('__PON__', PILL_ON).replace('__POFF__', PILL_OFF))


def edu_grid(mobile):
    card = (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 14px; {CARD} min-width: 0;">'
            f'<sc-if value="@@c.hasThumb@@" hint-placeholder-val="@@false@@"><img src="@@c.thumb@@" alt="" style="width: 100%; height: 150px; object-fit: cover; border-radius: 12px; display: block;"></sc-if>'
            f'<sc-if value="@@c.noThumb@@" hint-placeholder-val="@@true@@"><div style="@@c.band@@ height: 150px; border-radius: 12px; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;"><span style="font-size: 13px; font-weight: 700;">@@c.g@@</span><span style="font-size: 22px; font-weight: 800; letter-spacing: -0.02em; opacity: 0.85;">SeSAC @@c.cp@@</span></div></sc-if>'
            f'<div style="display: flex; align-items: center; gap: 6px;"><span style="@@c.stStyle@@">@@c.st@@</span><sc-if value="@@c.hasDue@@" hint-placeholder-val="@@false@@"><span style="font-size: 12px; font-weight: 700; color: {RED};">@@c.due@@</span></sc-if><span style="margin-left: auto;">{save_btn("c.sv", 32)}</span></div>'
            f'<span style="font-size: 16px; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 45px;">@@c.n@@</span>'
            f'<div style="display: flex; gap: 4px; flex-wrap: wrap;"><sc-if value="@@c.direct@@" hint-placeholder-val="@@false@@"><sc-for list="@@c.fills@@" as="x" hint-placeholder-count="1"><span style="padding: 3px 8px; border-radius: 6px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px; font-weight: 600;">@@x@@</span></sc-for></sc-if>'
            f'<sc-if value="@@c.related@@" hint-placeholder-val="@@true@@"><span style="padding: 3px 8px; border-radius: 6px; background: {FILL}; color: {SUB}; font-size: 12px;">관련 분야 · 커리큘럼 확인 필요</span></sc-if></div>'
            f'<span style="font-size: 12px; line-height: 1.5; color: {SUB};">@@c.cp@@ · @@c.f@@ · @@c.h@@ · @@c.edu@@</span>'
            f'<div style="margin-top: auto; padding-top: 10px; border-top: 1px solid {LINE}; display: flex; justify-content: flex-end;">'
            f'<sc-if value="@@c.detail@@" hint-placeholder-val="@@false@@"><a href="@@c.dhref@@" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none;">자세히 보기</a></sc-if>'
            f'<sc-if value="@@c.noDetail@@" hint-placeholder-val="@@true@@"><a href="@@c.u@@" {EXT} style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none;">SeSAC에서 보기 ↗</a></sc-if></div></div>')
    tabs = (f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;"><div style="display: flex; gap: 6px;">'
            f'<button type="button" onClick="@@liveTab.go@@" style="@@liveTab.style@@">모집 중, 예정 {MC_LIVE}</button><button type="button" onClick="@@allTab.go@@" style="@@allTab.style@@">지난 과정 포함 {len(MC)}</button></div>'
            f'<span style="font-size: 13px; color: {SUB};">빈 칸을 직접 채우는 과정 먼저</span></div>')
    pager = (f'<sc-if value="@@hasPages@@" hint-placeholder-val="@@false@@"><nav aria-label="페이지" style="display: flex; justify-content: center; gap: 4px;"><sc-for list="@@nums@@" as="x" hint-placeholder-count="3"><button type="button" onClick="@@x.go@@" aria-current="@@x.cur@@" style="@@x.style@@">@@x.n@@</button></sc-for></nav></sc-if>')
    grid = f'<div style="display: grid; grid-template-columns: repeat({1 if mobile else 2}, minmax(0, 1fr)); gap: 12px;"><sc-for list="@@cards@@" as="c" hint-placeholder-count="6">{card}</sc-for></div>'
    src = f'<span style="font-size: 12px; color: {MUTE};">출처: SeSAC 과정 정보 (팀 수집 210개, 2026.10.27 기준). "채움"은 과정명, 분야, 해시태그에 숏폼, 영상, 편집, 디자인 단어가 있는지로 표시해요</span>'
    return f'    {tabs}\n    {grid}\n    {pager}\n    {src}\n'


EDU_T, EDU_L = '숏폼, 영상 툴을 배울 수 있는 SeSAC 과정', f'관련 과정 {len(MC)}개 중 지금 신청할 수 있는 {MC_LIVE}개예요. 비교해 보고 직접 골라요'
boards['S4-next.dc.html'] = ('S3 다음 행동 · 교육 (관련 과정 목록)', dpage('S4-next.dc.html', EDU_T, 'find', next_page('edu', EDU_T, EDU_L, edu_grid(False), False), edu_grid_js(False)))
boards['m-S4-next.dc.html'] = ('M3 다음 행동 · 교육 (모바일)', mpage('m-S4-next.dc.html', EDU_T + ' (모바일)', topbar_back('m-S3-compare.dc.html#result', '다음 행동'), next_page('edu', EDU_T, EDU_L, edu_grid(True), True), 'find', edu_grid_js(True)))

# --- 강북5기 detail ---
CD_JS = ("  pageVals() {\n    const end = new Date('2026-11-08T23:59:59+09:00').getTime(), n = Math.ceil((end - Date.now()) / 86400000);\n"
         "    return { dday: n >= 0 ? 'D-' + n : '마감', open: n >= 0 };\n  }")


def cd_page(mobile):
    pre = 'm-' if mobile else ''
    badge = lambda t, bg, fg: f'<span style="padding: 4px 10px; border-radius: 999px; background: {bg}; color: {fg}; font-size: 13px; font-weight: 600;">{t}</span>'
    fact = lambda k, v, sub='': (f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 14px 16px; border-radius: 14px; background: #F9FAFB;"><span style="font-size: 12px; color: {MUTE};">{k}</span><span style="font-size: 15px; font-weight: 700; line-height: 1.35;">{v}</span>'
                                 + (f'<span style="font-size: 12px; color: {SUB};">{sub}</span>' if sub else '') + '</div>')
    facts = (f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">' + fact('모집 기간', '10.12 ~ 11.08', '@@dday@@')
             + fact('교육 기간', '2026.11.25 ~ 2027.03.17') + fact('교육 시간', '420시간', '59차시 · 오프라인') + fact('비용', '무료', '합격 후 예치금, 수료 시 반환') + '</div>')
    info = (f'<div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 14px; min-width: 0;"><div style="display: flex; gap: 6px; flex-wrap: wrap;">{badge("모집 중", BLUE_BG, BLUE_D)}{badge("강북 캠퍼스 · 디지털마케팅", FILL, SUB)}</div>'
            f'<div style="display: flex; align-items: flex-start; gap: 12px;"><h1 style="flex: 1 1 0; margin: 0; font-size: {23 if mobile else 30}px; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em;">(강북5기) AI 활용 SNS 마케터 양성 과정</h1>{save_btn("sv.e1421", 44)}</div>'
            f'<div style="display: flex; gap: 8px; flex-wrap: wrap; font-size: 13px; color: {SUB};">' + ''.join(f'<span>#{t}</span>' for t in ['AI', 'SNS마케팅', '콘텐츠마케팅', '퍼포먼스마케팅', '마케팅자동화']) + f'</div>{facts}</div>')
    img = f'<img src="{THUMB1}" alt="강북5기 AI 활용 SNS 마케터 양성 과정 안내 이미지" style="width: {"100%" if mobile else "340px"}; height: {"200px" if mobile else "300px"}; flex-shrink: 0; object-fit: cover; border-radius: 16px; display: block;">'
    hero = f'<section style="display: flex; {"flex-direction: column;" if mobile else ""} gap: 28px; padding: {"20px" if mobile else "28px"}; {CARD}">{img}{info}</section>'
    sec = lambda t, body, sub='': (f'<section style="display: flex; flex-direction: column; gap: 14px; padding: {"20px" if mobile else "28px 32px"}; {CARD}"><div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px;"><h2 style="margin: 0; font-size: {17 if mobile else 19}px; font-weight: 700;">{t}</h2><span style="font-size: 12px; color: {MUTE};">{sub}</span></div>{body}</section>')
    gaprow = lambda k, label, note, extra='': (f'<div style="display: flex; align-items: flex-start; gap: 12px; padding: 13px 0; border-top: 1px solid {LINE};">{mk_badge(k)}<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 15px; font-weight: 600;">{label}</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">{note}</span></span>{extra}</div>')
    link = lambda href, t: f'<a href="{href}" style="flex-shrink: 0; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">{t} ›</a>'
    fit = (gaprow('ok', '콘텐츠 기획, 채널 운영', '#SNS마케팅 #콘텐츠마케팅 키워드와 이어져요')
           + gaprow('ok', '성과 분석', '#퍼포먼스마케팅 키워드와 이어져요. 비교 결과 "일부"를 채우는 데 도움이 돼요')
           + gaprow('no', '숏폼 발행 경험', '과정 키워드에 숏폼이 없어요. 커리큘럼에 영상 실습이 있는지 확인해 보세요', link(pre + 'S4-activity.dc.html', '4주 프로젝트'))
           + gaprow('no', 'Premiere Pro, Photoshop', '과정 키워드에 영상 툴이 없어요', link(pre + 'S4-next.dc.html', '다른 과정')))
    steps = arrow = f'<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#B0B8C1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{"M12 5v14M6 13l6 6 6-6" if mobile else "M5 12h14M13 6l6 6-6 6"}"/></svg>'
    flow = arrow.join(f'<div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 4px; padding: 14px; border-radius: 12px; background: #F9FAFB;"><span style="font-size: 12px; color: {BLUE}; font-weight: 700;">{i}</span><span style="font-size: 14px; font-weight: 700;">{t}</span></div>' for i, t in [(1, '자기소개서'), (2, '레벨테스트'), (3, '면접'), (4, '선발 결과')])
    flow = f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 6px;">{flow}</div>'
    rule = lambda k, v: f'<div style="display: grid; grid-template-columns: {"96px" if mobile else "140px"} 1fr; gap: 12px; padding: 12px 0; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.5;"><span style="color: {MUTE};">{k}</span><span>{v}</span></div>'
    rules = (rule('지원 자격', '서울 거주 청년 구직자, 만 15세 이상, 수료 후 취업이나 창업이 목표') + rule('서울 외 거주', '정원의 10% 이내 (서울 소재 대학 재학, 3년 내 졸업 등)')
             + rule('내일배움카드', '필요 없어요') + rule('국민취업지원제도', '함께 참여할 수 있어요') + rule('중복 신청', '여러 과정에 신청 가능, 합격 후 1개만 선택'))
    dep = (rule('수료 기준', '출석률 80% 이상') + rule('예치금 반환', '80% 출석으로 수료, 진도 30% 뒤 조기 취업, 입과 전이나 5% 이내 포기, 중간평가 탈락'))
    rv = [('강사', 33), ('취업', 19), ('실무', 17), ('포트폴리오', 16), ('비전공', 14), ('프로젝트', 14)]
    rvb = ''.join(f'<div style="display: grid; grid-template-columns: 90px 1fr 40px; gap: 10px; align-items: center; font-size: 14px;"><span>{k}</span><span style="height: 8px; border-radius: 999px; background: {FILL};"><span style="display: block; width: {round(n / 33 * 100)}%; height: 8px; border-radius: 999px; background: {BLUE};"></span></span><span style="text-align: right; font-weight: 600;">{n}건</span></div>' for k, n in rv)
    reviews = (f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">' + fact('비슷한 마케팅 과정 후기', '72건') + fact('평균 별점', '4.99 / 5') + '</div>'
               f'<span style="font-size: 13px; color: {SUB};">후기에서 자주 나온 말 (72건 중 언급 건수)</span><div style="display: flex; flex-direction: column; gap: 10px;">{rvb}</div>'
               f'<span style="font-size: 12px; color: {MUTE};">이 과정은 새 기수라 후기가 아직 없어요. SeSAC 마케팅, 콘텐츠 과정 수강후기 기준 (팀 수집, 작성자 정보 제외)</span>')
    main = (sec('내 빈 칸과 맞춰 보면', f'<div>{fit}</div>', '과정 키워드 기준')
            + sec('지원 자격과 선발', flow + f'<div>{rules}</div>')
            + sec('수료와 예치금', f'<div>{dep}</div>')
            + sec('수료생 후기', reviews))
    me = [('서울 성북구', '서울 거주'), ('취업 준비생', '구직 중'), ('만 24세', '만 15세 이상')]
    me_rows = ''.join(f'<div style="display: flex; align-items: center; gap: 10px; font-size: 14px;"><span style="width: 20px; height: 20px; flex-shrink: 0; border-radius: 50%; background: {BLUE}; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><span><b style="font-weight: 600;">{a}</b> <span style="color: {SUB};">· {b}</span></span></div>' for a, b in me)
    side = (f'<aside style="{"" if mobile else "position: sticky; top: 24px;"} display: flex; flex-direction: column; gap: 14px; padding: {"20px" if mobile else "24px"}; {CARD}">'
            f'<div style="display: flex; align-items: baseline; justify-content: space-between;"><span style="font-size: 13px; color: {SUB};">모집 마감까지</span><span style="font-size: 26px; font-weight: 800; color: {BLUE}; letter-spacing: -0.02em;">@@dday@@</span></div>'
            f'<a href="{SESAC}1421" {EXT} style="height: 54px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; text-decoration: none;">SeSAC에서 지원하기 ↗</a>'
            f'<div style="height: 1px; background: {LINE};"></div><div style="display: flex; align-items: center; gap: 6px;">{AI}<span style="font-size: 15px; font-weight: 700;">내 이력서로 보면</span></div>{me_rows}'
            f'<span style="padding: 12px 14px; border-radius: 12px; background: #F4F9FF; font-size: 13px; line-height: 1.55; color: #333D4B;">비어 있는 4개 중 <b style="color: {BLUE_D};">성과 분석</b>은 이 과정으로 보완할 수 있어요. 숏폼, 영상 툴은 다른 길과 함께 보세요</span>'
            f'<span style="font-size: 11px; line-height: 1.5; color: {MUTE};">지원 자격만 맞춰 봐요. 선발 여부는 예측하지 않아요</span></aside>')
    others = [c for c in MC if c['st'] in ('모집 중', '모집 예정') and c['id'] != CD_ID][:3]
    rel = ''.join(f'<a href="{c["u"]}" {EXT} style="display: flex; flex-direction: column; gap: 6px; padding: 18px; {CARD} color: {INK}; text-decoration: none;"><span style="align-self: flex-start; padding: 2px 8px; border-radius: 999px; background: {BLUE_BG if c["st"] == "모집 중" else OR_BG}; color: {BLUE_D if c["st"] == "모집 중" else OR}; font-size: 12px; font-weight: 600;">{c["st"]}</span><span style="font-size: 15px; font-weight: 700; line-height: 1.4;">{c["n"]}</span><span style="font-size: 12px; color: {SUB};">SeSAC {c["cp"]} · {c["h"]}</span></a>' for c in others)
    related = (f'<section style="display: flex; flex-direction: column; gap: 12px;"><div style="display: flex; justify-content: space-between; align-items: baseline;"><h2 style="margin: 0; font-size: 19px; font-weight: 700;">함께 비교해 볼 과정</h2><a href="{pre}S4-next.dc.html" style="font-size: 13px; font-weight: 600; text-decoration: none;">전체 보기 ›</a></div>'
               f'<div style="display: grid; grid-template-columns: repeat({1 if mobile else 3}, minmax(0, 1fr)); gap: 12px;">{rel}</div>'
               f'<span style="font-size: 12px; color: {MUTE};">출처: SeSAC 과정 정보, 지원 규정 FAQ, 수강후기 (팀 수집, 2026.10.27 기준)</span></section>')
    if mobile:
        return f'    {hero}\n    {side}\n    {main}\n    {related}\n'
    return (f'  <div style="padding: 16px 56px 0;"><a href="S4-next.dc.html" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 교육으로 배우기</a></div>\n'
            f'  <div style="display: flex; flex-direction: column; gap: 24px; padding: 16px 56px 56px;">{hero}'
            f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 24px; align-items: start;"><div style="display: flex; flex-direction: column; gap: 16px; min-width: 0;">{main}</div>{side}</div>{related}</div>\n')


boards['C2-course.dc.html'] = ('C2 SeSAC 과정 상세 (강북5기)', dpage('C2-course.dc.html', '(강북5기) AI 활용 SNS 마케터 양성 과정', 'find', cd_page(False), CD_JS, saves=('e1421',)))
boards['m-C2-course.dc.html'] = ('MC2 SeSAC 과정 상세 (모바일)', mpage('m-C2-course.dc.html', '강북5기 과정 상세 (모바일)', topbar_back('m-S4-next.dc.html', '과정 상세'), cd_page(True), 'find', CD_JS, saves=('e1421',)))
