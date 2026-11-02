"""P02 직무 찾기: 7개 직무, 공고 검색, 필터, 정렬, 페이지."""

# --- S1 posting list: 46 real 2026 entry-level postings, search, filter, sort, pagination ---
_P = json.load(open(os.path.join(DATA, 'posts2026.json'), encoding='utf-8'))
POSTS = []
for p in _P:
    demo = p['company'] == '올리브인터내셔널'
    POSTS.append({'id': post_id(p['url'], len(POSTS)), 'c': p['company'], 't': p['title'], 'ty': p['type'], 'd': p['close'], 'u': p['url'], 's': p['size'] if p['size'] not in ('', '기타') else '',
                  'ov': len(set(p['ov'])), 'presetOverlapSkillIds': p['ov'], 'cr': p['created'], 'demo': demo})
POSTS_JSON = json.dumps(POSTS, ensure_ascii=False)
_OTHER = json.load(open(os.path.join(DATA, 'jobs_other.json'), encoding='utf-8'))
JOB_KEYS = [('sns', 'SNS 콘텐츠 마케팅')] + [(k, v['label']) for k, v in _OTHER.items()]
JOBS_DATA = {'sns': {'label': 'SNS 콘텐츠 마케팅', 'posts': POSTS, 'src': '링커리어, 채용 게시판 2026 수집 공고'}}
JOBS_DATA.update({k: {'label': v['label'], 'posts': v['posts'], 'src': '잡코리아 등 채용 사이트 수집 공고 (마감 전)'} for k, v in _OTHER.items()})
JOBS_JSON = json.dumps(JOBS_DATA, ensure_ascii=False)
N_ALL = len(POSTS)
N_TY = {k: sum(1 for p in POSTS if p['ty'] == k) for k in ('인턴', '신입')}
LOGO_BG = ['#2E7D4F', '#3182F6', '#F04452', '#6B4EE6', '#FF8A00', '#191F28', '#0FA3B1', '#C2185B', '#4E5968', '#8D6E63']

PROFILE_JSON = json.dumps({'resumeContent': EXP_LINES, 'resumeSkillIds': [name for name, _ in HAVE], 'seedId': 'preset-resume-v1'}, ensure_ascii=False)
MATCH_JS = r'''  hasResumeContent(profile) {
    return Array.isArray(profile.resumeContent) && profile.resumeContent.some(value => typeof value === 'string' && value.trim().length > 0);
  }
  matchState(post, profile) {
    if (!this.hasResumeContent(profile)) return { status: 'unregistered', count: null };
    const valid = (ids) => Array.isArray(ids) && ids.every(id => typeof id === 'string' && id.trim().length > 0);
    const required = post.postingSkillIds === undefined && profile.seedId === 'preset-resume-v1' ? post.presetOverlapSkillIds : post.postingSkillIds;
    if (!valid(profile.resumeSkillIds) || !valid(required)) return { status: 'pending', count: null };
    const mine = new Set(profile.resumeSkillIds);
    const count = [...new Set(required)].filter(id => mine.has(id)).length;
    return { status: 'analyzed', count };
  }
  rankPosts(posts, profile, sort) {
    const date = p => Number.isFinite(p.cr) && p.cr > 0 ? p.cr : 0;
    return posts.map((post, index) => ({ ...post, match: this.matchState(post, profile), index }))
      .sort((a, b) => {
        const demoFirst = Number(b.demo === true) - Number(a.demo === true);
        if (sort === 'rec' && demoFirst) return demoFirst;
        if (sort === 'rec' && this.hasResumeContent(profile)) {
          const ready = Number(b.match.status === 'analyzed') - Number(a.match.status === 'analyzed');
          if (ready) return ready;
          if (a.match.status === 'analyzed' && a.match.count !== b.match.count) return b.match.count - a.match.count;
        }
        return date(b) - date(a) || a.index - b.index;
      });
  }
'''

# 밑줄 탭: 데스크톱 직무 찾기와 교육과정이 같이 쓴다
UTAB = 'border: none; background: none; padding: 0 14px 12px; margin-bottom: -1px; font-size: 15px; font-family: inherit; cursor: pointer; white-space: nowrap; border-bottom: 2px solid '
TAB_ON = UTAB + f'{INK}; color: {INK}; font-weight: 700;'
TAB_OFF = UTAB + f'transparent; color: {SUB};'
FTAB = f'border: none; border-bottom: 2px solid transparent; background: none; margin-bottom: -1px; padding: 14px 4px 12px; font-size: 15px; font-family: inherit; color: #4E5968; cursor: pointer; white-space: nowrap;'
FCHIP = 'height: 36px; padding: 0 14px; border-radius: 999px; font-size: 14px; font-family: inherit; cursor: pointer; white-space: nowrap;'
FCHIP_ON = FCHIP + f' border: 1px solid {BLUE}; background: {BLUE_BG}; color: {BLUE_D}; font-weight: 600;'
FCHIP_OFF = FCHIP + ' border: 1px solid #E5E8EB; background: #FFFFFF; color: #4E5968;'
LIST_JS = MATCH_JS + f'''  constructor(props) {{ super(props); const jm = (typeof location !== 'undefined' && location.hash.match(/job=(\\w+)/)); this.state = {{ mode: 'new', trendOpen: {TREND_JS}, page: 1, sort: 'rec', ty: 'all', q: '', job: jm ? jm[1] : 'sns', jq: '', fo: '', fty: [], fsz: [], fdl: [] }}; }}
  renderVals() {{
    const D = {JOBS_JSON}, profile = {PROFILE_JSON};
    const job = D[this.state.job] ? this.state.job : 'sns', J = D[job], POSTS = J.posts, isSns = job === 'sns';
    const BG = {json.dumps(LOGO_BG)};
    const s = this.state, m = s.mode, set = (o) => this.setState(Object.assign({{ page: 1 }}, o));
    const now = Date.now(), day = 86400000;
    const dleft = (d) => d ? Math.ceil((new Date(d + 'T23:59:59+09:00').getTime() - now) / day) : null;
    const q = (s.q || '').trim().toLowerCase();
    const dlTag = (p) => {{ const n = dleft(p.d); return n === null ? '상시 채용' : n >= 0 && n <= 7 ? '7일 안에 마감' : '마감일 있음'; }};
    const fOk = (p) => (!s.fty.length || s.fty.indexOf(p.ty) >= 0) && (!s.fsz.length || s.fsz.indexOf(p.s || '정보 없음') >= 0)
      && (!s.fdl.length || s.fdl.indexOf(dlTag(p)) >= 0 || (s.fdl.indexOf('마감일 있음') >= 0 && dlTag(p) === '7일 안에 마감'));
    let L = POSTS.filter(p => (s.ty === 'all' || p.ty === s.ty) && fOk(p) && (!q || (p.c + ' ' + p.t).toLowerCase().indexOf(q) >= 0));
    const open = (p) => {{ const n = dleft(p.d); return n !== null && n >= 0 ? n : 9999; }};
    L = this.rankPosts(L, profile, s.sort);
    const unregistered = !this.hasResumeContent(profile);
    const allPending = L.length > 0 && L.every(p => p.match.status === 'pending');
    const sortNote = s.sort !== 'rec' ? '' : unregistered ? '이력서를 등록하면 겹치는 역량 순으로 볼 수 있어요. 현재는 최신순이에요' : allPending ? '역량 분석 준비 중이에요. 현재는 최신순이에요' : '';
    if (s.sort === 'close') L = L.slice().sort((a, b) => open(a) - open(b));
    const per = 10, pages = Math.max(1, Math.ceil(L.length / per)), page = Math.min(s.page, pages);
    const rows = L.slice((page - 1) * per, page * per).map((p) => {{
      const n = dleft(p.d), code = [...p.c].reduce((a, ch) => a + ch.charCodeAt(0), 0);
      const tags = [p.ty].concat(p.s ? [p.s] : []);
      const md = p.d ? p.d.slice(5).replace('-', '.') : '';
      return {{ c: p.c, t: p.t, tags, ty: p.ty, size: p.s || '정보 없음', closeTxt: p.d ? '~ ' + md : '상시 채용', closeStyle: 'font-size: 14px; color: ' + (n !== null && n < 0 ? '{MUTE}' : '{INK}') + ';', init: p.c.replace(/[()㈜\\s]/g, '').slice(0, 1), logo: 'width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; background: ' + BG[code % BG.length] + '; color: #FFFFFF; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: center;',
        ov: p.match.status === 'unregistered' ? '이력서를 등록해주세요' : p.match.status === 'pending' ? '역량 분석 준비 중' : '내 경험과 겹치는 역량 ' + p.match.count,
        ovStyle: 'padding: 3px 8px; border-radius: 6px; font-size: 12px; ' + (p.match.status === 'analyzed' ? 'background: {BLUE_BG}; color: {BLUE_D};' : 'background: #F2F4F6; color: #4E5968;'), demo: p.demo, notDemo: !p.demo, url: p.u || '#',
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
    const jobs = Object.keys(D).filter((k) => !jq || D[k].label.toLowerCase().replace(/\\s/g, '').indexOf(jq) >= 0).map((k) => ({{ label: D[k].label, style: k === job ? '{PILL_ON}' : '{PILL_OFF}', tab: k === job ? '{TAB_ON}' : '{TAB_OFF}', cur: k === job ? 'page' : 'false', go: () => this.setState({{ job: k, page: 1, q: '', ty: 'all', jq: '' }}) }}));
    const cnt = (t) => POSTS.filter((p) => t === 'all' || p.ty === t).length;
    // P02-F09 상세 필터 (데스크톱)
    const FG = [['fty', '채용형태', ['인턴', '신입']], ['fsz', '기업 형태', ['대기업', '중견기업', '중소기업', '스타트업', '기타', '정보 없음']], ['fdl', '마감', ['7일 안에 마감', '마감일 있음', '상시 채용']]];
    const toggle = (k, v) => () => {{ const a = s[k].slice(), i = a.indexOf(v); if (i >= 0) a.splice(i, 1); else a.push(v); set({{ [k]: a }}); }};
    const ftabs = FG.map(([k, label]) => {{ const n = s[k].length, on = s.fo === k; return {{ label: label + (n ? ' ' + n : '') + (on ? ' ▴' : ' ▾'), cur: on ? 'true' : 'false', go: () => this.setState({{ fo: on ? '' : k }}),
      style: '{FTAB}' + (on ? ' border-bottom-color: {BLUE};' : '') + (n || on ? ' color: {BLUE_D}; font-weight: 700;' : '') }}; }});
    const og = FG.find(([k]) => k === s.fo);
    const fopts = og ? og[2].map((v) => {{ const on = s[og[0]].indexOf(v) >= 0; return {{ label: v, on: on ? 'true' : 'false', go: toggle(og[0], v), style: on ? '{FCHIP_ON}' : '{FCHIP_OFF}' }}; }}) : [];
    const fsel = [];
    FG.forEach(([k, label]) => s[k].forEach((v) => fsel.push({{ label: label + ' > ' + v, go: toggle(k, v) }})));
    return {{ unregistered, registered: !unregistered, sortNote, hasSortNote: !!sortNote, jobName: J.label, isSns, notSns: !isSns, showFit: isSns && m === 'new', fitTodo: !isSns && m === 'new', jobs, jq: s.jq, setJq: (e) => this.setState({{ jq: e && e.target ? e.target.value : '' }}), noJob: jobs.length === 0, srcNote: J.src + ' ' + POSTS.length + '건' + (isSns ? ' · 시연은 올리브인터내셔널 공고로 비교해요' : ' · 공고 비교는 SNS 콘텐츠 마케팅으로 시연해요'),
      cntAll: '전체 ' + cnt('all'), cntIntern: '인턴 ' + cnt('인턴'), cntNew: '신입 ' + cnt('신입'),
      count: m === 'new' ? '신입, 인턴 공고 ' + POSTS.length + '건' : (isSns ? '경력 공고 22건 · 2026.10 수집' : '경력 공고는 준비 중'), isNew: m === 'new', isExp: m === 'exp', newStyle: st(m === 'new'), expStyle: st(m === 'exp'), pickNew: () => this.setState({{ mode: 'new' }}), pickExp: () => this.setState({{ mode: 'exp' }}),
      {TREND_VALS},
      rows, empty: L.length === 0, hasRows: L.length > 0, total: L.length, range: from + '–' + to, nums, pages,
      prev: () => this.setState({{ page: Math.max(1, page - 1) }}), next: () => this.setState({{ page: Math.min(pages, page + 1) }}),
      prevStyle: '{PG_OFF}' + (page === 1 ? ' opacity: 0.35;' : ''), nextStyle: '{PG_OFF}' + (page === pages ? ' opacity: 0.35;' : ''),
      ty: {{ all: pill('ty', 'all'), intern: pill('ty', '인턴'), newbie: pill('ty', '신입') }},
      sort: {{ rec: sortb('rec'), new: sortb('new'), close: sortb('close') }},
      ftabs, fopts, fPanel: !!og, fPanelTitle: og ? og[1] : '', fsel, hasF: fsel.length > 0, resetF: () => set({{ fty: [], fsz: [], fdl: [] }}),
      q: s.q, setQ: (e) => set({{ q: e && e.target ? e.target.value : '' }}), clearQ: () => set({{ q: '', fty: [], fsz: [], fdl: [] }}), hasQ: !!q }};
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
    fbar = (f'<div style="display: flex; align-items: center; gap: 28px; border-bottom: 1px solid #E5E8EB;">'
            f'<sc-for list="@@ftabs@@" as="f" hint-placeholder-count="3"><button type="button" onClick="@@f.go@@" aria-expanded="@@f.cur@@" style="@@f.style@@">@@f.label@@</button></sc-for>'
            f'<div style="margin-left: auto; padding: 8px 0;">{search}</div></div>'
            f'<sc-if value="@@fPanel@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; border-radius: 14px; background: #F9FAFB;">'
            f'<span style="font-size: 13px; color: {SUB};">@@fPanelTitle@@</span><div style="display: flex; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@fopts@@" as="o" hint-placeholder-count="3"><button type="button" onClick="@@o.go@@" aria-pressed="@@o.on@@" style="@@o.style@@">@@o.label@@</button></sc-for></div></div></sc-if>'
            f'<sc-if value="@@hasF@@" hint-placeholder-val="@@false@@"><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@fsel@@" as="x" hint-placeholder-count="1"><button type="button" onClick="@@x.go@@" aria-label="@@x.label@@ 빼기" style="display: flex; align-items: center; gap: 6px; height: 34px; padding: 0 12px; border: none; border-radius: 999px; background: {BLUE_BG}; color: {INK}; font-size: 13px; font-family: inherit; cursor: pointer;">@@x.label@@<span aria-hidden="true" style="font-size: 15px; color: #4E5968;">×</span></button></sc-for>'
            f'<button type="button" onClick="@@resetF@@" style="border: none; background: none; padding: 0 6px; font-size: 13px; font-weight: 600; color: #4E5968; cursor: pointer; font-family: inherit;">↺ 초기화</button></div></sc-if>')
    return (fbar +
            f'<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 4px;"><span style="font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@total@@</b>건 중 @@range@@</span><div style="display: flex; gap: 10px; align-items: center;">{sorts}</div></div>')


GRID = '200px minmax(0, 1fr) 72px 88px 92px 150px'


def list_rows(mobile):
    pre = 'm-' if mobile else ''
    tagchips = f'<sc-for list="@@r.tags@@" as="g" hint-placeholder-count="2"><span style="padding: 3px 8px; border-radius: 6px; background: {FILL}; font-size: 12px; color: {SUB};">@@g@@</span></sc-for>'
    ov = '<span style="@@r.ovStyle@@">@@r.ov@@</span>'
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
        # 데스크톱: 채용 사이트처럼 열 (기업명, 공고명, 채용형태, 기업 형태, 마감일). 필터 (P02-F09)와 같은 항목
        row = (f'<div style="display: grid; grid-template-columns: {GRID}; align-items: center; gap: 16px; padding: 16px 0; border-top: 1px solid {LINE};">'
               f'<span style="display: flex; align-items: center; gap: 12px; min-width: 0;"><span aria-hidden="true" style="@@r.logo@@">@@r.init@@</span><span style="font-size: 14px; color: #4E5968; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@@r.c@@</span></span>'
               f'<span style="min-width: 0; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 16px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@@r.t@@</span>'
               f'<span style="display: flex; gap: 4px; flex-wrap: wrap;">{demo_tag}{ov}</span></span>'
               f'<span style="font-size: 14px; color: {INK}; text-align: center;">@@r.ty@@</span>'
               f'<span style="font-size: 14px; color: #4E5968; text-align: center;">@@r.size@@</span>'
               f'<span style="display: flex; flex-direction: column; align-items: center; gap: 2px;"><span style="@@r.closeStyle@@">@@r.closeTxt@@</span><sc-if value="@@r.hasDue@@" hint-placeholder-val="@@false@@"><span style="font-size: 12px; font-weight: 700; color: {RED};">@@r.due@@</span></sc-if></span>'
               f'<span style="display: flex; justify-content: flex-end; gap: 8px;">{save_btn("r.sv", 38)}{act}</span></div>')
    empty = (f'<sc-if value="@@empty@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 0; border-top: 1px solid {LINE}; color: {SUB}; font-size: 15px;">'
             f'검색 결과가 없어요<button type="button" onClick="@@clearQ@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">검색어 지우기</button></div></sc-if>')
    pager = (f'<sc-if value="@@hasRows@@" hint-placeholder-val="@@true@@"><nav aria-label="페이지" style="display: flex; justify-content: center; align-items: center; gap: 4px; padding: {"14px 0 6px" if mobile else "20px 0 8px"}; border-top: 1px solid {LINE};">'
             f'<button type="button" onClick="@@prev@@" aria-label="이전 페이지" style="@@prevStyle@@">‹</button>'
             f'<sc-for list="@@nums@@" as="p" hint-placeholder-count="5"><button type="button" onClick="@@p.go@@" aria-current="@@p.cur@@" style="@@p.style@@">@@p.n@@</button></sc-for>'
             f'<button type="button" onClick="@@next@@" aria-label="다음 페이지" style="@@nextStyle@@">›</button></nav></sc-if>')
    head = '' if mobile else (f'<div style="display: grid; grid-template-columns: {GRID}; gap: 16px; padding: 10px 0; font-size: 13px; color: {SUB};">'
                              '<span>기업명</span><span>공고명</span><span style="text-align: center;">채용형태</span><span style="text-align: center;">기업 형태</span><span style="text-align: center;">마감일</span><span></span></div>')
    return f'{head}<sc-for list="@@rows@@" as="r" hint-placeholder-count="10">{row}</sc-for>{empty}{pager}'


def list_card(mobile):
    pad = '18px 18px 8px' if mobile else '24px 28px 12px'
    return (f'    <section aria-labelledby="{"m-" if mobile else ""}list" style="display: flex; flex-direction: column; gap: {12 if mobile else 14}px; padding: {pad}; {CARD}">\n'
            f'      <h2 id="{"m-" if mobile else ""}list" style="margin: 0; font-size: {17 if mobile else 18}px; font-weight: 700;">공고를 골라 비교해 보세요</h2>\n'
            f'      {list_toolbar(mobile)}<sc-if value="@@hasSortNote@@" hint-placeholder-val="@@true@@"><p role="status" style="margin: 0; font-size: 13px; line-height: 1.5; color: {SUB};">@@sortNote@@</p></sc-if>\n      <div>{list_rows(mobile)}</div>\n'
            f'      <span style="font-size: 12px; color: {MUTE};">출처: @@srcNote@@</span>\n    </section>\n')

def job_fit_card_d():
    items = ''.join(f'<span style="display: flex; align-items: center; gap: 6px; font-size: 14px; color: #4E5968;"><span style="font-weight: 700; color: {BLUE_D};">{i}</span>{name}</span>' for i, (name, _, _) in enumerate(RANK, 1))
    return (f'<section aria-label="이 직무가 원하는 역량" style="display: flex; align-items: center; gap: 24px; padding: 20px 28px; {CARD}">'
            f'<h2 style="flex-shrink: 0; margin: 0; font-size: 15px; font-weight: 700;">많이 찾는 역량</h2><div style="display: flex; gap: 8px 16px; flex-wrap: wrap;">{items}</div>'
            f'<div style="flex-shrink: 0; margin-left: auto; display: flex; align-items: center; gap: 16px;"><sc-if value="@@unregistered@@" hint-placeholder-val="@@true@@"><span style="padding: 3px 8px; border-radius: 6px; background: #F2F4F6; color: #4E5968; font-size: 12px;">이력서를 등록해주세요</span></sc-if><button type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; background: none; padding: 0; font-size: 14px; font-weight: 600; color: {BLUE_D}; cursor: pointer; font-family: inherit; white-space: nowrap;">이 직무 트렌드 보기 ›</button></div></section>')


def job_fit_card(mobile):
    chips = ''.join(f'<span style="padding: 8px 13px; border-radius: 999px; background: {FILL}; color: {SUB}; font-size: 14px;">{name}</span>' for name, _, _ in RANK)
    return (f'<section aria-label="이 직무가 원하는 역량" style="display: flex; flex-direction: column; gap: 14px; padding: {"18px" if mobile else "22px 28px"}; {CARD}">'
            f'<h2 style="margin: 0; font-size: 16px;">이 직무 공고가 많이 찾는 역량</h2><div style="display: flex; gap: 6px; flex-wrap: wrap;">{chips}</div>'
            '<sc-if value="@@unregistered@@" hint-placeholder-val="@@true@@"><span style="align-self: flex-start; padding: 3px 8px; border-radius: 6px; background: #F2F4F6; color: #4E5968; font-size: 12px;">이력서를 등록해주세요</span></sc-if></section>')


s1_body = f'''  <div style="padding: 28px 56px 0; display: flex; justify-content: space-between; align-items: center;">
    <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">@@jobName@@</h1>
    <div role="tablist" aria-label="경력 구분" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);"><button type="button" role="tab" onClick="@@pickNew@@" style="@@newStyle@@">신입, 인턴</button><button type="button" role="tab" onClick="@@pickExp@@" style="@@expStyle@@">경력</button></div>
  </div>
  <nav aria-label="직무" style="margin: 20px 56px 0; display: flex; align-items: flex-end; gap: 4px; border-bottom: 1px solid #E5E8EB;"><sc-for list="@@jobs@@" as="j" hint-placeholder-count="7"><button type="button" onClick="@@j.go@@" aria-current="@@j.cur@@" style="@@j.tab@@">@@j.label@@</button></sc-for>
    <label style="margin: 0 0 8px auto; display: flex; align-items: center; gap: 6px; height: 34px; padding: 0 12px; border-radius: 10px; background: {FILL};"><svg aria-hidden="true" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="{SUB}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">직무 검색</span><input type="search" value="@@jq@@" onChange="@@setJq@@" placeholder="직무 검색" style="width: 110px; border: none; background: transparent; font-size: 14px; font-family: inherit; color: {INK}; outline: none;"></label></nav>
  <sc-if value="@@noJob@@" hint-placeholder-val="@@false@@"><p style="margin: 10px 56px 0; font-size: 13px; color: {SUB};">"@@jq@@" 직무는 아직 준비 중이에요. 검색어를 지우면 7개 직무가 다시 보여요</p></sc-if>
  <div style="display: flex; flex-direction: column; gap: 16px; padding: 24px 56px 56px;">
    <sc-if value="@@showFit@@" hint-placeholder-val="@@true@@">
{job_fit_card_d()}    </sc-if>
    <sc-if value="@@fitTodo@@" hint-placeholder-val="@@false@@"><section style="display: flex; align-items: center; gap: 12px; padding: 20px 28px; {CARD}">{AI}<span style="font-size: 15px; line-height: 1.5; color: #4E5968;">이 직무의 역량 분석은 준비 중이에요. 공고 원문은 지금 볼 수 있고, 공고 비교는 <b style="color: {INK};">SNS 콘텐츠 마케팅</b>으로 시연해요</span></section></sc-if>
    <sc-if value="@@isExp@@" hint-placeholder-val="@@false@@"><section aria-label="경력 공고 안내" style="display: flex; align-items: center; gap: 24px; padding: 20px 28px; {CARD}"><h2 style="flex-shrink: 0; margin: 0; font-size: 15px; font-weight: 700;">경력 공고</h2><span style="font-size: 14px; color: #4E5968;">공고를 골라 바로 비교해요. 시연은 맨 위 공고로 진행해요</span><sc-if value="@@isSns@@" hint-placeholder-val="@@true@@"><div style="margin-left: auto;"><button type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; background: none; padding: 0; font-size: 14px; font-weight: 600; color: {BLUE_D}; cursor: pointer; font-family: inherit; white-space: nowrap;">이 직무 트렌드 보기 ›</button></div></sc-if></section></sc-if>
{list_card(False)}  </div>
{trend_popup(False, None)}'''
s1_script = LIST_JS.replace('@@ON@@', seg_style(True)).replace('@@OFF@@', seg_style(False))
boards['S1-list.dc.html'] = ('S1 직무 찾기 (신입, 인턴은 적합도 / 경력은 공고)', dpage('S1-list.dc.html', '직무 찾기', 'find', s1_body, s1_script))

# --- mobile ---
m_jobs = f'''<div class="illo-scroll" style="display: flex; gap: 6px; overflow-x: auto; padding: 4px 0;"><sc-for list="@@jobs@@" as="j" hint-placeholder-count="7"><button type="button" onClick="@@j.go@@" style="@@j.style@@">@@j.label@@</button></sc-for></div>
<label style="display: flex; gap: 8px; align-items: center; font-size: 13px;">직무 검색<input type="search" aria-label="직무 검색" value="@@jq@@" onChange="@@setJq@@" placeholder="다른 직무 검색" style="flex: 1; min-width: 0; height: 36px; border: none; border-radius: 12px; padding: 0 12px; background: {FILL}; font: inherit;"></label>
<sc-if value="@@noJob@@" hint-placeholder-val="@@false@@"><span style="font-size: 13px; color: {SUB};">"@@jq@@" 직무는 아직 준비 중이에요. 검색어를 지우면 7개 직무가 다시 보여요</span></sc-if>'''
m_s1 = f'''
    <div style="display: flex; gap: 8px; justify-content: space-between; align-items: flex-end; padding: 8px 4px 4px;"><div style="min-width: 0; display: flex; flex-direction: column; gap: 4px;"><h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: -0.02em;">@@jobName@@</h1><span style="font-size: 13px; color: {SUB};">@@count@@</span></div><sc-if value="@@isSns@@" hint-placeholder-val="@@true@@"><button type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; background: none; padding: 0 0 2px; font-size: 13px; font-weight: 600; color: {BLUE}; cursor: pointer;">트렌드 ›</button></sc-if></div>
    {m_jobs}
    <div role="tablist" aria-label="경력 구분" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);"><button type="button" role="tab" onClick="@@pickNew@@" style="@@newStyle@@">신입, 인턴</button><button type="button" role="tab" onClick="@@pickExp@@" style="@@expStyle@@">경력</button></div>
    <sc-if value="@@showFit@@" hint-placeholder-val="@@true@@">{job_fit_card(True)}</sc-if>
    <sc-if value="@@fitTodo@@" hint-placeholder-val="@@false@@"><section style="padding: 18px; {CARD} font-size: 14px; line-height: 1.5;">이 직무의 역량 분석은 준비 중이에요. 공고 원문은 지금 볼 수 있고, 공고 비교는 SNS 콘텐츠 마케팅으로 시연해요</section></sc-if>
    <sc-if value="@@isExp@@" hint-placeholder-val="@@false@@">{exp_card(True)}</sc-if>
{list_card(True)}{trend_popup(True, None)}'''
m_s1_script = LIST_JS.replace('@@ON@@', seg_style(True, True)).replace('@@OFF@@', seg_style(False, True))
boards['m-S1-list.dc.html'] = ('M1 직무 찾기 (모바일)', mpage('m-S1-list.dc.html', 'M1 직무 찾기 (모바일)', topbar_logo(auth_mobile()), m_s1, 'find', m_s1_script))
