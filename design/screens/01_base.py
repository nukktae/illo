"""모든 화면이 같이 쓰는 것: 토큰, 로그인과 저장 (브라우저 저장), 상단 메뉴, 페이지 틀, AI 배지,
트렌드 팝업, 공통 카드, 목록 스타일, 공통 데이터."""

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
    'kakao': {'id': 'post-358108', 'kind': '공고', 't': '숏폼 서비스 영상 콘텐츠 제작 및 운영_어시스턴트', 's': '카카오 · 신입', 'u': 'https://linkareer.com/activity/358108', 'h': ''},
    'c101': {'id': 'post-327328', 'kind': '공고', 't': '[인턴] 콘텐츠 마케터', 's': '클래스101 · 인턴', 'u': 'https://linkareer.com/activity/327328', 'h': ''},
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
    const u = this.illoGet('illo-user', null), n = this.illoSaved().length, gate = '__GATE__';
    if (gate && !u) { try { window.location.replace('L1-login.dc.html?next=' + gate); } catch (e) {} }
    return { loggedIn: !!u, loggedOut: !u, userName: u ? u.name : '', userInit: u ? u.name.slice(0, 1) : '', profileName: u ? u.name : '예시 프로필',
      savedCount: n, hasSaved: n > 0,
      loginAs: (e) => { let name = '김하늘'; try { const el = document.getElementById('su-name'); if (el && el.value.trim()) name = el.value.trim(); window.localStorage.setItem('illo-user', JSON.stringify({ name })); } catch (e) {}
        try { const nx = (window.location.search.match(/[?&]next=([\w.-]+\.html)$/) || [])[1]; if (nx) { if (e && e.preventDefault) e.preventDefault(); window.location.href = nx; } } catch (e2) {} },
      logout: () => this.illoSet('illo-user', null),
      menuOpen: !!(this.state || {}).illoMenu, toggleMenu: () => this.setState({ illoMenu: !(this.state || {}).illoMenu }), closeMenu: () => this.setState({ illoMenu: false }),
      logoutHome: () => { try { window.localStorage.removeItem('illo-user'); } catch (e) {} try { window.location.href = 'Main.dc.html'; } catch (e) {} } };
  }
'''.replace('__SEED__', json.dumps(SEED, ensure_ascii=False))


def inject(script, saves=(), gate=''):
    """Wrap a page script: page values + login/saved values + static save buttons."""
    script = script.replace('renderVals()', 'pageVals()', 1)
    sv = ''
    if saves:
        sv = ('  svVals() { return { sv: { ' + ', '.join(f"{k}: this.sv({json.dumps(SAVE_ITEMS[k], ensure_ascii=False)})" for k in saves) + ' } }; }\n')
    merge = '  renderVals() { return Object.assign({}, this.illoVals(), ' + ('this.svVals(), ' if saves else '') + 'this.pageVals()); }\n'
    return ILLO_METHODS.replace('__GATE__', gate) + sv + merge + script


def save_btn(p, size=36, bg=None):
    bg = bg or FILL
    return (f'<button type="button" onClick="@@{p}.toggle@@" aria-label="@@{p}.label@@" aria-pressed="@@{p}.saved@@" title="@@{p}.label@@" style="width: {size}px; height: {size}px; flex-shrink: 0; border: none; border-radius: 10px; background: {bg}; display: flex; align-items: center; justify-content: center; cursor: pointer;">'
            f'<sc-if value="@@{p}.saved@@" hint-placeholder-val="@@false@@"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="{BLUE}" stroke="{BLUE}" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg></sc-if>'
            f'<sc-if value="@@{p}.unsaved@@" hint-placeholder-val="@@true@@"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B95A1" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg></sc-if></button>')


def AVATAR_IMG(size):
    # 김하늘 프로필 사진 (데스크톱 상단, 마이페이지 프로필)
    return f'<img src="/_blob/70b2d2f6c328b6f5ee29ac16d9bb4509" alt="" style="width: {size}px; height: {size}px; flex-shrink: 0; border-radius: 50%; object-fit: cover; display: block;">'


# P02-F10 진행 단계: 직무 찾기 -> 공고 비교 -> 다음 행동 (데스크톱 세 화면 상단 오른쪽). 지난 단계는 링크, 지금 단계는 파랑, 다음 단계는 회색
FLOW = [('직무 찾기', 'S1-list.dc.html'), ('공고 비교', 'S3-compare.dc.html#result'), ('다음 행동', 'S4-next.dc.html')]


def flow_steps(active):
    out = ''
    for i, (label, href) in enumerate(FLOW, 1):
        if i < active:
            dot = (f'<span style="width: 20px; height: 20px; border-radius: 50%; background: {BLUE_BG}; color: {BLUE_D}; display: flex; align-items: center; justify-content: center;">'
                   f'<svg aria-hidden="true" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>')
            item = f'<a href="{href}" style="display: flex; align-items: center; gap: 6px; color: {SUB}; text-decoration: none;">{dot}{label}</a>'
        elif i == active:
            dot = f'<span style="width: 20px; height: 20px; border-radius: 50%; background: {BLUE}; color: #FFFFFF; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span>'
            item = f'<span aria-current="step" style="display: flex; align-items: center; gap: 6px; color: {INK}; font-weight: 700;">{dot}{label}</span>'
        else:
            dot = f'<span style="width: 20px; height: 20px; border-radius: 50%; background: {FILL}; color: {MUTE}; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i}</span>'
            item = f'<span style="display: flex; align-items: center; gap: 6px; color: {MUTE};">{dot}{label}</span>'
        sep = '' if i == 1 else f'<li aria-hidden="true" style="color: #C9CED6;">›</li>'
        out += f'{sep}<li style="display: flex;">{item}</li>'
    return (f'<nav aria-label="진행 단계"><ol style="margin: 0; padding: 0; list-style: none; display: flex; align-items: center; gap: 10px; font-size: 13px;">{out}</ol></nav>')


def auth_desktop():
    return (f'<div style="justify-self: end; display: flex; align-items: center; gap: 8px;">'
            f'<sc-if value="@@loggedOut@@" hint-placeholder-val="@@true@@"><a href="L1-login.dc.html" style="height: 40px; padding: 0 14px; display: flex; align-items: center; color: {INK}; font-size: 14px; font-weight: 600; text-decoration: none;">로그인</a>'
            f'<a href="L2-signup.dc.html" style="height: 40px; padding: 0 18px; display: flex; align-items: center; border-radius: 999px; background: {INK}; color: #FFFFFF; font-size: 14px; font-weight: 600; text-decoration: none;">회원가입</a></sc-if>'
            f'<sc-if value="@@loggedIn@@" hint-placeholder-val="@@false@@"><a href="S5-saved.dc.html" aria-label="저장함 @@savedCount@@개" style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: {INK};"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">{BOOK}</svg>'
            f'<sc-if value="@@hasSaved@@" hint-placeholder-val="@@true@@"><span style="position: absolute; top: 3px; right: 1px; min-width: 18px; height: 18px; padding: 0 5px; box-sizing: border-box; border-radius: 999px; background: {BLUE}; color: #FFFFFF; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">@@savedCount@@</span></sc-if></a>'
            f'<div style="position: relative;"><button type="button" onClick="@@toggleMenu@@" aria-haspopup="menu" aria-expanded="@@menuOpen@@" style="display: flex; align-items: center; gap: 8px; height: 40px; padding: 0 12px 0 4px; border: none; border-radius: 999px; background: #FFFFFF; color: {INK}; font-size: 14px; font-weight: 600; font-family: inherit; cursor: pointer;">{AVATAR_IMG(32)}@@userName@@님<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button>'
            f'<sc-if value="@@menuOpen@@" hint-placeholder-val="@@false@@"><div onClick="@@closeMenu@@" style="position: fixed; inset: 0; z-index: 40;"></div>'
            f'<div role="menu" style="position: absolute; right: 0; top: 48px; z-index: 41; width: 240px; padding: 8px; border-radius: 16px; background: #FFFFFF; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.10), 0 0 0 1px rgba(0, 0, 0, 0.05);">'
            f'<div style="display: flex; align-items: center; gap: 10px; padding: 10px 10px 12px;">{AVATAR_IMG(40)}<span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 15px; font-weight: 700; color: {INK};">@@userName@@</span><span style="font-size: 12px; color: {MUTE};">시연용 계정</span></span></div>'
            f'<div style="height: 1px; margin: 0 6px 6px; background: {LINE};"></div>'
            f'<a href="S5-path.dc.html" role="menuitem" style="display: flex; align-items: center; height: 42px; padding: 0 14px; border-radius: 10px; color: {INK}; font-size: 14px; text-decoration: none;">마이페이지</a>'
            f'<a href="S5-resume.dc.html" role="menuitem" style="display: flex; align-items: center; height: 42px; padding: 0 14px; border-radius: 10px; color: {INK}; font-size: 14px; text-decoration: none;">이력서 등록, 수정</a>'
            f'<a href="S5-saved.dc.html" role="menuitem" style="display: flex; align-items: center; height: 42px; padding: 0 14px; border-radius: 10px; color: {INK}; font-size: 14px; text-decoration: none;">저장함 @@savedCount@@</a>'
            f'<div style="height: 1px; margin: 6px; background: {LINE};"></div>'
            f'<button type="button" role="menuitem" onClick="@@logoutHome@@" style="width: 100%; display: flex; align-items: center; height: 42px; padding: 0 14px; border: none; border-radius: 10px; background: none; color: {RED}; font-size: 14px; font-family: inherit; text-align: left; cursor: pointer;">로그아웃</button>'
            f'</div></sc-if></div></sc-if></div>')


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

def dpage(name, title, active, body, script='  renderVals() { return {}; }', default_h=1200, saves=()):
    script = inject(script, saves, name if name.startswith('S5-') else '')
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


def trend_popup(mobile, cta_href, close_label="공고 목록으로 돌아가기"):
    facts = ''.join(f'<div style="display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 12px; background: {FILL};"><span style="font-size: 11px; color: {SUB};">{k}</span><span style="font-size: 16px; font-weight: 700;">{v}</span></div>'
                    for k, v in [('자격증을 적은 공고', '3% · 3건'), ('외국어를 적은 공고', '14% · 15건'), ('개인 채널 운영 경험', '15% · 16건')])
    wrap = ('align-items: flex-end;' if mobile else 'align-items: center;')
    box = ('width: 100%; max-height: 88vh; border-radius: 24px 24px 0 0; padding: 22px 20px 28px;' if mobile else 'width: 560px; max-height: 88vh; border-radius: 24px; padding: 28px;')
    cta = (f'<a href="{cta_href}" style="height: 52px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; text-decoration: none;">이 직무 공고 보기</a>'
           if cta_href else
           f'<button type="button" onClick="@@closeTrend@@" style="height: 52px; border: none; border-radius: 14px; background: {BLUE}; color: #FFFFFF; font-size: 16px; font-weight: 600; cursor: pointer;">{close_label}</button>')
    return f'''  <sc-if value="@@trendOpen@@" hint-placeholder-val="@@false@@">
  <div role="dialog" aria-modal="true" aria-label="실시간 공고 키워드 전체 순위" style="position: fixed; inset: 0; z-index: 50; display: flex; justify-content: center; {wrap} background: rgba(0,23,51,0.38);">
    <div style="{box} box-sizing: border-box; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; background: #FFFFFF;">
      <div style="display: flex; justify-content: space-between; align-items: center;"><div style="display: flex; align-items: center; gap: 8px;"><h2 style="margin: 0; font-size: 20px; font-weight: 700;">실시간 공고 키워드</h2><span style="display: flex; align-items: center; gap: 4px; padding: 3px 7px; border-radius: 999px; background: #FFEEEE; color: {RED}; font-size: 10px; font-weight: 700;"><span class="illo-live" style="width: 6px; height: 6px; border-radius: 50%; background: {RED};"></span>LIVE</span></div>
        <button type="button" onClick="@@closeTrend@@" aria-label="닫기" style="width: 36px; height: 36px; border: none; border-radius: 50%; background: {FILL}; color: {INK}; font-size: 18px; cursor: pointer;">✕</button></div>
      <span style="font-size: 13px; line-height: 1.5; color: {SUB};">SNS 콘텐츠 마케팅 2026 공고 59건이 가장 많이 적은 역량이에요. 순위 변화는 2023~25 공고 45건과 비교</span>
      <div style="display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 14px; background: #FFF4F4;"><span style="font-size: 11px; font-weight: 600; color: {RED};">급상승</span><span style="font-size: 15px; font-weight: 700;">데이터, 성과 분석 8위에서 3위로</span></div>
      <div style="display: flex; flex-direction: column;">{trend_rows(RANK, pad='0 4px')}</div>
      <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px;">{facts}</div>
      <span style="font-size: 11px; line-height: 1.5; color: {MUTE};">출처: SNS 콘텐츠 마케팅 {SRC104}. 104건 = 2026 공고 59건 + 2023~25 공고 45건. 직무 찾기 목록은 2026 신입, 인턴 46건이에요. 퍼센트는 해당 단어가 나온 공고 비율</span>
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

# ---------- list controls (pills, sort, pages) ----------
PILL = 'flex-shrink: 0; height: 36px; padding: 0 14px; border-radius: 999px; font-size: 14px; cursor: pointer; white-space: nowrap;'
PILL_ON = PILL + f' border: 1px solid {INK}; background: {INK}; color: #FFFFFF; font-weight: 600;'
PILL_OFF = PILL + f' border: 1px solid #E5E8EB; background: #FFFFFF; color: #4E5968;'
SORT_ON = f'border: none; background: none; padding: 0; font-size: 14px; color: {INK}; font-weight: 700; cursor: pointer;'
SORT_OFF = f'border: none; background: none; padding: 0; font-size: 14px; color: {MUTE}; cursor: pointer;'
PG = 'min-width: 36px; height: 36px; padding: 0 6px; border-radius: 10px; font-size: 14px; cursor: pointer;'
PG_ON = PG + f' border: none; background: {INK}; color: #FFFFFF; font-weight: 700;'
PG_OFF = PG + f' border: none; background: transparent; color: #4E5968;'

# ---------- comparison row used by 지원 준비 ----------
d_match = lambda b, c, bg, need, kind, mine, note='': (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 0; border-top: 1px solid {LINE};"><div style="display: flex; align-items: center; gap: 8px;"><span style="padding: 4px 10px; border-radius: 999px; background: {bg}; color: {c}; font-size: 12px; font-weight: 700;">{b}</span><span style="font-size: 12px; color: {MUTE};">{kind}</span></div>'
                                                       f'<span style="font-size: 15px; line-height: 1.5;">공고 "{need}"</span><div style="display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; border-radius: 12px; background: {bg};"><span style="font-size: 12px; color: {c}; font-weight: 600;">내 경험</span><span style="font-size: 14px; line-height: 1.55;">{mine}</span>'
                                                       + (f'<span style="font-size: 13px; color: {c};">{note}</span>' if note else '') + '</div></div>')

# ---------- form inputs (이력서, 로그인) ----------
INP_D = f'height: 48px; box-sizing: border-box; padding: 0 14px; font-size: 16px; border: none; border-radius: 12px; font-family: inherit; background: {FILL}; color: {INK}; width: 100%;'
TA_D = f'height: 112px; box-sizing: border-box; padding: 14px; font-size: 16px; line-height: 1.6; border: none; border-radius: 12px; font-family: inherit; resize: none; background: {FILL}; color: {INK}; width: 100%;'

# ---------- course and policy data ----------
COURSE_JSON = json.dumps(COURSES_ALL, ensure_ascii=False)
POL_JSON = json.dumps(POL_ALL, ensure_ascii=False)
GCOL = {'마케팅': ('#FFF4E5', '#C26A00'), 'AI': ('#F0EBFF', '#6B4EE6'), '데이터': ('#E8F3FF', '#1B64DA'), '기획, PM': ('#E6F7F1', '#0E8A63'),
        '개발': ('#EEF1F5', '#4E5968'), '디자인': ('#FFEEF3', '#D6336C'), '기타': ('#F2F4F6', '#6B7684')}
STC = {'모집 중': (BLUE_BG, BLUE_D), '모집 예정': (OR_BG, OR), '상시': ('#E6F7F1', '#0E8A63'), '진행 중': (FILL, SUB), '종료': (FILL, MUTE),
       '신청 중': (BLUE_BG, BLUE_D), '예정': (OR_BG, OR), '마감': (FILL, MUTE)}
THUMBS = {'edu-1421': THUMB1, 'edu-1235': THUMB2, 'edu-1233': '/_blob/da3e1859d4a5fb5d959f9a68a85e87a4', 'edu-1202': '/_blob/3353abd4717e44ab69d847de14e0e40c', 'edu-1419': '/_blob/2b1701dbd5336858481fae2422be0183', 'edu-1182': '/_blob/87f89c5a192c25ef010b457ee17e7c45', 'edu-1195': '/_blob/900a268958a372285a19d0476c1ef3dd', 'edu-715': '/_blob/6fc9bd2821d6438cc5b97a683759372c', 'edu-835': '/_blob/c88a1eb7bb1518ac0f871c8ae631c6ad'}  # 4개는 아노 제공 포스터 (2026.11.02)
# 청년 정책 카드 이미지 (아노 제공 포스터, 2026.11.02)
PTHUMBS = {'pol-20261018005400213993': '/_blob/61db9921e026af1c40c1407f866018d8', 'pol-20261018005400213991': '/_blob/c2dbb8dd0f747dc2fecc62ed45422aed', 'pol-20261018005400213990': '/_blob/2903327b271a5f5367228d0fbc308a83', 'pol-20261018005400213983': '/_blob/7260be2b13adc600fd41dc50e54baf09', 'pol-20261018005400213984': '/_blob/a63c4957a0dce8ee767691f6f6c7fd7f', 'pol-20260317005400112169': '/_blob/3f861b175e3d523ff52cf3b172a934bc'}
N_LIVE = sum(1 for c in COURSES_ALL if c['st'] in ('모집 중', '모집 예정', '상시'))

boards = {}
