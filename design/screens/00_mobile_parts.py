"""모바일 공통 부품: 색, 하단 탭 바, 페이지 틀, 칩, 버튼, 회사 로고, 공고 줄, 키워드 순위.
screens/01_base.py보다 먼저 실행된다."""
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


ADD = '<span style="padding: 6px 11px; border-radius: 999px; border: 1.5px dashed #D1D6DB; font-size: 13px; color: #6B7684;">+ 추가</span>'
CICON = {'edu': '<path d="M3 9l9-5 9 5-9 5z"/><path d="M7 11v5c0 1 2 3 5 3s5-2 5-3v-5"/>', 'cert': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
         'act': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9l5 3-5 3z"/>', 'apply': '<path d="M4 12l16-8-6 16-3-6z"/>'}
