"""P01 홈 (데스크톱, 모바일). 구조는 docs/prd/P01-home.md v1.1을 따른다."""

JOBKEY = {'서비스 기획, PM': 'pm', '데이터 분석': 'data', 'UI/UX 디자인': 'uiux', '웹 개발': 'web', 'AI 엔지니어': 'ai', '클라우드 엔지니어': 'cloud'}
GREY_CHIP = f'flex-shrink: 0; padding: 8px 14px; border-radius: 999px; background: {FILL}; color: #4E5968; font-size: 13px; text-decoration: none; white-space: nowrap;'


def job_chips(pre):
    first = f'<a href="{pre}S1-list.dc.html" style="{GREY_CHIP}">SNS 콘텐츠 마케팅</a>'
    return first + ''.join(f'<a href="{pre}S1-list.dc.html#job={JOBKEY[j]}" style="{GREY_CHIP}">{j}</a>' for j in JOBS7)


# P01-F06 이어서 하기: 로그인했을 때만
def resume_strip(pre, mobile):
    link = f'font-size: {13 if mobile else 14}px; font-weight: 600; color: {BLUE_D}; text-decoration: none; white-space: nowrap;'
    return (f'<sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><div style="display: flex; {"flex-direction: column; align-items: flex-start; gap: 8px; padding: 16px 18px;" if mobile else "align-items: center; gap: 20px; padding: 16px 24px;"} background: {BLUE_BG}; border-radius: 16px;">'
            f'<span style="font-size: {14 if mobile else 15}px; font-weight: 700; color: {INK};">@@userName@@님, 이어서 볼까요?</span>'
            f'<span style="display: flex; flex-wrap: wrap; gap: {12 if mobile else 20}px;">'
            f'<a href="{pre}S3-compare.dc.html#result" style="{link}">올리브인터내셔널 비교 결과 ›</a>'
            f'<a href="{pre}S5-saved.dc.html" style="{link}">저장함 @@savedCount@@개 ›</a>'
            f'<a href="{pre}S5-resume.dc.html" style="{link}">이력서 수정 ›</a></span></div></sc-if>')


# P01-F07 이렇게 비교해요: 시연 공고의 실제 문장 (30_compare.py POST_REQ)
EX_ROWS = [
    ('ok', '채널을 직접 운영한 경험', '인스타그램 팔로워 300명에서 1,200명'),
    ('no', '숏폼 발행 경험', '찾지 못했어요'),
]


def ex_card(mobile):
    rows = ''
    for k, req, ev in EX_ROWS:
        label, fg, bg = {'ok': ('맞음', BLUE_D, BLUE_BG), 'no': ('없음', SUB, '#EEF0F3')}[k]  # 30_compare.py MK와 같은 색
        rows += (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: {"14px" if mobile else "16px 18px"}; background: #FFFFFF; border-radius: 14px;">'
                 f'<div style="display: flex; align-items: flex-start; gap: 10px;"><span style="flex-shrink: 0; padding: 3px 8px; border-radius: 6px; background: {bg}; color: {fg}; font-size: 12px; font-weight: 700;">{label}</span>'
                 f'<span style="font-size: {14 if mobile else 15}px; line-height: 1.5; color: {INK};">"{req}"</span></div>'
                 f'<span style="font-size: 13px; line-height: 1.5; color: {SUB};">{ev}</span></div>')
    return (f'<div style="display: flex; flex-direction: column; gap: 12px; {"padding: 18px 16px; border-radius: 18px;" if mobile else "padding: 40px 36px; height: 100%; box-sizing: border-box; justify-content: center;"} background: {BLUE_BG};">'
            f'<div style="display: flex; align-items: center; gap: 8px;"><span style="font-size: {15 if mobile else 16}px; font-weight: 700; color: {INK};">이렇게 비교해요</span>{AI}'
            f'<span style="margin-left: auto; padding: 3px 8px; border-radius: 6px; background: #FFFFFF; color: #4E5968; font-size: 12px; font-weight: 600;">시연 예시</span></div>'
            f'{rows}</div>')


# P01-F05 핫 공고: 시연 공고만 비교하기 (글자 링크), 나머지는 비교 준비 중. 흐리게 하지 않는다
def hot_row(k, company, title, href):
    act = (f'<span style="flex-shrink: 0; font-size: 14px; font-weight: 600; color: {BLUE_D};">비교하기 ›</span>' if href else
           f'<span style="flex-shrink: 0; padding: 4px 9px; border-radius: 999px; background: {FILL}; font-size: 12px; color: #4E5968;">비교 준비 중</span>')
    inner = (f'{mark(k, 40)}<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: {SUB};">{company}</span>'
             f'<span style="font-size: 16px; font-weight: 600; color: {INK};">{title}</span></span>{act}')
    row = 'flex: 1 1 0; min-width: 0; display: flex; align-items: center; gap: 14px; padding: 14px 0;'
    body = f'<a href="{href}" style="{row} text-decoration: none;">{inner}</a>' if href else f'<span style="{row}">{inner}</span>'
    return f'<div style="display: flex; align-items: center; gap: 10px; border-top: 1px solid {LINE};">{body}{save_btn("sv." + k)}</div>'


def hot_section(pre, mobile):
    rows = (hot_row('olive', '올리브인터내셔널', '성분에디터 콘텐츠 마케팅 인턴', f'{pre}S3-compare.dc.html')
            + hot_row('ks', '카카오스타일', 'SNS 콘텐츠 마케터', None)
            + hot_row('rxc', 'RXC', '숏폼 콘텐츠 기획 편집', None))
    return (f'<section aria-labelledby="{pre}hot" style="display: flex; flex-direction: column; padding: {"20px 18px 8px" if mobile else "26px 32px 12px"}; {CARD}">'
            f'<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px;"><h2 id="{pre}hot" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">이번 주 핫 공고</h2>'
            f'</div>{rows}</section>')


# P01-F04 실시간 공고 키워드: 핫 공고 아래, 작게, LIVE 표시 없음
def kw_section(pre, mobile):
    return (f'<section aria-labelledby="{pre}kw" style="display: flex; flex-direction: column; gap: 6px; padding: {"18px 12px 14px" if mobile else "22px 22px 16px"}; {CARD}">'
            f'<div style="display: flex; align-items: center; gap: 8px; padding: 0 10px 4px;"><h2 id="{pre}kw" style="margin: 0; font-size: {16 if mobile else 17}px; font-weight: 700;">요즘 공고에 많이 나오는 말</h2>'
            f'<button type="button" onClick="@@openTrend@@" style="margin-left: auto; border: none; background: none; padding: 0; font-size: 13px; color: {SUB}; cursor: pointer; font-family: inherit;">전체 보기 ›</button></div>'
            f'<div style="display: flex; flex-direction: column;">{trend_rows(RANK[:5], button=True, pad="0 10px", h=42)}</div>'
            f'<span style="padding: 0 10px; font-size: 12px; color: {MUTE};">SNS 콘텐츠 마케팅 2026 공고 59건 기준</span></section>')


H1 = '공고 문장마다,<br>내 경험을 비교해요'
SUBLINE = '비어 있는 부분은 SeSAC 과정과 청년 정책으로 채워요'
SLOGAN = '청년의 경험으로, 다음 청년의 기회를'
CTA = '내 경험과 비교해 보기'

main_body = f'''  <div style="margin: 24px 56px 0;">{resume_strip('', False)}</div>
  <section style="margin: 16px 56px 0; display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); {CARD} overflow: hidden;">
    <div style="padding: 56px 56px 48px; display: flex; flex-direction: column; gap: 20px;">
      <span style="font-size: 15px; font-weight: 600; color: {BLUE_D};">{SLOGAN}</span>
      <h1 style="margin: 0; font-size: 48px; font-weight: 700; line-height: 1.2; letter-spacing: -0.03em;">{H1}</h1>
      <p style="margin: 0; font-size: 18px; color: {SUB}; line-height: 1.6;">{SUBLINE}</p>
      <div style="display: flex; align-items: center; gap: 20px; margin-top: 4px;">
        <a href="S3-compare.dc.html" style="height: 56px; padding: 0 28px; display: flex; align-items: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; text-decoration: none;">{CTA}</a>
        <a href="S1-list.dc.html" style="font-size: 15px; font-weight: 600; color: #4E5968; text-decoration: none;">직무별 공고 보기 ›</a>
      </div>
      <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 12px; padding-top: 20px; border-top: 1px solid {LINE};">
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">{job_chips('')}</div>
      </div>
    </div>
    {ex_card(False)}
  </section>
  <div style="margin: 20px 56px 56px; display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: 20px; align-items: start;">
    {hot_section('', False)}
    {kw_section('', False)}
  </div>
{trend_popup(False, 'S1-list.dc.html')}'''
TREND_SCRIPT = (f"  constructor(props) {{ super(props); this.state = {{ trendOpen: {TREND_JS} }}; }}\n"
                f"  renderVals() {{ return {{ {TREND_VALS} }}; }}")
boards['Main.dc.html'] = ('S0 홈', dpage('Main.dc.html', '일로 홈', 'home', main_body, TREND_SCRIPT, saves=('olive', 'ks', 'rxc')))

# --- mobile (11/6까지 데스크톱만 개편, 모바일은 이전 구조 유지) ---
m_main = f'''    <section style="display: flex; flex-direction: column; gap: 16px; padding: 26px 20px; {CARD}">
      <sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><a href="m-S5-saved.dc.html" style="align-self: flex-start; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; font-weight: 600; text-decoration: none;">@@userName@@님, 저장함 @@savedCount@@개 ›</a></sc-if>
      <h1 style="margin: 0; font-size: 30px; font-weight: 700; line-height: 1.25; letter-spacing: -0.03em;">청년의 경험으로,<br>다음 청년의 기회를</h1>
      <p style="margin: 0; font-size: 15px; line-height: 1.6; color: {SUB};">공고와 내 경험을 AI로 비교하고, 지금 할 일 하나를 골라요</p>
      <a href="m-S1-list.dc.html" style="display: flex; align-items: center; gap: 10px; height: 52px; padding: 0 6px 0 16px; border-radius: 14px; background: {FILL}; color: {MUTE}; text-decoration: none; font-size: 15px;"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><span style="flex: 1 1 0;">직무를 검색하세요</span><span style="height: 40px; padding: 0 16px; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 600; display: flex; align-items: center;">찾아보기</span></a>
      <div class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -20px; padding: 0 20px;"><a href="m-S1-list.dc.html" style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; font-weight: 600; text-decoration: none;">SNS 콘텐츠 마케팅</a>{''.join(chip(j) for j in JOBS7)}</div>
    </section>
    <section aria-labelledby="m-kw" style="display: flex; flex-direction: column; gap: 6px; padding: 20px 12px 14px; {CARD}">
      <div style="display: flex; align-items: center; gap: 8px; padding: 0 8px 4px;"><h2 id="m-kw" style="margin: 0; font-size: 18px; font-weight: 700;">실시간 공고 키워드</h2><span style="display: flex; align-items: center; gap: 4px; padding: 3px 7px; border-radius: 999px; background: #FFEEEE; color: {RED}; font-size: 10px; font-weight: 700;"><span class="illo-live" style="width: 6px; height: 6px; border-radius: 50%; background: {RED};"></span>LIVE</span><button type="button" onClick="@@openTrend@@" style="margin-left: auto; border: none; background: none; padding: 0; font-size: 13px; color: {SUB}; cursor: pointer;">전체 보기 ›</button></div>
      <div style="display: flex; flex-direction: column;">{trend_rows(RANK[:5], button=True, pad='0 10px', h=44)}</div>
      <span style="padding: 0 10px; font-size: 11px; color: {MUTE};">2026 공고 59건 기준</span>
    </section>
    <section aria-labelledby="m-hot" style="display: flex; flex-direction: column; padding: 20px 18px 8px; {CARD}">
      <h2 id="m-hot" style="margin: 0 0 8px; font-size: 18px; font-weight: 700;">이번 주 핫 공고</h2>
      {srow('olive', '올리브인터내셔널', '성분에디터 콘텐츠 마케팅 인턴', 'm-S3-compare.dc.html', 'olive')}
      {srow('ks', '카카오스타일', 'SNS 콘텐츠 마케터', None, 'ks')}
      {srow('rxc', 'RXC', '숏폼 콘텐츠 기획 편집', None, 'rxc')}
    </section>
{trend_popup(True, 'm-S1-list.dc.html')}'''
boards['m-Main.dc.html'] = ('M0 홈 (모바일)', mpage('m-Main.dc.html', 'M0 홈 (모바일)', topbar_logo(auth_mobile()), m_main, 'home', TREND_SCRIPT, saves=('olive', 'ks', 'rxc')))
