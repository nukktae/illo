"""Mobile (390px) artboards for the 일로 canvas, bottom tab bar instead of the top menu.
Content mirrors the desktop boards; every number comes from the same team data."""
import json, os, re, sys

ROOT = sys.argv[1]
LOGO = '/_blob/4757cee651690b4f0f72b4b674e6cbc2'
ILLU = '/_blob/a4f09a990e0582846a840e9525e3e4e3'
THUMB1 = '/_blob/967096ee53e44801f4e34a94c058eadc'
THUMB2 = '/_blob/8431548dc6d24b077041f20d09190c12'
POSTING = 'https://linkareer.com/activity/327326'
SESAC = 'https://sesac.seoul.kr/sesac/course/offline/courseDetail.do?crsSn='
EXT = 'target="_blank" rel="noopener"'

INK, SUB, MUTE, LINE, FILL = '#191F28', '#6B7684', '#8B95A1', '#F2F4F6', '#F2F4F6'
BLUE, BLUE_D, BLUE_BG = '#3182F6', '#1B64DA', '#E8F3FF'
OR, OR_BG, RED = '#C26A00', '#FFF6E5', '#F04452'
CARD = 'background: #FFFFFF; border-radius: 20px;'

CSS = '''body{margin:0}
a{color:#3182F6}
.illo-rank{animation:illo-hl 16s ease-in-out infinite}
@keyframes illo-hl{0%,13%{background:#F4F9FF}16%,100%{background:transparent}}
.illo-live{animation:illo-pulse 1.6s ease-in-out infinite}
@keyframes illo-pulse{0%,100%{opacity:1}50%{opacity:.25}}
.illo-scroll{scrollbar-width:none}.illo-scroll::-webkit-scrollbar{display:none}
@media (prefers-reduced-motion: reduce){.illo-rank,.illo-live{animation:none}}'''

# ---------- bottom tab bar (reference: white card, light-blue filled active icon, home indicator) ----------
ICON_OUT = {
    'home': '<path d="M4 10.5 12 4l8 6.5V19a1 1 0 0 1-1 1h-4v-5h-6v5H5a1 1 0 0 1-1-1z"/>',
    'find': '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    'trend': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'path': '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>',
}
ICON_ON = {
    'home': '<path d="M3.5 10.6 12 3.8l8.5 6.8V19a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 19z" fill="#6AA6F8"/><rect x="11" y="14" width="2" height="4" rx="1" fill="#FFFFFF"/>',
    'find': '<circle cx="11" cy="11" r="7.5" fill="#6AA6F8"/><circle cx="11" cy="11" r="3.5" fill="#FFFFFF"/><path d="m20.5 20.5-4-4" stroke="#6AA6F8" stroke-width="2.6" stroke-linecap="round"/>',
    'trend': '<rect x="3" y="10" width="4.5" height="10" rx="1.5" fill="#6AA6F8"/><rect x="9.75" y="4" width="4.5" height="16" rx="1.5" fill="#6AA6F8"/><rect x="16.5" y="13" width="4.5" height="7" rx="1.5" fill="#6AA6F8"/>',
    'path': '<circle cx="12" cy="7.8" r="4" fill="#6AA6F8"/><path d="M4.5 20.5c.8-4 3.8-6.2 7.5-6.2s6.7 2.2 7.5 6.2z" fill="#6AA6F8"/>',
}
TABS = [('home', '홈', 'm-Main.dc.html'), ('find', '직무 찾기', 'm-S1-list.dc.html'),
        ('trend', '트렌드', 'm-P1-trend.dc.html'), ('path', '내 경로', 'm-S5-path.dc.html')]


def tabbar(active):
    items = []
    for key, label, href in TABS:
        on = key == active
        svg = (f'<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24">{ICON_ON[key]}</svg>' if on else
               f'<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#191F28" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON_OUT[key]}</svg>')
        cur = ' aria-current="page"' if on else ''
        items.append(f'<a href="{href}"{cur} style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding-top: 12px; text-decoration: none; color: {BLUE if on else INK}; font-size: 13px; font-weight: {600 if on else 500};">{svg}{label}</a>')
    return ('  <nav aria-label="주요 메뉴" style="position: sticky; bottom: 0; z-index: 10; display: flex; flex-direction: column; background: #FFFFFF; border-radius: 22px 22px 0 0; box-shadow: 0 -1px 0 rgba(0,23,51,0.06), 0 -6px 20px rgba(0,23,51,0.04);">\n'
            f'    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));">{"".join(items)}</div>\n'
            '    <span aria-hidden="true" style="align-self: center; width: 134px; height: 5px; margin: 18px 0 8px; border-radius: 999px; background: #191F28;"></span>\n'
            '  </nav>\n')


def topbar_logo(right=''):
    return (f'  <div style="display: flex; justify-content: space-between; align-items: center; height: 56px; padding: 0 20px;">'
            f'<img src="{LOGO}" alt="일로" style="height: 22px; width: auto; display: block;">{right}</div>\n')


def topbar_flow(back, title, step):
    segs = ''.join(f'<span style="flex: 1 1 0; height: 4px; border-radius: 999px; background: {BLUE if i <= step else "#E5E8EB"};"></span>' for i in (1, 2, 3))
    return ('  <div style="position: sticky; top: 0; z-index: 10; display: flex; flex-direction: column; gap: 10px; padding: 0 16px 12px; background: rgba(250,250,250,0.96);">\n'
            f'    <div style="display: grid; grid-template-columns: 40px 1fr 40px; align-items: center; height: 52px;"><a href="{back}" aria-label="뒤로" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: {INK};"><svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></a>'
            f'<span style="text-align: center; font-size: 17px; font-weight: 700;">{title}</span><span style="text-align: right; font-size: 13px; color: {MUTE};">{step}/3</span></div>\n'
            f'    <div aria-label="{step}단계 중 3단계" style="display: flex; gap: 4px;">{segs}</div>\n  </div>\n')


def page(name, title, top, body, active, script='  renderVals() { return {}; }'):
    return ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            f'<title>{title}</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">\n'
            f'<style>\n{CSS}\n</style>\n</helmet>\n'
            f'<div style="width: 390px; min-height: 844px; box-sizing: border-box; background: #FAFAFA; color: {INK}; font-family: Pretendard, -apple-system, system-ui, sans-serif; display: flex; flex-direction: column;">\n'
            f'{top}  <main style="flex: 1 1 auto; display: flex; flex-direction: column; gap: 12px; padding: 4px 16px 28px;">\n{body}  </main>\n{tabbar(active)}</div>\n</x-dc>\n'
            '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":390,"height":844}}\'>\n'
            f'class Component extends DCLogic {{\n{script}\n}}\n</script>\n</body>\n</html>\n')


# ---------- small building blocks ----------
def chip(t, on=False):
    return (f'<span style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG if on else FILL}; color: {BLUE_D if on else "#4E5968"}; font-size: 13px;">{t}</span>')


def h2(t, right=''):
    return f'<div style="display: flex; justify-content: space-between; align-items: center;"><h2 style="margin: 0; font-size: 18px; font-weight: 700;">{t}</h2>{right}</div>'


def btn(href, label, primary=True, ext=False):
    st = (f'background: {BLUE}; color: #FFFFFF;' if primary else f'background: {FILL}; color: {INK};')
    e = f' {EXT}' if ext else ''
    return f'<a href="{href}"{e} style="height: 52px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border-radius: 14px; {st} font-size: 16px; font-weight: 600; text-decoration: none;">{label}</a>'


MARKS = {
    'olive': ('#2E7D4F', '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24"><path d="M5 19C5 11 10 5 19 5c0 9-6 14-14 14z" fill="#FFFFFF"/><path d="M6 18c3-4 6-7 10-9" stroke="#2E7D4F" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'),
    'ks': ('#111111', '<span style="color: #FFFFFF; font-size: 17px; font-weight: 800; letter-spacing: -0.04em;">ks</span>'),
    'rxc': ('#FF4B3E', '<span style="color: #FFFFFF; font-size: 12px; font-weight: 800; letter-spacing: -0.05em;">RXC</span>'),
    'home': ('#24306B', '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"><path d="M4 11l8-6 8 6v8a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><circle cx="12" cy="14.5" r="2.2"/></svg>'),
}


def mark(k, size=44):
    c, inner = MARKS[k]
    return f'<span role="img" aria-label="로고" style="width: {size}px; height: {size}px; flex-shrink: 0; border-radius: 12px; background: {c}; display: flex; align-items: center; justify-content: center;">{inner}</span>'


DEMO = f'<span style="flex-shrink: 0; padding: 4px 9px; border-radius: 999px; background: {FILL}; font-size: 11px; color: {MUTE};">시연 제외</span>'


def job_row(k, company, title, tags, href=None):
    inner = (f'{mark(k)}<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 12px; color: {SUB};">{company}</span>'
             f'<span style="font-size: 16px; font-weight: 600; line-height: 1.35;">{title}</span><span style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 3px;">'
             + ''.join(f'<span style="padding: 3px 8px; border-radius: 999px; background: {FILL}; font-size: 11px; color: {SUB};">{t}</span>' for t in tags) + '</span></span>')
    if href:
        return (f'<a href="{href}" style="display: flex; align-items: center; gap: 14px; padding: 16px; {CARD} color: {INK}; text-decoration: none;">{inner}'
                f'<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></a>')
    return f'<div style="display: flex; align-items: center; gap: 14px; padding: 16px; {CARD}">{inner}{DEMO}</div>'


# ---------- live ranking (same data as desktop) ----------
RANK = [('트렌드 감각, 밈', 64, 1), ('콘텐츠 기획', 63, 1), ('데이터, 성과 분석', 49, 5), ('디자인 툴', 44, 1),
        ('영상, 숏폼 제작', 42, -4), ('영상 툴 (프리미어 등)', 39, 0), ('포트폴리오', 36, -3), ('카피라이팅', 29, 3)]


def delta(d):
    if d > 0:
        return f'<span style="width: 34px; text-align: right; font-size: 13px; font-weight: 600; color: {RED};">▲{d}</span>'
    if d < 0:
        return f'<span style="width: 34px; text-align: right; font-size: 13px; font-weight: 600; color: {BLUE};">▼{-d}</span>'
    return '<span style="width: 34px; text-align: right; font-size: 13px; color: #B0B8C1;">–</span>'


def rank_rows(rows):
    out = ''
    for i, (n, p, d) in enumerate(rows, 1):
        c = BLUE if i <= 3 else MUTE
        out += (f'<a href="m-P1-trend.dc.html" class="illo-rank" style="animation-delay: {(i - 1) * 2}s; display: flex; align-items: center; gap: 12px; height: 46px; padding: 0 10px; border-radius: 12px; color: {INK}; text-decoration: none;">'
                f'<span style="width: 16px; font-size: 16px; font-weight: 700; color: {c};">{i}</span><span style="flex: 1 1 0; font-size: 15px; font-weight: 500;">{n}</span>'
                f'<span style="font-size: 14px; color: #4E5968;">{p}%</span>{delta(d)}</a>')
    return out


boards = {}

# ===== m-Main =====
jobs7 = ['서비스 기획, PM', '데이터 분석', 'UI/UX 디자인', '웹 개발', 'AI 엔지니어', '클라우드 엔지니어']
main = f'''    <section style="display: flex; flex-direction: column; gap: 16px; padding: 24px 20px; {CARD}">
      <span style="align-self: flex-start; display: flex; align-items: center; gap: 6px; padding: 6px 11px 6px 8px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px; font-weight: 600;"><span style="width: 7px; height: 7px; border-radius: 50%; background: {BLUE};"></span>서울시 청년취업사관학교 SeSAC 연계</span>
      <h1 style="margin: 0; font-size: 30px; font-weight: 700; line-height: 1.25; letter-spacing: -0.03em;">청년의 경험으로,<br>다음 청년의 기회를</h1>
      <p style="margin: 0; font-size: 15px; line-height: 1.6; color: {SUB};">지원하고 싶은 공고와 내 경험을 나란히 놓고, 근거 문장으로 비교한 뒤 지금 할 일 하나를 골라요</p>
      <a href="m-S1-list.dc.html" style="display: flex; align-items: center; gap: 10px; height: 52px; padding: 0 6px 0 16px; border-radius: 14px; background: {FILL}; color: {MUTE}; text-decoration: none; font-size: 15px;"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><span style="flex: 1 1 0;">직무를 검색하세요</span><span style="height: 40px; padding: 0 16px; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 600; display: flex; align-items: center;">찾아보기</span></a>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <span style="font-size: 12px; color: {SUB};">많이 찾는 직무 7</span>
        <div class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -20px; padding: 0 20px;"><a href="m-S1-list.dc.html" style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none;">SNS 콘텐츠 마케팅</a>{''.join(chip(j) for j in jobs7)}</div>
        <span style="font-size: 11px; color: {MUTE};">시연은 SNS 콘텐츠 마케팅으로 진행돼요</span>
      </div>
    </section>
    <section style="position: relative; display: flex; justify-content: center; padding-top: 20px; background: {BLUE_BG}; border-radius: 20px; overflow: hidden;">
      <div style="position: absolute; top: 16px; left: 16px; display: flex; flex-direction: column; gap: 3px; padding: 10px 12px; background: #FFFFFF; border-radius: 12px;"><span style="font-size: 11px; color: {SUB};">이 공고가 원하는 것</span><span style="font-size: 13px; font-weight: 600;">"SNS 채널 운영 경험"</span><span style="align-self: flex-start; margin-top: 2px; padding: 2px 7px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 11px; font-weight: 600;">내 경험과 맞음</span></div>
      <img src="{ILLU}" alt="두 장의 카드를 들고 무엇을 먼저 할지 고민하는 취준생" style="height: 230px; width: auto; display: block;">
    </section>
    <section aria-label="실시간 공고 키워드" style="display: flex; flex-direction: column; gap: 12px; padding: 22px 16px 16px; {CARD}">
      <div style="display: flex; align-items: center; gap: 8px; padding: 0 4px;"><h2 style="margin: 0; font-size: 18px; font-weight: 700;">실시간 공고 키워드</h2><span style="display: flex; align-items: center; gap: 4px; padding: 3px 7px; border-radius: 999px; background: #FFEEEE; color: {RED}; font-size: 10px; font-weight: 700;"><span class="illo-live" style="width: 6px; height: 6px; border-radius: 50%; background: {RED};"></span>LIVE</span></div>
      <span style="padding: 0 4px; font-size: 12px; line-height: 1.5; color: {SUB};">SNS 콘텐츠 마케팅 2026 공고 59건 기준 · 순위 변화는 2023~25 공고 45건과 비교</span>
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 14px; background: #FFF4F4;"><span style="font-size: 11px; font-weight: 600; color: {RED};">급상승</span><span style="font-size: 15px; font-weight: 700;">데이터, 성과 분석 8위에서 3위로</span><span style="font-size: 12px; color: {SUB};">자격증은 13위, 3%예요</span></div>
      <div style="display: flex; flex-direction: column;">{rank_rows(RANK)}</div>
      {btn('m-P1-trend.dc.html', '트렌드 자세히 보기', False)}
    </section>
    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 14px; {CARD}"><span style="font-size: 22px; font-weight: 700;">104<span style="font-size: 13px;">건</span></span><span style="font-size: 11px; line-height: 1.4; color: {SUB};">공고 원문 분석</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 14px; {CARD}"><span style="font-size: 22px; font-weight: 700;">210<span style="font-size: 13px;">개</span></span><span style="font-size: 11px; line-height: 1.4; color: {SUB};">SeSAC 과정 연결</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 14px; {CARD}"><span style="font-size: 22px; font-weight: 700;">0<span style="font-size: 13px;">번</span></span><span style="font-size: 11px; line-height: 1.4; color: {SUB};">합격 여부 예측</span></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 12px; padding: 0 4px;"><h2 style="margin: 0; font-size: 18px; font-weight: 700;">이번 주 핫 공고</h2><span style="font-size: 12px; color: {MUTE};">시연은 첫 공고로 진행</span></div>
    {job_row('olive', '올리브인터내셔널', '성분에디터 콘텐츠 마케팅 인턴', ['인턴', '채용연계'], 'm-S2-input.dc.html')}
    {job_row('ks', '카카오스타일', 'SNS 콘텐츠 마케터', ['인턴', '인스타그램'])}
    {job_row('rxc', 'RXC', '숏폼 콘텐츠 기획 편집', ['인턴 6개월', '숏폼'])}
'''
boards['m-Main.dc.html'] = ('M0 홈 (모바일)', topbar_logo(f'<span style="font-size: 12px; color: {MUTE};">로그인 없이 바로 써요</span>'), main, 'home')

# ===== m-S1 =====
bars = ''.join(f'<div style="display: grid; grid-template-columns: 96px 1fr 36px; gap: 10px; align-items: center; font-size: 13px;"><span>{n}</span><span style="height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; height: 6px; width: {p}%; border-radius: 999px; background: {BLUE};"></span></span><span style="text-align: right; font-weight: 600;">{p}%</span></div>'
               for n, p in [('콘텐츠 기획', 51), ('영상, 숏폼 제작', 40), ('디자인 툴', 37), ('자격증', 3)])
s1 = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;">
      <span style="font-size: 12px; color: {MUTE};">직무 찾기 · 마케팅</span>
      <h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">SNS 콘텐츠 마케팅</h1>
      <span style="font-size: 14px; color: {SUB};">신입, 인턴 공고 <b style="color: {INK}; font-weight: 600;">82</b>건 · 2026.10 수집</span>
    </div>
    <div role="tablist" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);"><span role="tab" aria-selected="true" style="flex: 1 1 0; text-align: center; padding: 9px 0; border-radius: 9px; background: #FFFFFF; font-size: 14px; font-weight: 600;">신입, 인턴</span><span role="tab" style="flex: 1 1 0; text-align: center; padding: 9px 0; font-size: 14px; color: {SUB};">경력</span><span role="tab" style="flex: 1 1 0; text-align: center; padding: 9px 0; font-size: 14px; color: {SUB};">전체</span></div>
    <a href="m-P1-trend.dc.html" style="display: flex; flex-direction: column; gap: 12px; padding: 18px; {CARD} color: {INK}; text-decoration: none;">
      <div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 16px; font-weight: 700;">이 직무 최신 트렌드</span><span style="font-size: 13px; color: {BLUE}; font-weight: 600;">자세히 ›</span></div>
      {bars}
      <span style="padding: 10px 12px; border-radius: 10px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px;">이 직무는 자격증보다 직접 만든 콘텐츠를 훨씬 많이 봐요</span>
    </a>
    <a href="m-S2-input.dc.html" style="display: flex; flex-direction: column; gap: 14px; padding: 16px; {CARD} color: {INK}; text-decoration: none;">
      <div style="display: flex; align-items: center; gap: 14px;">{mark('olive')}<span style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 12px; color: {SUB};">올리브인터내셔널</span><span style="font-size: 16px; font-weight: 600;">성분에디터 콘텐츠 마케팅 인턴</span></span></div>
      <div style="display: flex; gap: 4px;">{chip('채용연계형 인턴')}{chip('숏폼')}{chip('성과 분석')}</div>
      <span style="height: 46px; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: {BLUE}; color: #FFFFFF; font-size: 15px; font-weight: 600;">내 경험과 비교</span>
    </a>
    {job_row('ks', '카카오스타일', 'SNS 콘텐츠 마케터', ['인턴', '인스타그램, Threads'])}
    {job_row('rxc', 'RXC', '숏폼 콘텐츠 기획 편집', ['인턴 6개월', '포트폴리오 필수'])}
    {job_row('home', '앳홈', '미닉스 세일즈 콘텐츠 마케터', ['전환형 인턴', '미니홈'])}
'''
boards['m-S1-list.dc.html'] = ('M1 직무 공고 목록 (모바일)', topbar_logo(), s1, 'find')

# ===== m-P1 (reuses the desktop P1 logic) =====
p1_src = open(os.path.join(ROOT, 'P1-trend.dc.html'), encoding='utf-8').read()
p1_script = re.search(r'class Component extends DCLogic \{\n(.*)\n\}\n</script>', p1_src, re.S).group(1)
p1_script = p1_script.replace("height: 40px; padding: 0 18px;", "height: 38px; padding: 0 14px;")
extra_rows = [('개인 SNS, 채널 운영 경험', 25), ('관련 경험, 실무 경험', 25), ('공모전, 수상', 14), ('서포터즈, 기자단, 대외활동', 3), ('인턴 경험', 2)]
extra_html = ''.join(f'<div style="display: grid; grid-template-columns: 1fr 70px 36px; gap: 10px; align-items: center; font-size: 14px;"><span>{n}</span><span style="height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; height: 6px; width: {p}%; border-radius: 999px; background: {BLUE};"></span></span><span style="text-align: right; font-weight: 600;">{p}%</span></div>' for n, p in extra_rows)
p1 = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;">
      <a href="m-S1-list.dc.html" style="font-size: 13px; color: {SUB}; text-decoration: none;">‹ SNS 콘텐츠 마케팅 공고</a>
      <h1 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.02em;">이 직무 공고는 무엇을 볼까</h1>
      <span style="font-size: 13px; color: {SUB};">공고 104건 · 신입, 인턴 82건 원문 분석</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px;">
      <div style="display: flex; flex-direction: column; gap: 4px; padding: 14px; {CARD}"><span style="font-size: 11px; color: {SUB};">가장 많이 언급한 역량</span><span style="font-size: 18px; font-weight: 700; color: {BLUE};">콘텐츠 기획 51%</span></div>
      <div style="display: flex; flex-direction: column; gap: 4px; padding: 14px; {CARD}"><span style="font-size: 11px; color: {SUB};">자격증을 언급한 공고</span><span style="font-size: 18px; font-weight: 700;">3% · 3건</span></div>
    </div>
    <div role="tablist" style="display: flex; gap: 4px; padding: 4px; background: rgba(0,23,51,0.06); border-radius: 12px; align-self: flex-start;">
      <button type="button" role="tab" onClick="{{{{ tabs.course.pick }}}}" style="{{{{ tabs.course.style }}}}">역량, 교육과정</button>
      <button type="button" role="tab" onClick="{{{{ tabs.cert.pick }}}}" style="{{{{ tabs.cert.style }}}}">자격증</button>
      <button type="button" role="tab" onClick="{{{{ tabs.extra.pick }}}}" style="{{{{ tabs.extra.style }}}}">비교과 경험</button>
    </div>
    <sc-if value="{{{{ showCourse }}}}" hint-placeholder-val="{{{{ true }}}}">
    <section style="display: flex; flex-direction: column; {CARD} overflow: hidden;">
      <div style="padding: 18px 18px 10px; display: flex; flex-direction: column; gap: 4px;"><h2 style="margin: 0; font-size: 17px; font-weight: 700;">공고에서 많이 언급한 역량</h2><span style="font-size: 12px; color: {SUB};">누르면 공고 원문이 보여요</span></div>
      <sc-for list="{{{{ skills }}}}" as="s" hint-placeholder-count="7">
        <div style="display: flex; flex-direction: column; border-top: 1px solid {LINE};">
          <button type="button" onClick="{{{{ s.toggle }}}}" aria-expanded="{{{{ s.open }}}}" style="display: grid; grid-template-columns: 1fr 64px 40px 14px; gap: 10px; align-items: center; padding: 14px 18px; border: none; background: none; font-family: inherit; font-size: 15px; color: {INK}; text-align: left; cursor: pointer;">
            <span style="{{{{ s.labelStyle }}}}">{{{{ s.name }}}}</span>
            <span style="display: block; height: 6px; background: {FILL}; border-radius: 999px;"><span style="{{{{ s.barStyle }}}}"></span></span>
            <span style="text-align: right; font-weight: 600;">{{{{ s.pct }}}}</span>
            <span style="text-align: right; color: {MUTE};">{{{{ s.chevron }}}}</span>
          </button>
          <sc-if value="{{{{ s.open }}}}" hint-placeholder-val="{{{{ false }}}}">
            <div style="display: flex; flex-direction: column; gap: 10px; margin: 0 14px 16px; padding: 16px; background: #F4F9FF; border-radius: 14px;">
              <span style="font-size: 12px; font-weight: 600; color: {BLUE_D};">공고에서 이렇게 말해요</span>
              <sc-for list="{{{{ s.quotes }}}}" as="q" hint-placeholder-count="2"><span style="font-size: 14px; line-height: 1.5; padding: 10px 12px; background: #FFFFFF; border-radius: 10px;">"{{{{ q }}}}"</span></sc-for>
              <span style="font-size: 12px; font-weight: 600; color: {BLUE_D}; margin-top: 4px;">{{{{ s.statTitle }}}}</span>
              <div style="display: flex; gap: 6px; flex-wrap: wrap;"><sc-for list="{{{{ s.stats }}}}" as="t" hint-placeholder-count="3"><span style="padding: 5px 10px; background: #FFFFFF; border-radius: 999px; font-size: 12px;">{{{{ t }}}}</span></sc-for></div>
              <span style="font-size: 13px; line-height: 1.6; color: #333D4B;">{{{{ s.note }}}}</span>
              <a href="m-S1-list.dc.html" style="font-size: 13px; font-weight: 600; text-decoration: none;">이 역량을 언급한 공고 {{{{ s.count }}}}건 보기 ›</a>
              <a href="m-S4-next.dc.html" style="font-size: 13px; font-weight: 600; text-decoration: none;">채울 수 있는 SeSAC 과정 ›</a>
            </div>
          </sc-if>
        </div>
      </sc-for>
    </section>
    </sc-if>
    <sc-if value="{{{{ showCert }}}}" hint-placeholder-val="{{{{ false }}}}">
    <section style="display: flex; flex-direction: column; {CARD} overflow: hidden;">
      <div style="padding: 18px 18px 10px; display: flex; flex-direction: column; gap: 4px;"><h2 style="margin: 0; font-size: 17px; font-weight: 700;">자격증은 거의 보지 않아요</h2><span style="font-size: 12px; color: {SUB};">누르면 어떤 시험인지, 공고는 대신 무엇을 보는지 보여요</span></div>
      <sc-for list="{{{{ certs }}}}" as="c" hint-placeholder-count="4">
        <div style="display: flex; flex-direction: column; border-top: 1px solid {LINE};">
          <button type="button" onClick="{{{{ c.toggle }}}}" aria-expanded="{{{{ c.open }}}}" style="display: grid; grid-template-columns: 1fr auto 14px; gap: 10px; align-items: center; padding: 14px 18px; border: none; background: none; font-family: inherit; font-size: 15px; color: {INK}; text-align: left; cursor: pointer;">
            <span style="{{{{ c.labelStyle }}}}">{{{{ c.name }}}}</span><span style="padding: 3px 8px; border-radius: 999px; background: {FILL}; font-size: 12px; color: {SUB};">언급 {{{{ c.mentions }}}}</span><span style="color: {MUTE};">{{{{ c.chevron }}}}</span>
          </button>
          <sc-if value="{{{{ c.open }}}}" hint-placeholder-val="{{{{ false }}}}">
            <div style="display: flex; flex-direction: column; gap: 8px; margin: 0 14px 16px; padding: 16px; background: #F4F9FF; border-radius: 14px; font-size: 14px; line-height: 1.5;">
              <span><b style="font-weight: 600; color: {SUB};">어떤 시험</b> · {{{{ c.what }}}}</span>
              <span><b style="font-weight: 600; color: {SUB};">주관</b> · {{{{ c.org }}}}</span>
              <span style="color: {BLUE_D}; font-weight: 600;">공고는 대신 · {{{{ c.instead }}}}</span>
            </div>
          </sc-if>
        </div>
      </sc-for>
    </section>
    </sc-if>
    <sc-if value="{{{{ showExtra }}}}" hint-placeholder-val="{{{{ false }}}}">
    <section style="display: flex; flex-direction: column; gap: 14px; padding: 18px; {CARD}">
      <h2 style="margin: 0; font-size: 17px; font-weight: 700;">공고에서 언급한 경험</h2>
      {extra_html}
      <span style="padding: 12px 14px; border-radius: 12px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; line-height: 1.55;">대외활동 이름보다 직접 채널을 운영해 본 경험을 더 많이 적어요</span>
    </section>
    </sc-if>
    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD}">
      <h2 style="margin: 0; font-size: 17px; font-weight: 700;">이 트렌드, 내 경험과 비교해 볼까요?</h2>
      <p style="margin: 0; font-size: 14px; line-height: 1.6; color: {SUB};">공고 하나를 고르면 이 역량들이 내 경험에 있는지 근거 문장으로 보여드려요</p>
      {btn('m-S1-list.dc.html', '이 직무 공고 보기')}
    </section>
'''
boards['m-P1-trend.dc.html'] = ('MP1 트렌드 상세 (모바일)', topbar_logo(), p1, 'trend', p1_script)

# ===== m-S2 =====
reqs = [('자격요건', '숏폼 콘텐츠를 즐겨보며, 최신 콘텐츠 트렌드와 밈에 관심'), ('자격요건', '콘텐츠 성과를 수치로 분석하고 다음 액션을 제안하는 데이터 감각'),
        ('우대', '개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸 숏폼 발행 경험'), ('우대', '뷰티 산업에 대한 애정, 셀링 포인트를 캐치하는 센스'),
        ('우대', '마케팅 학회, 공모전 수상, 인턴십 등 실무 베이스 마케팅 경험'), ('우대', 'Premiere Pro, Photoshop으로 기획안을 영상으로 직접 구현')]
req_html = ''.join(f'<li style="display: flex; gap: 8px; font-size: 14px; line-height: 1.5;"><span style="flex-shrink: 0; padding: 1px 7px; border-radius: 6px; background: {BLUE_BG if k == "자격요건" else FILL}; color: {BLUE_D if k == "자격요건" else SUB}; font-size: 11px; font-weight: 600; height: fit-content; margin-top: 2px;">{k}</span><span>{t}</span></li>' for k, t in reqs)
INP = f'height: 48px; box-sizing: border-box; padding: 0 14px; font-size: 16px; border: none; border-radius: 12px; font-family: inherit; background: {FILL}; color: {INK}; width: 100%;'
TA = f'height: 120px; box-sizing: border-box; padding: 14px; font-size: 16px; line-height: 1.6; border: none; border-radius: 12px; font-family: inherit; resize: none; background: {FILL}; color: {INK}; width: 100%;'
ADD = '<span style="padding: 6px 11px; border-radius: 999px; border: 1.5px dashed #D1D6DB; font-size: 13px; color: #6B7684;">+ 추가</span>'
LBL = f'font-size: 13px; color: {SUB};'
s2 = f'''    <section style="display: flex; flex-direction: column; gap: 14px; padding: 20px; {CARD}">
      <div style="display: flex; align-items: center; gap: 12px;">{mark('olive', 40)}<span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 13px; font-weight: 600;">올리브인터내셔널</span><span style="font-size: 11px; color: {MUTE};">뷰티 브랜드 성분에디터 · 마케팅본부</span></span></div>
      <h1 style="margin: 0; font-size: 19px; font-weight: 700; line-height: 1.4;">[마케팅본부] 성분에디터 콘텐츠 마케팅 인턴 (채용연계형)</h1>
      <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; padding: 12px 14px; background: #F9FAFB; border-radius: 12px; font-size: 13px;"><span><span style="color: {MUTE};">고용</span> 인턴 (채용연계)</span><span><span style="color: {MUTE};">경력</span> 무관</span><span><span style="color: {MUTE};">직무</span> 콘텐츠 마케터</span><span><span style="color: {MUTE};">마감</span> 채용 시 마감</span></div>
      <div style="display: flex; flex-direction: column; gap: 10px;"><span style="font-size: 14px; font-weight: 700;">공고가 원하는 것 6</span><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;">{req_html}</ul></div>
      <a href="{POSTING}" {EXT} style="font-size: 13px; color: {BLUE}; text-decoration: none;">원문 공고 전체 보기 ↗</a>
    </section>
    <section style="display: flex; flex-direction: column; gap: 16px; padding: 20px; {CARD}">
      {h2('내 경험', f'<button type="button" onClick="{{{{ toggle }}}}" style="height: 34px; padding: 0 12px; border: none; border-radius: 999px; background: {FILL}; font-size: 13px; font-family: inherit; color: {INK}; cursor: pointer;">{{{{ fillLabel }}}}</button>')}
      <sc-if value="{{{{ empty }}}}" hint-placeholder-val="{{{{ true }}}}">
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-major0" style="{LBL}">전공</label><input id="m-major0" type="text" placeholder="예: 미디어커뮤니케이션학과" style="{INP}"></div>
        <div style="display: flex; gap: 24px;"><div style="display: flex; flex-direction: column; gap: 6px;"><span style="{LBL}">자격증</span>{ADD}</div><div style="display: flex; flex-direction: column; gap: 6px;"><span style="{LBL}">어학</span>{ADD}</div></div>
        <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-act0" style="{LBL}">활동과 프로젝트 · 편하게 적어도 돼요</label><textarea id="m-act0" placeholder="예: 학생회 홍보부 인스타그램 운영 1년" style="{TA}"></textarea></div>
      </div>
      </sc-if>
      <sc-if value="{{{{ filled }}}}" hint-placeholder-val="{{{{ false }}}}">
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-major" style="{LBL}">전공</label><input id="m-major" type="text" value="미디어커뮤니케이션학과" style="{INP}"></div>
        <div style="display: flex; gap: 24px;"><div style="display: flex; flex-direction: column; gap: 6px;"><span style="{LBL}">자격증</span><div style="display: flex; gap: 6px;">{chip('컴활 2급')}{ADD}</div></div><div style="display: flex; flex-direction: column; gap: 6px;"><span style="{LBL}">어학</span><div style="display: flex; gap: 6px;">{chip('OPIc IM2')}</div></div></div>
        <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-act" style="{LBL}">활동과 프로젝트 · 편하게 적어도 돼요</label><textarea id="m-act" style="{TA}">학생회 홍보부 인스타그램 운영 1년
카드뉴스 주 1회 제작 (캔바)
팔로워 300명에서 1,200명</textarea></div>
      </div>
      </sc-if>
      <div style="display: flex; flex-direction: column; gap: 6px;"><span style="{LBL}">이력서, 포트폴리오 PDF · 선택</span><label for="m-pdf" style="height: 48px; display: flex; align-items: center; gap: 10px; padding: 0 14px; border-radius: 12px; background: {FILL}; cursor: pointer;"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4"/><path d="M7 9l5-5 5 5"/><path d="M5 20h14"/></svg><span style="font-size: 15px;">PDF 올리기</span><span style="margin-left: auto; font-size: 12px; color: {MUTE};">10MB까지</span></label><input id="m-pdf" type="file" accept="application/pdf" style="display: none;"></div>
      <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-link" style="{LBL}">링크 · 선택</label><input id="m-link" type="url" placeholder="노션, 인스타그램, 블로그 주소" style="{INP} font-size: 15px;"></div>
      <sc-if value="{{{{ filled }}}}" hint-placeholder-val="{{{{ false }}}}">{btn('m-S3-compare.dc.html', '공고와 비교하기')}</sc-if>
      <sc-if value="{{{{ empty }}}}" hint-placeholder-val="{{{{ true }}}}"><button type="button" onClick="{{{{ toggle }}}}" style="height: 52px; border: none; border-radius: 14px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 16px; font-weight: 600; font-family: inherit; cursor: pointer;">예시로 채우고 비교해 보기</button></sc-if>
      <span style="font-size: 12px; color: {MUTE}; text-align: center;">시연에서는 예시 경험으로 비교해요 · 입력한 내용은 저장하지 않아요</span>
    </section>
'''
s2_script = ("  constructor(props) { super(props); this.state = { filled: false }; }\n"
             "  renderVals() {\n    const filled = this.state.filled;\n"
             "    return { filled, empty: !filled, fillLabel: filled ? '지우기' : '예시로 채우기', toggle: () => this.setState({ filled: !filled }) };\n  }")
boards['m-S2-input.dc.html'] = ('M2 공고와 내 경험 입력 (모바일)', topbar_flow('m-S1-list.dc.html', '경험 입력', 1), s2, 'find', s2_script)

# ===== m-S3 =====
seg = lambda c: f'<span style="flex: 1 1 0; height: 8px; border-radius: 999px; background: {c};"></span>'


def match(badge, color, bg, kind, need, mine, note=''):
    n = f'<span style="font-size: 12px; line-height: 1.5; color: {color};">{note}</span>' if note else ''
    return (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px 0; border-top: 1px solid {LINE};"><div style="display: flex; align-items: center; gap: 6px;"><span style="padding: 3px 9px; border-radius: 999px; background: {bg}; color: {color}; font-size: 12px; font-weight: 700;">{badge}</span><span style="font-size: 11px; color: {MUTE};">{kind}</span></div>'
            f'<span style="font-size: 14px; line-height: 1.5;">공고 "{need}"</span><div style="display: flex; flex-direction: column; gap: 3px; padding: 10px 12px; border-radius: 10px; background: {bg};"><span style="font-size: 11px; font-weight: 600; color: {color};">내 경험</span><span style="font-size: 13px; line-height: 1.5;">{mine}</span>{n}</div></div>')


def gap(need, why, href, action):
    return (f'<div style="display: flex; align-items: center; gap: 10px; padding: 14px 0; border-top: 1px solid {LINE};"><span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 14px; line-height: 1.45;">{need}</span><span style="font-size: 11px; color: {MUTE};">{why}</span></span>'
            f'<a href="{href}" style="flex-shrink: 0; padding: 7px 10px; border-radius: 9px; background: {FILL}; color: {INK}; font-size: 12px; font-weight: 600; text-decoration: none;">{action} ›</a></div>')


CICON = {'edu': '<path d="M3 9l9-5 9 5-9 5z"/><path d="M7 11v5c0 1 2 3 5 3s5-2 5-3v-5"/>', 'cert': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
         'act': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9l5 3-5 3z"/>', 'apply': '<path d="M4 12l16-8-6 16-3-6z"/>'}


def choice(href, ic, title, sub, badge=''):
    b = f'<span style="padding: 2px 7px; border-radius: 6px; background: {BLUE}; color: #FFFFFF; font-size: 10px; font-weight: 700;">{badge}</span>' if badge else ''
    return (f'<a href="{href}" style="display: flex; align-items: center; gap: 14px; padding: 16px; {CARD} color: {INK}; text-decoration: none;"><span style="width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; background: {BLUE_BG}; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{CICON[ic]}</svg></span>'
            f'<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="display: flex; align-items: center; gap: 6px; font-size: 16px; font-weight: 700;">{title}{b}</span><span style="font-size: 12px; color: {SUB};">{sub}</span></span><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B0B8C1" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></a>')


s3 = f'''    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD}">
      <span style="font-size: 12px; color: {SUB};">올리브인터내셔널 · 성분에디터 콘텐츠 마케팅 인턴</span>
      <h1 style="margin: 0; font-size: 22px; font-weight: 700; line-height: 1.35; letter-spacing: -0.02em;">공고 요구 6개 중 <span style="color: {BLUE};">2개</span>가<br>내 경험과 이어져요</h1>
      <div role="img" aria-label="맞음 1, 일부 1, 찾지 못함 4" style="display: flex; gap: 4px; margin-top: 4px;">{seg(BLUE)}{seg('#FFB331')}{seg('#E5E8EB')}{seg('#E5E8EB')}{seg('#E5E8EB')}{seg('#E5E8EB')}</div>
      <div style="display: flex; gap: 14px; font-size: 12px; color: #4E5968;"><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #3182F6;"></span>맞음 <b style="color: #191F28;">1</b></span><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #FFB331;"></span>일부 <b style="color: #191F28;">1</b></span><span style="display: flex; align-items: center; gap: 5px;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #D1D6DB;"></span>찾지 못함 <b style="color: #191F28;">4</b></span></div>
      <span style="font-size: 11px; color: {MUTE};">공고 문장과 입력 문장을 비교한 결과예요. 합격 여부 예측이 아니에요</span>
    </section>
    <section style="display: flex; flex-direction: column; padding: 18px 18px 6px; {CARD}">
      <h2 style="margin: 0 0 8px; font-size: 17px; font-weight: 700;">이어지는 경험 <span style="color: {BLUE};">2</span></h2>
      {match('맞음', BLUE_D, BLUE_BG, '우대 · SNS 채널 운영', '개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸', '학생회 홍보부 인스타그램 운영 1년, 팔로워 300명에서 1,200명')}
      {match('일부', OR, OR_BG, '자격요건 · 성과 분석', '콘텐츠의 성과를 객관적인 수치로 분석하고, 다음 액션을 제안', '팔로워 300명에서 1,200명', '무엇을 보고 무엇을 바꿨는지 한 문장 더하면 맞음이 돼요')}
    </section>
    <section style="display: flex; flex-direction: column; padding: 18px 18px 14px; {CARD}">
      <h2 style="margin: 0 0 8px; font-size: 17px; font-weight: 700;">아직 비어 있는 것 <span style="color: {MUTE};">4</span></h2>
      {gap('숏폼 발행 경험', '우대 · 입력엔 카드뉴스만 있어요', 'm-S4-activity.dc.html', '프로젝트')}
      {gap('Premiere Pro, Photoshop으로 직접 구현', '우대 · 캔바만 찾았어요', 'm-S4-next.dc.html', 'SeSAC')}
      {gap('최신 콘텐츠 트렌드와 밈에 관심', '자격요건 · 입력에서 찾지 못했어요', 'm-P1-trend.dc.html', '트렌드')}
      {gap('학회, 공모전, 인턴십 등 실무 경험', '우대 · 입력에서 찾지 못했어요', 'm-S4-activity.dc.html', '공모전')}
      <a href="m-S2-input.dc.html" style="margin-top: 6px; font-size: 12px; color: {SUB}; text-decoration: none;">빠뜨린 경험이 있나요? <span style="color: {BLUE};">입력 고치기 ›</span></a>
    </section>
    <div style="display: flex; flex-direction: column; gap: 4px; margin-top: 12px; padding: 0 4px;"><h2 style="margin: 0; font-size: 19px; font-weight: 700;">어느 부분을 먼저 채울까요?</h2><span style="font-size: 12px; color: {SUB};">고르는 건 나. 일로는 근거와 선택지만 보여줘요</span></div>
    {choice('m-S4-next.dc.html', 'edu', '교육으로 배우기', 'SeSAC 과정 2개 모집 중', '빈 칸 2개')}
    {choice('m-S4-cert.dc.html', 'cert', '자격증, 어학', '이 직무 공고 언급 3%')}
    {choice('m-S4-activity.dc.html', 'act', '대외활동, 프로젝트', '숏폼 직접 발행해 보기')}
    {choice('m-S4-apply.dc.html', 'apply', '지원 준비', '지금 경험으로 지원하기')}
'''
boards['m-S3-compare.dc.html'] = ('M3 비교 결과 (모바일)', topbar_flow('m-S2-input.dc.html', '비교 결과', 2), s3, 'find')

# ===== m-S4 family =====
S4TABS = [('m-S4-next.dc.html', '교육으로 배우기'), ('m-S4-cert.dc.html', '자격증, 어학'), ('m-S4-activity.dc.html', '대외활동, 프로젝트'), ('m-S4-apply.dc.html', '지원 준비')]


def s4tabs(active):
    out = ''
    for h, l in S4TABS:
        if h == active:
            out += f'<span aria-current="page" style="flex-shrink: 0; padding: 8px 13px; border-radius: 999px; background: {INK}; color: #FFFFFF; font-size: 13px; font-weight: 600;">{l}</span>'
        else:
            out += f'<a href="{h}" style="flex-shrink: 0; padding: 8px 13px; border-radius: 999px; background: #FFFFFF; color: {INK}; font-size: 13px; text-decoration: none;">{l}</a>'
    return f'<div class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -16px; padding: 0 16px;">{out}</div>'


def s4head(title):
    return f'    <h1 style="margin: 4px 4px 0; font-size: 22px; font-weight: 700; line-height: 1.35; letter-spacing: -0.02em;">{title}</h1>\n'


TAG = f'padding: 4px 9px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px; font-weight: 600;'
QUOTE = f'margin: 0; padding: 12px 14px; background: {FILL}; border-radius: 12px; font-size: 13px; line-height: 1.55; color: #333D4B;'
SRC = f'    <span style="padding: 4px 4px 0; font-size: 11px; line-height: 1.5; color: {MUTE};">출처: SNS 콘텐츠 마케팅 공고 104건 (링커리어 64 + 2026 채용 게시판 40, 10/27 기준)</span>\n'

info = lambda k, v: f'<div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid {LINE}; font-size: 14px;"><span style="color: {SUB};">{k}</span><span style="font-weight: 600;">{v}</span></div>'
s4 = s4head('숏폼, 영상 제작을 채울 수 있는 SeSAC 과정') + f'''    {s4tabs('m-S4-next.dc.html')}
    <section style="display: flex; flex-direction: column; gap: 14px; padding: 16px; {CARD}">
      <img src="{THUMB1}" alt="(강북5기) AI 활용 SNS 마케터 양성 과정 썸네일" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 14px; display: block;">
      <div style="display: flex; gap: 6px; flex-wrap: wrap;"><span style="{TAG}">모집중 · 11.08 마감</span>{chip('강북')}{chip('디지털마케팅')}</div>
      <h2 style="margin: 0; font-size: 20px; font-weight: 700; line-height: 1.35;">(강북5기) AI 활용 SNS 마케터 양성 과정</h2>
      <div style="display: flex; flex-direction: column;">{info('교육 기간', '2026.11.25 ~ 2027.03.17')}{info('교육 시간', '420시간')}{info('비용', '무료 (예치금 반환)')}{info('수료 기준', '출석률 80% 이상')}</div>
      <span style="font-size: 12px; color: {SUB};"># AI # SNS마케팅 # 콘텐츠마케팅 # 퍼포먼스마케팅 # 마케팅자동화</span>
      <p style="margin: 0; padding: 12px 14px; background: {OR_BG}; border-radius: 12px; font-size: 13px; line-height: 1.55; color: {OR};">과정 키워드에 "숏폼, 영상 편집"은 없어요. 커리큘럼에 영상 실습이 있는지 SeSAC 페이지에서 확인해 보세요</p>
      {btn(SESAC + '1421', 'SeSAC에서 과정 보기 ↗', True, True)}
      {btn('m-S5-path.dc.html', '내 경로에 저장', False)}
    </section>
    <a href="{SESAC}1235" {EXT} style="display: flex; align-items: center; gap: 14px; padding: 14px; {CARD} color: {INK}; text-decoration: none;"><img src="{THUMB2}" alt="전Z전능 브랜드 마케팅 실전 과정 썸네일" style="width: 88px; height: 66px; flex-shrink: 0; object-fit: cover; border-radius: 10px; display: block;"><span style="display: flex; flex-direction: column; gap: 3px; min-width: 0;"><span style="font-size: 11px; color: {SUB};">모집중 · 11.10 마감 · 금천 · 360시간</span><span style="font-size: 14px; font-weight: 600; line-height: 1.4;">⭐K-브랜드 마케팅 실무 프로젝트⭐전Z전능 브랜드 마케팅 실전 과정</span></span></a>
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 18px; background: #FFFFFF; border: 1.5px dashed #D1D6DB; border-radius: 20px;">
      <span style="font-size: 12px; color: {SUB};">숏폼 전문 과정</span>
      <span style="font-size: 16px; font-weight: 700;">지금 모집 중인 기수가 없어요</span>
      <span style="font-size: 13px; line-height: 1.55; color: #333D4B;">지난 기수: (강동7기/AI융합) 생성형 AI 기반 숏폼 영상콘텐츠 제작 실무과정 · 2026.07.03 ~ 10.02 종료</span>
      <a href="{SESAC}1266" {EXT} style="font-size: 13px; font-weight: 600; text-decoration: none;">지난 기수 과정 보기 ↗</a>
    </section>
    <span style="padding: 4px 4px 0; font-size: 11px; color: {MUTE};">출처: SeSAC 과정 정보 (팀 수집 210개, 2026.10.27 기준)</span>
'''
boards['m-S4-next.dc.html'] = ('M4 다음 행동 · 교육 (모바일)', topbar_flow('m-S3-compare.dc.html', '다음 행동', 3), s4, 'find')

row = lambda n, r: f'<div style="display: flex; justify-content: space-between; padding: 11px 0; border-bottom: 1px solid {LINE}; font-size: 14px;"><span>{n}</span><span style="color: {MUTE};">{r}</span></div>'
cert = s4head('자격증보다 툴로 만든 결과물을 봐요') + f'''    {s4tabs('m-S4-cert.dc.html')}
    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: center;"><span style="{TAG}">자격증</span><span style="font-size: 12px; color: {SUB};">공고 104건 기준</span></div>
      <h2 style="margin: 0; font-size: 18px; font-weight: 700; line-height: 1.4;">자격증을 적은 공고는 3%(3건)뿐이에요</h2>
      <div>{row('GTQ (그래픽기술자격)', '0건')}{row('컴퓨터활용능력', '0건 · 내 자격증')}{row('GAIQ (구글 애널리틱스)', '0건')}{row('검색광고마케터', '0건')}</div>
      <p style="{QUOTE}">대신 공고는 툴 이름을 직접 적어요. 이 툴로 만든 결과물을 보여주는 쪽이 공고 문장과 이어져요</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap;">{chip('프리미어 30건')}{chip('포토샵 28건')}{chip('피그마 19건')}{chip('캡컷 10건')}</div>
    </section>
    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: center;"><span style="{TAG}">어학</span><span style="font-size: 12px; color: {SUB};">내 어학: OPIc IM2</span></div>
      <h2 style="margin: 0; font-size: 17px; font-weight: 700;">외국어를 적은 공고는 14%(15건)예요</h2>
      <p style="{QUOTE}">"영어로 커뮤니케이션이 원활한 분"<br>"중급 이상의 일본어 활용 능력 (SNS, 밈, 트렌드를 이해할 수 있는 수준)"</p>
      <span style="font-size: 12px; line-height: 1.55; color: {SUB};">필요한 공고는 언어와 수준을 직접 적어요. 지원할 공고 원문에서 어학 문장이 있는지만 확인하면 돼요</span>
    </section>
    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; background: {BLUE_BG}; border-radius: 20px;">
      <span style="font-size: 12px; font-weight: 600; color: {BLUE_D};">일로가 보는 다음 한 걸음</span>
      <span style="font-size: 17px; font-weight: 700;">자격증 공부 대신 프리미어로 숏폼 1개</span>
      {btn('m-S4-next.dc.html', '툴 실습 과정 보기')}
      {btn('m-S5-path.dc.html', '내 경로에 저장', False)}
    </section>
''' + SRC
boards['m-S4-cert.dc.html'] = ('M4b 자격증, 어학 (모바일)', topbar_flow('m-S3-compare.dc.html', '다음 행동', 3), cert, 'find')

step = lambda n, t, d: f'<div style="display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid {LINE};"><span style="width: 26px; height: 26px; flex-shrink: 0; border-radius: 50%; background: {BLUE_BG}; color: {BLUE_D}; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">{n}</span><span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 14px; font-weight: 600;">{t}</span><span style="font-size: 12px; color: {SUB};">{d}</span></span></div>'
stat = lambda l, v, s: f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 12px; background: #FFFFFF; border-radius: 14px;"><span style="font-size: 11px; color: {SUB};">{l}</span><span style="font-size: 20px; font-weight: 700;">{v}</span><span style="font-size: 11px; color: {MUTE};">{s}</span></div>'
act = s4head('숏폼을 직접 발행해 본 경험을 만들어요') + f'''    {s4tabs('m-S4-activity.dc.html')}
    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">{stat('개인 채널 운영', '15%', '16건')}{stat('공모전, 수상', '9%', '9건')}{stat('서포터즈', '2%', '2건')}</div>
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; {CARD}">
      <span style="align-self: flex-start; {TAG}">일로 제안 · 4주 프로젝트</span>
      <h2 style="margin: 0; font-size: 18px; font-weight: 700; line-height: 1.4;">내 채널에 숏폼 6개 올리고 숫자로 정리하기</h2>
      <div>{step(1, '1주차 · 레퍼런스 10개 모으기', '지원할 브랜드 릴스, 쇼츠의 훅과 길이 기록')}{step(2, '2주차 · 숏폼 3개 발행', '캡컷이나 프리미어로 편집해 올리기')}{step(3, '3주차 · 훅 바꿔서 3개 더', '조회수가 낮은 영상의 첫 3초만 바꾸기')}{step(4, '4주차 · 결과 한 장으로', '조회수, 저장 수 비교를 링크로 정리')}</div>
    </section>
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; {CARD}">
      <span style="font-size: 12px; color: {SUB};">공고가 실제로 적은 문장</span>
      <p style="{QUOTE}">"콘텐츠 기획 및 제작 경험을 보유하신 분 (개인 SNS 채널도 무관)"</p>
      <p style="{QUOTE}">"팀 프로젝트, 공모전, SNS 개인 콘텐츠 등 어떤 형태든 상관없어요"</p>
      <span style="font-size: 12px; color: {SUB};">결과 링크는 경험 입력의 "링크" 칸에 넣으면 다음 비교에 반영돼요</span>
      {btn('m-S5-path.dc.html', '내 경로에 추가')}
      {btn('https://linkareer.com/list/contest', '공모전 찾아보기 ↗', False, True)}
    </section>
''' + SRC
boards['m-S4-activity.dc.html'] = ('M4c 대외활동, 프로젝트 (모바일)', topbar_flow('m-S3-compare.dc.html', '다음 행동', 3), act, 'find')

verdict = lambda v, c, bg, need, mine: f'<div style="display: flex; gap: 10px; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid {LINE};"><span style="flex-shrink: 0; padding: 3px 9px; border-radius: 999px; background: {bg}; color: {c}; font-size: 11px; font-weight: 700;">{v}</span><span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 14px;">{need}</span><span style="font-size: 12px; color: {SUB};">{mine}</span></span></div>'
check = lambda t, d: f'<div style="display: flex; gap: 10px; align-items: flex-start;"><span style="width: 18px; height: 18px; flex-shrink: 0; border-radius: 6px; background: {FILL};"></span><span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 14px;">{t}</span><span style="font-size: 11px; color: {MUTE};">{d}</span></span></div>'
apply = s4head('지금 경험으로 지원해 볼 수 있어요') + f'''    {s4tabs('m-S4-apply.dc.html')}
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; {CARD}">
      <span style="font-size: 12px; color: {SUB};">올리브인터내셔널 · 성분에디터 콘텐츠 마케팅 인턴</span>
      <h2 style="margin: 0; font-size: 18px; font-weight: 700;">이어지는 2개를 앞에 두고 써요</h2>
      <div>{verdict('맞음', BLUE_D, BLUE_BG, '채널을 직접 운영하며 고객 반응을 이끌어낸 경험', '학생회 인스타그램 1년, 팔로워 300명에서 1,200명')}{verdict('일부', OR, OR_BG, '성과를 수치로 분석하고 다음 액션 제안', '무엇을 보고 무엇을 바꿨는지 한 문장 더하기')}</div>
    </section>
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; {CARD}">
      <span style="align-self: flex-start; {TAG}">문장 다듬기</span>
      <div style="display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; background: {FILL}; border-radius: 12px;"><span style="font-size: 11px; color: {SUB};">지금 입력</span><span style="font-size: 14px; line-height: 1.55;">학생회 홍보부 인스타그램 운영 1년. 카드뉴스 주 1회 제작 (캔바). 팔로워 300명에서 1,200명</span></div>
      <div style="display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; background: {BLUE_BG}; border-radius: 12px;"><span style="font-size: 11px; color: {BLUE_D};">공고 문장에 맞춰서</span><span style="font-size: 14px; line-height: 1.55;">학생회 인스타그램을 1년간 직접 운영하며 카드뉴스를 매주 발행해 팔로워를 300명에서 1,200명으로 늘렸습니다</span></div>
      <span style="font-size: 11px; color: {MUTE};">입력한 사실만 순서를 바꿨어요. 없는 숫자나 경험은 넣지 않아요</span>
    </section>
    <section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD}">
      <h2 style="margin: 0; font-size: 17px; font-weight: 700;">지원 전에 확인</h2>
      {check('인스타그램 계정 링크 첨부', '공고: "SNS 운영 경험이 있는 경우 URL 기재" 같은 문장이 많아요')}
      {check('숏폼, 툴 경험은 쓰지 않기', '없는 경험은 면접에서 드러나요')}
      {check('원문 공고에서 마감일 확인', '수집 데이터에는 마감일이 없을 수 있어요')}
      {btn(POSTING, '원문 공고에서 지원하기 ↗', True, True)}
      {btn('m-S5-path.dc.html', '내 경로에 저장', False)}
    </section>
''' + SRC
boards['m-S4-apply.dc.html'] = ('M4d 지원 준비 (모바일)', topbar_flow('m-S3-compare.dc.html', '다음 행동', 3), apply, 'find')

# ===== m-S5 =====
tl = lambda n, label, title, sub, on=True: (f'<div style="display: flex; gap: 14px; padding: 14px 0; border-bottom: 1px solid {LINE};"><span style="width: 28px; height: 28px; flex-shrink: 0; border-radius: 50%; background: {BLUE_BG if on else FILL}; color: {BLUE_D if on else MUTE}; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700;">{n}</span>'
                                            f'<span style="display: flex; flex-direction: column; gap: 3px; min-width: 0;"><span style="font-size: 11px; color: {MUTE};">{label}</span><span style="font-size: 15px; font-weight: 600; line-height: 1.4;">{title}</span><span style="font-size: 12px; line-height: 1.5; color: {SUB};">{sub}</span></span></div>')
s5 = f'''    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">내 취업 경로</h1><span style="padding: 6px 11px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px; font-weight: 600;">저장했어요</span></div>
    <section style="display: flex; flex-direction: column; padding: 6px 18px 10px; {CARD}">
      {tl(1, '목표 공고', '[올리브인터내셔널] 성분에디터 콘텐츠 마케팅 인턴', f'채용연계형 인턴 · <a href="{POSTING}" {EXT}>원문 공고</a>')}
      {tl(2, '비교 결과', '공고 요구 6개 중 맞음 1개, 일부 1개', '찾지 못함: 숏폼 발행, 영상 툴, 트렌드, 실무 경험 · <a href="m-S3-compare.dc.html">다시 보기</a>')}
      {tl(3, '다음 행동 (내가 고름)', 'SeSAC (강북5기) AI 활용 SNS 마케터 양성 과정', f'11/25 개강 · 모집 마감 11/8 · <a href="{SESAC}1421" {EXT}>과정 페이지</a>')}
      {tl('', '그다음', '과정을 마치면 같은 공고와 다시 비교해 보세요', '', False)}
    </section>
    {btn('m-S1-list.dc.html', '다른 공고와도 비교하기', False)}
    <section style="display: flex; flex-direction: column; gap: 10px; padding: 20px; background: {BLUE_BG}; border-radius: 20px;">
      <span style="font-size: 17px; font-weight: 700;">취업하셨나요?</span>
      <span style="font-size: 13px; line-height: 1.6; color: #333D4B;">어떤 경험과 과정이 도움이 됐는지 남겨 주시면, 같은 공고를 보는 다음 청년의 추천 근거가 돼요</span>
      {btn('m-S6-story.dc.html', '취업 수기 남기기')}
    </section>
'''
boards['m-S5-path.dc.html'] = ('M5 내 취업 경로 (모바일)', topbar_logo(), s5, 'path')

# ===== m-S6 =====
SEL = f'height: 48px; padding: 0 12px; font-size: 15px; border: none; border-radius: 12px; font-family: inherit; background: #FFFFFF; color: {INK}; width: 100%;'
pill = lambda t, on: f'<span style="padding: 8px 13px; border-radius: 999px; background: {BLUE_BG if on else "#FFFFFF"}; color: {BLUE_D if on else INK}; font-size: 13px;">{t}</span>'
s6 = f'''    <div style="display: flex; flex-direction: column; gap: 4px; padding: 8px 4px 4px;"><a href="m-S5-path.dc.html" style="font-size: 13px; color: {SUB}; text-decoration: none;">‹ 내 경로</a><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">취업 수기 남기기</h1><span style="font-size: 13px; color: {SUB};">내 경험이 다음 청년의 기회가 돼요. 이름과 회사명은 공개되지 않아요</span></div>
    <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-job" style="{LBL}">합격한 직무</label><select id="m-job" style="{SEL}"><option>SNS 콘텐츠 마케터</option></select></div>
    <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-course" style="{LBL}">도움이 된 과정</label><select id="m-course" style="{SEL}"><option>(강북5기) AI 활용 SNS 마케터 양성 과정</option></select></div>
    <div style="display: flex; flex-direction: column; gap: 8px;"><span style="{LBL}">도움이 된 경험 (여러 개 선택)</span><div style="display: flex; gap: 6px; flex-wrap: wrap;">{pill('학생회 인스타 운영', True)}{pill('숏폼 과정 포트폴리오', True)}{pill('자격증', False)}{pill('어학', False)}{pill('공모전', False)}</div></div>
    <div style="display: flex; flex-direction: column; gap: 6px;"><label for="m-tip" style="{LBL}">다음 청년에게 한마디 (선택)</label><textarea id="m-tip" style="height: 100px; box-sizing: border-box; padding: 12px 14px; font-size: 15px; line-height: 1.6; border: none; border-radius: 12px; font-family: inherit; resize: none; background: #FFFFFF; width: 100%;">면접에서 팔로워 증가 수치랑 릴스 포트폴리오를 많이 물어봤어요</textarea></div>
    <button type="button" onClick="{{{{ submit }}}}" style="height: 52px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; font-family: inherit; cursor: pointer;">수기 남기기</button>
    <sc-if value="{{{{ sent }}}}" hint-placeholder-val="{{{{ false }}}}"><span role="status" style="padding: 12px 14px; border-radius: 12px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; line-height: 1.5;">고마워요! 수기가 등록됐어요 · 시연용이라 실제로 저장되지는 않아요</span></sc-if>
    <sc-if value="{{{{ notSent }}}}" hint-placeholder-val="{{{{ true }}}}"><span style="font-size: 12px; color: {MUTE}; text-align: center;">남긴 수기는 개인정보를 뺀 통계로만 쓰여요</span></sc-if>
    <section style="display: flex; flex-direction: column; gap: 10px; margin-top: 8px; padding: 18px; background: {FILL}; border-radius: 16px;">
      <span style="font-size: 12px; color: {SUB};">다음 청년의 화면에 이렇게 보여요</span>
      <div style="display: flex; flex-direction: column; gap: 6px; padding: 14px; background: #FFFFFF; border-radius: 12px;"><span style="font-size: 14px; font-weight: 600;">(강북5기) AI 활용 SNS 마케터 양성 과정</span><span style="font-size: 13px; color: #333D4B;">이 과정을 듣고 SNS 콘텐츠 마케터로 취업한 수기 [N]건</span><span style="font-size: 12px; color: {SUB};">"면접에서 릴스 포트폴리오를 많이 물어봤어요"</span></div>
      <span style="align-self: flex-start; padding: 4px 8px; border: 1.5px dashed #D1D6DB; border-radius: 6px; font-size: 11px; color: {SUB};">예시 데이터 · 실제 수기가 쌓이면 표시</span>
    </section>
'''
s6_script = ("  constructor(props) { super(props); this.state = { sent: false }; }\n"
             "  renderVals() { const sent = this.state.sent; return { sent, notSent: !sent, submit: () => this.setState({ sent: true }) }; }")
s6_top = topbar_logo()
boards['m-S6-story.dc.html'] = ('M6 취업 수기 (모바일)', s6_top, s6, 'path', s6_script)

# ---------- write + place on canvas ----------
c = json.load(open(os.path.join(ROOT, 'canvas.json')))
Y = 4400
for i, (fname, spec) in enumerate(boards.items()):
    title, top, body, active = spec[:4]
    script = spec[4] if len(spec) > 4 else '  renderVals() { return {}; }'
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(page(fname, title, top, body, active, script))
    prev = c['boards'].get(fname, {})
    c['boards'][fname] = {'h': prev.get('h', 1600), 'is_interactive': True, 'title': title, 'w': 390, 'x': i * 470, 'y': Y}
    if fname not in c['order']:
        c['order'].append(fname)
c['notes']['mobileTitle'] = {'kind': 'title1', 'maxW': 5200, 'text': '모바일 (390px) · 하단 탭 바: 홈, 직무 찾기, 트렌드, 내 경로', 'w': 240, 'x': 0, 'y': Y - 220}
c['notes']['mobileNote'] = {'color': 'blue', 'text': '데스크톱과 같은 흐름과 데이터. 상단 메뉴 대신 하단 탭 바. 공고 비교 흐름(M2~M4)은 위에 뒤로 가기와 1/3 단계 바를 두고, 탭 바에서는 직무 찾기가 켜진 상태.', 'w': 1280, 'x': 0, 'y': Y - 110}
for k in ('mobileTitle', 'mobileNote'):
    if k not in c['noteOrder']:
        c['noteOrder'].append(k)
json.dump(c, open(os.path.join(ROOT, 'canvas.json'), 'w'), ensure_ascii=False, indent=2)
print('wrote', len(boards), 'mobile boards')
