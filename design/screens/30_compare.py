"""P03 공고 비교: 공고 원문에 AI 비교 결과 표시, 오른쪽 결과 패널."""

# ===== v6 compare: the posting as written, AI results marked on its own sentences, one side panel =====

COMPARE_COLORS = {
    'ok': ('#166534', '#E8F5EC'),
    'part': (OR, OR_BG),
    'no': ('#B42318', '#FDECEC'),
}
MK = {'ok': ('맞음', BLUE_D, BLUE_BG), 'part': ('일부', OR, OR_BG), 'no': ('없음', SUB, '#EEF0F3')}
# Each posting line: text pieces (piece, mark-or-None) and what the comparison found for it.
POST_REQ = [
    ('자격요건', [('평소 릴스, 숏츠, 틱톡 등 숏폼 콘텐츠를 즐겨보며, ', None), ('최신 콘텐츠 트렌드와 밈(Meme)에 관심', 'no'), ('이 많으신 분', None)],
     [('no', '입력에서 찾지 못했어요', '트렌드 보기', 'S1-list.dc.html#trend')]),
    ('자격요건', [('콘텐츠의 ', None), ('성과를 객관적인 수치로 분석하고', 'part'), (', 논리적인 근거를 바탕으로 다음 액션을 제안할 수 있는 데이터 감각을 갖추신 분', None)],
     [('part', '팔로워 300명에서 1,200명 · 무엇을 보고 무엇을 바꿨는지 한 문장 더하면 맞음', '이력서 고치기', 'S5-resume.dc.html')]),
    ('우대사항', [('유튜브, 틱톡, 인스타그램 등 ', None), ('개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸', 'ok'), (' ', None), ('숏폼 발행 경험', 'no'), ('이 있으신 분', None)],
     [('ok', '학생회 홍보부 인스타그램 운영 1년, 팔로워 300명에서 1,200명', '', ''), ('no', '숏폼 발행은 찾지 못했어요 · 입력엔 카드뉴스만 있어요', '프로젝트', 'S4-activity.dc.html')]),
    ('우대사항', [('뷰티 산업에 대한 애정이 깊고, 셀링 포인트를 센스 있게 캐치하시는 분', None)], []),
    ('우대사항', [('마케팅 학회, 공모전 수상, 혹은 타 기업에서의 인턴십 등 ', None), ('실무 베이스의 마케팅 경험', 'no'), ('을 보유하신 분', None)],
     [('no', '입력에서 찾지 못했어요', '공모전', 'S4-activity.dc.html')]),
    ('우대사항', [('Adobe Premiere Pro, Photoshop 등을 활용해 ', None), ('본인의 기획안을 영상 결과물로 직접 구현', 'no'), ('할 수 있는 분', None)],
     [('no', '캔바만 찾았어요', 'SeSAC 과정', 'S4-next.dc.html')]),
]
DUTIES = ['Meta(FB/IG), YouTube, TikTok 등 주요 매체에 최적화된 숏폼 영상 및 이미지 광고 소재를 직접 기획하고 제작',
          '본인이 기획한 콘텐츠의 CTR, CVR, ROAS 데이터를 분석하고 A/B 테스트 진행', '뷰티 및 라이프스타일 시장 내 고효율 콘텐츠 트렌드 모니터링']
PROCEDURE = "서류 전형, 1차 인터뷰, 최종 합격 · 포트폴리오 자유 양식"
V6_JS = r'''  constructor(props) {
    super(props);
    this.state = { trendOpen: false, done: (typeof location !== 'undefined' && location.hash === '#result') };
  }
  openCompareTrend() {
    this.setState({ trendOpen: true });
    requestAnimationFrame(() => {
      if (!this.state.trendOpen) return;
      const close = document.querySelector('#p03-trend-popup [aria-label="닫기"]');
      if (close) close.focus();
    });
  }
  closeCompareTrend() {
    this.setState({ trendOpen: false });
    requestAnimationFrame(() => {
      if (this.state.trendOpen) return;
      const target = document.getElementById('p03-trend-trigger') || document.getElementById('p03-posting');
      if (target) target.focus({ preventScroll: true });
    });
  }
  handleCompareTrendKey(event) {
    if (!this.state.trendOpen) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      this.closeCompareTrend();
    } else if (event.key === 'Tab') {
      const popup = document.getElementById('p03-trend-popup');
      if (!popup) return;
      const targets = [...popup.querySelectorAll('button:not([disabled]), a[href], input:not([disabled]), [tabindex="0"]')]
        .filter(el => el.getClientRects().length > 0);
      const first = targets[0], last = targets[targets.length - 1];
      if (!first) { event.preventDefault(); popup.focus(); }
      else if (event.shiftKey && (document.activeElement === first || !popup.contains(document.activeElement))) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && (document.activeElement === last || !popup.contains(document.activeElement))) {
        event.preventDefault(); first.focus();
      }
    }
  }
  pageVals() {
    const d = this.state.done;
    const hl = (k) => d ? __HL__[k] : '';
    return {
      trendOpen: this.state.trendOpen,
      openTrend: () => this.openCompareTrend(), closeTrend: () => this.closeCompareTrend(),
      trendKey: (event) => this.handleCompareTrendKey(event),
      done: d, notDone: !d,
      run: () => this.setState({ done: true }), reset: () => this.setState({ done: false, trendOpen: false }),
      hl: { ok: hl('ok'), part: hl('part'), no: hl('no') }
    };
  }
'''

HL = {
    key: (f'border: 1px solid {foreground}; background: {background}; color: {foreground}; '
          'border-radius: 4px; padding: 1px 2px; font-weight: 600; text-decoration: none; '
          '-webkit-box-decoration-break: clone; box-decoration-break: clone;')
    for key, (foreground, background) in COMPARE_COLORS.items()
}


def mk_badge(k, *, compare=False):
    t, c, bg = MK[k]
    if compare:
        c, bg = COMPARE_COLORS[k]
    return f'<span style="flex-shrink: 0; padding: 2px 8px; border-radius: 6px; background: {bg}; color: {c}; font-size: 12px; font-weight: 700;">{t}</span>'


def post_li(pieces, finds, mobile):
    pre = 'm-' if mobile else ''
    txt = ''.join(f'<span style="@@hl.{m}@@">{t}</span>' if m else t for t, m in pieces)
    ev = ''
    for k, note, act, href in finds:
        a = f'<a href="{pre}{href}" style="flex-shrink: 0; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">{act} ›</a>' if act else ''
        if act == '트렌드 보기':
            a = f'<button id="p03-trend-trigger" type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; padding: 0; background: none; color: {BLUE}; font: inherit; font-size: 13px; font-weight: 600; cursor: pointer;">{act} ›</button>'
        ev += f'<div style="display: flex; flex-wrap: wrap; align-items: flex-start; gap: 8px; font-size: 13px; line-height: 1.5; color: #4E5968;">{mk_badge(k, compare=True)}<span style="flex: 1 1 100px; min-width: 0;">{note}</span>{a}</div>'
    evb = (f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 6px; margin-top: 8px; padding: 10px 12px; border-radius: 10px; background: #F9FAFB;">{ev}</div></sc-if>' if ev else
           f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="margin-top: 6px; font-size: 12px; color: {MUTE};">관심, 태도 문장이라 비교하지 않았어요</div></sc-if>')
    return f'<li style="padding: 2px 0;"><span style="font-size: 15px; line-height: 1.75; color: #333D4B;">{txt}</span>{evb}</li>'


def posting_section(title, content, mobile, subtitle=''):
    body = content if content.strip() else '<p style="margin: 0; font-size: 15px; color: #4E5968;">공고에 기재된 내용이 없어요</p>'
    sub = f'<span style="font-size: 13px; font-weight: 600; color: {SUB};">{subtitle}</span>' if subtitle else ''
    return (f'<section aria-label="{title}" style="display: flex; flex-direction: column; gap: 10px; min-width: 0; overflow-wrap: anywhere;">'
            f'<h3 style="margin: 0; font-size: 16px; font-weight: 700;">{title}</h3>{sub}{body}</section>')


def posting_card(mobile):
    pad = '20px' if mobile else '32px 36px'
    ul = lambda items: f'<ul style="margin: 0; padding: 0 0 0 18px; display: flex; flex-direction: column; gap: 8px;">{items}</ul>' if items else ''
    duties = ''.join(f'<li style="font-size: 15px; line-height: 1.75; color: #333D4B;">{t}</li>' for t in DUTIES)
    quals = ''.join(post_li(p, f, mobile) for k, p, f in POST_REQ if k == '자격요건')
    prefs = ''.join(post_li(p, f, mobile) for k, p, f in POST_REQ if k == '우대사항')
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: {MUTE};">{k}</span><span style="font-size: 14px;">{v}</span></div>'
                   for k, v in [('직무', '콘텐츠 마케터'), ('고용형태', '인턴 (채용연계)'), ('경력', '경력 무관'), ('마감', '채용 시 마감')])
    procedure = f'<p style="margin: 0; font-size: 15px; line-height: 1.75; color: #333D4B;">{PROCEDURE}</p>' if PROCEDURE.strip() else ''
    return (f'<article id="p03-posting" tabindex="-1" aria-label="채용 공고" style="display: flex; flex-direction: column; gap: 16px; min-width: 0;">'
            f'<div style="display: flex; flex-direction: column; gap: 24px; padding: {pad}; {CARD} min-width: 0; overflow-wrap: anywhere;">'
            f'<div style="display: flex; align-items: center; gap: 12px;">{mark("olive")}<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 15px; font-weight: 600;">올리브인터내셔널</span><span style="font-size: 12px; color: {MUTE};">뷰티 브랜드 성분에디터 운영 · 마케팅본부</span></span>{save_btn("sv.olive", 40)}</div>'
            f'<h1 style="margin: 0; font-size: {20 if mobile else 26}px; font-weight: 700; line-height: 1.4; letter-spacing: -0.02em;">[마케팅본부] 성분에디터 콘텐츠 마케팅 인턴 (채용연계형)</h1>'
            f'<div style="display: grid; grid-template-columns: repeat({2 if mobile else 4}, minmax(0, 1fr)); gap: 12px; padding: 14px 16px; border-radius: 12px; background: #F9FAFB;">{meta}</div>'
            '</div>'
            f'<div aria-label="공고 본문" class="p03-posting-body" style="padding: {"20px" if mobile else "24px 28px"}; {CARD}">'
            f'{posting_section("담당업무", ul(duties), mobile)}'
            f'{posting_section("자격요건", ul(quals), mobile, "Skillset")}'
            f'{posting_section("우대사항", ul(prefs), mobile)}'
            f'{posting_section("전형절차", procedure, mobile)}'
            '</div>'
            '</article>')


def compare_trend_popup(mobile):
    return ('<style>.p03-posting-body > section + section { border-top: 1px solid #E5E8EB; margin-top: 20px; padding-top: 20px; }</style>'
            '<div id="p03-trend-popup" tabindex="-1" onKeyDown="@@trendKey@@">'
            + trend_popup(mobile, None, '공고 비교로 돌아가기') + '</div>')


def next_rows(mobile):
    pre = 'm-' if mobile else ''
    rows = [('S4-next.dc.html', 'edu', '교육으로 배우기', '숏폼, 영상 툴을 채워요 · SeSAC 2개 모집 중', True), ('S4-activity.dc.html', 'act', '대외활동, 프로젝트', '4주 숏폼 프로젝트로 발행 경험 만들기', False),
            ('S4-cert.dc.html', 'cert', '자격증, 어학', '이 직무 공고는 3%만 자격증을 적어요', False), ('S4-apply.dc.html', 'apply', '지원 준비', '맞는 경험을 앞에 두고 바로 지원', False)]
    out = ''
    for h, ic, t, sub, rec in rows:
        box = (f'background: #F4F9FF; box-shadow: inset 0 0 0 1.5px {BLUE};' if rec else 'background: #F9FAFB;')
        tag = f'<span style="padding: 2px 8px; border-radius: 999px; background: {BLUE}; color: #FFFFFF; font-size: 11px; font-weight: 700;">추천</span>' if rec else ''
        out += (f'<a href="{pre}{h}" style="display: flex; align-items: center; gap: 12px; padding: 14px; border-radius: 16px; {box} color: {INK}; text-decoration: none;">'
                f'<span style="width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; background: #FFFFFF; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{CICON[ic]}</svg></span>'
                f'<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 3px;"><span style="display: flex; align-items: center; gap: 6px; font-size: 15px; font-weight: 700;">{t}{tag}</span><span style="font-size: 12px; line-height: 1.4; color: {SUB};">{sub}</span></span>'
                f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B0B8C1" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></a>')
    return f'<div style="display: flex; flex-direction: column; gap: 8px;">{out}</div>'


RING_COLORS = {'ok': '#22C55E', 'part': '#F59E0B', 'no': '#EF4444'}


def score_ring():
    r, c = 30, 2 * 3.14159 * 30
    one = c / 6
    arc = lambda color, length, offset: f'<circle cx="38" cy="38" r="{r}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="butt" stroke-dasharray="{length - 2:.1f} {c:.1f}" stroke-dashoffset="{-offset:.1f}" transform="rotate(-90 38 38)"/>'
    return (f'<span role="img" aria-label="6개 중 맞음 1, 일부 1, 없음 4" style="position: relative; width: 76px; height: 76px; flex-shrink: 0;"><svg width="76" height="76" viewBox="0 0 76 76" aria-hidden="true">'
            f'<circle cx="38" cy="38" r="{r}" fill="none" stroke="#EEF0F3" stroke-width="9"/>{arc(RING_COLORS["ok"], one, 0)}{arc(RING_COLORS["part"], one, one)}{arc(RING_COLORS["no"], 4 * one, 2 * one)}</svg>'
            f'<span style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 800; letter-spacing: -0.02em;">2<span style="font-size: 13px; color: {MUTE}; font-weight: 600;">/6</span></span></span>')


def cta_pair(pre, mobile):
    # P03-F14: 데스크톱은 두 버튼을 같은 크기 (전체 너비, 52px)로. 파란색은 AI 비교 하나에만
    if mobile:
        return (f'<button type="button" onClick="@@run@@" style="height: 54px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; cursor: pointer;">AI로 비교하기</button>'
                f'<a href="{pre}S5-resume.dc.html" style="align-self: flex-start; box-sizing: border-box; display: flex; align-items: center; justify-content: center; min-height: 44px; max-width: 100%; padding: 0 16px; border: 1px solid #D1D6DB; border-radius: 12px; background: #FFFFFF; color: #191F28; font-size: 14px; font-weight: 600; text-decoration: none;">나의 이력서 수정</a>')
    btn = 'box-sizing: border-box; width: 100%; height: 52px; display: flex; align-items: center; justify-content: center; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; font-family: inherit; cursor: pointer; text-decoration: none;'
    return (f'<button type="button" onClick="@@run@@" style="{btn} background: {BLUE}; color: #FFFFFF;">AI로 비교하기</button>'
            f'<a href="{pre}S5-resume.dc.html" style="{btn} background: #F2F4F6; color: #333D4B;">나의 이력서 수정</a>')


def side_panel(mobile):
    example_badge = '<span style="align-self: flex-start; padding: 3px 8px; border-radius: 6px; background: #F2F4F6; color: #4E5968; font-size: 12px; font-weight: 600;">시연 예시</span>'
    example_notice = '<span style="font-size: 12px; line-height: 1.5; color: #4E5968;">시연용 예시 비교 결과<br>실제 AI 분석은 아직 연결되지 않았어요</span>'
    pre = 'm-' if mobile else ''
    seg = lambda c: f'<span style="flex: 1 1 0; height: 8px; border-radius: 999px; background: {c};"></span>'
    exp = (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px; border-radius: 14px; background: #F9FAFB;">'
           f'<div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 13px; font-weight: 700;">비교에 쓰는 내 경험</span></div>'
           f'<span style="font-size: 13px; line-height: 1.55; color: #4E5968;">학생회 홍보부 인스타그램 운영 1년 · 카드뉴스 주 1회 (캔바) · 팔로워 300명에서 1,200명 · 컴활 2급 · OPIc IM2</span></div>')
    before = (f'<sc-if value="@@notDone@@" hint-placeholder-val="@@true@@"><div style="display: flex; flex-direction: column; gap: 14px;">{example_badge}'
              f'<span style="font-size: 20px; font-weight: 700; line-height: 1.4;">이 공고 문장에<br>내 경험을 맞춰 볼게요</span>{exp}'
              f'<div style="display: flex; flex-direction: column; gap: 8px;">'
              f'{cta_pair(pre, mobile)}</div>'
              f'{example_notice}</div></sc-if>')
    tile = lambda n, label, bg, fg: f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 12px; border-radius: 14px; background: {bg};"><span style="font-size: 22px; font-weight: 800; color: {fg}; letter-spacing: -0.02em;">{n}</span><span style="font-size: 12px; font-weight: 600; color: {fg};">{label}</span></div>'
    refresh = f'<svg aria-hidden="true" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/></svg>'
    point = f'<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="{"M12 5v14M6 13l6 6 6-6" if mobile else "M19 12H5M11 6l-6 6 6 6"}"/></svg>'
    after = (f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 12px;">'
             f'<div style="display: flex; justify-content: space-between; align-items: center;">{example_badge}<button type="button" onClick="@@reset@@" style="display: flex; align-items: center; gap: 4px; border: none; background: none; padding: 0; font-size: 12px; color: {MUTE}; cursor: pointer;">{refresh}다시 비교</button></div>'
             f'{example_notice}'
             f'<div style="display: flex; align-items: center; gap: 16px;">{score_ring()}<span style="font-size: 20px; font-weight: 700; line-height: 1.4; letter-spacing: -0.02em;">공고 요구 6개 중<br><span style="color: {BLUE};">2개</span>가 이어져요</span></div>'
             f'<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">{tile(1, "맞음", COMPARE_COLORS["ok"][1], COMPARE_COLORS["ok"][0])}{tile(1, "일부", COMPARE_COLORS["part"][1], COMPARE_COLORS["part"][0])}{tile(4, "없음", COMPARE_COLORS["no"][1], COMPARE_COLORS["no"][0])}</div>'
             f'<span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: {SUB};">{point}{"아래" if mobile else "왼쪽"} 공고 문장에 같은 색으로 표시했어요</span>'
             f'<div style="height: 1px; background: {LINE};"></div>'
             f'<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 17px; font-weight: 700;">어느 부분을 먼저 채울까요?</span><span style="font-size: 12px; color: {MUTE};">고르는 건 나예요. 비어 있는 4개 기준으로 추천했어요</span></div>'
             f'{next_rows(mobile)}</div></sc-if>')
    sticky = '' if mobile else 'position: sticky; top: 24px;'
    return f'<aside style="{sticky} display: flex; flex-direction: column; padding: {"20px" if mobile else "24px"}; {CARD}">{before}{after}</aside>'


v6_body = (f'  <div style="padding: 16px 56px 0;"><a href="S1-list.dc.html" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 공고 목록</a></div>\n'
           f'  <div style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 24px; padding: 16px 56px 56px; align-items: start;">{posting_card(False)}{side_panel(False)}</div>\n')
V6_SCRIPT = V6_JS.replace('__HL__', json.dumps(HL, ensure_ascii=False))
boards['S3-compare.dc.html'] = ('S2 공고 원문 + AI 비교 (한 화면)', dpage('S3-compare.dc.html', '공고와 내 경험 비교', 'find', v6_body + compare_trend_popup(False), V6_SCRIPT, saves=('olive',)))
m_v6 = f'    {side_panel(True)}\n    {posting_card(True)}\n'
# phone: the panel goes first so the button and the score are on the first screen
boards['m-S3-compare.dc.html'] = ('M2 공고 원문 + AI 비교 (모바일)', mpage('m-S3-compare.dc.html', 'M2 공고와 내 경험 비교 (모바일)', topbar_back('m-S1-list.dc.html', '공고와 비교'), m_v6 + compare_trend_popup(True), 'find', V6_SCRIPT, saves=('olive',)))
