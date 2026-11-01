"""v4 structure from the 10/30 team meeting: 홈, 직무 찾기, 교육과정, 마이페이지.
- 공고, AI 비교, 다음 행동이 한 페이지 (S3-compare). 경험은 마이페이지에 한 번 저장.
- 트렌드 상세는 페이지 대신 팝업. 내 경로는 마이페이지 안으로.
Usage: python3 design/scripts/build_screens.py design/canvas design/data/v4_heights.json"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')  # design/data
_src = open(os.path.join(HERE, 'mobile_boards.py'), encoding='utf-8').read()
exec(_src[:_src.index('boards = {}')])  # shared tokens and mobile helpers (tabbar, page, chip, btn, mark, job_row, RANK)
import ast as _ast
_want = {'ADD', 'LBL', 'match', 'gap', 'CICON', 'choice'}
for _n in _ast.parse(_src).body:  # pick the later helpers without running the old board builders
    _names = {_n.name} if isinstance(_n, _ast.FunctionDef) else {t.id for t in getattr(_n, 'targets', []) if isinstance(t, _ast.Name)}
    if _names & _want:
        exec(_ast.get_source_segment(_src, _n))

HEIGHTS = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}

CSS = CSS + '''
a:hover{color:#1B64DA}
button{font-family:inherit}
.illo-rank:hover{background:#F2F4F6}'''

# ---------- mobile tab bar: 4 sections ----------
ICON_OUT['edu'] = '<path d="M2.5 9.5 12 5l9.5 4.5L12 14z"/><path d="M6.5 11.8V16c0 1.2 2.5 3 5.5 3s5.5-1.8 5.5-3v-4.2"/>'
ICON_ON['edu'] = '<path d="M2 9.5 12 4.8l10 4.7-10 4.8z" fill="#6AA6F8"/><path d="M6.5 12.4V16c0 1.4 2.6 3.2 5.5 3.2s5.5-1.8 5.5-3.2v-3.6L12 15z" fill="#6AA6F8"/>'
ICON_OUT['my'], ICON_ON['my'] = ICON_OUT['path'], ICON_ON['path']
TABS = [('home', '홈', 'm-Main.dc.html'), ('find', '직무 찾기', 'm-S1-list.dc.html'),
        ('edu', '교육과정', 'm-E1-edu.dc.html'), ('my', '마이페이지', 'm-S5-path.dc.html')]


def holes(s):
    """@@x@@ -> {{ x }} so the f-strings stay readable."""
    return re.sub(r'@@([^@]+)@@', r'{{ \1 }}', s)


# ===== v5: login state + saved items, shared by every screen =====
# Kept in the viewer's browser only (localStorage), wrapped so a blocked storage never breaks a page.
BOOK = '<path d="M6.5 3.5h11a1 1 0 0 1 1 1V20.5l-6.5-4-6.5 4V4.5a1 1 0 0 1 1-1z"/>'
POL_ALL = json.load(open(os.path.join(DATA, 'policies.json'), encoding='utf-8'))
COURSES_ALL = json.load(open(os.path.join(DATA, 'courses.json'), encoding='utf-8'))
_pol_seed = next((p for p in POL_ALL if p['r'] == '서울' and p['st'] in ('신청 중', '상시')), POL_ALL[0])
SAVE_ITEMS = {
    'olive': {'id': 'post-327326', 'kind': '공고', 't': '성분에디터 콘텐츠 마케팅 인턴', 's': '올리브인터내셔널 · 채용연계형 인턴', 'u': POSTING, 'h': 'S3-compare.dc.html'},
    'ks': {'id': 'post-ks', 'kind': '공고', 't': 'SNS 콘텐츠 마케터', 's': '카카오스타일 · 인턴', 'u': 'https://linkareer.com/activity/342493', 'h': ''},
    'rxc': {'id': 'post-rxc', 'kind': '공고', 't': '숏폼 콘텐츠 기획 편집', 's': 'RXC · 인턴 6개월', 'u': 'https://linkareer.com', 'h': ''},
    'e1421': {'id': 'edu-1421', 'kind': '교육', 't': '(강북5기) AI 활용 SNS 마케터 양성 과정', 's': 'SeSAC 강북 · 모집 중 · 11.08 마감', 'u': SESAC + '1421', 'h': 'C2-course.dc.html'},
    'e1235': {'id': 'edu-1235', 'kind': '교육', 't': '전Z전능 브랜드 마케팅 실전 과정', 's': 'SeSAC 금천 · 모집 중 · 11.10 마감', 'u': SESAC + '1235', 'h': ''},
    'e1266': {'id': 'edu-1266', 'kind': '교육', 't': '(강동7기) 생성형 AI 기반 숏폼 영상콘텐츠 제작 실무과정', 's': 'SeSAC 강동 · 종료', 'u': SESAC + '1266', 'h': ''},
}
import re as _re
_PP = json.load(open(os.path.join(DATA, 'posts2026.json'), encoding='utf-8'))
def post_id(u, i=0):
    m = _re.search(r'(\d+)$', u or '')
    return 'post-' + (m.group(1) if m else str(i))
for _k, _co in (('ks', '카카오스타일'), ('rxc', 'RXC')):
    _hit = next((x for x in _PP if _co in x['company']), None)
    if _hit:
        SAVE_ITEMS[_k].update({'id': post_id(_hit['url']), 'u': _hit['url'] or SAVE_ITEMS[_k]['u']})
SEED = [SAVE_ITEMS['olive'], SAVE_ITEMS['e1421'],
        {'id': _pol_seed['id'], 'kind': '정책', 't': _pol_seed['n'], 's': f"{_pol_seed['o']} · {_pol_seed['st']}", 'u': _pol_seed['u'], 'h': 'P2-policy.dc.html' if _pol_seed['id'] == 'pol-20261018005400213991' else ''}]

ILLO_METHODS = '''  illoGet(k, d) { try { const v = window.localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  illoSet(k, v) { try { if (v === null) window.localStorage.removeItem(k); else window.localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} this.setState({ illoTick: Date.now() }); }
  illoSaved() { return this.illoGet('illo-saved', __SEED__); }
  sv(item) {
    const on = this.illoSaved().some((x) => x.id === item.id);
    return { saved: on, unsaved: !on, label: on ? '저장 해제' : '저장', toggle: () => { const s = this.illoSaved(); this.illoSet('illo-saved', on ? s.filter((x) => x.id !== item.id) : [item].concat(s)); } };
  }
  illoVals() {
    const u = this.illoGet('illo-user', null), n = this.illoSaved().length;
    return { loggedIn: !!u, loggedOut: !u, userName: u ? u.name : '', userInit: u ? u.name.slice(0, 1) : '', profileName: u ? u.name : '예시 프로필',
      savedCount: n, hasSaved: n > 0,
      loginAs: () => { let name = '김하늘'; try { const el = document.getElementById('su-name'); if (el && el.value.trim()) name = el.value.trim(); window.localStorage.setItem('illo-user', JSON.stringify({ name })); } catch (e) {} },
      logout: () => this.illoSet('illo-user', null) };
  }
'''.replace('__SEED__', json.dumps(SEED, ensure_ascii=False))


def inject(script, saves=()):
    """Wrap a page script: page values + login/saved values + static save buttons."""
    script = script.replace('renderVals()', 'pageVals()', 1)
    sv = ''
    if saves:
        sv = ('  svVals() { return { sv: { ' + ', '.join(f"{k}: this.sv({json.dumps(SAVE_ITEMS[k], ensure_ascii=False)})" for k in saves) + ' } }; }\n')
    merge = '  renderVals() { return Object.assign({}, this.illoVals(), ' + ('this.svVals(), ' if saves else '') + 'this.pageVals()); }\n'
    return ILLO_METHODS + sv + merge + script


def save_btn(p, size=36, bg=None):
    bg = bg or FILL
    return (f'<button type="button" onClick="@@{p}.toggle@@" aria-label="@@{p}.label@@" aria-pressed="@@{p}.saved@@" title="@@{p}.label@@" style="width: {size}px; height: {size}px; flex-shrink: 0; border: none; border-radius: 10px; background: {bg}; display: flex; align-items: center; justify-content: center; cursor: pointer;">'
            f'<sc-if value="@@{p}.saved@@" hint-placeholder-val="@@false@@"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="{BLUE}" stroke="{BLUE}" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg></sc-if>'
            f'<sc-if value="@@{p}.unsaved@@" hint-placeholder-val="@@true@@"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B95A1" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg></sc-if></button>')


def auth_desktop():
    return (f'<div style="justify-self: end; display: flex; align-items: center; gap: 8px;">'
            f'<sc-if value="@@loggedOut@@" hint-placeholder-val="@@true@@"><a href="L1-login.dc.html" style="height: 40px; padding: 0 14px; display: flex; align-items: center; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;">로그인</a>'
            f'<a href="L2-signup.dc.html" style="height: 40px; padding: 0 18px; display: flex; align-items: center; border-radius: 999px; background: {INK}; color: #FFFFFF; font-size: 14px; font-weight: 600; text-decoration: none;">회원가입</a></sc-if>'
            f'<sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><a href="S5-saved.dc.html" aria-label="저장함 @@savedCount@@개" style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: {INK};"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg>'
            f'<sc-if value="@@hasSaved@@" hint-placeholder-val="@@true@@"><span style="position: absolute; top: 3px; right: 1px; min-width: 18px; height: 18px; padding: 0 5px; box-sizing: border-box; border-radius: 999px; background: {BLUE}; color: #FFFFFF; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">@@savedCount@@</span></sc-if></a>'
            f'<a href="S5-path.dc.html" style="display: flex; align-items: center; gap: 8px; height: 40px; padding: 0 14px 0 4px; border-radius: 999px; background: #FFFFFF; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;"><span aria-hidden="true" style="width: 32px; height: 32px; border-radius: 50%; background: {BLUE_BG}; color: {BLUE_D}; font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center;">@@userInit@@</span>@@userName@@님</a></sc-if></div>')


def auth_mobile():
    return (f'<sc-if value="@@loggedOut@@" hint-placeholder-val="@@true@@"><a href="m-L1-login.dc.html" style="height: 34px; padding: 0 14px; display: flex; align-items: center; border-radius: 999px; background: {INK}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none;">로그인</a></sc-if>'
            f'<sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><a href="m-S5-path.dc.html" style="display: flex; align-items: center; gap: 6px; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none;"><span aria-hidden="true" style="width: 30px; height: 30px; border-radius: 50%; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">@@userInit@@</span>@@userName@@님</a></sc-if>')

def topbar_back(back, title):
    return ('  <div style="position: sticky; top: 0; z-index: 10; display: grid; grid-template-columns: 40px 1fr 40px; align-items: center; height: 52px; padding: 0 16px; background: rgba(250,250,250,0.96);">'
            f'<a href="{back}" aria-label="뒤로" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: {INK};"><svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></a>'
            f'<span style="text-align: center; font-size: 17px; font-weight: 700;">{title}</span><span></span></div>\n')


# ---------- desktop chrome ----------
NAV = [('home', '홈', 'Main.dc.html'), ('find', '직무 찾기', 'S1-list.dc.html'),
       ('edu', '교육과정', 'E1-edu.dc.html'), ('my', '마이페이지', 'S5-path.dc.html')]


def dheader(active):
    items = ''
    for k, label, href in NAV:
        on = k == active
        st = ('color: #191F28; font-weight: 600; background: #FFFFFF; box-shadow: 0 1px 3px rgba(0,23,51,0.08);' if on else 'color: #4E5968;')
        cur = ' aria-current="page"' if on else ''
        items += f'<li><a href="{href}"{cur} style="display: block; padding: 9px 18px; border-radius: 999px; font-size: 14px; line-height: 1.4; {st} text-decoration: none; white-space: nowrap;">{label}</a></li>'
    return ('  <header style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; height: 88px; padding: 0 40px;">\n'
            f'    <a href="Main.dc.html" style="justify-self: start; display: block;"><img src="{LOGO}" alt="일로 홈" style="height: 26px; width: auto; display: block;"></a>\n'
            f'    <nav aria-label="주요 메뉴"><ol style="display: flex; gap: 2px; padding: 4px; margin: 0; list-style: none; border-radius: 999px; background: rgba(0,23,51,0.06);">{items}</ol></nav>\n'
            f'    {auth_desktop()}\n'
            '  </header>\n')


STEPS = [('공고 고르기', 'S1-list.dc.html'), ('AI 비교', 'S3-compare.dc.html#result'), ('다음 행동 고르기', 'S4-next.dc.html')]
CHECK = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ARROW = f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B0B8C1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def dsteps(cur):
    parts = []
    for i, (label, href) in enumerate(STEPS, 1):
        if i < cur:
            dot, col, w = f'<span style="width: 24px; height: 24px; border-radius: 50%; background: {BLUE}; display: flex; align-items: center; justify-content: center;">{CHECK}</span>', SUB, 500
        elif i == cur:
            dot, col, w = f'<span style="width: 24px; height: 24px; border-radius: 50%; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span>', INK, 700
        else:
            dot, col, w = f'<span style="width: 24px; height: 24px; border-radius: 50%; background: #E5E8EB; color: {SUB}; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span>', MUTE, 500
        cur_attr = ' aria-current="step"' if i == cur else ''
        parts.append(f'<a href="{href}"{cur_attr} style="display: flex; align-items: center; gap: 10px; color: {col}; font-size: 15px; font-weight: {w}; text-decoration: none;">{dot}{label}</a>')
    return (f'  <nav aria-label="비교 단계 {cur}/3" style="margin: 0 56px; display: flex; align-items: center; gap: 20px; padding: 14px 24px; {CARD}">'
            + ARROW.join(parts) + f'<span style="margin-left: auto; font-size: 13px; color: {MUTE};">{cur}/3 단계</span></nav>\n')


def dpage(name, title, active, body, script='  renderVals() { return {}; }', default_h=1200, saves=()):
    script = inject(script, saves)
    h = HEIGHTS.get(name, default_h)
    return holes('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
                 f'<title>{title}</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
                 '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">\n'
                 f'<style>\n{CSS}\n</style>\n</helmet>\n'
                 f'<div style="width: 1280px; height: {h}px; box-sizing: border-box; background: #FAFAFA; color: {INK}; font-family: Pretendard, -apple-system, system-ui, sans-serif; display: flex; flex-direction: column;">\n'
                 f'{dheader(active)}{body}</div>\n</x-dc>\n'
                 f'<script type="text/x-dc" data-dc-script data-props=\'{{"$preview":{{"width":1280,"height":{h}}}}}\'>\n'
                 f'class Component extends DCLogic {{\n{script}\n}}\n</script>\n</body>\n</html>\n')


def mpage(name, title, top, body, active, script='  renderVals() { return {}; }', saves=()):
    return holes(page(name, title, top, body, active, inject(script, saves)))


AI = f'<span style="display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 6px; background: #F0EBFF; color: #6B4EE6; font-size: 11px; font-weight: 700; letter-spacing: 0.02em;"><svg aria-hidden="true" width="11" height="11" viewBox="0 0 24 24" fill="#6B4EE6"><path d="M12 2l2.2 6.6L21 11l-6.8 2.4L12 20l-2.2-6.6L3 11l6.8-2.4z"/></svg>AI</span>'
SRC104 = '공고 104건 (링커리어 64 + 2026 채용 게시판 40) · 팀 수집 2026.10.27 기준'


# ---------- trend popup (replaces the P1 page) ----------
def trend_rows(rows, button=False, pad='0 14px', h=48):
    out = ''
    for i, (n, p, d) in enumerate(rows, 1):
        c = BLUE if i <= 3 else MUTE
        inner = (f'<span style="width: 18px; font-size: 16px; font-weight: 700; color: {c};">{i}</span><span style="flex: 1 1 0; min-width: 0; font-size: 15px; font-weight: 500; white-space: nowrap;">{n}</span>'
                 f'<span style="font-size: 14px; color: #4E5968; font-variant-numeric: tabular-nums;">{p}%</span>{delta(d)}')
        if button:
            out += (f'<button type="button" onClick="@@openTrend@@" class="illo-rank" style="animation-delay: {(i - 1) * 2}s; display: flex; align-items: center; gap: 12px; width: 100%; height: {h}px; padding: {pad}; border: none; border-radius: 12px; background: transparent; color: {INK}; text-align: left; cursor: pointer;">{inner}</button>')
        else:
            out += f'<div style="display: flex; align-items: center; gap: 12px; height: 44px; padding: {pad}; border-top: 1px solid {LINE};">{inner}</div>'
    return out


def trend_popup(mobile, cta_href):
    facts = ''.join(f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 12px; background: {FILL};"><span style="font-size: 11px; color: {SUB};">{k}</span><span style="font-size: 16px; font-weight: 700;">{v}</span></div>'
                    for k, v in [('자격증을 적은 공고', '3% · 3건'), ('외국어를 적은 공고', '14% · 15건'), ('개인 채널 운영 경험', '15% · 16건')])
    wrap = ('align-items: flex-end;' if mobile else 'align-items: center;')
    box = ('width: 100%; max-height: 88vh; border-radius: 24px 24px 0 0; padding: 22px 20px 28px;' if mobile else 'width: 560px; max-height: 88vh; border-radius: 24px; padding: 28px;')
    cta = (f'<a href="{cta_href}" style="height: 52px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; text-decoration: none;">이 직무 공고 보기</a>'
           if cta_href else
           f'<button type="button" onClick="@@closeTrend@@" style="height: 52px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; cursor: pointer;">공고 목록으로 돌아가기</button>')
    return f'''  <sc-if value="@@trendOpen@@" hint-placeholder-val="@@false@@">
  <div role="dialog" aria-modal="true" aria-label="실시간 공고 키워드 전체 순위" style="position: fixed; inset: 0; z-index: 50; display: flex; justify-content: center; {wrap} background: rgba(0,23,51,0.38);">
    <div style="{box} box-sizing: border-box; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; background: #FFFFFF;">
      <div style="display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 8px;"><h2 style="margin: 0; font-size: 20px; font-weight: 700;">실시간 공고 키워드</h2><span style="display: flex; align-items: center; gap: 4px; padding: 3px 7px; border-radius: 999px; background: #FFEEEE; color: {RED}; font-size: 10px; font-weight: 700;"><span class="illo-live" style="width: 6px; height: 6px; border-radius: 50%; background: {RED};"></span>LIVE</span></div>
        <button type="button" onClick="@@closeTrend@@" aria-label="닫기" style="width: 36px; height: 36px; border: none; border-radius: 50%; background: {FILL}; color: {INK}; font-size: 18px; cursor: pointer;">✕</button></div>
      <span style="font-size: 13px; line-height: 1.5; color: {SUB};">SNS 콘텐츠 마케팅 2026 공고 59건이 가장 많이 적은 역량이에요. 순위 변화는 2023~25 공고 45건과 비교</span>
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 14px; background: #FFF4F4;"><span style="font-size: 11px; font-weight: 600; color: {RED};">급상승</span><span style="font-size: 15px; font-weight: 700;">데이터, 성과 분석 8위에서 3위로</span></div>
      <div style="display: flex; flex-direction: column;">{trend_rows(RANK, pad='0 4px')}</div>
      <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">{facts}</div>
      <span style="font-size: 11px; line-height: 1.5; color: {MUTE};">출처: SNS 콘텐츠 마케팅 {SRC104}. 퍼센트는 해당 단어가 나온 공고 비율</span>
      {cta}
    </div>
  </div>
  </sc-if>
'''


TREND_JS = "(typeof location !== 'undefined' && location.hash === '#trend')"
TREND_VALS = "trendOpen: this.state.trendOpen, openTrend: () => this.setState({ trendOpen: true }), closeTrend: () => this.setState({ trendOpen: false })"


def seg_style(on, mobile=False):
    pad = '9px 0' if mobile else '9px 18px'
    flex = 'flex: 1 1 0; ' if mobile else ''
    base = f'{flex}padding: {pad}; border: none; border-radius: 9px; font-size: 14px; cursor: pointer; text-align: center;'
    return base + (f' background: #FFFFFF; color: {INK}; font-weight: 600; box-shadow: 0 1px 3px rgba(0,23,51,0.08);' if on else f' background: transparent; color: {SUB};')


# ---------- shared content ----------
JOBS7 = ['서비스 기획, PM', '데이터 분석', 'UI/UX 디자인', '웹 개발', 'AI 엔지니어', '클라우드 엔지니어']
HAVE = [('콘텐츠 기획', '카드뉴스 주 1회 제작'), ('디자인 툴', '캔바'), ('데이터, 성과 분석', '팔로워 수치만, 일부')]
MISS = ['트렌드 감각, 밈', '영상, 숏폼 제작', '영상 툴 (프리미어 등)', '포트폴리오', '카피라이팅']
REQS = [('자격요건', '숏폼 콘텐츠를 즐겨보며, 최신 콘텐츠 트렌드와 밈에 관심'), ('자격요건', '콘텐츠 성과를 수치로 분석하고 다음 액션을 제안하는 데이터 감각'),
        ('우대', '개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸 숏폼 발행 경험'), ('우대', '뷰티 산업에 대한 애정, 셀링 포인트를 캐치하는 센스'),
        ('우대', '마케팅 학회, 공모전 수상, 인턴십 등 실무 베이스 마케팅 경험'), ('우대', 'Premiere Pro, Photoshop으로 기획안을 영상으로 직접 구현')]
REQ_HTML = ''.join(f'<li style="display: flex; gap: 8px; font-size: 14px; line-height: 1.55;"><span style="flex-shrink: 0; padding: 1px 7px; border-radius: 6px; background: {BLUE_BG if k == "자격요건" else FILL}; color: {BLUE_D if k == "자격요건" else SUB}; font-size: 11px; font-weight: 600; height: fit-content; margin-top: 3px;">{k}</span><span>{t}</span></li>' for k, t in REQS)
EXP_LINES = ['학생회 홍보부 인스타그램 운영 1년', '카드뉴스 주 1회 제작 (캔바)', '팔로워 300명에서 1,200명']
SAVED_CHIPS = ''.join(chip(t) for t in ['미디어커뮤니케이션학과', '컴활 2급', 'OPIc IM2'])


def fit_card(mobile):
    have = {'콘텐츠 기획', '데이터, 성과 분석', '디자인 툴'}
    tick = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
    chips = ''.join((f'<span style="display: flex; align-items: center; gap: 5px; padding: 8px 13px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 14px; font-weight: 600;">{tick}{n}</span>' if n in have else
                     f'<span style="padding: 8px 13px; border-radius: 999px; background: {FILL}; color: {MUTE}; font-size: 14px;">{n}</span>') for n, _, _ in RANK)
    return f'''    <section aria-label="이 직무가 원하는 역량" style="display: flex; flex-direction: column; gap: 14px; padding: {'18px' if mobile else '22px 28px'}; {CARD}">
      <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">{AI}<span style="font-size: {15 if mobile else 16}px; font-weight: 700;">이 직무 공고가 많이 찾는 역량</span><span style="font-size: 14px; color: {SUB};">· 내 경험에 있는 건 <b style="color: {BLUE}; font-weight: 700;">체크</b>했어요</span></div>
      <div style="display: flex; gap: 6px; flex-wrap: wrap;">{chips}</div>
    </section>
'''


def exp_card(mobile):
    return f'''    <section style="display: flex; flex-direction: column; gap: 6px; padding: {'18px' if mobile else '22px 28px'}; {CARD}">
      <span style="font-size: 16px; font-weight: 700;">경력은 공고를 골라 바로 비교해요</span>
      <span style="font-size: 14px; color: {SUB};">이 직무 경력 공고 22건 · 시연은 아래 공고로 진행해요</span>
    </section>
'''


def srow(k, company, title, href=None, save=None):
    sb = save_btn('sv.' + save) if save else ''
    inner = f'{mark(k, 40)}<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: {SUB};">{company}</span><span style="font-size: 16px; font-weight: 600;">{title}</span></span>'
    cmp = f'<span style="flex-shrink: 0; height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 600;">비교하기</span>'
    if href:
        return (f'<div style="display: flex; align-items: center; gap: 10px; border-top: 1px solid {LINE};"><a href="{href}" style="flex: 1 1 0; min-width: 0; display: flex; align-items: center; gap: 14px; padding: 14px 0; color: {INK}; text-decoration: none;">{inner}{cmp}</a>{sb}</div>')
    return (f'<div style="display: flex; align-items: center; gap: 10px; padding: 14px 0; border-top: 1px solid {LINE};"><span style="flex: 1 1 0; min-width: 0; display: flex; align-items: center; gap: 14px; opacity: 0.55;">{inner}</span>{DEMO}{sb}</div>')


def drow(k, company, title, tags, href=None):
    t = ''.join(f'<span style="padding: 4px 10px; border-radius: 999px; background: {FILL}; font-size: 12px; color: {SUB};">{x}</span>' for x in tags)
    inner = (f'{mark(k)}<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 13px; color: {SUB};">{company}</span>'
             f'<span style="font-size: 16px; font-weight: 600;">{title}</span><span style="display: flex; gap: 6px; margin-top: 2px;">{t}</span></span>')
    if href:
        return (f'<a href="{href}" style="display: flex; align-items: center; gap: 16px; padding: 18px 0; border-top: 1px solid {LINE}; color: {INK}; text-decoration: none;">{inner}'
                f'<span style="flex-shrink: 0; height: 40px; padding: 0 16px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 600;">내 경험과 비교 ›</span></a>')
    return f'<div style="display: flex; align-items: center; gap: 16px; padding: 18px 0; border-top: 1px solid {LINE};">{inner}{DEMO}</div>'


STEP_INFO = [('1', '공고 고르기', '직무를 찾고 지원하고 싶은 공고 하나를 골라요', '직무 찾기', 'S1-list.dc.html', False),
             ('2', '내 경험과 비교', '저장한 경험과 공고 문장을 근거 문장으로 맞춰 봐요', '비교해 보기', 'S3-compare.dc.html', True),
             ('3', '다음 행동 고르기', '비어 있는 것 중 무엇부터 채울지 직접 골라요', '교육과정 보기', 'E1-edu.dc.html', False)]

boards = {}

# ===================== desktop =====================
JOBKEY = {'서비스 기획, PM': 'pm', '데이터 분석': 'data', 'UI/UX 디자인': 'uiux', '웹 개발': 'web', 'AI 엔지니어': 'ai', '클라우드 엔지니어': 'cloud'}
chips7 = ''.join(f'<a href="S1-list.dc.html#job={JOBKEY[j]}" style="padding: 8px 14px; border-radius: 999px; background: {FILL}; color: #4E5968; font-size: 13px; text-decoration: none;">{j}</a>' for j in JOBS7)
steps_d = ''
for i, (n, t, d, cta, href, ai) in enumerate(STEP_INFO):
    if i:
        steps_d += f'<span aria-hidden="true" style="display: flex; align-items: center; justify-content: center;">{ARROW}</span>'
    steps_d += (f'<a href="{href}" style="display: flex; flex-direction: column; gap: 10px; padding: 24px; border-radius: 16px; background: {"#F4F9FF" if ai else "#F9FAFB"}; color: {INK}; text-decoration: none;">'
                f'<div style="display: flex; align-items: center; gap: 8px;"><span style="width: 28px; height: 28px; border-radius: 50%; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{n}</span>{AI if ai else ""}</div>'
                f'<span style="font-size: 19px; font-weight: 700;">{t}</span><span style="font-size: 14px; line-height: 1.55; color: {SUB};">{d}</span><span style="margin-top: 4px; font-size: 14px; font-weight: 600; color: {BLUE};">{cta} ›</span></a>')

main_body = f'''  <section style="margin: 24px 56px 0; display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); {CARD} overflow: hidden;">
    <div style="padding: 64px 56px; display: flex; flex-direction: column; gap: 24px;">
      <sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><a href="S5-saved.dc.html" style="align-self: flex-start; display: flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 14px; font-weight: 600; text-decoration: none;">@@userName@@님, 저장함에 @@savedCount@@개가 있어요 ›</a></sc-if>
      <h1 style="margin: 0; font-size: 52px; font-weight: 700; line-height: 1.15; letter-spacing: -0.03em;">청년의 경험으로,<br>다음 청년의 기회를</h1>
      <p style="margin: 0; font-size: 18px; color: {SUB}; line-height: 1.6;">공고와 내 경험을 AI로 비교하고, 지금 할 일 하나를 골라요</p>
      <div style="display: flex; gap: 8px; align-items: center; padding: 8px 8px 8px 20px; background: {FILL}; border-radius: 14px;">
        <label for="job-search" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">직무 검색</label>
        <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
        <input id="job-search" type="text" placeholder="직무를 검색하세요" style="flex: 1 1 0; min-width: 0; height: 48px; border: none; background: #FFFFFF; font-size: 16px; font-family: inherit; color: {INK}; outline: none; border-radius: 12px; padding: 0 12px;">
        <a href="S1-list.dc.html" style="height: 50px; padding: 0 26px; box-sizing: border-box; display: flex; align-items: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; text-decoration: none;">찾아보기</a>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap;"><a href="S1-list.dc.html" style="padding: 8px 14px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 13px; font-weight: 600; text-decoration: none;">SNS 콘텐츠 마케팅</a>{chips7}</div>
    </div>
    <div style="background: {BLUE_BG}; display: flex; align-items: flex-end; justify-content: center; padding-top: 40px;">
      <img src="{ILLU}" alt="두 장의 카드를 들고 무엇을 먼저 할지 고민하는 취준생" style="height: 400px; width: auto; display: block;">
    </div>
  </section>

  <div style="margin: 20px 56px 56px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 20px;">
    <section aria-labelledby="kw" style="display: flex; flex-direction: column; gap: 8px; padding: 26px 26px 18px; {CARD}">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;"><h2 id="kw" style="margin: 0; font-size: 20px; font-weight: 700;">실시간 공고 키워드</h2><span style="display: flex; align-items: center; gap: 5px; padding: 3px 8px; border-radius: 999px; background: #FFEEEE; color: {RED}; font-size: 11px; font-weight: 700;"><span class="illo-live" style="width: 6px; height: 6px; border-radius: 50%; background: {RED};"></span>LIVE</span><button type="button" onClick="@@openTrend@@" style="margin-left: auto; border: none; background: none; padding: 0; font-size: 14px; color: {SUB}; cursor: pointer;">전체 보기 ›</button></div>
      <div style="display: flex; flex-direction: column;">{trend_rows(RANK[:5], button=True, pad='0 10px', h=46)}</div>
      <span style="padding: 0 10px; font-size: 12px; color: {MUTE};">SNS 콘텐츠 마케팅 2026 공고 59건 기준</span>
    </section>
    <section aria-labelledby="hot" style="display: flex; flex-direction: column; padding: 26px 26px 12px; {CARD}">
      <h2 id="hot" style="margin: 0 0 12px; font-size: 20px; font-weight: 700;">이번 주 핫 공고</h2>
      {srow('olive', '올리브인터내셔널', '성분에디터 콘텐츠 마케팅 인턴', 'S3-compare.dc.html', 'olive')}
      {srow('ks', '카카오스타일', 'SNS 콘텐츠 마케터', None, 'ks')}
      {srow('rxc', 'RXC', '숏폼 콘텐츠 기획 편집', None, 'rxc')}
    </section>
  </div>
{trend_popup(False, 'S1-list.dc.html')}'''
TREND_SCRIPT = (f"  constructor(props) {{ super(props); this.state = {{ trendOpen: {TREND_JS} }}; }}\n"
                f"  renderVals() {{ return {{ {TREND_VALS} }}; }}")
boards['Main.dc.html'] = ('S0 홈', dpage('Main.dc.html', '일로 홈', 'home', main_body, TREND_SCRIPT, saves=('olive', 'ks', 'rxc')))

# --- S1 posting list: 46 real 2026 entry-level postings, search, filter, sort, pagination ---
_P = json.load(open(os.path.join(DATA, 'posts2026.json'), encoding='utf-8'))
POSTS = []
for p in _P:
    demo = p['company'] == '올리브인터내셔널'
    POSTS.append({'id': post_id(p['url'], len(POSTS)), 'c': p['company'], 't': p['title'], 'ty': p['type'], 'd': p['close'], 'u': p['url'], 's': p['size'] if p['size'] not in ('', '기타') else '',
                  'ov': len(p['ov']), 'cr': p['created'], 'demo': demo})
POSTS_JSON = json.dumps(POSTS, ensure_ascii=False)
_OTHER = json.load(open(os.path.join(DATA, 'jobs_other.json'), encoding='utf-8'))
JOB_KEYS = [('sns', 'SNS 콘텐츠 마케팅')] + [(k, v['label']) for k, v in _OTHER.items()]
JOBS_DATA = {'sns': {'label': 'SNS 콘텐츠 마케팅', 'posts': POSTS, 'src': '링커리어, 채용 게시판 2026 수집 공고'}}
JOBS_DATA.update({k: {'label': v['label'], 'posts': v['posts'], 'src': '잡코리아 등 채용 사이트 수집 공고 (마감 전)'} for k, v in _OTHER.items()})
JOBS_JSON = json.dumps(JOBS_DATA, ensure_ascii=False)
N_ALL = len(POSTS)
N_TY = {k: sum(1 for p in POSTS if p['ty'] == k) for k in ('인턴', '신입')}
LOGO_BG = ['#2E7D4F', '#3182F6', '#F04452', '#6B4EE6', '#FF8A00', '#191F28', '#0FA3B1', '#C2185B', '#4E5968', '#8D6E63']

PILL = 'flex-shrink: 0; height: 36px; padding: 0 14px; border-radius: 999px; font-size: 14px; cursor: pointer; white-space: nowrap;'
PILL_ON = PILL + f' border: 1px solid {INK}; background: {INK}; color: #FFFFFF; font-weight: 600;'
PILL_OFF = PILL + f' border: 1px solid #E5E8EB; background: #FFFFFF; color: #4E5968;'
SORT_ON = f'border: none; background: none; padding: 0; font-size: 14px; color: {INK}; font-weight: 700; cursor: pointer;'
SORT_OFF = f'border: none; background: none; padding: 0; font-size: 14px; color: {MUTE}; cursor: pointer;'
PG = 'min-width: 36px; height: 36px; padding: 0 6px; border-radius: 10px; font-size: 14px; cursor: pointer;'
PG_ON = PG + f' border: none; background: {INK}; color: #FFFFFF; font-weight: 700;'
PG_OFF = PG + f' border: none; background: transparent; color: #4E5968;'

LIST_JS = f'''  constructor(props) {{ super(props); const jm = (typeof location !== 'undefined' && location.hash.match(/job=(\\w+)/)); this.state = {{ mode: 'new', trendOpen: {TREND_JS}, page: 1, sort: 'rec', ty: 'all', q: '', job: jm ? jm[1] : 'sns', jq: '' }}; }}
  renderVals() {{
    const D = {JOBS_JSON};
    const job = D[this.state.job] ? this.state.job : 'sns', J = D[job], POSTS = J.posts, isSns = job === 'sns';
    const BG = {json.dumps(LOGO_BG)};
    const s = this.state, m = s.mode, set = (o) => this.setState(Object.assign({{ page: 1 }}, o));
    const now = Date.now(), day = 86400000;
    const dleft = (d) => d ? Math.ceil((new Date(d + 'T23:59:59+09:00').getTime() - now) / day) : null;
    const q = (s.q || '').trim().toLowerCase();
    let L = POSTS.filter(p => (s.ty === 'all' || p.ty === s.ty) && (!q || (p.c + ' ' + p.t).toLowerCase().indexOf(q) >= 0));
    const open = (p) => {{ const n = dleft(p.d); return n !== null && n >= 0 ? n : 9999; }};
    if (s.sort === 'rec') L = L.slice().sort((a, b) => (b.demo - a.demo) || (b.ov - a.ov));
    if (s.sort === 'new') L = L.slice().sort((a, b) => (b.cr - a.cr));
    if (s.sort === 'close') L = L.slice().sort((a, b) => open(a) - open(b));
    const per = 10, pages = Math.max(1, Math.ceil(L.length / per)), page = Math.min(s.page, pages);
    const rows = L.slice((page - 1) * per, page * per).map((p) => {{
      const n = dleft(p.d), code = [...p.c].reduce((a, ch) => a + ch.charCodeAt(0), 0);
      const tags = [p.ty].concat(p.s ? [p.s] : []);
      return {{ c: p.c, t: p.t, tags, init: p.c.replace(/[()㈜\\s]/g, '').slice(0, 1), logo: 'width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; background: ' + BG[code % BG.length] + '; color: #FFFFFF; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: center;',
        hasOv: p.ov > 0, ov: '내 경험과 겹치는 역량 ' + p.ov, demo: p.demo, notDemo: !p.demo, url: p.u || '#',
        sv: this.sv({{ id: p.id, kind: '공고', t: p.t, s: p.c + ' · ' + p.ty, u: p.u, h: p.demo ? 'S3-compare.dc.html' : '' }}),
        due: n !== null && n >= 0 ? (n === 0 ? 'D-DAY' : 'D-' + n) : '', hasDue: n !== null && n >= 0, noDue: !(n !== null && n >= 0) }};
    }});
    const pick = (k, v) => () => set({{ [k]: v }});
    const pill = (k, v) => ({{ style: s[k] === v ? '{PILL_ON}' : '{PILL_OFF}', go: pick(k, v) }});
    const sortb = (v) => ({{ style: s.sort === v ? '{SORT_ON}' : '{SORT_OFF}', go: pick('sort', v) }});
    const nums = [];
    for (let i = 1; i <= pages; i++) nums.push({{ n: i, style: i === page ? '{PG_ON}' : '{PG_OFF}', go: () => this.setState({{ page: i }}), cur: i === page ? 'page' : 'false' }});
    const from = L.length ? (page - 1) * per + 1 : 0, to = Math.min(page * per, L.length);
    const st = (on) => on ? '@@ON@@' : '@@OFF@@';
    const jq = (s.jq || '').trim().toLowerCase().replace(/\\s/g, '');
    const jobs = Object.keys(D).filter((k) => !jq || D[k].label.toLowerCase().replace(/\\s/g, '').indexOf(jq) >= 0).map((k) => ({{ label: D[k].label, style: k === job ? '{PILL_ON}' : '{PILL_OFF}', go: () => this.setState({{ job: k, page: 1, q: '', ty: 'all', jq: '' }}) }}));
    const cnt = (t) => POSTS.filter((p) => t === 'all' || p.ty === t).length;
    return {{ jobName: J.label, isSns, notSns: !isSns, showFit: isSns && m === 'new', fitTodo: !isSns && m === 'new', jobs, jq: s.jq, setJq: (e) => this.setState({{ jq: e && e.target ? e.target.value : '' }}), noJob: jobs.length === 0, srcNote: J.src + ' ' + POSTS.length + '건' + (isSns ? ' · 시연은 올리브인터내셔널 공고로 비교해요' : ' · 공고 비교는 SNS 콘텐츠 마케팅으로 시연해요'),
      cntAll: '전체 ' + cnt('all'), cntIntern: '인턴 ' + cnt('인턴'), cntNew: '신입 ' + cnt('신입'),
      count: m === 'new' ? '신입, 인턴 공고 ' + POSTS.length + '건' : (isSns ? '경력 공고 22건 · 2026.10 수집' : '경력 공고는 준비 중'), isNew: m === 'new', isExp: m === 'exp', newStyle: st(m === 'new'), expStyle: st(m === 'exp'), pickNew: () => this.setState({{ mode: 'new' }}), pickExp: () => this.setState({{ mode: 'exp' }}),
      {TREND_VALS},
      rows, empty: L.length === 0, hasRows: L.length > 0, total: L.length, range: from + '–' + to, nums, pages,
      prev: () => this.setState({{ page: Math.max(1, page - 1) }}), next: () => this.setState({{ page: Math.min(pages, page + 1) }}),
      prevStyle: '{PG_OFF}' + (page === 1 ? ' opacity: 0.35;' : ''), nextStyle: '{PG_OFF}' + (page === pages ? ' opacity: 0.35;' : ''),
      ty: {{ all: pill('ty', 'all'), intern: pill('ty', '인턴'), newbie: pill('ty', '신입') }},
      sort: {{ rec: sortb('rec'), new: sortb('new'), close: sortb('close') }},
      q: s.q, setQ: (e) => set({{ q: e && e.target ? e.target.value : '' }}), clearQ: () => set({{ q: '' }}), hasQ: !!q }};
  }}'''


def list_toolbar(mobile):
    pre = 'm-' if mobile else ''
    search = (f'<label style="{"" if mobile else "width: 320px; "}display: flex; align-items: center; gap: 8px; height: 44px; padding: 0 14px; border-radius: 12px; background: {FILL};">'
              f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
              f'<span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">회사명, 공고 제목 검색</span>'
              f'<input type="search" value="@@q@@" onChange="@@setQ@@" placeholder="회사명, 공고 제목" style="flex: 1 1 0; min-width: 0; border: none; background: transparent; font-size: 15px; font-family: inherit; color: {INK}; outline: none;"></label>')
    pills = (f'<button type="button" onClick="@@ty.all.go@@" style="@@ty.all.style@@">@@cntAll@@</button>'
             f'<button type="button" onClick="@@ty.intern.go@@" style="@@ty.intern.style@@">@@cntIntern@@</button>'
             f'<button type="button" onClick="@@ty.newbie.go@@" style="@@ty.newbie.style@@">@@cntNew@@</button>')
    sorts = (f'<button type="button" onClick="@@sort.rec.go@@" style="@@sort.rec.style@@">추천순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             f'<button type="button" onClick="@@sort.new.go@@" style="@@sort.new.style@@">최신순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             f'<button type="button" onClick="@@sort.close.go@@" style="@@sort.close.style@@">마감 임박순</button>')
    if mobile:
        return (f'{search}<div class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -18px; padding: 0 18px;">{pills}</div>'
                f'<div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 13px; color: {SUB};">@@total@@건</span><div style="display: flex; gap: 8px; align-items: center;">{sorts.replace("font-size: 14px", "font-size: 13px")}</div></div>')
    return (f'<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">{search}<div style="display: flex; gap: 6px;">{pills}</div></div>'
            f'<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 4px;"><span style="font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@total@@</b>건 중 @@range@@</span><div style="display: flex; gap: 10px; align-items: center;">{sorts}</div></div>')


def list_rows(mobile):
    pre = 'm-' if mobile else ''
    tagchips = f'<sc-for list="@@r.tags@@" as="g" hint-placeholder-count="2"><span style="padding: 3px 8px; border-radius: 6px; background: {FILL}; font-size: 12px; color: {SUB};">@@g@@</span></sc-for>'
    ov = f'<sc-if value="@@r.hasOv@@" hint-placeholder-val="@@true@@"><span style="padding: 3px 8px; border-radius: 6px; background: {BLUE_BG}; font-size: 12px; color: {BLUE_D};">@@r.ov@@</span></sc-if>'
    demo_tag = f'<sc-if value="@@r.demo@@" hint-placeholder-val="@@false@@"><span style="padding: 3px 8px; border-radius: 6px; background: #F0EBFF; font-size: 12px; color: #6B4EE6; font-weight: 600;">시연 공고</span></sc-if>'
    due = (f'<sc-if value="@@r.hasDue@@" hint-placeholder-val="@@false@@"><span style="font-size: 13px; font-weight: 700; color: {RED};">@@r.due@@</span></sc-if>'
           f'<sc-if value="@@r.noDue@@" hint-placeholder-val="@@true@@"><span style="font-size: 12px; color: {MUTE};">상시, 채용 시 마감</span></sc-if>')
    act = (f'<sc-if value="@@r.demo@@" hint-placeholder-val="@@false@@"><a href="{pre}S3-compare.dc.html" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 14px; font-weight: 600; text-decoration: none; white-space: nowrap;">비교하기</a></sc-if>'
           f'<sc-if value="@@r.notDemo@@" hint-placeholder-val="@@true@@"><a href="@@r.url@@" {EXT} style="height: 38px; padding: 0 12px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">원문 ↗</a></sc-if>')
    if mobile:
        row = (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 0; border-top: 1px solid {LINE};">'
               f'<div style="display: flex; gap: 12px;"><span aria-hidden="true" style="@@r.logo@@">@@r.init@@</span><span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 12px; color: {SUB};">@@r.c@@</span><span style="font-size: 15px; font-weight: 600; line-height: 1.4;">@@r.t@@</span></span></div>'
               f'<div style="display: flex; gap: 4px; flex-wrap: wrap;">{demo_tag}{tagchips}{ov}</div>'
               f'<div style="display: flex; justify-content: space-between; align-items: center;">{due}<div style="display: flex; gap: 8px;">{save_btn("r.sv", 38)}{act}</div></div></div>')
    else:
        row = (f'<div style="display: flex; align-items: center; gap: 16px; padding: 16px 0; border-top: 1px solid {LINE};">'
               f'<span aria-hidden="true" style="@@r.logo@@">@@r.init@@</span>'
               f'<span style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 13px; color: {SUB};">@@r.c@@</span><span style="font-size: 16px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@@r.t@@</span>'
               f'<span style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 2px;">{demo_tag}{tagchips}{ov}</span></span>'
               f'<span style="width: 120px; flex-shrink: 0; text-align: right;">{due}</span>{save_btn("r.sv", 38)}{act}</div>')
    empty = (f'<sc-if value="@@empty@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 0; border-top: 1px solid {LINE}; color: {SUB}; font-size: 15px;">'
             f'검색 결과가 없어요<button type="button" onClick="@@clearQ@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">검색어 지우기</button></div></sc-if>')
    pager = (f'<sc-if value="@@hasRows@@" hint-placeholder-val="@@true@@"><nav aria-label="페이지" style="display: flex; justify-content: center; align-items: center; gap: 4px; padding: {"14px 0 6px" if mobile else "20px 0 8px"}; border-top: 1px solid {LINE};">'
             f'<button type="button" onClick="@@prev@@" aria-label="이전 페이지" style="@@prevStyle@@">‹</button>'
             f'<sc-for list="@@nums@@" as="p" hint-placeholder-count="5"><button type="button" onClick="@@p.go@@" aria-current="@@p.cur@@" style="@@p.style@@">@@p.n@@</button></sc-for>'
             f'<button type="button" onClick="@@next@@" aria-label="다음 페이지" style="@@nextStyle@@">›</button></nav></sc-if>')
    return f'<sc-for list="@@rows@@" as="r" hint-placeholder-count="10">{row}</sc-for>{empty}{pager}'


def list_card(mobile):
    pad = '18px 18px 8px' if mobile else '24px 28px 12px'
    return (f'    <section aria-labelledby="{"m-" if mobile else ""}list" style="display: flex; flex-direction: column; gap: {12 if mobile else 14}px; padding: {pad}; {CARD}">\n'
            f'      <h2 id="{"m-" if mobile else ""}list" style="margin: 0; font-size: {17 if mobile else 18}px; font-weight: 700;">공고를 골라 비교해 보세요</h2>\n'
            f'      {list_toolbar(mobile)}\n      <div>{list_rows(mobile)}</div>\n'
            f'      <span style="font-size: 12px; color: {MUTE};">출처: @@srcNote@@</span>\n    </section>\n')

# --- S1 직무 찾기 ---
S1_SCRIPT = (f"  constructor(props) {{ super(props); this.state = {{ mode: 'new', trendOpen: {TREND_JS} }}; }}\n"
             "  renderVals() {\n    const m = this.state.mode;\n"
             "    const st = (on) => on ? '@@ON@@' : '@@OFF@@';\n"
             f"    return {{ isNew: m === 'new', isExp: m === 'exp', count: m === 'new' ? '신입, 인턴 공고 82건 · 2026.10 수집' : '경력 공고 22건 · 2026.10 수집',\n"
             "      newStyle: st(m === 'new'), expStyle: st(m === 'exp'), pickNew: () => this.setState({ mode: 'new' }), pickExp: () => this.setState({ mode: 'exp' }),\n"
             f"      {TREND_VALS} }};\n  }}")
s1_body = f'''  <div style="padding: 20px 56px 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap;"><span style="font-size: 13px; font-weight: 600; color: {SUB}; margin-right: 4px;">직무</span><sc-for list="@@jobs@@" as="j" hint-placeholder-count="7"><button type="button" onClick="@@j.go@@" style="@@j.style@@">@@j.label@@</button></sc-for>
    <label style="display: flex; align-items: center; gap: 6px; height: 36px; padding: 0 12px; border-radius: 999px; background: {FILL};"><svg aria-hidden="true" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">직무 검색</span><input type="search" value="@@jq@@" onChange="@@setJq@@" placeholder="다른 직무 검색" style="width: 120px; border: none; background: transparent; font-size: 14px; font-family: inherit; color: {INK}; outline: none;"></label>
    <sc-if value="@@noJob@@" hint-placeholder-val="@@false@@"><span style="font-size: 13px; color: {SUB};">"@@jq@@" 직무는 아직 준비 중이에요. 검색어를 지우면 7개 직무가 다시 보여요</span></sc-if></div>
  <div style="padding: 20px 56px 0; display: flex; justify-content: space-between; align-items: flex-end;">
    <div style="display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">@@jobName@@</h1><span style="font-size: 15px; color: {SUB};">@@count@@</span></div>
    <div style="display: flex; align-items: center; gap: 16px;"><sc-if value="@@isSns@@" hint-placeholder-val="@@true@@"><button type="button" onClick="@@openTrend@@" style="border: none; background: none; padding: 0; font-size: 14px; font-weight: 600; color: {BLUE}; cursor: pointer;">이 직무 트렌드 보기 ›</button></sc-if>
    <div role="tablist" aria-label="경력 구분" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);"><button type="button" role="tab" onClick="@@pickNew@@" style="@@newStyle@@">신입, 인턴</button><button type="button" role="tab" onClick="@@pickExp@@" style="@@expStyle@@">경력</button></div></div>
  </div>
  <div style="display: flex; flex-direction: column; gap: 16px; padding: 24px 56px 56px;">
    <sc-if value="@@showFit@@" hint-placeholder-val="@@true@@">
{fit_card(False)}    </sc-if>
    <sc-if value="@@fitTodo@@" hint-placeholder-val="@@false@@"><section style="display: flex; align-items: center; gap: 12px; padding: 20px 28px; {CARD}">{AI}<span style="font-size: 15px; line-height: 1.5; color: #4E5968;">이 직무의 역량 분석은 준비 중이에요. 공고 원문은 지금 볼 수 있고, 공고 비교는 <b style="color: {INK};">SNS 콘텐츠 마케팅</b>으로 시연해요</span></section></sc-if>
    <sc-if value="@@isExp@@" hint-placeholder-val="@@false@@">
{exp_card(False)}    </sc-if>
{list_card(False)}  </div>
{trend_popup(False, None)}'''
s1_script = LIST_JS.replace('@@ON@@', seg_style(True)).replace('@@OFF@@', seg_style(False))
boards['S1-list.dc.html'] = ('S1 직무 찾기 (신입, 인턴은 적합도 / 경력은 공고)', dpage('S1-list.dc.html', '직무 찾기', 'find', s1_body, s1_script))

# --- S3 공고 + AI 비교 + 다음 행동 (한 페이지) ---
seg_d = lambda c: f'<span style="flex: 1 1 0; height: 10px; border-radius: 999px; background: {c};"></span>'
legend = lambda c, l, n: f'<span style="display: flex; align-items: center; gap: 6px; font-size: 13px; color: #4E5968;"><span style="width: 8px; height: 8px; border-radius: 50%; background: {c};"></span>{l} <b style="font-weight: 700; color: {INK};">{n}</b></span>'
COMPARE_SCRIPT = ("  constructor(props) { super(props); this.state = { done: (typeof location !== 'undefined' && location.hash === '#result') }; }\n"
                  "  renderVals() { const d = this.state.done; return { done: d, notDone: !d, run: () => this.setState({ done: true }), reset: () => this.setState({ done: false }) }; }")


def exp_strip(mobile):
    pre = 'm-' if mobile else ''
    lines = ''.join(f'<li>{l}</li>' for l in EXP_LINES)
    return f'''    <section aria-label="마이페이지에 저장된 내 경험" style="display: flex; flex-direction: column; gap: 10px; padding: {'16px 18px' if mobile else '20px 24px'}; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 14px; font-weight: 700;">내 경험 <span style="font-weight: 400; font-size: 12px; color: {MUTE};">마이페이지 이력서에서</span></span><a href="{pre}S5-resume.dc.html" style="font-size: 13px; color: {SUB}; text-decoration: none;">수정 ›</a></div>
      <div style="display: flex; gap: 6px; flex-wrap: wrap;">{SAVED_CHIPS}</div>
      <ul style="margin: 0; padding: 0 0 0 18px; display: flex; flex-direction: column; gap: 2px; font-size: 14px; line-height: 1.55; color: #333D4B;">{lines}</ul>
    </section>
'''


def run_card(mobile):
    return f'''    <sc-if value="@@notDone@@" hint-placeholder-val="@@true@@">
    <section style="display: flex; flex-direction: column; gap: 14px; padding: {'20px' if mobile else '28px'}; {CARD}">
      {AI}
      <h2 style="margin: 0; font-size: {19 if mobile else 22}px; font-weight: 700; line-height: 1.4;">저장한 경험으로 바로 비교할게요</h2>
      <p style="margin: 0; font-size: 14px; line-height: 1.6; color: {SUB};">AI가 공고 문장 6개마다 내 경험에서 근거 문장을 찾아요. 맞음, 일부, 찾지 못함은 정해진 규칙으로 판정해요</p>
      <button type="button" onClick="@@run@@" style="height: 54px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; cursor: pointer;">AI로 비교하기</button>
      <span style="font-size: 12px; color: {MUTE}; text-align: center;">합격 여부는 예측하지 않아요 · 시연은 예시 경험으로 비교해요</span>
    </section>
    </sc-if>
'''


def result_head(mobile):
    return f'''    <section style="display: flex; flex-direction: column; gap: 12px; padding: {'20px' if mobile else '24px 28px'}; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: center;">{AI}<button type="button" onClick="@@reset@@" style="border: none; background: none; padding: 0; font-size: 12px; color: {MUTE}; cursor: pointer;">다시 비교</button></div>
      <h2 style="margin: 0; font-size: {21 if mobile else 26}px; font-weight: 700; line-height: 1.35; letter-spacing: -0.02em;">공고 요구 6개 중 <span style="color: {BLUE};">2개</span>가 내 경험과 이어져요</h2>
      <div role="img" aria-label="맞음 1, 일부 1, 찾지 못함 4" style="display: flex; gap: 4px;">{seg_d(BLUE)}{seg_d('#FFB331')}{seg_d('#E5E8EB')}{seg_d('#E5E8EB')}{seg_d('#E5E8EB')}{seg_d('#E5E8EB')}</div>
      <div style="display: flex; gap: 16px; flex-wrap: wrap;">{legend(BLUE, '맞음', 1)}{legend('#FFB331', '일부', 1)}{legend('#D1D6DB', '찾지 못함', 4)}</div>
      <span style="font-size: 12px; line-height: 1.5; color: {MUTE};">AI는 근거 문장을 찾고, 판정은 규칙으로 해요. 같은 행동과 근거 수치가 있으면 맞음, 행동만 있으면 일부</span>
    </section>
'''


d_match = lambda b, c, bg, need, kind, mine, note='': (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 0; border-top: 1px solid {LINE};"><div style="display: flex; align-items: center; gap: 8px;"><span style="padding: 4px 10px; border-radius: 999px; background: {bg}; color: {c}; font-size: 12px; font-weight: 700;">{b}</span><span style="font-size: 12px; color: {MUTE};">{kind}</span></div>'
                                                       f'<span style="font-size: 15px; line-height: 1.5;">공고 "{need}"</span><div style="display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; border-radius: 12px; background: {bg};"><span style="font-size: 12px; color: {c}; font-weight: 600;">내 경험</span><span style="font-size: 14px; line-height: 1.55;">{mine}</span>'
                                                       + (f'<span style="font-size: 13px; color: {c};">{note}</span>' if note else '') + '</div></div>')
d_gap = lambda need, kind, why, href, action: (f'<div style="display: flex; align-items: center; gap: 14px; padding: 15px 0; border-top: 1px solid {LINE};"><div style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 15px; line-height: 1.45;">{need}</span><span style="font-size: 12px; color: {MUTE};">{kind} · {why}</span></div>'
                                               f'<a href="{href}" style="flex-shrink: 0; padding: 8px 12px; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">{action} ›</a></div>')


def d_choice(href, ic, title, sub, badge=''):
    b = f'<span style="padding: 3px 8px; border-radius: 6px; background: {BLUE}; color: #FFFFFF; font-size: 11px; font-weight: 700;">{badge}</span>' if badge else ''
    return (f'<a href="{href}" style="display: flex; flex-direction: column; gap: 12px; padding: 20px; {CARD} color: {INK}; text-decoration: none;"><div style="display: flex; justify-content: space-between; align-items: center;"><span style="width: 40px; height: 40px; border-radius: 12px; background: {BLUE_BG}; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{CICON[ic]}</svg></span>{b}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 17px; font-weight: 700;">{title}</span><span style="font-size: 13px; color: {SUB};">{sub}</span></div><span style="font-size: 13px; font-weight: 600; color: {BLUE};">선택하기 ›</span></a>')


s3_body = f'''{dsteps(2)}  <div style="padding: 20px 56px 0; display: flex; flex-direction: column; gap: 6px;"><a href="S1-list.dc.html" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 공고 목록</a><h1 style="margin: 0; font-size: 30px; font-weight: 700; letter-spacing: -0.02em;">이 공고와 내 경험을 비교해요</h1></div>
  <div style="display: grid; grid-template-columns: 440px minmax(0, 1fr); gap: 24px; padding: 20px 56px 56px; align-items: start;">
    <section aria-label="채용 공고" style="display: flex; flex-direction: column; gap: 16px; padding: 26px; {CARD}">
      <div style="display: flex; align-items: center; gap: 12px;">{mark('olive')}<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 14px; font-weight: 600;">올리브인터내셔널</span><span style="font-size: 12px; color: {MUTE};">뷰티 브랜드 성분에디터 · 마케팅본부</span></span>{save_btn('sv.olive', 40)}</div>
      <h2 style="margin: 0; font-size: 20px; font-weight: 700; line-height: 1.4;">[마케팅본부] 성분에디터 콘텐츠 마케팅 인턴 (채용연계형)</h2>
      <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; padding: 12px 14px; background: #F9FAFB; border-radius: 12px; font-size: 13px;"><span><span style="color: {MUTE};">직무</span> 콘텐츠 마케터</span><span><span style="color: {MUTE};">고용</span> 인턴 (채용연계)</span><span><span style="color: {MUTE};">경력</span> 무관</span><span><span style="color: {MUTE};">마감</span> 채용 시 마감</span></div>
      <div style="display: flex; flex-direction: column; gap: 10px;"><span style="font-size: 15px; font-weight: 700;">공고가 원하는 것 6</span><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;">{REQ_HTML}</ul></div>
      <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 1px solid {LINE};"><span style="font-size: 12px; color: {MUTE};">출처: 링커리어 · 팀 수집 공고 원문</span><a href="{POSTING}" {EXT} style="font-size: 13px; text-decoration: none;">원문 공고 보기 ↗</a></div>
    </section>
    <div style="display: flex; flex-direction: column; gap: 16px; min-width: 0;">
{exp_strip(False)}{run_card(False)}    <sc-if value="@@done@@" hint-placeholder-val="@@false@@">
{result_head(False)}    <div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; align-items: start;">
      <section style="display: flex; flex-direction: column; padding: 22px 24px 8px; {CARD}"><h3 style="margin: 0 0 10px; font-size: 17px; font-weight: 700;">이어지는 경험 <span style="color: {BLUE};">2</span></h3>
        {d_match('맞음', BLUE_D, BLUE_BG, '개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸', '우대 · SNS 채널 운영', '학생회 홍보부 인스타그램 운영 1년, 팔로워 300명에서 1,200명')}
        {d_match('일부', OR, OR_BG, '콘텐츠의 성과를 객관적인 수치로 분석하고, 다음 액션을 제안', '자격요건 · 성과 분석', '팔로워 300명에서 1,200명', '무엇을 보고 무엇을 바꿨는지 한 문장 더하면 맞음이 돼요')}
      </section>
      <section style="display: flex; flex-direction: column; padding: 22px 24px 14px; {CARD}"><h3 style="margin: 0 0 10px; font-size: 17px; font-weight: 700;">아직 비어 있는 것 <span style="color: {MUTE};">4</span></h3>
        {d_gap('숏폼 발행 경험', '우대', '입력엔 카드뉴스만 있어요', 'S4-activity.dc.html', '프로젝트')}
        {d_gap('Premiere Pro, Photoshop으로 직접 구현', '우대', '캔바만 찾았어요', 'S4-next.dc.html', 'SeSAC')}
        {d_gap('최신 콘텐츠 트렌드와 밈에 관심', '자격요건', '찾지 못했어요', 'S1-list.dc.html#trend', '트렌드')}
        {d_gap('학회, 공모전, 인턴십 등 실무 경험', '우대', '찾지 못했어요', 'S4-activity.dc.html', '공모전')}
        <a href="S5-resume.dc.html" style="margin-top: 6px; font-size: 13px; color: {SUB}; text-decoration: none;">빠뜨린 경험이 있나요? <span style="color: {BLUE};">이력서에서 고치기 ›</span></a>
      </section>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px;"><h2 style="margin: 0; font-size: 22px; font-weight: 700;">어느 부분을 먼저 채울까요?</h2><span style="font-size: 13px; color: {SUB};">고르는 건 나. 4가지 모두 언제든 볼 수 있어요</span></div>
    <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px;">{d_choice('S4-next.dc.html', 'edu', '교육으로 배우기', 'SeSAC 과정 2개 모집 중', '빈 칸 2개')}{d_choice('S4-cert.dc.html', 'cert', '자격증, 어학', '이 직무 공고 언급 3%')}{d_choice('S4-activity.dc.html', 'act', '대외활동, 프로젝트', '숏폼 직접 발행해 보기')}{d_choice('S4-apply.dc.html', 'apply', '지원 준비', '지금 경험으로 지원하기')}</div>
    </sc-if>
    </div>
  </div>
'''
boards['S3-compare.dc.html'] = ('S2 공고 + AI 비교 + 다음 행동 (한 페이지)', dpage('S3-compare.dc.html', '공고와 내 경험 비교', 'find', s3_body, COMPARE_SCRIPT, saves=('olive',)))

# --- E1 교육과정 ---
CATS = [('all', '전체'), ('sesac', 'SeSAC 교육'), ('cert', '자격증, 어학'), ('act', '대외활동'), ('policy', '취업 지원 정책')]
E1_SCRIPT = ("  constructor(props) { super(props); this.state = { cat: 'all' }; }\n"
             "  renderVals() {\n    const c = this.state.cat;\n    const tab = (k) => ({ style: c === k ? '@@ON@@' : '@@OFF@@', pick: () => this.setState({ cat: k }) });\n"
             "    const show = (k) => c === 'all' || c === k;\n"
             "    return { tabs: { " + ', '.join(f"{k}: tab('{k}')" for k, _ in CATS) + " }, show: { sesac: show('sesac'), cert: show('cert'), act: show('act'), policy: show('policy') } };\n  }")
POLICY = [('국민내일배움카드', '고용24', '직업훈련 비용을 지원하는 카드. 훈련 과정 검색과 신청까지', 'https://www.work24.go.kr'),
          ('국민취업지원제도', '고용24', '취업지원 서비스와 구직촉진수당을 함께 지원', 'https://www.work24.go.kr'),
          ('K-디지털 트레이닝', '고용24', '디지털, 신기술 분야 집중 훈련 과정', 'https://www.work24.go.kr'),
          ('서울 청년수당', '서울청년몽땅정보통', '서울 거주 미취업 청년의 구직 활동 지원', 'https://youth.seoul.go.kr')]


def course_card(thumb, status, title, meta, tags, href, ended=False, mobile=False):
    img = (f'<img src="{thumb}" alt="" style="width: 100%; height: {150 if mobile else 168}px; object-fit: cover; display: block; border-radius: 14px;">' if thumb else
           f'<div style="height: {150 if mobile else 168}px; border-radius: 14px; background: {FILL}; display: flex; align-items: center; justify-content: center; color: {MUTE}; font-size: 13px;">지금 모집 중인 기수가 없어요</div>')
    sc = (f'background: {FILL}; color: {SUB};' if ended else f'background: {BLUE_BG}; color: {BLUE_D};')
    t = ''.join(f'<span style="font-size: 12px; color: {SUB};">#{x}</span>' for x in tags)
    return (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: {16 if mobile else 18}px; {CARD}">{img}<span style="align-self: flex-start; padding: 3px 9px; border-radius: 999px; {sc} font-size: 12px; font-weight: 600;">{status}</span>'
            f'<span style="font-size: 16px; font-weight: 700; line-height: 1.4;">{title}</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">{meta}</span><span style="display: flex; gap: 8px; flex-wrap: wrap;">{t}</span>'
            f'<a href="{href}" {EXT} style="margin-top: auto; padding-top: 6px; font-size: 14px; font-weight: 600; text-decoration: none;">{"지난 기수 보기" if ended else "SeSAC에서 과정 보기"} ↗</a></div>')


COURSES = [(THUMB1, '모집중 · 11.08 마감', '(강북5기) AI 활용 SNS 마케터 양성 과정', '2026.11.25 ~ 2027.03.17 · 420시간 · 무료', ['SNS마케팅', '콘텐츠마케팅', 'AI'], SESAC + '1421', False),
           (THUMB2, '모집중 · 11.10 마감', '전Z전능 브랜드 마케팅 실전 과정 (금천)', '2026.11.30 ~ 2027.02.26 · 360시간', ['브랜드마케팅', 'GA4', '메타광고'], SESAC + '1235', False),
           (None, '지난 기수 · 10.02 종료', '(강동7기) 생성형 AI 기반 숏폼 영상콘텐츠 제작 실무과정', '2026.07.03 ~ 10.02 · 다음 기수 공지 전', ['숏폼', '영상편집'], SESAC + '1266', True)]


def stat_line(n, p, c):
    return f'<div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-top: 1px solid {LINE}; font-size: 14px;"><span>{n}</span><span style="font-weight: 700;">{p} <span style="font-weight: 400; color: {MUTE}; font-size: 12px;">{c}</span></span></div>'


def edu_sections(mobile):
    pre = 'm-' if mobile else ''
    cols = 1 if mobile else 3
    courses = ''.join(course_card(*c, mobile=mobile) for c in COURSES)
    pol = ''.join(f'<a href="{u}" {EXT} style="display: flex; flex-direction: column; gap: 6px; padding: 18px; {CARD} color: {INK}; text-decoration: none;"><span style="font-size: 12px; color: {MUTE};">{o}</span><span style="font-size: 16px; font-weight: 700;">{n}</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">{d}</span><span style="margin-top: 4px; font-size: 13px; font-weight: 600; color: {BLUE};">공식 사이트 ↗</span></a>' for n, o, d, u in POLICY)
    h = lambda t, r='': f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px; {"padding: 0 4px;" if mobile else ""}"><h2 style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">{t}</h2><span style="font-size: 12px; color: {MUTE};">{r}</span></div>'
    pcols = 1 if mobile else 4
    return f'''    <sc-if value="@@show.sesac@@" hint-placeholder-val="@@true@@">
    <section style="display: flex; flex-direction: column; gap: 12px;">{h('SeSAC 교육 과정', '마케팅 분야 · 모집 중 2')}<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;">{courses}</div></section>
    </sc-if>
    <sc-if value="@@show.cert@@" hint-placeholder-val="@@true@@">
    <section style="display: flex; flex-direction: column; gap: 12px;">{h('자격증, 어학', '이 직무 공고 104건 기준')}
      <div style="display: grid; grid-template-columns: repeat({1 if mobile else 2}, minmax(0, 1fr)); gap: 12px;">
        <a href="{pre}S4-cert.dc.html" style="display: flex; flex-direction: column; padding: 20px 20px 8px; {CARD} color: {INK}; text-decoration: none;"><span style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">자격증보다 툴로 만든 결과물을 봐요</span>{stat_line('자격증을 적은 공고', '3%', '3건')}{stat_line('프리미어를 적은 공고', '30건', '툴')}{stat_line('포토샵을 적은 공고', '28건', '툴')}</a>
        <a href="{pre}S4-cert.dc.html" style="display: flex; flex-direction: column; padding: 20px 20px 8px; {CARD} color: {INK}; text-decoration: none;"><span style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">어학은 공고 원문에서 확인해요</span>{stat_line('외국어를 적은 공고', '14%', '15건')}{stat_line('내 어학', 'OPIc IM2', '마이페이지')}<span style="padding: 12px 0; font-size: 13px; font-weight: 600; color: {BLUE};">자세히 보기 ›</span></a>
      </div></section>
    </sc-if>
    <sc-if value="@@show.act@@" hint-placeholder-val="@@true@@">
    <section style="display: flex; flex-direction: column; gap: 12px;">{h('대외활동, 프로젝트', '이 직무 공고 104건 기준')}
      <div style="display: grid; grid-template-columns: repeat({1 if mobile else 2}, minmax(0, 1fr)); gap: 12px;">
        <div style="display: flex; flex-direction: column; padding: 20px 20px 8px; {CARD}"><span style="font-size: 16px; font-weight: 700; margin-bottom: 8px;">공고가 적은 경험</span>{stat_line('개인 SNS, 채널 운영 경험', '15%', '16건')}{stat_line('공모전, 수상', '9%', '9건')}{stat_line('서포터즈, 기자단', '2%', '2건')}</div>
        <a href="{pre}S4-activity.dc.html" style="display: flex; flex-direction: column; gap: 8px; padding: 20px; background: #F4F9FF; border-radius: 20px; color: {INK}; text-decoration: none;"><span style="align-self: flex-start; padding: 3px 9px; border-radius: 999px; background: #FFFFFF; color: {BLUE_D}; font-size: 12px; font-weight: 600;">일로 제안 · 4주 프로젝트</span><span style="font-size: 17px; font-weight: 700; line-height: 1.4;">내 채널에 숏폼 6개 올리고 숫자로 정리하기</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">비어 있는 "숏폼 발행 경험"을 채워요. 레퍼런스 모으기부터 결과 한 장까지</span><span style="margin-top: auto; font-size: 13px; font-weight: 600; color: {BLUE};">프로젝트 보기 ›</span></a>
      </div>
      <a href="https://linkareer.com/list/contest" {EXT} style="{"padding: 0 4px; " if mobile else ""}font-size: 13px; text-decoration: none;">링커리어에서 공모전 찾아보기 ↗</a></section>
    </sc-if>
    <sc-if value="@@show.policy@@" hint-placeholder-val="@@true@@">
    <section style="display: flex; flex-direction: column; gap: 12px;">{h('청년 취업 지원 정책', '공공 API 연결 예정 · 지금은 공식 사이트로 연결')}<div style="display: grid; grid-template-columns: repeat({pcols}, minmax(0, 1fr)); gap: 12px;">{pol}</div></section>
    </sc-if>
'''


def edu_tabs(mobile):
    btns = ''.join(f'<button type="button" role="tab" onClick="@@tabs.{k}.pick@@" style="@@tabs.{k}.style@@">{l}</button>' for k, l in CATS)
    if mobile:
        return f'<div role="tablist" class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -16px; padding: 0 16px;">{btns}</div>'
    return f'<div role="tablist" style="display: flex; gap: 8px;">{btns}</div>'


def ai_banner(mobile):
    pre = 'm-' if mobile else ''
    return (f'<a href="{pre}S3-compare.dc.html#result" style="display: flex; {"flex-direction: column; align-items: flex-start;" if mobile else "align-items: center;"} gap: {10 if mobile else 16}px; padding: {"16px 18px" if mobile else "18px 24px"}; border-radius: 16px; background: #F4F9FF; color: {INK}; text-decoration: none;">'
            f'{AI}<span style="flex: 1 1 0; font-size: {14 if mobile else 15}px; line-height: 1.5;">내 비교 결과에서 비어 있는 <b style="font-weight: 700;">숏폼 발행, 영상 툴, 트렌드, 실무 경험</b>을 채울 수 있는 것부터 보여드려요</span>'
            f'<span style="flex-shrink: 0; font-size: 13px; font-weight: 600; color: {BLUE};">비교 결과 보기 ›</span></a>')


EDU_PILL = 'flex-shrink: 0; padding: 9px 16px; border-radius: 999px; font-size: 14px; cursor: pointer; white-space: nowrap;'
E1_ON = EDU_PILL + f' border: none; background: {INK}; color: #FFFFFF; font-weight: 600;'
E1_OFF = EDU_PILL + f' border: none; background: #FFFFFF; color: #4E5968;'
e1_body = f'''  <div style="padding: 24px 56px 0; display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">교육과정과 취업 지원</h1><span style="font-size: 15px; color: {SUB};">SeSAC 과정과 청년 취업 정책을 한곳에서 봐요. 신청은 각 기관 사이트에서 해요</span></div>
  <div style="display: flex; flex-direction: column; gap: 24px; padding: 24px 56px 56px;">
    {ai_banner(False)}
    {edu_tabs(False)}
{edu_sections(False)}    <p style="margin: 0; font-size: 12px; color: {MUTE};">출처: SeSAC 과정 정보 (팀 수집 210개, 2026.10.27 기준) · SNS 콘텐츠 마케팅 {SRC104}</p>
  </div>
'''
boards['E1-edu.dc.html'] = ('E1 교육과정 (SeSAC, 자격증, 대외활동, 정책)', dpage('E1-edu.dc.html', '교육과정', 'edu', e1_body, E1_SCRIPT.replace('@@ON@@', E1_ON).replace('@@OFF@@', E1_OFF)))

# --- S5 마이페이지 (내 경험 + 내 경로) ---
MY_SCRIPT = "  renderVals() { return {}; }"


def mytabs(active, mobile=False):
    pre = 'm-' if mobile else ''
    out = ''
    for k, label, href in [('home', '한눈에 보기', 'S5-path.dc.html'), ('saved', '저장함 @@savedCount@@', 'S5-saved.dc.html'), ('resume', '이력서 등록', 'S5-resume.dc.html')]:
        on = k == active
        st = (f'background: #FFFFFF; color: {INK}; font-weight: 600; box-shadow: 0 1px 3px rgba(0,23,51,0.08);' if on else f'color: {SUB};')
        cur = ' aria-current="page"' if on else ''
        out += f'<a href="{pre}{href}"{cur} style="{"flex: 1 1 0; text-align: center; " if mobile else ""}padding: 9px 18px; border-radius: 9px; font-size: 14px; {st} text-decoration: none;">{label}</a>'
    return f'<nav aria-label="마이페이지 메뉴" style="display: {"flex" if mobile else "inline-flex"}; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06); {"" if mobile else "align-self: flex-start;"}">{out}</nav>'


INP_D = f'height: 48px; box-sizing: border-box; padding: 0 14px; font-size: 16px; border: none; border-radius: 12px; font-family: inherit; background: {FILL}; color: {INK}; width: 100%;'
TA_D = f'height: 112px; box-sizing: border-box; padding: 14px; font-size: 16px; line-height: 1.6; border: none; border-radius: 12px; font-family: inherit; resize: none; background: {FILL}; color: {INK}; width: 100%;'


def my_exp(mobile):
    p = 'm-' if mobile else ''
    rows = ''.join(f'<div style="display: flex; gap: 12px; padding: 12px 0; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.5;"><span style="width: 72px; flex-shrink: 0; color: {MUTE};">{k}</span><span>{v}</span></div>'
                   for k, v in [('학력', '미디어커뮤니케이션학과 · 2026.02 졸업 예정'), ('활동', '학생회 홍보부 인스타그램 운영 1년'), ('자격증', '컴퓨터활용능력 2급'), ('어학', 'OPIc IM2'), ('스킬', '캔바, 인스타그램 운영, 엑셀')])
    bar = f'<span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: 73%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span>'
    return f'''    <section aria-labelledby="{p}cv" style="display: flex; flex-direction: column; gap: 12px; padding: {'20px' if mobile else '28px'}; {CARD}">
      <div style="display: flex; justify-content: space-between; align-items: baseline;"><h2 id="{p}cv" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">내 이력서</h2><span style="font-size: 13px; color: {SUB};">15개 항목 중 11개 작성</span></div>
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
    steps = (path_step(1, '목표 공고', '[올리브인터내셔널] 성분에디터 콘텐츠 마케팅 인턴', f'채용연계형 인턴 · <a href="{POSTING}" {EXT} style="text-decoration: none;">원문 공고 ↗</a>')
             + path_step(2, 'AI 비교 결과', '공고 요구 6개 중 맞음 1개, 일부 1개', f'찾지 못함: 숏폼 발행, 영상 툴, 트렌드, 실무 경험 · <a href="{p}S3-compare.dc.html#result" style="text-decoration: none;">다시 보기</a>')
             + path_step(3, '다음 행동 (내가 고름)', 'SeSAC (강북5기) AI 활용 SNS 마케터 양성 과정', f'11/25 개강 · 모집 마감 11/8 · <a href="{SESAC}1421" {EXT} style="text-decoration: none;">과정 페이지 ↗</a>')
             + path_step('·', '그다음', '과정을 마치면 같은 공고와 다시 비교해 보세요', f'<a href="{p}S1-list.dc.html" style="text-decoration: none;">다른 공고와도 비교하기 ›</a>', False))
    return f'''    <section aria-labelledby="{p}path" style="display: flex; flex-direction: column; gap: 16px; padding: {'20px' if mobile else '28px'}; {CARD}">
      <h2 id="{p}path" style="margin: 0; font-size: {18 if mobile else 20}px; font-weight: 700;">내 취업 경로</h2>
      <ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 14px;">{steps}</ol>
    </section>
'''


def my_profile(mobile):
    p = 'm-' if mobile else ''
    return f'''    <section style="display: flex; flex-direction: column; gap: 14px; padding: {'20px' if mobile else '24px'}; {CARD}">
      <div style="display: flex; align-items: center; gap: 14px;"><span aria-hidden="true" style="width: 52px; height: 52px; border-radius: 50%; background: {BLUE_BG}; display: flex; align-items: center; justify-content: center;"><svg width="26" height="26" viewBox="0 0 24 24">{ICON_ON['my']}</svg></span><span style="display: flex; flex-direction: column; gap: 3px;"><span style="font-size: 17px; font-weight: 700;">@@profileName@@</span><span style="font-size: 13px; color: {SUB};">취업 준비생 · 미디어커뮤니케이션학과</span></span></div>
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

# ===================== mobile =====================
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

m_s1 = f'''    <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 8px 4px 4px;"><div style="display: flex; flex-direction: column; gap: 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">SNS 콘텐츠 마케팅</h1><span style="font-size: 13px; color: {SUB};">@@count@@</span></div><button type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; background: none; padding: 0 0 2px; font-size: 13px; font-weight: 600; color: {BLUE}; cursor: pointer;">트렌드 ›</button></div>
    <div role="tablist" aria-label="경력 구분" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);"><button type="button" role="tab" onClick="@@pickNew@@" style="@@newStyle@@">신입, 인턴</button><button type="button" role="tab" onClick="@@pickExp@@" style="@@expStyle@@">경력</button></div>
    <sc-if value="@@isNew@@" hint-placeholder-val="@@true@@">
{fit_card(True)}    </sc-if>
    <sc-if value="@@isExp@@" hint-placeholder-val="@@false@@">
{exp_card(True)}    </sc-if>
{list_card(True)}{trend_popup(True, None)}'''
m_s1_script = LIST_JS.replace('@@ON@@', seg_style(True, True)).replace('@@OFF@@', seg_style(False, True))
boards['m-S1-list.dc.html'] = ('M1 직무 찾기 (모바일)', mpage('m-S1-list.dc.html', 'M1 직무 찾기 (모바일)', topbar_logo(auth_mobile()), m_s1, 'find', m_s1_script))

m_s3 = f'''    <section style="display: flex; flex-direction: column; gap: 14px; padding: 20px; {CARD}">
      <div style="display: flex; align-items: center; gap: 12px;">{mark('olive', 40)}<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 13px; font-weight: 600;">올리브인터내셔널</span><span style="font-size: 11px; color: {MUTE};">뷰티 브랜드 성분에디터 · 마케팅본부</span></span>{save_btn('sv.olive', 38)}</div>
      <h1 style="margin: 0; font-size: 19px; font-weight: 700; line-height: 1.4;">[마케팅본부] 성분에디터 콘텐츠 마케팅 인턴 (채용연계형)</h1>
      <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; padding: 12px 14px; background: #F9FAFB; border-radius: 12px; font-size: 13px;"><span><span style="color: {MUTE};">고용</span> 인턴 (채용연계)</span><span><span style="color: {MUTE};">경력</span> 무관</span><span><span style="color: {MUTE};">직무</span> 콘텐츠 마케터</span><span><span style="color: {MUTE};">마감</span> 채용 시 마감</span></div>
      <div style="display: flex; flex-direction: column; gap: 10px;"><span style="font-size: 14px; font-weight: 700;">공고가 원하는 것 6</span><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;">{REQ_HTML}</ul></div>
      <a href="{POSTING}" {EXT} style="font-size: 13px; text-decoration: none;">원문 공고 전체 보기 ↗</a>
    </section>
{exp_strip(True)}{run_card(True)}    <sc-if value="@@done@@" hint-placeholder-val="@@false@@">
{result_head(True)}    <section style="display: flex; flex-direction: column; padding: 18px 18px 6px; {CARD}">
      <h2 style="margin: 0 0 8px; font-size: 17px; font-weight: 700;">이어지는 경험 <span style="color: {BLUE};">2</span></h2>
      {match('맞음', BLUE_D, BLUE_BG, '우대 · SNS 채널 운영', '개인 또는 비즈니스 채널을 직접 운영하며 고객 반응을 이끌어낸', '학생회 홍보부 인스타그램 운영 1년, 팔로워 300명에서 1,200명')}
      {match('일부', OR, OR_BG, '자격요건 · 성과 분석', '콘텐츠의 성과를 객관적인 수치로 분석하고, 다음 액션을 제안', '팔로워 300명에서 1,200명', '무엇을 보고 무엇을 바꿨는지 한 문장 더하면 맞음이 돼요')}
    </section>
    <section style="display: flex; flex-direction: column; padding: 18px 18px 14px; {CARD}">
      <h2 style="margin: 0 0 8px; font-size: 17px; font-weight: 700;">아직 비어 있는 것 <span style="color: {MUTE};">4</span></h2>
      {gap('숏폼 발행 경험', '우대 · 입력엔 카드뉴스만 있어요', 'm-S4-activity.dc.html', '프로젝트')}
      {gap('Premiere Pro, Photoshop으로 직접 구현', '우대 · 캔바만 찾았어요', 'm-S4-next.dc.html', 'SeSAC')}
      {gap('최신 콘텐츠 트렌드와 밈에 관심', '자격요건 · 찾지 못했어요', 'm-S1-list.dc.html#trend', '트렌드')}
      {gap('학회, 공모전, 인턴십 등 실무 경험', '우대 · 찾지 못했어요', 'm-S4-activity.dc.html', '공모전')}
      <a href="m-S5-resume.dc.html" style="margin-top: 6px; font-size: 12px; color: {SUB}; text-decoration: none;">빠뜨린 경험이 있나요? <span style="color: {BLUE};">이력서에서 고치기 ›</span></a>
    </section>
    <div style="display: flex; flex-direction: column; gap: 4px; margin-top: 12px; padding: 0 4px;"><h2 style="margin: 0; font-size: 19px; font-weight: 700;">어느 부분을 먼저 채울까요?</h2><span style="font-size: 12px; color: {SUB};">고르는 건 나. 4가지 모두 언제든 볼 수 있어요</span></div>
    {choice('m-S4-next.dc.html', 'edu', '교육으로 배우기', 'SeSAC 과정 2개 모집 중', '빈 칸 2개')}
    {choice('m-S4-cert.dc.html', 'cert', '자격증, 어학', '이 직무 공고 언급 3%')}
    {choice('m-S4-activity.dc.html', 'act', '대외활동, 프로젝트', '숏폼 직접 발행해 보기')}
    {choice('m-S4-apply.dc.html', 'apply', '지원 준비', '지금 경험으로 지원하기')}
    </sc-if>
'''
boards['m-S3-compare.dc.html'] = ('M2 공고 + AI 비교 + 다음 행동 (모바일)', mpage('m-S3-compare.dc.html', 'M2 공고와 내 경험 비교 (모바일)', topbar_flow('m-S1-list.dc.html', '공고와 비교', 2), m_s3, 'find', COMPARE_SCRIPT, saves=('olive',)))

m_e1 = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">교육과정과 취업 지원</h1><span style="font-size: 13px; line-height: 1.5; color: {SUB};">SeSAC 과정과 청년 취업 정책을 한곳에서 봐요. 신청은 각 기관 사이트에서 해요</span></div>
    {ai_banner(True)}
    {edu_tabs(True)}
{edu_sections(True)}    <span style="padding: 0 4px; font-size: 11px; line-height: 1.5; color: {MUTE};">출처: SeSAC 과정 정보 (팀 수집 210개, 2026.10.27 기준) · SNS 콘텐츠 마케팅 {SRC104}</span>
'''
boards['m-E1-edu.dc.html'] = ('ME1 교육과정 (모바일)', mpage('m-E1-edu.dc.html', 'ME1 교육과정 (모바일)', topbar_logo(), m_e1, 'edu', E1_SCRIPT.replace('@@ON@@', E1_ON).replace('@@OFF@@', E1_OFF)))

m_s5 = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 13px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아요</span></div>
    {mytabs('home', True)}
{my_profile(True).split('    <a href=')[0]}{my_exp(True)}{my_path(True)}    <a href={my_profile(True).split('    <a href=')[1]}'''
boards['m-S5-path.dc.html'] = ('M5 마이페이지 (모바일)', mpage('m-S5-path.dc.html', 'M5 마이페이지 (모바일)', topbar_logo(auth_mobile()), m_s5, 'my', MY_SCRIPT))

# --- S5b 이력서 등록 (마이페이지 두 번째 탭) ---
# 15 sections like a job-board resume. Filled ones show the persona, empty optional ones fold into one line.
RSEC = [('basic', '인적사항', True, True), ('job', '희망 직무', True, True), ('skill', '스킬', True, False), ('school', '학력', True, True),
        ('career', '경력', True, False), ('act', '인턴, 대외활동', True, False), ('train', '교육', False, False), ('cert', '자격증', True, False),
        ('award', '수상', False, False), ('abroad', '해외 경험', False, False), ('lang', '어학', True, False), ('pf', '포트폴리오', True, False),
        ('pref', '취업 우대, 병역', False, False), ('intro', '자기소개서', True, False), ('cond', '희망 근무 조건', True, False)]
FOLD = [k for k, _, filled, _ in RSEC if not filled]
INTRO = ('학생회 홍보부에서 1년 동안 인스타그램 계정을 맡았습니다. 매주 카드뉴스를 캔바로 만들어 올렸고, 팔로워는 300명에서 1,200명으로 늘었습니다. '
         '반응이 좋았던 게시물의 공통점을 정리해 다음 기획에 반영했던 경험을 살려, 숫자로 이야기하는 콘텐츠 마케터가 되고 싶습니다.')


def rf(label, val='', ph='', span=1, req=False, kind='text'):
    star = f' <span style="color: {RED};">*</span>' if req else ''
    v = f' value="{val}"' if val else ''
    return (f'<label style="grid-column: span {span}; display: flex; flex-direction: column; gap: 6px; min-width: 0;"><span style="font-size: 13px; color: {SUB};">{label}{star}</span>'
            f'<input type="{kind}"{v} placeholder="{ph}" style="{INP_D} font-size: 15px;"></label>')


def rta(label, val='', ph='', h=96, span=2, count=''):
    c = f'<span style="align-self: flex-end; font-size: 12px; color: {MUTE};">{count}</span>' if count else ''
    return (f'<label style="grid-column: span {span}; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 13px; color: {SUB};">{label}</span>'
            f'<textarea placeholder="{ph}" style="{TA_D} height: {h}px; font-size: 15px;">{val}</textarea>{c}</label>')


def rgrid(cols, *fields):
    return f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;">{"".join(fields)}</div>'


def rentry(*rows):
    return f'<div style="display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: 14px; background: #F9FAFB;">{"".join(rows)}</div>'


def radd(label):
    return f'<button type="button" style="height: 44px; border: 1.5px dashed #D1D6DB; border-radius: 12px; background: #FFFFFF; color: {SUB}; font-size: 14px; cursor: pointer;">+ {label} 추가</button>'


def rchips(items, on=True):
    x = '<span aria-hidden="true" style="margin-left: 4px; opacity: 0.6;">✕</span>'
    return ''.join(f'<span style="display: inline-flex; align-items: center; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG if on else FILL}; color: {BLUE_D if on else "#4E5968"}; font-size: 14px;">{t}{x if on else ""}</span>' for t in items)


def rcard(key, title, body, sub='', mobile=False):
    return (f'    <section id="{"m-" if mobile else ""}r-{key}" aria-labelledby="{"m-" if mobile else ""}rh-{key}" style="display: flex; flex-direction: column; gap: 16px; padding: {"20px 18px" if mobile else "26px 28px"}; {CARD} scroll-margin-top: 16px;">\n'
            f'      <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px;"><h2 id="{"m-" if mobile else ""}rh-{key}" style="margin: 0; font-size: {17 if mobile else 19}px; font-weight: 700;">{title}</h2><span style="font-size: 12px; color: {MUTE}; text-align: right;">{sub}</span></div>\n'
            f'      {body}\n    </section>\n')


def rfold(key, title, hint, body, mobile=False):
    """Empty optional section: one line until opened."""
    return (f'    <sc-if value="@@shut.{key}@@" hint-placeholder-val="@@true@@">\n'
            f'    <div id="{"m-" if mobile else ""}r-{key}" style="display: flex; align-items: center; gap: 12px; padding: {"16px 18px" if mobile else "18px 28px"}; {CARD}"><span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 16px; font-weight: 700;">{title}</span><span style="font-size: 12px; color: {MUTE};">{hint}</span></span>'
            f'<button type="button" onClick="@@toggle.{key}@@" style="flex-shrink: 0; height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">+ 추가</button></div>\n'
            f'    </sc-if>\n    <sc-if value="@@open.{key}@@" hint-placeholder-val="@@false@@">\n'
            + rcard(key, title, body + f'<button type="button" onClick="@@toggle.{key}@@" style="align-self: flex-start; border: none; background: none; padding: 0; font-size: 13px; color: {MUTE}; cursor: pointer;">접기</button>', '선택', mobile)
            + '    </sc-if>\n')


def resume_sections(mobile):
    c2, c3, c4 = (2, 2, 2) if mobile else (2, 3, 4)
    tools = '<span style="font-size: 12px; color: {}; ">공고에서 많이 찾는 툴</span>'.format(SUB)
    sugg = ''.join(f'<span style="padding: 7px 12px; border-radius: 999px; border: 1px solid #E5E8EB; font-size: 13px; color: #4E5968;">+ {t} <span style="color: {MUTE};">{n}건</span></span>' for t, n in [('프리미어', 30), ('포토샵', 28), ('피그마', 19), ('캡컷', 10)])
    photo = (f'<span aria-hidden="true" style="width: 96px; height: 120px; flex-shrink: 0; border-radius: 12px; border: 1.5px dashed #D1D6DB; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: {MUTE}; font-size: 12px;">'
             f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="9" r="3.5"/><path d="M5 20c1-3.5 3.8-5 7-5s6 1.5 7 5"/></svg>사진 · 선택</span>')
    basic = (rgrid(c3, rf('이름', '김하늘', req=True), rf('생년월일', '2002.03.14', req=True), rf('성별', '여', 'ex. 여'), rf('이메일', '', 'name@example.com', req=True, kind='email'), rf('휴대폰', '', '010-0000-0000', req=True, kind='tel'), rf('주소', '서울 성북구', '시, 구까지만'))
             + rgrid(1, rf('홈페이지, SNS', '', 'https://')))
    basic = basic if mobile else f'<div style="display: flex; gap: 20px; align-items: flex-start;"><div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 12px;">{basic}</div>{photo}</div>'
    out = ''
    out += rcard('basic', '인적사항', basic, '연락처는 기업에만 보여요', mobile)
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
    pref = ''.join(f'<label style="display: flex; align-items: center; gap: 8px; padding: 12px 14px; border-radius: 12px; background: {FILL}; font-size: 14px; cursor: pointer;"><input type="checkbox" style="width: 17px; height: 17px; accent-color: {BLUE};">{t}</label>' for t in ['보훈 대상', '취업 보호 대상', '고용 지원금 대상', '장애', '병역'])
    out += rfold('pref', '취업 우대, 병역', '해당할 때만', f'<div style="display: grid; grid-template-columns: repeat({2 if mobile else 5}, minmax(0, 1fr)); gap: 8px;">{pref}</div>', mobile)
    out += rcard('intro', '자기소개서', rgrid(1, rf('제목', '숫자로 이야기하는 콘텐츠 마케터')) + rta('내용', INTRO, h=150 if mobile else 128, span=1, count=f'{len(INTRO)} / 1,000자'),
                 f'{AI} 이력서로 초안 만들기', mobile)
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
      <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 6px;"><span style="font-size: 15px; font-weight: 700;">15개 중 11개 작성</span><span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: 73%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span></div>
      <nav aria-label="이력서 항목" style="display: flex; flex-direction: column;">{items}</nav>
      <button type="button" onClick="@@save@@" style="height: 52px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; cursor: pointer;">이력서 저장</button>
      <sc-if value="@@saved@@" hint-placeholder-val="@@false@@"><span style="padding: 0 6px; font-size: 12px; line-height: 1.5; color: {BLUE_D};">저장했어요 · 시연용이라 실제로 저장되지 않아요</span></sc-if>
    </aside>
'''


def resume_ai(mobile):
    return f'''    <div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 12px; padding: {"16px 18px" if mobile else "18px 24px"}; border-radius: 20px; background: #F4F9FF;">
      <span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 4px;"><span style="display: flex; align-items: center; gap: 6px; font-size: 15px; font-weight: 700;">{AI}이력서 PDF가 있나요?</span><span style="font-size: 13px; line-height: 1.5; color: {SUB};">올리면 AI가 항목을 나눠 채워요. 채운 뒤 맞는지만 확인하면 돼요</span></span>
      <button type="button" onClick="@@toggleAi@@" style="flex-shrink: 0; height: 44px; padding: 0 18px; border: none; border-radius: 12px; background: #FFFFFF; color: {BLUE_D}; font-size: 14px; font-weight: 600; cursor: pointer;">@@aiLabel@@</button>
    </div>
    <sc-if value="@@aiDone@@" hint-placeholder-val="@@false@@"><div style="display: flex; align-items: center; gap: 8px; padding: 12px 16px; border-radius: 14px; background: #F0EBFF; font-size: 14px; color: #4B36B5;">{AI}예시 이력서에서 11개 항목을 채웠어요. 비어 있는 4개는 접어 두었어요</div></sc-if>
'''


_fold_js = ', '.join(f'{k}: false' for k in FOLD)
RESUME_SCRIPT = ("  constructor(props) { super(props); this.state = { open: { " + _fold_js + " }, ai: false, saved: false }; }\n"
                 "  renderVals() {\n    const o = this.state.open, toggle = {}, shut = {};\n"
                 "    Object.keys(o).forEach(k => { shut[k] = !o[k]; toggle[k] = () => this.setState({ open: Object.assign({}, o, { [k]: !o[k] }) }); });\n"
                 "    const a = this.state.ai;\n"
                 "    return { open: o, shut, toggle, aiDone: a, aiLabel: a ? '다시 올리기' : 'PDF 올리기', toggleAi: () => this.setState({ ai: !a }), saved: this.state.saved, save: () => this.setState({ saved: true }) };\n  }")

resume_body = f'''  <div style="padding: 24px 56px 0; display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 15px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아도 돼요</span><div style="margin-top: 12px;">{mytabs('resume')}</div></div>
  <div style="display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 24px; padding: 24px 56px 56px; align-items: start;">
{resume_nav()}    <div style="display: flex; flex-direction: column; gap: 14px; min-width: 0;">
{resume_ai(False)}{resume_sections(False)}    </div>
  </div>
'''
boards['S5-resume.dc.html'] = ('S5b 마이페이지 · 이력서 등록', dpage('S5-resume.dc.html', '이력서 등록', 'my', resume_body, RESUME_SCRIPT))

m_jump = ''.join(f'<a href="#m-r-{k}" style="flex-shrink: 0; padding: 7px 12px; border-radius: 999px; background: {BLUE_BG if f else "#FFFFFF"}; color: {BLUE_D if f else SUB}; font-size: 13px; text-decoration: none;">{n}</a>' for k, n, f, _ in RSEC)
m_resume = f'''    <div style="display: flex; flex-direction: column; gap: 6px; padding: 8px 4px 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">마이페이지</h1><span style="font-size: 13px; color: {SUB};">이력서를 한 번 등록하면 공고마다 다시 입력하지 않아요</span></div>
    {mytabs('resume', True)}
    <div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 18px; {CARD}"><span style="font-size: 15px; font-weight: 700;">15개 중 11개 작성</span><span style="display: block; height: 6px; border-radius: 999px; background: {FILL};"><span style="display: block; width: 73%; height: 6px; border-radius: 999px; background: {BLUE};"></span></span>
      <nav aria-label="이력서 항목" class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; margin: 0 -18px; padding: 2px 18px;">{m_jump}</nav></div>
{resume_ai(True)}{resume_sections(True)}    <button type="button" onClick="@@save@@" style="height: 54px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; cursor: pointer;">이력서 저장</button>
    <sc-if value="@@saved@@" hint-placeholder-val="@@false@@"><span style="text-align: center; font-size: 12px; color: {BLUE_D};">저장했어요 · 시연용이라 실제로 저장되지 않아요</span></sc-if>
'''
boards['m-S5-resume.dc.html'] = ('M5b 이력서 등록 (모바일)', mpage('m-S5-resume.dc.html', 'M5b 이력서 등록 (모바일)', topbar_logo(auth_mobile()), m_resume, 'my', RESUME_SCRIPT))

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
            + ('' if mobile else f'<a href="S3-compare.dc.html#result" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 비교 결과</a>')
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


def next_edu(mobile):
    meta = lambda k, v: f'<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: {MUTE};">{k}</span><span style="font-size: 14px; font-weight: 600;">{v}</span></div>'
    lay = 'flex-direction: column;' if mobile else ''
    img_w = '100%; height: 170px;' if mobile else '260px; height: 200px;'
    c1 = (f'<div style="display: flex; {lay} gap: 20px;"><img src="{THUMB1}" alt="" style="width: {img_w} flex-shrink: 0; object-fit: cover; border-radius: 14px; display: block;">'
          f'<div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 12px; min-width: 0;"><div style="display: flex; gap: 6px;"><span style="padding: 3px 9px; border-radius: 999px; background: {BLUE_BG}; color: {BLUE_D}; font-size: 12px; font-weight: 600;">모집 중 · 11.08 마감</span><span style="padding: 3px 9px; border-radius: 999px; background: {FILL}; color: {SUB}; font-size: 12px;">강북 · 디지털마케팅</span></div>'
          f'<span style="font-size: 19px; font-weight: 700; line-height: 1.4;">(강북5기) AI 활용 SNS 마케터 양성 과정</span>'
          f'<div style="display: grid; grid-template-columns: repeat({2 if mobile else 3}, minmax(0, 1fr)); gap: 12px; padding: 12px 14px; border-radius: 12px; background: #F9FAFB;">{meta("교육 기간", "2026.11.25 ~ 2027.03.17")}{meta("교육 시간", "420시간")}{meta("비용", "무료 (예치금 반환)")}</div>'
          f'<span style="font-size: 13px; color: {SUB};">#AI #SNS마케팅 #콘텐츠마케팅 #퍼포먼스마케팅 #마케팅자동화</span></div></div>'
          f'<div style="display: flex; gap: 8px; padding: 12px 14px; border-radius: 12px; background: {OR_BG}; color: {OR}; font-size: 13px; line-height: 1.5;">과정 키워드에 "숏폼, 영상 편집"은 없어요. 커리큘럼에 영상 실습이 있는지 SeSAC 페이지에서 확인해 보세요</div>'
          + btnrow(pbtn(SESAC + '1421', 'SeSAC에서 과정 보기 ↗', True, True), save_btn('sv.e1421', 46)))
    c2 = (f'<div style="display: flex; gap: 16px; align-items: center;"><img src="{THUMB2}" alt="" style="width: {88 if mobile else 120}px; height: {88 if mobile else 90}px; flex-shrink: 0; object-fit: cover; border-radius: 12px; display: block;">'
          f'<div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 6px; min-width: 0;"><span style="font-size: 12px; color: {BLUE_D}; font-weight: 600;">모집 중 · 11.10 마감 · 금천</span><span style="font-size: 16px; font-weight: 700; line-height: 1.4;">전Z전능 브랜드 마케팅 실전 과정</span><span style="font-size: 13px; color: {SUB};">2026.11.30 ~ 2027.02.26 · 360시간 · #GA4 #메타광고</span></div>'
          f'{save_btn("sv.e1235")}<a href="{SESAC}1235" {EXT} style="flex-shrink: 0; font-size: 14px; font-weight: 600; text-decoration: none;">보기 ↗</a></div>')
    c3 = (f'<div style="display: flex; gap: 16px; align-items: center; opacity: 0.7;"><div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 12px; color: {MUTE}; font-weight: 600;">지금 모집 중인 기수 없음 · 10.02 종료</span><span style="font-size: 16px; font-weight: 700; line-height: 1.4;">(강동7기) 생성형 AI 기반 숏폼 영상콘텐츠 제작 실무과정</span><span style="font-size: 13px; color: {SUB};">숏폼 전문 과정 · 다음 기수가 열리면 알려 드릴게요</span></div>'
          f'{save_btn("sv.e1266")}<a href="{SESAC}1266" {EXT} style="flex-shrink: 0; font-size: 14px; font-weight: 600; text-decoration: none;">지난 기수 ↗</a></div>')
    src = f'<span style="font-size: 12px; color: {MUTE};">출처: SeSAC 과정 정보 (팀 수집 210개, 2026.10.27 기준). 연결은 과정명과 해시태그 기준</span>'
    return (sec('가장 가까운 과정', c1, 'SeSAC 마케팅 분야 · 모집 중 2', mobile) + sec('다른 과정', c2 + f'<div style="height: 1px; background: {LINE};"></div>' + c3, '', mobile) + f'    {src}\n')


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


NEXT_PAGES = [('S4-next.dc.html', 'edu', 'S3 다음 행동 · 교육', '숏폼, 영상 툴을 배울 수 있는 SeSAC 과정', '비어 있는 4개 중 "숏폼 발행"과 "영상 툴"을 과정으로 채울 수 있어요', next_edu),
              ('S4-cert.dc.html', 'cert', 'S3b 자격증, 어학', '자격증보다 툴로 만든 결과물을 봐요', '이 직무 공고 104건에서 자격증, 툴, 어학을 얼마나 적었는지 세어 봤어요', next_cert),
              ('S4-activity.dc.html', 'act', 'S3c 대외활동, 프로젝트', '숏폼을 직접 발행해 본 경험을 만들어요', '비어 있는 "숏폼 발행"과 "실무 경험"을 프로젝트로 채워요', next_act),
              ('S4-apply.dc.html', 'apply', 'S3d 지원 준비', '지금 경험으로 지원해 볼 수 있어요', '맞는 경험을 앞에 두고, 빈 것은 솔직하게 두고 가요', next_apply)]
for fname, key, btitle, title, lead, fn in NEXT_PAGES:
    sv_keys = ('e1421', 'e1235', 'e1266') if key == 'edu' else ()
    boards[fname] = (btitle, dpage(fname, title, 'find', next_page(key, title, lead, fn(False), False), NEXT_SCRIPT, saves=sv_keys))
    mname = 'm-' + fname
    body = next_page(key, title, lead, fn(True).replace('href="S4-', 'href="m-S4-'), True)
    boards[mname] = ('M' + btitle[1:] + ' (모바일)', mpage(mname, btitle + ' (모바일)', topbar_back('m-S3-compare.dc.html#result', '다음 행동'), body, 'find', NEXT_SCRIPT, saves=sv_keys))

# ===== v5 pages: 교육과정 for 200+ items, 저장함, 로그인, 회원가입 =====
COURSE_JSON = json.dumps(COURSES_ALL, ensure_ascii=False)
POL_JSON = json.dumps(POL_ALL, ensure_ascii=False)
GCOL = {'마케팅': ('#FFF4E5', '#C26A00'), 'AI': ('#F0EBFF', '#6B4EE6'), '데이터': ('#E8F3FF', '#1B64DA'), '기획, PM': ('#E6F7F1', '#0E8A63'),
        '개발': ('#EEF1F5', '#4E5968'), '디자인': ('#FFEEF3', '#D6336C'), '기타': ('#F2F4F6', '#6B7684')}
STC = {'모집 중': (BLUE_BG, BLUE_D), '모집 예정': (OR_BG, OR), '상시': ('#E6F7F1', '#0E8A63'), '진행 중': (FILL, SUB), '종료': (FILL, MUTE),
       '신청 중': (BLUE_BG, BLUE_D), '예정': (OR_BG, OR), '마감': (FILL, MUTE)}
THUMBS = {'edu-1421': THUMB1, 'edu-1235': THUMB2}
N_LIVE = sum(1 for c in COURSES_ALL if c['st'] in ('모집 중', '모집 예정', '상시'))

E1_JS = '''  constructor(props) { super(props); const h = (typeof location !== 'undefined' && location.hash) || ''; this.state = { tab: h === '#policy' ? 'pol' : h === '#cert' ? 'cert' : h === '#act' ? 'act' : 'edu', q: '', g: 'all', live: true, sort: 'rec', page: 1, pq: '', pc: 'all', pr: 'all', pOpen: false, pp: 1 }; }
  pageVals() {
    const C = __C__, P = __P__, GC = __GC__, SC = __SC__, TH = __TH__;
    const s = this.state, set = (o) => this.setState(o);
    const tabStyle = (on) => on ? '__TON__' : '__TOFF__', pill = (on) => on ? '__PON__' : '__POFF__', srt = (on) => on ? '__SON__' : '__SOFF__';
    const pg = (on) => on ? '__GON__' : '__GOFF__';
    const badge = (st) => 'padding: 3px 9px; border-radius: 999px; background: ' + (SC[st] || SC['종료'])[0] + '; color: ' + (SC[st] || SC['종료'])[1] + '; font-size: 12px; font-weight: 600; white-space: nowrap;';
    const pager = (page, pages, key) => { const nums = []; const lo = Math.max(1, Math.min(page - 2, pages - 4)), hi = Math.min(pages, lo + 4); for (let i = lo; i <= hi; i++) nums.push({ n: i, style: pg(i === page), cur: i === page ? 'page' : 'false', go: () => set({ [key]: i }) }); return { nums, prev: () => set({ [key]: Math.max(1, page - 1) }), next: () => set({ [key]: Math.min(pages, page + 1) }), prevStyle: pg(false) + (page === 1 ? ' opacity: 0.35;' : ''), nextStyle: pg(false) + (page === pages ? ' opacity: 0.35;' : ''), first: pages > 5 && lo > 1, last: pages > 5 && hi < pages, pages, goFirst: () => set({ [key]: 1 }), goLast: () => set({ [key]: pages }) }; };
    const T = (k) => ({ style: tabStyle(s.tab === k), go: () => set({ tab: k }) });
    // SeSAC courses
    const isLive = (c) => c.st === '모집 중' || c.st === '모집 예정' || c.st === '상시';
    const q = s.q.trim().toLowerCase();
    const base = C.filter((c) => (!s.live || isLive(c)) && (!q || (c.n + ' ' + c.cp + ' ' + c.f + ' ' + c.tags.join(' ')).toLowerCase().indexOf(q) >= 0));
    const groups = ['all', '마케팅', 'AI', '데이터', '기획, PM', '개발', '디자인', '기타'].map((g) => ({ label: (g === 'all' ? '전체' : g) + ' ' + base.filter((c) => g === 'all' || c.g === g).length, style: pill(s.g === g), go: () => set({ g, page: 1 }) }));
    let L = base.filter((c) => s.g === 'all' || c.g === s.g);
    const rank = (c) => ({ '모집 중': 0, '모집 예정': 1, '상시': 2, '진행 중': 3, '종료': 4 })[c.st];
    if (s.sort === 'rec') L = L.slice().sort((a, b) => ((b.g === '마케팅') - (a.g === '마케팅')) || (rank(a) - rank(b)) || (b.rv - a.rv));
    if (s.sort === 'close') L = L.slice().sort((a, b) => (rank(a) - rank(b)) || (a.recEnd || '9').localeCompare(b.recEnd || '9'));
    if (s.sort === 'rv') L = L.slice().sort((a, b) => b.rv - a.rv);
    const per = __PER__, pages = Math.max(1, Math.ceil(L.length / per)), page = Math.min(s.page, pages);
    const cards = L.slice((page - 1) * per, page * per).map((c) => {
      const sv = this.sv({ id: c.id, kind: '교육', t: c.n, s: 'SeSAC ' + c.cp + ' · ' + c.st + (c.recEnd && c.st === '모집 중' ? ' · ' + c.recEnd.slice(5) + ' 마감' : ''), u: c.u, h: c.id === 'edu-1421' ? 'C2-course.dc.html' : '' });
      const col = GC[c.g] || GC['기타'];
      return { n: c.n, cp: c.cp, f: c.f, st: c.st, stStyle: badge(c.st), edu: c.edu, h: c.h, tags: c.tags.map((t) => '#' + t.replace(/^#/, '')), rv: c.rv, hasRv: c.rv > 0, u: c.u,
        due: c.st === '모집 중' && c.recEnd ? c.recEnd.slice(5).replace('.', '.') + ' 마감' : '', hasDue: c.st === '모집 중' && !!c.recEnd,
        thumb: TH[c.id] || '', hasThumb: !!TH[c.id], noThumb: !TH[c.id], band: 'background: ' + col[0] + '; color: ' + col[1] + ';', g: c.g, sv,
        detail: c.id === 'edu-1421', noDetail: c.id !== 'edu-1421', dhref: '__DPRE__C2-course.dc.html' };
    });
    const cp = pager(page, pages, 'page');
    // policies
    const pq = s.pq.trim().toLowerCase();
    const pbase = P.filter((p) => (s.pr === 'all' || p.r === s.pr) && (!s.pOpen || p.st === '신청 중' || p.st === '상시') && (!pq || (p.n + ' ' + p.o + ' ' + p.k.join(' ') + ' ' + p.d).toLowerCase().indexOf(pq) >= 0));
    const pcats = ['all', '취업', '창업', '재직자', '권익보호'].map((c) => ({ label: (c === 'all' ? '전체' : c) + ' ' + pbase.filter((p) => c === 'all' || p.c === c).length, style: pill(s.pc === c), go: () => set({ pc: c, pp: 1 }) }));
    const PL = pbase.filter((p) => s.pc === 'all' || p.c === s.pc).slice().sort((a, b) => ({ '신청 중': 0, '상시': 1, '예정': 2, '마감': 3 })[a.st] - ({ '신청 중': 0, '상시': 1, '예정': 2, '마감': 3 })[b.st] || (b.r === '서울') - (a.r === '서울') || b.v - a.v);
    const pper = 10, ppages = Math.max(1, Math.ceil(PL.length / pper)), ppage = Math.min(s.pp, ppages);
    const pols = PL.slice((ppage - 1) * pper, ppage * pper).map((p) => ({ n: p.n, o: p.o, r: p.r, c: p.c, k: p.k, hasK: p.k.length > 0, d: p.d, st: p.st, stStyle: badge(p.st), per: p.per, u: p.u,
      detail: p.id === 'pol-20261018005400213991', noDetail: p.id !== 'pol-20261018005400213991', dhref: '__DPRE__P2-policy.dc.html',
      sv: this.sv({ id: p.id, kind: '정책', t: p.n, s: p.o + ' · ' + p.st, u: p.u, h: p.id === 'pol-20261018005400213991' ? 'P2-policy.dc.html' : '' }) }));
    const pp = pager(ppage, ppages, 'pp');
    return { tabs: { edu: T('edu'), pol: T('pol'), cert: T('cert'), act: T('act') }, isEdu: s.tab === 'edu', isPol: s.tab === 'pol', isCert: s.tab === 'cert', isAct: s.tab === 'act',
      q: s.q, setQ: (e) => set({ q: e && e.target ? e.target.value : '', page: 1 }), groups, live: { style: pill(s.live), go: () => set({ live: !s.live, page: 1 }), label: s.live ? '✓ 모집 중, 예정만' : '모집 중, 예정만' },
      sort: { rec: { style: srt(s.sort === 'rec'), go: () => set({ sort: 'rec', page: 1 }) }, close: { style: srt(s.sort === 'close'), go: () => set({ sort: 'close', page: 1 }) }, rv: { style: srt(s.sort === 'rv'), go: () => set({ sort: 'rv', page: 1 }) } },
      cards, total: L.length, range: L.length ? ((page - 1) * per + 1) + '–' + Math.min(page * per, L.length) : '0', empty: L.length === 0, hasCards: L.length > 0, cp,
      clear: () => set({ q: '', g: 'all', live: false, page: 1 }),
      pq: s.pq, setPq: (e) => set({ pq: e && e.target ? e.target.value : '', pp: 1 }), pcats,
      preg: { all: { style: pill(s.pr === 'all'), go: () => set({ pr: 'all', pp: 1 }) }, seoul: { style: pill(s.pr === '서울'), go: () => set({ pr: '서울', pp: 1 }) }, gov: { style: pill(s.pr === '중앙부처'), go: () => set({ pr: '중앙부처', pp: 1 }) } },
      popen: { style: pill(s.pOpen), go: () => set({ pOpen: !s.pOpen, pp: 1 }), label: s.pOpen ? '✓ 신청 가능만' : '신청 가능만' },
      pols, ptotal: PL.length, prange: PL.length ? ((ppage - 1) * pper + 1) + '–' + Math.min(ppage * pper, PL.length) : '0', pempty: PL.length === 0, hasPols: PL.length > 0, pp,
      pclear: () => set({ pq: '', pc: 'all', pr: 'all', pOpen: false, pp: 1 }) };
  }'''


def e1_js(mobile):
    TAB = 'flex-shrink: 0; height: 44px; padding: 0 18px; border: none; border-radius: 12px; font-size: 15px; cursor: pointer; white-space: nowrap;'
    js = (E1_JS.replace('__C__', COURSE_JSON).replace('__P__', POL_JSON).replace('__GC__', json.dumps(GCOL, ensure_ascii=False)).replace('__SC__', json.dumps(STC, ensure_ascii=False))
          .replace('__TH__', json.dumps(THUMBS)).replace('__PER__', '6' if mobile else '9').replace('__DPRE__', 'm-' if mobile else '')
          .replace('__TON__', TAB + f' background: {INK}; color: #FFFFFF; font-weight: 700;').replace('__TOFF__', TAB + ' background: #FFFFFF; color: #4E5968;')
          .replace('__PON__', PILL_ON).replace('__POFF__', PILL_OFF).replace('__SON__', SORT_ON).replace('__SOFF__', SORT_OFF).replace('__GON__', PG_ON).replace('__GOFF__', PG_OFF))
    return js


def pager_html(p, mobile):
    return (f'<nav aria-label="페이지" style="display: flex; justify-content: center; align-items: center; gap: 4px; padding-top: {10 if mobile else 16}px;">'
            f'<button type="button" onClick="@@{p}.prev@@" aria-label="이전 페이지" style="@@{p}.prevStyle@@">‹</button>'
            f'<sc-if value="@@{p}.first@@" hint-placeholder-val="@@false@@"><button type="button" onClick="@@{p}.goFirst@@" style="{PG_OFF}">1</button><span style="color: {MUTE};">…</span></sc-if>'
            f'<sc-for list="@@{p}.nums@@" as="x" hint-placeholder-count="5"><button type="button" onClick="@@x.go@@" aria-current="@@x.cur@@" style="@@x.style@@">@@x.n@@</button></sc-for>'
            f'<sc-if value="@@{p}.last@@" hint-placeholder-val="@@true@@"><span style="color: {MUTE};">…</span><button type="button" onClick="@@{p}.goLast@@" style="{PG_OFF}">@@{p}.pages@@</button></sc-if>'
            f'<button type="button" onClick="@@{p}.next@@" aria-label="다음 페이지" style="@@{p}.nextStyle@@">›</button></nav>')


def search_box(val, handler, ph, w=None):
    return (f'<label style="{"width: " + str(w) + "px; " if w else ""}display: flex; align-items: center; gap: 8px; height: 44px; padding: 0 14px; border-radius: 12px; background: #FFFFFF;">'
            f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
            f'<span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">{ph}</span>'
            f'<input type="search" value="@@{val}@@" onChange="@@{handler}@@" placeholder="{ph}" style="flex: 1 1 0; min-width: 0; border: none; background: transparent; font-size: 15px; font-family: inherit; color: {INK}; outline: none;"></label>')


def e1_v5(mobile):
    pre = 'm-' if mobile else ''
    sc = ' class="illo-scroll"' if mobile else ''
    tabs = (f'<div role="tablist"{sc} style="display: flex; gap: 8px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else ""}">'
            f'<button type="button" role="tab" onClick="@@tabs.edu.go@@" style="@@tabs.edu.style@@">SeSAC 과정 {len(COURSES_ALL)}</button>'
            f'<button type="button" role="tab" onClick="@@tabs.pol.go@@" style="@@tabs.pol.style@@">청년 정책 {len(POL_ALL)}</button>'
            f'<button type="button" role="tab" onClick="@@tabs.cert.go@@" style="@@tabs.cert.style@@">자격증, 어학</button>'
            f'<button type="button" role="tab" onClick="@@tabs.act.go@@" style="@@tabs.act.style@@">대외활동</button></div>')
    chips = f'<sc-for list="@@groups@@" as="g" hint-placeholder-count="8"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.label@@</button></sc-for>'
    live = '<button type="button" onClick="@@live.go@@" style="@@live.style@@">@@live.label@@</button>'
    sorts = ('<button type="button" onClick="@@sort.rec.go@@" style="@@sort.rec.style@@">추천순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             '<button type="button" onClick="@@sort.close.go@@" style="@@sort.close.style@@">마감 임박순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             '<button type="button" onClick="@@sort.rv.go@@" style="@@sort.rv.style@@">후기 많은 순</button>')
    img_h = 132 if mobile else 140
    card = (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 14px; {CARD} min-width: 0;">'
            f'<sc-if value="@@c.hasThumb@@" hint-placeholder-val="@@false@@"><img src="@@c.thumb@@" alt="" style="width: 100%; height: {img_h}px; object-fit: cover; border-radius: 12px; display: block;"></sc-if>'
            f'<sc-if value="@@c.noThumb@@" hint-placeholder-val="@@true@@"><div style="@@c.band@@ height: {img_h}px; border-radius: 12px; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;"><span style="font-size: 13px; font-weight: 700;">@@c.g@@</span><span style="font-size: 22px; font-weight: 800; letter-spacing: -0.02em; opacity: 0.85;">SeSAC @@c.cp@@</span></div></sc-if>'
            f'<div style="display: flex; align-items: center; gap: 6px;"><span style="@@c.stStyle@@">@@c.st@@</span><sc-if value="@@c.hasDue@@" hint-placeholder-val="@@false@@"><span style="font-size: 12px; font-weight: 700; color: {RED};">@@c.due@@</span></sc-if><span style="margin-left: auto;">{save_btn("c.sv", 32)}</span></div>'
            f'<span style="font-size: 15px; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 42px;">@@c.n@@</span>'
            f'<span style="font-size: 12px; line-height: 1.5; color: {SUB};">@@c.cp@@ · @@c.f@@ · @@c.h@@<br>@@c.edu@@</span>'
            f'<span style="display: flex; gap: 6px; flex-wrap: wrap; font-size: 12px; color: {MUTE};"><sc-for list="@@c.tags@@" as="t" hint-placeholder-count="3"><span>@@t@@</span></sc-for></span>'
            f'<div style="margin-top: auto; padding-top: 8px; border-top: 1px solid {LINE}; display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 12px; color: {MUTE};"><sc-if value="@@c.hasRv@@" hint-placeholder-val="@@false@@">후기 @@c.rv@@</sc-if></span><sc-if value="@@c.detail@@" hint-placeholder-val="@@false@@"><a href="@@c.dhref@@" style="font-size: 13px; font-weight: 600; text-decoration: none;">자세히 보기 ›</a></sc-if><sc-if value="@@c.noDetail@@" hint-placeholder-val="@@true@@"><a href="@@c.u@@" {EXT} style="font-size: 13px; font-weight: 600; text-decoration: none;">SeSAC에서 보기 ↗</a></sc-if></div></div>')
    empty = lambda clear, msg: (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 0; {CARD} color: {SUB}; font-size: 15px;">{msg}'
                                f'<button type="button" onClick="@@{clear}@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">조건 지우기</button></div>')
    cols = 1 if mobile else 3
    edu = (f'<sc-if value="@@isEdu@@" hint-placeholder-val="@@true@@"><div style="display: flex; flex-direction: column; gap: 14px;">'
           f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 10px;">{search_box("q", "setQ", "과정명, 캠퍼스, 해시태그", None if mobile else 320)}{live}</div>'
           f'<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else "flex-wrap: wrap;"}">{chips}</div>'
           f'<div style="display: flex; justify-content: space-between; align-items: center; {"flex-direction: column; align-items: flex-start; gap: 8px;" if mobile else ""}"><span style="font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@total@@</b>개 중 @@range@@</span><div style="display: flex; gap: 10px; align-items: center;">{sorts}</div></div>'
           f'<sc-if value="@@hasCards@@" hint-placeholder-val="@@true@@"><div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;"><sc-for list="@@cards@@" as="c" hint-placeholder-count="{6 if mobile else 9}">{card}</sc-for></div>{pager_html("cp", mobile)}</sc-if>'
           f'<sc-if value="@@empty@@" hint-placeholder-val="@@false@@">{empty("clear", "조건에 맞는 과정이 없어요")}</sc-if>'
           f'<span style="font-size: 12px; color: {MUTE};">출처: SeSAC 사이트 전수 조사 (오프라인 197 + 온라인 13개 과정, 2026.10.27 기준). 신청은 SeSAC 사이트에서 해요</span></div></sc-if>')
    pchips = '<sc-for list="@@pcats@@" as="g" hint-placeholder-count="5"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.label@@</button></sc-for>'
    preg = ('<button type="button" onClick="@@preg.all.go@@" style="@@preg.all.style@@">전국, 서울</button><button type="button" onClick="@@preg.seoul.go@@" style="@@preg.seoul.style@@">서울시</button>'
            '<button type="button" onClick="@@preg.gov.go@@" style="@@preg.gov.style@@">중앙부처</button><button type="button" onClick="@@popen.go@@" style="@@popen.style@@">@@popen.label@@</button>')
    prow = (f'<div style="display: flex; {"flex-direction: column;" if mobile else "align-items: center;"} gap: 12px; padding: 18px 0; border-top: 1px solid {LINE};">'
            f'<div style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 6px;"><div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;"><span style="@@p.stStyle@@">@@p.st@@</span><span style="font-size: 12px; color: {SUB};">@@p.r@@ · @@p.c@@</span></div>'
            f'<span style="font-size: 16px; font-weight: 700; line-height: 1.4;">@@p.n@@</span><span style="font-size: 13px; color: {SUB};">@@p.o@@ · @@p.per@@</span>'
            f'<span style="font-size: 13px; line-height: 1.5; color: #4E5968;">@@p.d@@</span>'
            f'<sc-if value="@@p.hasK@@" hint-placeholder-val="@@true@@"><span style="display: flex; gap: 4px; flex-wrap: wrap;"><sc-for list="@@p.k@@" as="k" hint-placeholder-count="2"><span style="padding: 3px 8px; border-radius: 6px; background: {FILL}; font-size: 12px; color: {SUB};">@@k@@</span></sc-for></span></sc-if></div>'
            f'<div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">{save_btn("p.sv", 38)}'
            f'<sc-if value="@@p.detail@@" hint-placeholder-val="@@false@@"><a href="@@p.dhref@@" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">자세히 보기</a></sc-if>'
            f'<sc-if value="@@p.noDetail@@" hint-placeholder-val="@@true@@"><a href="@@p.u@@" {EXT} style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">자세히 ↗</a></sc-if></div></div>')
    pol = (f'<sc-if value="@@isPol@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 14px;">'
           f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 10px;">{search_box("pq", "setPq", "정책 이름, 기관, 키워드", None if mobile else 320)}<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else ""}">{preg}</div></div>'
           f'<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else "flex-wrap: wrap;"}">{pchips}</div>'
           f'<section style="display: flex; flex-direction: column; padding: {"4px 18px 16px" if mobile else "8px 28px 20px"}; {CARD}">'
           f'<span style="padding: 12px 0; font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@ptotal@@</b>건 중 @@prange@@ · 신청 가능한 정책 먼저</span>'
           f'<sc-if value="@@hasPols@@" hint-placeholder-val="@@true@@"><sc-for list="@@pols@@" as="p" hint-placeholder-count="10">{prow}</sc-for>{pager_html("pp", mobile)}</sc-if>'
           f'<sc-if value="@@pempty@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 40px 0; color: {SUB}; font-size: 15px;">조건에 맞는 정책이 없어요<button type="button" onClick="@@pclear@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">조건 지우기</button></div></sc-if></section>'
           f'<span style="font-size: 12px; color: {MUTE};">출처: 온통청년 청년정책 API (일자리 분야 중 서울시, 중앙부처 {len(POL_ALL)}건, 2026.11.01 조회). 신청 조건은 각 정책 페이지에서 확인해요</span></div></sc-if>')
    cert = f'<sc-if value="@@isCert@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 16px;">{next_cert(mobile)}</div></sc-if>'
    act = f'<sc-if value="@@isAct@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 16px;">{next_act(mobile)}</div></sc-if>'
    head = (f'<div style="display: flex; flex-direction: column; gap: 6px; {"padding: 8px 4px 4px;" if mobile else ""}"><h1 style="margin: 0; font-size: {26 if mobile else 32}px; font-weight: 700; letter-spacing: -0.02em;">교육과정과 취업 지원</h1>'
            f'<span style="font-size: {13 if mobile else 15}px; line-height: 1.5; color: {SUB};">SeSAC 과정 {len(COURSES_ALL)}개와 청년 일자리 정책 {len(POL_ALL)}건을 한곳에서 찾아요. 마음에 들면 저장해 두세요</span></div>')
    body = f'{head}{ai_banner(mobile)}{tabs}{edu}{pol}{cert}{act}'
    if mobile:
        return '    ' + body.replace('href="S4-', 'href="m-S4-') + '\n'
    return f'  <div style="display: flex; flex-direction: column; gap: 20px; padding: 24px 56px 56px;">{body}</div>\n'


boards['E1-edu.dc.html'] = ('E1 교육과정 (SeSAC 210, 청년 정책, 자격증, 대외활동)', dpage('E1-edu.dc.html', '교육과정', 'edu', e1_v5(False), e1_js(False)))
boards['m-E1-edu.dc.html'] = ('ME1 교육과정 (모바일)', mpage('m-E1-edu.dc.html', 'ME1 교육과정 (모바일)', topbar_logo(auth_mobile()), e1_v5(True), 'edu', e1_js(True)))

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

# --- 로그인, 회원가입 ---
SOCIAL = [('카카오로 시작하기', '#FEE500', '#191919', '<path d="M12 4C7 4 3 7.1 3 11c0 2.5 1.7 4.7 4.2 5.9l-.9 3.4c-.1.3.3.6.6.4l4-2.6h1.1c5 0 9-3.1 9-7.1S17 4 12 4z" fill="#191919"/>'),
          ('네이버로 시작하기', '#03C75A', '#FFFFFF', '<path d="M14.6 12.5 9.2 5H5v14h4.4v-7.5L14.8 19H19V5h-4.4z" fill="#FFFFFF"/>'),
          ('Google로 시작하기', '#FFFFFF', '#191F28', '<path d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z" fill="#4285F4"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z" fill="#34A853"/><path d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9z" fill="#FBBC05"/><path d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5L6.4 10C7.2 7.8 9.4 6 12 6z" fill="#EA4335"/>')]


def social_btns(href):
    return ''.join(f'<a href="{href}" onClick="@@loginAs@@" style="height: 50px; display: flex; align-items: center; justify-content: center; gap: 8px; border-radius: 12px; background: {bg}; color: {fg}; font-size: 15px; font-weight: 600; text-decoration: none;{" box-shadow: inset 0 0 0 1px #E5E8EB;" if bg == "#FFFFFF" else ""}">'
                   f'<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24">{ic}</svg>{label}</a>' for label, bg, fg, ic in SOCIAL)


def divider(t):
    return f'<div style="display: flex; align-items: center; gap: 12px; color: {MUTE}; font-size: 13px;"><span style="flex: 1 1 0; height: 1px; background: #E5E8EB;"></span>{t}<span style="flex: 1 1 0; height: 1px; background: #E5E8EB;"></span></div>'


def af(label, id_, ph, kind='text', val=''):
    v = f' value="{val}"' if val else ''
    return (f'<label for="{id_}" style="display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 13px; color: {SUB};">{label}</span>'
            f'<input id="{id_}" type="{kind}"{v} placeholder="{ph}" style="{INP_D} font-size: 15px;"></label>')


def login_page(mobile):
    pre = 'm-' if mobile else ''
    inner = (f'<div style="display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: {26 if mobile else 28}px; font-weight: 700; letter-spacing: -0.02em;">로그인</h1>'
             f'<span style="font-size: 14px; line-height: 1.5; color: {SUB};">저장한 공고와 이력서를 어디서든 이어서 봐요</span></div>'
             f'<div style="display: flex; flex-direction: column; gap: 8px;">{social_btns(pre + "Main.dc.html")}</div>{divider("또는 이메일로")}'
             f'{af("이메일", pre + "li-email", "name@example.com", "email")}{af("비밀번호", pre + "li-pw", "비밀번호", "password")}'
             f'<a href="{pre}Main.dc.html" onClick="@@loginAs@@" style="height: 52px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; text-decoration: none;">로그인</a>'
             f'<div style="display: flex; justify-content: space-between; font-size: 13px;"><a href="{pre}L1-login.dc.html" style="color: {SUB}; text-decoration: none;">비밀번호 찾기</a><span style="color: {SUB};">처음이세요? <a href="{pre}L2-signup.dc.html" style="font-weight: 600; text-decoration: none;">회원가입</a></span></div>'
             f'<span style="padding: 10px 12px; border-radius: 10px; background: {FILL}; font-size: 12px; line-height: 1.5; color: {SUB};">시연용 화면이에요. 아무 값이나 넣고 눌러도 예시 계정(김하늘)으로 로그인돼요</span>')
    box = f'<section style="display: flex; flex-direction: column; gap: 18px; padding: {"24px 20px" if mobile else "36px 40px"}; {CARD} {"" if mobile else "width: 440px; box-sizing: border-box;"}">{inner}</section>'
    return f'    {box}\n' if mobile else f'  <div style="display: flex; justify-content: center; padding: 32px 56px 72px;">{box}</div>\n'


def signup_page(mobile):
    pre = 'm-' if mobile else ''
    jobs = ''.join(chip(j, j == 'SNS 콘텐츠 마케팅') for j in ['SNS 콘텐츠 마케팅'] + JOBS7[:4])
    stat = ''.join(f'<span style="flex: 1 1 0; text-align: center; padding: 10px 0; border-radius: 10px; font-size: 14px; {("background: #FFFFFF; font-weight: 600; box-shadow: 0 1px 3px rgba(0,23,51,0.08);" if s == "취업 준비생" else "color: " + SUB + ";")}">{s}</span>' for s in ['재학생', '취업 준비생', '재직자'])
    terms = ''.join(f'<label style="display: flex; align-items: center; gap: 10px; font-size: 14px; color: #333D4B; cursor: pointer;"><input type="checkbox" checked style="width: 17px; height: 17px; accent-color: {BLUE};">{t}</label>' for t in ['[필수] 서비스 이용약관 동의', '[필수] 개인정보 수집, 이용 동의', '[선택] 새 공고, 마감 알림 받기'])
    inner = (f'<div style="display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: {26 if mobile else 28}px; font-weight: 700; letter-spacing: -0.02em;">회원가입</h1>'
             f'<span style="font-size: 14px; line-height: 1.5; color: {SUB};">가입하고 이력서를 한 번 등록하면 공고마다 바로 비교할 수 있어요</span></div>'
             f'<div style="display: flex; flex-direction: column; gap: 8px;">{social_btns(pre + "S5-resume.dc.html")}</div>{divider("또는 이메일로 가입")}'
             f'{af("이름", "su-name", "이름", "text", "김하늘")}{af("이메일", pre + "su-email", "name@example.com", "email")}'
             f'<div style="display: grid; grid-template-columns: {"1fr" if mobile else "1fr 1fr"}; gap: 12px;">{af("비밀번호", pre + "su-pw", "8자 이상", "password")}{af("비밀번호 확인", pre + "su-pw2", "한 번 더", "password")}</div>'
             f'<div style="display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 13px; color: {SUB};">지금 상태</span><div style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);">{stat}</div></div>'
             f'<div style="display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 13px; color: {SUB};">관심 직무 · 나중에 바꿀 수 있어요</span><div style="display: flex; gap: 6px; flex-wrap: wrap;">{jobs}</div></div>'
             f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 14px 16px; border-radius: 12px; background: #F9FAFB;"><label style="display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 700; cursor: pointer;"><input type="checkbox" checked style="width: 18px; height: 18px; accent-color: {BLUE};">전체 동의</label>{terms}</div>'
             f'<a href="{pre}S5-resume.dc.html" onClick="@@loginAs@@" style="height: 52px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; text-decoration: none;">가입하고 이력서 등록하기</a>'
             f'<span style="text-align: center; font-size: 13px; color: {SUB};">이미 계정이 있나요? <a href="{pre}L1-login.dc.html" style="font-weight: 600; text-decoration: none;">로그인</a></span>')
    box = f'<section style="display: flex; flex-direction: column; gap: 18px; padding: {"24px 20px" if mobile else "36px 40px"}; {CARD} {"" if mobile else "width: 520px; box-sizing: border-box;"}">{inner}</section>'
    return f'    {box}\n' if mobile else f'  <div style="display: flex; justify-content: center; padding: 32px 56px 72px;">{box}</div>\n'


AUTH_JS = '  renderVals() { return {}; }'
boards['L1-login.dc.html'] = ('L1 로그인', dpage('L1-login.dc.html', '로그인', '', login_page(False), AUTH_JS))
boards['L2-signup.dc.html'] = ('L2 회원가입', dpage('L2-signup.dc.html', '회원가입', '', signup_page(False), AUTH_JS))
boards['m-L1-login.dc.html'] = ('ML1 로그인 (모바일)', mpage('m-L1-login.dc.html', 'ML1 로그인 (모바일)', topbar_logo(), login_page(True), 'my', AUTH_JS))
boards['m-L2-signup.dc.html'] = ('ML2 회원가입 (모바일)', mpage('m-L2-signup.dc.html', 'ML2 회원가입 (모바일)', topbar_logo(), signup_page(True), 'my', AUTH_JS))

# ===== v6 compare: the posting as written, AI results marked on its own sentences, one side panel =====
def topbar_back(back, title):
    return ('  <div style="position: sticky; top: 0; z-index: 10; display: grid; grid-template-columns: 40px 1fr 40px; align-items: center; height: 52px; padding: 0 16px; background: rgba(250,250,250,0.96);">'
            f'<a href="{back}" aria-label="뒤로" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: {INK};"><svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></a>'
            f'<span style="text-align: center; font-size: 17px; font-weight: 700;">{title}</span><span></span></div>\n')


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
V6_JS = ("  constructor(props) { super(props); this.state = { done: (typeof location !== 'undefined' && location.hash === '#result') }; }\n"
         "  pageVals() {\n    const d = this.state.done;\n"
         "    const hl = (k) => d ? __HL__[k] : '';\n"
         "    return { done: d, notDone: !d, run: () => this.setState({ done: true }), reset: () => this.setState({ done: false }), hl: { ok: hl('ok'), part: hl('part'), no: hl('no') } };\n  }")
HL = {'ok': f'background: {BLUE_BG}; color: {BLUE_D}; border-radius: 4px; padding: 1px 2px; font-weight: 600;',
      'part': f'background: {OR_BG}; color: {OR}; border-radius: 4px; padding: 1px 2px; font-weight: 600;',
      'no': 'background: #EEF0F3; color: #4E5968; border-radius: 4px; padding: 1px 2px; text-decoration: underline dotted #B0B8C1; text-underline-offset: 3px;'}


def mk_badge(k):
    t, c, bg = MK[k]
    return f'<span style="flex-shrink: 0; padding: 2px 8px; border-radius: 6px; background: {bg}; color: {c}; font-size: 12px; font-weight: 700;">{t}</span>'


def post_li(pieces, finds, mobile):
    pre = 'm-' if mobile else ''
    txt = ''.join(f'<span style="@@hl.{m}@@">{t}</span>' if m else t for t, m in pieces)
    ev = ''
    for k, note, act, href in finds:
        a = f'<a href="{pre}{href}" style="flex-shrink: 0; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">{act} ›</a>' if act else ''
        ev += f'<div style="display: flex; align-items: flex-start; gap: 8px; font-size: 13px; line-height: 1.5; color: #4E5968;">{mk_badge(k)}<span style="flex: 1 1 0;">{note}</span>{a}</div>'
    evb = (f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 6px; margin-top: 8px; padding: 10px 12px; border-radius: 10px; background: #F9FAFB;">{ev}</div></sc-if>' if ev else
           f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="margin-top: 6px; font-size: 12px; color: {MUTE};">관심, 태도 문장이라 비교하지 않았어요</div></sc-if>')
    return f'<li style="padding: 2px 0;"><span style="font-size: 15px; line-height: 1.75; color: #333D4B;">{txt}</span>{evb}</li>'


def posting_card(mobile):
    pad = '20px' if mobile else '32px 36px'
    h3 = lambda t, extra='': f'<h3 style="margin: 0; font-size: 16px; font-weight: 700;">{t}{extra}</h3>'
    ul = lambda items: f'<ul style="margin: 0; padding: 0 0 0 18px; display: flex; flex-direction: column; gap: 8px;">{items}</ul>'
    duties = ''.join(f'<li style="font-size: 15px; line-height: 1.75; color: #333D4B;">{t}</li>' for t in DUTIES)
    quals = ''.join(post_li(p, f, mobile) for k, p, f in POST_REQ if k == '자격요건')
    prefs = ''.join(post_li(p, f, mobile) for k, p, f in POST_REQ if k == '우대사항')
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 12px; color: {MUTE};">{k}</span><span style="font-size: 14px;">{v}</span></div>'
                   for k, v in [('직무', '콘텐츠 마케터'), ('고용형태', '인턴 (채용연계)'), ('경력', '경력 무관'), ('마감', '채용 시 마감')])
    return (f'<article aria-label="채용 공고" style="display: flex; flex-direction: column; gap: 24px; padding: {pad}; {CARD} min-width: 0;">'
            f'<div style="display: flex; align-items: center; gap: 12px;">{mark("olive")}<span style="flex: 1 1 0; display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 15px; font-weight: 600;">올리브인터내셔널</span><span style="font-size: 12px; color: {MUTE};">뷰티 브랜드 성분에디터 운영 · 마케팅본부</span></span>{save_btn("sv.olive", 40)}</div>'
            f'<h1 style="margin: 0; font-size: {20 if mobile else 26}px; font-weight: 700; line-height: 1.4; letter-spacing: -0.02em;">[마케팅본부] 성분에디터 콘텐츠 마케팅 인턴 (채용연계형)</h1>'
            f'<div style="display: grid; grid-template-columns: repeat({2 if mobile else 4}, minmax(0, 1fr)); gap: 12px; padding: 14px 16px; border-radius: 12px; background: #F9FAFB;">{meta}</div>'
            f'<section style="display: flex; flex-direction: column; gap: 10px;">{h3("담당업무")}{ul(duties)}</section>'
            f'<section style="display: flex; flex-direction: column; gap: 10px;">{h3("자격요건")}<span style="font-size: 13px; font-weight: 600; color: {SUB};">Skillset</span>{ul(quals)}</section>'
            f'<section style="display: flex; flex-direction: column; gap: 10px;">{h3("우대사항")}{ul(prefs)}</section>'
            f'<section style="display: flex; flex-direction: column; gap: 10px;">{h3("전형절차")}<p style="margin: 0; font-size: 15px; line-height: 1.75; color: #333D4B;">서류 전형, 1차 인터뷰, 최종 합격 · 포트폴리오 자유 양식</p></section>'
            '</article>')


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


def score_ring():
    r, c = 30, 2 * 3.14159 * 30
    one = c / 6
    arc = lambda color, length, offset: f'<circle cx="38" cy="38" r="{r}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="butt" stroke-dasharray="{length - 2:.1f} {c:.1f}" stroke-dashoffset="{-offset:.1f}" transform="rotate(-90 38 38)"/>'
    return (f'<span role="img" aria-label="6개 중 맞음 1, 일부 1" style="position: relative; width: 76px; height: 76px; flex-shrink: 0;"><svg width="76" height="76" viewBox="0 0 76 76" aria-hidden="true">'
            f'<circle cx="38" cy="38" r="{r}" fill="none" stroke="#EEF0F3" stroke-width="9"/>{arc(BLUE, one, 0)}{arc("#FFB331", one, one)}</svg>'
            f'<span style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 800; letter-spacing: -0.02em;">2<span style="font-size: 13px; color: {MUTE}; font-weight: 600;">/6</span></span></span>')


def side_panel(mobile):
    pre = 'm-' if mobile else ''
    seg = lambda c: f'<span style="flex: 1 1 0; height: 8px; border-radius: 999px; background: {c};"></span>'
    exp = (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px; border-radius: 14px; background: #F9FAFB;">'
           f'<div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 13px; font-weight: 700;">비교에 쓰는 내 경험</span><a href="{pre}S5-resume.dc.html" style="font-size: 12px; color: {SUB}; text-decoration: none;">이력서 수정 ›</a></div>'
           f'<span style="font-size: 13px; line-height: 1.55; color: #4E5968;">학생회 홍보부 인스타그램 운영 1년 · 카드뉴스 주 1회 (캔바) · 팔로워 300명에서 1,200명 · 컴활 2급 · OPIc IM2</span></div>')
    before = (f'<sc-if value="@@notDone@@" hint-placeholder-val="@@true@@"><div style="display: flex; flex-direction: column; gap: 14px;">{AI}'
              f'<span style="font-size: 20px; font-weight: 700; line-height: 1.4;">이 공고 문장에<br>내 경험을 맞춰 볼게요</span>{exp}'
              f'<button type="button" onClick="@@run@@" style="height: 54px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; cursor: pointer;">AI로 비교하기</button>'
              f'<span style="font-size: 12px; line-height: 1.5; color: {MUTE};">AI가 문장마다 근거를 찾고, 판정은 규칙으로 해요. 합격 여부는 예측하지 않아요</span></div></sc-if>')
    tile = lambda n, label, bg, fg: f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 12px; border-radius: 14px; background: {bg};"><span style="font-size: 22px; font-weight: 800; color: {fg}; letter-spacing: -0.02em;">{n}</span><span style="font-size: 12px; font-weight: 600; color: {fg};">{label}</span></div>'
    refresh = f'<svg aria-hidden="true" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/></svg>'
    point = f'<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="{"M12 5v14M6 13l6 6 6-6" if mobile else "M19 12H5M11 6l-6 6 6 6"}"/></svg>'
    after = (f'<sc-if value="@@done@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 18px;">'
             f'<div style="display: flex; justify-content: space-between; align-items: center;">{AI}<button type="button" onClick="@@reset@@" style="display: flex; align-items: center; gap: 4px; border: none; background: none; padding: 0; font-size: 12px; color: {MUTE}; cursor: pointer;">{refresh}다시 비교</button></div>'
             f'<div style="display: flex; align-items: center; gap: 16px;">{score_ring()}<span style="font-size: 20px; font-weight: 700; line-height: 1.4; letter-spacing: -0.02em;">공고 요구 6개 중<br><span style="color: {BLUE};">2개</span>가 이어져요</span></div>'
             f'<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">{tile(1, "맞음", BLUE_BG, BLUE_D)}{tile(1, "일부", OR_BG, OR)}{tile(4, "없음", "#F2F4F6", "#4E5968")}</div>'
             f'<span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: {SUB};">{point}{"아래" if mobile else "왼쪽"} 공고 문장에 같은 색으로 표시했어요</span>'
             f'<div style="height: 1px; background: {LINE};"></div>'
             f'<div style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 17px; font-weight: 700;">어느 부분을 먼저 채울까요?</span><span style="font-size: 12px; color: {MUTE};">고르는 건 나예요. 비어 있는 4개 기준으로 추천했어요</span></div>'
             f'{next_rows(mobile)}</div></sc-if>')
    sticky = '' if mobile else 'position: sticky; top: 24px;'
    return f'<aside style="{sticky} display: flex; flex-direction: column; padding: {"20px" if mobile else "24px"}; {CARD}">{before}{after}</aside>'


v6_body = (f'  <div style="padding: 16px 56px 0;"><a href="S1-list.dc.html" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 공고 목록</a></div>\n'
           f'  <div style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 24px; padding: 16px 56px 56px; align-items: start;">{posting_card(False)}{side_panel(False)}</div>\n')
V6_SCRIPT = V6_JS.replace('__HL__', json.dumps(HL, ensure_ascii=False))
boards['S3-compare.dc.html'] = ('S2 공고 원문 + AI 비교 (한 화면)', dpage('S3-compare.dc.html', '공고와 내 경험 비교', 'find', v6_body, V6_SCRIPT, saves=('olive',)))
m_v6 = f'    {side_panel(True)}\n    {posting_card(True)}\n'
# phone: the panel goes first so the button and the score are on the first screen
boards['m-S3-compare.dc.html'] = ('M2 공고 원문 + AI 비교 (모바일)', mpage('m-S3-compare.dc.html', 'M2 공고와 내 경험 비교 (모바일)', topbar_back('m-S1-list.dc.html', '공고와 비교'), m_v6, 'find', V6_SCRIPT, saves=('olive',)))

# ===== v7: policy detail page (first policy card only), from the 온통청년 API record =====
PD_ID = 'pol-20261018005400213991'
PD = {'n': '2026 서울형 청년인턴 직무캠프', 'expl': '사전직무교육 ✚ 인턴십(4개월) 및 직장적응교육 ➔ 취업연계',
      'sprt': '실무중심 직무교육과 인턴십 과정의 접목으로 청년 구직자에게 일경험 및 취업역량 강화 지원',
      'kw': ['교육지원', '인턴'], 'apply_from': '2026.03.01', 'apply_to': '2026.12.31', 'end': '2026-12-31', 'scale': '270명', 'age': '만 18세 ~ 34세',
      'how': '참여기업 모집·선정 후 참여자 모집·선발', 'sup': '서울특별시 미래청년기획관 청년정책담당관', 'op': '재단법인 서울경제진흥원 (SBA)',
      'apply_url': 'https://youth.seoul.go.kr/content.do?key=2310100012', 'ref': 'https://youth.seoul.go.kr', 'reg': '2026.10.18', 'mod': '2026.10.20', 'views': 58}
SAVE_ITEMS['pd'] = {'id': PD_ID, 'kind': '정책', 't': PD['n'], 's': '서울특별시 미래청년기획관 청년정책담당관 · 신청 중', 'u': PD['apply_url'], 'h': 'P2-policy.dc.html'}
PD_JS = ("  pageVals() {\n    const end = new Date('" + PD['end'] + "T23:59:59+09:00').getTime(), n = Math.ceil((end - Date.now()) / 86400000);\n"
         "    return { dday: n >= 0 ? 'D-' + n : '마감', open: n >= 0 };\n  }")


def pd_page(mobile):
    pre = 'm-' if mobile else ''
    P = PD
    badge = lambda t, bg, fg: f'<span style="padding: 4px 10px; border-radius: 999px; background: {bg}; color: {fg}; font-size: 13px; font-weight: 600;">{t}</span>'
    steps = [('1', '사전 직무교육', '실무 중심 교육'), ('2', '인턴십 4개월', '참여기업에서 일경험'), ('3', '직장적응교육', '함께 진행'), ('4', '취업 연계', '정규 채용으로')]
    arrow = f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B0B8C1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{"M12 5v14M6 13l6 6 6-6" if mobile else "M5 12h14M13 6l6 6-6 6"}"/></svg>'
    flow = arrow.join(f'<div style="flex: 1 1 0; display: flex; flex-direction: column; gap: 6px; padding: 16px; border-radius: 14px; background: {"#F4F9FF" if i == "2" else "#F9FAFB"};"><span style="width: 26px; height: 26px; border-radius: 50%; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span><span style="font-size: 15px; font-weight: 700;">{t}</span><span style="font-size: 12px; color: {SUB};">{d}</span></div>' for i, t, d in steps)
    flow = f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 8px;">{flow}</div>'
    fact = lambda k, v, sub='': f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 16px; border-radius: 14px; background: #F9FAFB;"><span style="font-size: 12px; color: {MUTE};">{k}</span><span style="font-size: 16px; font-weight: 700; line-height: 1.35;">{v}</span>{f"<span style=\"font-size: 12px; color: {SUB};\">{sub}</span>" if sub else ""}</div>'
    facts = (f'<div style="display: grid; grid-template-columns: repeat({2 if mobile else 4}, minmax(0, 1fr)); gap: 10px;">'
             + fact('신청 기간', f'{P["apply_from"]} ~ {P["apply_to"][5:]}', '@@dday@@') + fact('모집 규모', P['scale']) + fact('나이', P['age']) + fact('운영', '서울경제진흥원', 'SBA') + '</div>')
    hero = (f'<section style="display: flex; flex-direction: column; gap: 18px; padding: {"22px 20px" if mobile else "32px 36px"}; {CARD}">'
            f'<div style="display: flex; gap: 6px; flex-wrap: wrap; align-items: center;">{badge("신청 중", BLUE_BG, BLUE_D)}{badge("서울 · 취업", FILL, SUB)}' + ''.join(badge("#" + k, FILL, SUB) for k in P['kw']) + '</div>'
            f'<div style="display: flex; align-items: flex-start; gap: 12px;"><h1 style="flex: 1 1 0; margin: 0; font-size: {24 if mobile else 32}px; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em;">{P["n"]}</h1>{save_btn("sv.pd", 44)}</div>'
            f'<p style="margin: 0; font-size: {15 if mobile else 17}px; line-height: 1.6; color: #4E5968;">{P["sprt"]}</p>{facts}</section>')
    sec = lambda t, body: f'<section style="display: flex; flex-direction: column; gap: 14px; padding: {"20px" if mobile else "28px 32px"}; {CARD}"><h2 style="margin: 0; font-size: {17 if mobile else 19}px; font-weight: 700;">{t}</h2>{body}</section>'
    cond_rows = [('나이', P['age'], True), ('거주지', '서울 청년정책 (세부 조건은 모집 공고에서 확인)', None), ('소득', '제한 없음', True), ('학력, 전공', '제한 없음', True), ('취업 상태', '제한 없음', True), ('혼인 여부', '제한 없음', True)]
    conds = ''.join(f'<div style="display: grid; grid-template-columns: {"88px" if mobile else "120px"} 1fr; gap: 12px; padding: 13px 0; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.5;"><span style="color: {MUTE};">{k}</span><span style="font-weight: 600;">{v}</span></div>' for k, v, _ in cond_rows)
    how = ''.join(f'<li style="display: flex; gap: 12px;"><span style="width: 24px; height: 24px; flex-shrink: 0; border-radius: 50%; background: {FILL}; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span><span style="font-size: 15px; line-height: 1.5;">{t}</span></li>' for i, t in [(1, '서울시가 참여기업을 모집하고 선정해요'), (2, '선정된 기업에 맞춰 참여자를 모집하고 선발해요'), (3, '신청은 서울청년몽땅정보통 신청 페이지에서 해요')])
    org = (f'<div style="display: grid; grid-template-columns: {"1fr" if mobile else "1fr 1fr"}; gap: 10px;">' + fact('주관', P['sup']) + fact('운영', P['op']) + '</div>')
    main = (sec('어떻게 진행되나요', flow + f'<span style="font-size: 13px; color: {SUB};">원문: {P["expl"]}</span>')
            + sec('신청 자격', f'<div>{conds}</div><span style="font-size: 12px; color: {MUTE};">온통청년 등록 정보 기준이에요. 실제 선발 조건은 모집 공고를 꼭 확인하세요</span>')
            + sec('신청 방법', f'<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px;">{how}</ol>')
            + sec('담당 기관', org))
    me = [('나이 만 24세', '만 18~34세 안에 있어요'), ('취업 준비생', '취업 상태 제한 없음'), ('서울 성북구', '서울 거주')]
    me_rows = ''.join(f'<div style="display: flex; align-items: center; gap: 10px; font-size: 14px;"><span style="width: 20px; height: 20px; flex-shrink: 0; border-radius: 50%; background: {BLUE}; display: flex; align-items: center; justify-content: center;"><svg aria-hidden="true" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span><span style="flex: 1 1 0;"><b style="font-weight: 600;">{a}</b> <span style="color: {SUB};">· {b}</span></span></div>' for a, b in me)
    side = (f'<aside style="{"" if mobile else "position: sticky; top: 24px;"} display: flex; flex-direction: column; gap: 14px; padding: {"20px" if mobile else "24px"}; {CARD}">'
            f'<div style="display: flex; align-items: baseline; justify-content: space-between;"><span style="font-size: 13px; color: {SUB};">신청 마감까지</span><span style="font-size: 26px; font-weight: 800; color: {BLUE}; letter-spacing: -0.02em;">@@dday@@</span></div>'
            f'<a href="{P["apply_url"]}" {EXT} style="height: 54px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 17px; font-weight: 600; text-decoration: none;">신청 페이지로 가기 ↗</a>'
            f'<div style="height: 1px; background: {LINE};"></div>'
            f'<div style="display: flex; align-items: center; gap: 6px;">{AI}<span style="font-size: 15px; font-weight: 700;">내 이력서로 보면</span></div>{me_rows}'
            f'<span style="padding: 12px 14px; border-radius: 12px; background: #F4F9FF; font-size: 13px; line-height: 1.55; color: #333D4B;">인턴십 4개월이 끝나면 비교 결과에서 비어 있던 <b style="color: {BLUE_D};">"실무 경험"</b>을 채울 수 있어요. <a href="{pre}S3-compare.dc.html#result" style="font-weight: 600; text-decoration: none;">비교 결과 ›</a></span>'
            f'<span style="font-size: 11px; line-height: 1.5; color: {MUTE};">조건이 맞는지만 보여줘요. 선발 여부는 예측하지 않아요</span></aside>')
    others = [p for p in POL_ALL if p['r'] == '서울' and p['st'] in ('신청 중', '상시') and p['id'] != PD_ID][:3]
    rel = ''.join(f'<a href="{p["u"]}" {EXT} style="display: flex; flex-direction: column; gap: 6px; padding: 18px; {CARD} color: {INK}; text-decoration: none;"><span style="align-self: flex-start; padding: 2px 8px; border-radius: 999px; background: {BLUE_BG if p["st"] == "신청 중" else "#E6F7F1"}; color: {BLUE_D if p["st"] == "신청 중" else "#0E8A63"}; font-size: 12px; font-weight: 600;">{p["st"]}</span><span style="font-size: 15px; font-weight: 700; line-height: 1.4;">{p["n"]}</span><span style="font-size: 12px; line-height: 1.5; color: {SUB};">{p["d"]}</span></a>' for p in others)
    related = (f'<section style="display: flex; flex-direction: column; gap: 12px;"><h2 style="margin: 0; font-size: 19px; font-weight: 700;">함께 보면 좋은 서울 청년 정책</h2>'
               f'<div style="display: grid; grid-template-columns: repeat({1 if mobile else 3}, minmax(0, 1fr)); gap: 12px;">{rel}</div>'
               f'<span style="font-size: 12px; color: {MUTE};">출처: 온통청년 청년정책 API · 등록 {P["reg"]} · 수정 {P["mod"]} · 조회 {P["views"]}</span></section>')
    if mobile:
        return f'    {hero}\n    {side}\n    {main}\n    {related}\n'
    return (f'  <div style="padding: 16px 56px 0;"><a href="E1-edu.dc.html#policy" style="font-size: 14px; color: {SUB}; text-decoration: none;">‹ 청년 정책</a></div>\n'
            f'  <div style="display: flex; flex-direction: column; gap: 24px; padding: 16px 56px 56px;">{hero}'
            f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 24px; align-items: start;"><div style="display: flex; flex-direction: column; gap: 16px; min-width: 0;">{main}</div>{side}</div>{related}</div>\n')


boards['P2-policy.dc.html'] = ('P2 청년 정책 상세 (서울형 청년인턴 직무캠프)', dpage('P2-policy.dc.html', PD['n'], 'edu', pd_page(False), PD_JS, saves=('pd',)))
boards['m-P2-policy.dc.html'] = ('MP2 청년 정책 상세 (모바일)', mpage('m-P2-policy.dc.html', PD['n'] + ' (모바일)', topbar_back('m-E1-edu.dc.html#policy', '청년 정책'), pd_page(True), 'edu', PD_JS, saves=('pd',)))

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

# ===================== keep S4 / S6, swap chrome and links =====================
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


KEEP = {'S6-story.dc.html': ('my', 0)}
for name, (active, step) in KEEP.items():
    s = open(os.path.join(DATA, 'source', name), encoding='utf-8').read()  # 원본에서 매번 새로 만듦
    s = re.sub(r'  <header .*?</header>\n', lambda m: dheader(active) + (dsteps(step) if step else ''), s, count=1, flags=re.S)
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

# ===================== write files + canvas.json =====================
GONE = ['S2-input.dc.html', 'P1-trend.dc.html', 'm-S2-input.dc.html', 'm-P1-trend.dc.html']
for name, (_, html) in boards.items():
    assert '@@' not in html, name
    assert not any(g in html for g in GONE), (name, [g for g in GONE if g in html])
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(html)
for g in GONE:
    p = os.path.join(ROOT, g)
    if os.path.exists(p):
        os.replace(p, os.path.join(DATA, 'removed-' + g))

c = json.load(open(os.path.join(ROOT, 'canvas.json'), encoding='utf-8'))
old = c['boards']
TITLES = {k: v[0] for k, v in boards.items() if v[0]}
TITLES.update({'S4-next.dc.html': 'S3 다음 행동 · 교육', 'S4-cert.dc.html': 'S3b 자격증, 어학', 'S4-activity.dc.html': 'S3c 대외활동, 프로젝트', 'S4-apply.dc.html': 'S3d 지원 준비', 'S6-story.dc.html': 'S6 취업 수기 (마이페이지에서)',
               'm-S4-next.dc.html': 'M3 다음 행동 · 교육 (모바일)', 'm-S4-cert.dc.html': 'M3b 자격증, 어학 (모바일)', 'm-S4-activity.dc.html': 'M3c 대외활동, 프로젝트 (모바일)', 'm-S4-apply.dc.html': 'M3d 지원 준비 (모바일)', 'm-S6-story.dc.html': 'M6 취업 수기 (모바일)'})
nb = {}
x = 0
ybottom = 0
for name in ['Main.dc.html', 'S1-list.dc.html', 'S3-compare.dc.html', ['S4-next.dc.html', 'C2-course.dc.html', 'S4-cert.dc.html', 'S4-activity.dc.html', 'S4-apply.dc.html'], ['E1-edu.dc.html', 'P2-policy.dc.html'], ['S5-path.dc.html', 'S5-saved.dc.html', 'S5-resume.dc.html'], 'S6-story.dc.html', ['L1-login.dc.html', 'L2-signup.dc.html']]:
    y = 0
    for n in (name if isinstance(name, list) else [name]):
        h = HEIGHTS.get(n, old.get(n, {}).get('h', 1200))
        nb[n] = {'h': h, 'is_interactive': True, 'title': TITLES[n], 'w': 1280, 'x': x, 'y': y}
        y += h + 80
        ybottom = max(ybottom, y)
    x += 1360
MY = ybottom + 320
for i, n in enumerate(['m-Main.dc.html', 'm-S1-list.dc.html', 'm-S3-compare.dc.html', 'm-S4-next.dc.html', 'm-C2-course.dc.html', 'm-S4-cert.dc.html', 'm-S4-activity.dc.html', 'm-S4-apply.dc.html', 'm-E1-edu.dc.html', 'm-P2-policy.dc.html', 'm-S5-path.dc.html', 'm-S5-saved.dc.html', 'm-S5-resume.dc.html', 'm-S6-story.dc.html', 'm-L1-login.dc.html', 'm-L2-signup.dc.html']):
    nb[n] = {'h': HEIGHTS.get(n, old.get(n, {}).get('h', 1400)), 'is_interactive': True, 'title': TITLES[n], 'w': 390, 'x': i * 470, 'y': MY}
c['boards'] = nb
c['order'] = list(nb.keys()) if 'order' in c else c.get('order')
c['notes'] = {
    'flow': {'kind': 'title1', 'maxW': 6720, 'text': '시연 2분 흐름: 홈, 직무 찾기, 공고와 AI 비교, 다음 행동 (10/30 회의 반영 v4)', 'w': 240, 'x': 0, 'y': -300},
    'rule': {'color': 'gray', 'text': '메뉴는 홈, 직무 찾기, 교육과정, 마이페이지 4개. 경험은 마이페이지에 한 번 저장하고 공고 페이지에서 바로 AI 비교. 다음 행동 4개는 고정, 사용자가 고름. 트렌드 상세는 팝업. AI가 쓰인 곳은 보라색 AI 배지로 표시. 판정은 규칙, AI는 근거 문장 찾기. 공고 104건과 SeSAC 과정 210개는 팀 수집 실제 데이터(10/27 기준).', 'w': 1280, 'x': 0, 'y': -170},
    'modeNote': {'color': 'blue', 'text': '직무 찾기: 신입, 인턴을 고르면 내 경험 기준 직무 적합도(AI)를 먼저, 경력을 고르면 공고 비교로 바로. 트렌드 TOP 3 옆 "전체 순위 보기"는 팝업.', 'w': 1280, 'x': 1360, 'y': -170},
    'pathNote': {'color': 'blue', 'text': '"어느 부분을 먼저 채울까요?" 4개 선택지가 S3, S3b, S3c, S3d로 연결. 교육과정 메뉴에서도 같은 내용을 분야별로 볼 수 있음.', 'w': 1280, 'x': 4080, 'y': -170},
    'afterNote': {'color': 'orange', 'text': '마이페이지 = 내 경험(PDF를 AI가 읽어 채움) + 내 취업 경로 + 취업 수기. 수기 저장은 계정이 필요해서 11/6에는 화면만.', 'w': 1280, 'x': 6800, 'y': -170},
    'mobileTitle': {'kind': 'title1', 'maxW': 5200, 'text': '모바일 (390px) · 하단 탭 바: 홈, 직무 찾기, 교육과정, 마이페이지', 'w': 240, 'x': 0, 'y': MY - 260},
    'mobileNote': {'color': 'blue', 'text': '데스크톱과 같은 흐름과 데이터. 트렌드 전체 순위는 아래에서 올라오는 시트. 공고 비교 화면은 위에 뒤로 가기와 단계 바.', 'w': 1280, 'x': 0, 'y': MY - 130},
}
c['noteOrder'] = list(c['notes'].keys())
json.dump(c, open(os.path.join(ROOT, 'canvas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('wrote', len(boards), 'boards; mobile row y =', MY)
