"""P02 직무 찾기: 7개 직무, 공고 검색, 필터, 정렬, 페이지."""

# --- S1 posting list: 46 real 2026 entry-level postings, search, filter, sort, pagination ---
_P = json.load(open(os.path.join(DATA, 'posts2026.json'), encoding='utf-8'))
POSTS = []
for p in _P:
    demo = p['company'] == '올리브인터내셔널'
    POSTS.append({'id': post_id(p['url'], len(POSTS)), 'c': p['company'], 't': p['title'], 'ty': p['type'], 'd': p['close'], 'u': p['url'], 's': p['size'] if p['size'] not in ('', '기타') else '',
                  'ov': len(set(p['ov'])), 'presetOverlapSkillIds': p['ov'], 'cr': p['created'], 'demo': demo})
# 회사 로고 (아노 제공 이미지에서 잘라 냄, design/assets/logo-*.png). 없는 회사는 첫 글자
LOGOS = [('올리브인터내셔널', None, 'd55bb7e0ea8e688c8f6c3ae2f3515559'), ('카카오', None, 'e1e6c601728778273841a8308cc0b7df'), ('클래스101', None, '1801b663d968a47c82d6f4456feebf05'), ('트립비토즈', None, 'e87c804c93a65a6a60510230407ef8bd'), ('뷰에누보', None, '7847030e62073a1e1de9e174e11a11a8'),
         ('앳홈', None, 'd4d2d0bfac8d1a4f475013e7c6b579ac'), ('기업명 비공개', '뷰티 콘텐츠 마케터(전환형', '961013624ee02d6d64f63007fc2705bf'), ('기업명 비공개', '뷰티 색동서울', '514ec4644b47e250236e6cbeeee6a0bb'), ('퍼포즈드', None, '2ed7d28a95c601ad1d55664bc55d55c6'), ('패스트뷰', None, '694ea27b38f150b3051b8f71451558b2')]
for p in POSTS:
    for co, tit, h in LOGOS:
        if p['c'] == co and (tit is None or tit in p['t']):
            p['logo'] = '/_blob/' + h
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
FTAB = f'border: none; border-bottom: 2px solid transparent; background: none; margin-bottom: -1px; padding: 18px 4px 16px; font-size: 16px; font-family: inherit; color: #333D4B; cursor: pointer; white-space: nowrap;'
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
      return {{ logoImg: p.logo || '', hasLogo: !!p.logo, noLogo: !p.logo, c: p.c, t: p.t, tags, ty: p.ty, size: p.s || '정보 없음', closeTxt: p.d ? '~ ' + md : '상시 채용', closeStyle: 'font-size: 14px; color: ' + (n !== null && n < 0 ? '{MUTE}' : '{INK}') + ';', init: p.c.replace(/[()㈜\\s]/g, '').slice(0, 1), logo: 'width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; background: ' + BG[code % BG.length] + '; color: #FFFFFF; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: center;',
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
    const jobOn = s.fo === 'job';
    const jobTab = {{ label: '직무' + (jobOn ? ' ▴' : ' ▾'), cur: jobOn ? 'true' : 'false', go: () => this.setState({{ fo: jobOn ? '' : 'job' }}), style: '{FTAB}' + (jobOn ? ' border-bottom-color: {BLUE}; color: {BLUE_D}; font-weight: 700;' : '') }};
    const ftabs = [jobTab].concat(FG.map(([k, label]) => {{ const n = s[k].length, on = s.fo === k; return {{ label: label + (n ? ' ' + n : '') + (on ? ' ▴' : ' ▾'), cur: on ? 'true' : 'false', go: () => this.setState({{ fo: on ? '' : k }}),
      style: '{FTAB}' + (on ? ' border-bottom-color: {BLUE};' : '') + (n || on ? ' color: {BLUE_D}; font-weight: 700;' : '') }}; }}));
    const og = FG.find(([k]) => k === s.fo);
    const jobOpts = Object.keys(D).map((k) => ({{ label: D[k].label, on: k === job ? 'true' : 'false', go: () => this.setState({{ job: k, page: 1, q: '', ty: 'all', fo: '' }}), style: k === job ? '{FCHIP_ON}' : '{FCHIP_OFF}' }}));
    const fopts = jobOn ? jobOpts : og ? og[2].map((v) => {{ const on = s[og[0]].indexOf(v) >= 0; return {{ label: v, on: on ? 'true' : 'false', go: toggle(og[0], v), style: on ? '{FCHIP_ON}' : '{FCHIP_OFF}' }}; }}) : [];
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
      ftabs, fopts, fPanel: jobOn || !!og, fPanelTitle: jobOn ? '직무' : og ? og[1] : '', fsel, hasF: fsel.length > 0, resetF: () => set({{ fty: [], fsz: [], fdl: [] }}),
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
    return list_sortrow(search)


def filter_bar():
    search = (f'<label style="width: 300px; display: flex; align-items: center; gap: 8px; height: 46px; padding: 0 14px; border: 1px solid #E5E8EB; border-radius: 12px; background: #FFFFFF; box-sizing: border-box;">'
              f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
              f'<span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">공고명, 기업 검색</span>'
              f'<input type="search" value="@@q@@" onChange="@@setQ@@" placeholder="공고명, 기업 검색" style="flex: 1 1 0; min-width: 0; border: none; background: transparent; font-size: 15px; font-family: inherit; color: {INK}; outline: none;"></label>')
    fbar = (f'<div style="display: flex; align-items: center; gap: 36px; padding-left: 8px; border-top: 1px solid #E5E8EB; border-bottom: 1px solid #E5E8EB;">'
            f'<sc-for list="@@ftabs@@" as="f" hint-placeholder-count="3"><button type="button" onClick="@@f.go@@" aria-expanded="@@f.cur@@" style="@@f.style@@">@@f.label@@</button></sc-for>'
            f'<div style="margin-left: auto; padding: 8px 0;">{search}</div></div>'
            f'<sc-if value="@@jobPanel@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 18px; padding: 20px 22px; border-radius: 14px; background: #FFFFFF;">'
            f'<sc-if value="@@showAi@@" hint-placeholder-val="@@true@@"><div style="display: flex; flex-direction: column; gap: 10px;"><div style="display: flex; align-items: center; gap: 8px;"><span style="font-size: 13px; color: {SUB};">AI 추천 직무</span>{AI}'
            f'<span style="font-size: 12px; color: {MUTE};">내 이력서와 저장한 공고로 골랐어요 · 시연 예시</span>'
            f'<button type="button" onClick="@@aiAll@@" style="margin-left: auto; border: none; background: none; padding: 0; font-size: 13px; font-weight: 600; color: {BLUE_D}; cursor: pointer; font-family: inherit;">모두 추가</button></div>'
            f'<div style="display: flex; gap: 8px; flex-wrap: wrap;"><sc-for list="@@aiJobs@@" as="a" hint-placeholder-count="3"><button type="button" onClick="@@a.go@@" aria-pressed="@@a.on@@" style="@@a.style@@">@@a.label@@<span style="margin-left: 6px; font-size: 12px; font-weight: 400; opacity: 0.75;">@@a.why@@</span></button></sc-for></div></div></sc-if>'
            f'<sc-if value="@@aiLogin@@" hint-placeholder-val="@@false@@"><span style="font-size: 13px; color: {SUB};">{AI} 로그인하면 이력서로 맞는 직무를 AI가 골라 줘요</span></sc-if>'
            f'<div style="display: flex; flex-direction: column; gap: 10px;"><span style="font-size: 13px; color: {SUB};">직무 대분류</span><div style="display: flex; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@cats@@" as="c" hint-placeholder-count="14"><button type="button" onClick="@@c.go@@" aria-current="@@c.cur@@" style="@@c.style@@">@@c.label@@</button></sc-for></div></div>'
            f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; border-radius: 12px; background: #F6F7F9;"><span style="font-size: 13px; color: {SUB};">@@fcatName@@ 상세</span><div style="display: flex; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@subs@@" as="u" hint-placeholder-count="9"><button type="button" onClick="@@u.go@@" aria-pressed="@@u.on@@" style="@@u.style@@">@@u.label@@</button></sc-for></div></div></div></sc-if>'
            f'<sc-if value="@@fPanel@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; border-radius: 14px; background: #FFFFFF;">'
            f'<span style="font-size: 13px; color: {SUB};">@@fPanelTitle@@</span><div style="display: flex; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@fopts@@" as="o" hint-placeholder-count="3"><button type="button" onClick="@@o.go@@" aria-pressed="@@o.on@@" style="@@o.style@@">@@o.label@@</button></sc-for></div></div></sc-if>'
            f'<sc-if value="@@hasF@@" hint-placeholder-val="@@false@@"><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">'
            f'<sc-for list="@@fsel@@" as="x" hint-placeholder-count="1"><button type="button" onClick="@@x.go@@" aria-label="@@x.label@@ 빼기" style="display: flex; align-items: center; gap: 6px; height: 34px; padding: 0 12px; border: none; border-radius: 999px; background: {BLUE_BG}; color: {INK}; font-size: 13px; font-family: inherit; cursor: pointer;">@@x.label@@<span aria-hidden="true" style="font-size: 15px; color: #4E5968;">×</span></button></sc-for>'
            f'<button type="button" onClick="@@resetF@@" style="border: none; background: none; padding: 0 6px; font-size: 13px; font-weight: 600; color: #4E5968; cursor: pointer; font-family: inherit;">↺ 초기화</button></div></sc-if>')
    return fbar


def list_sortrow(search):
    sorts = (f'<button type="button" onClick="@@sort.rec.go@@" style="@@sort.rec.style@@">추천순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             f'<button type="button" onClick="@@sort.new.go@@" style="@@sort.new.style@@">최신순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             f'<button type="button" onClick="@@sort.close.go@@" style="@@sort.close.style@@">마감 임박순</button>')
    return (
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
               f'<span style="display: flex; align-items: center; gap: 12px; min-width: 0;"><sc-if value="@@r.hasLogo@@" hint-placeholder-val="@@false@@"><img src="@@r.logoImg@@" alt="" style="width: 40px; height: 40px; flex-shrink: 0; border-radius: 12px; border: 1px solid #F2F4F6; object-fit: cover; display: block; box-sizing: border-box;"></sc-if><sc-if value="@@r.noLogo@@" hint-placeholder-val="@@true@@"><span aria-hidden="true" style="@@r.logo@@">@@r.init@@</span></sc-if><span style="font-size: 14px; color: #4E5968; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@@r.c@@</span></span>'
               f'<span style="min-width: 0; display: flex; flex-direction: column; gap: 6px;"><span style="font-size: 16px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">@@r.t@@</span>'
               f'<span style="display: flex; gap: 4px; flex-wrap: wrap;">{demo_tag}{ov}</span></span>'
               f'<span style="font-size: 14px; color: {INK}; text-align: center;">@@r.ty@@</span>'
               f'<span style="font-size: 14px; color: #4E5968; text-align: center;">@@r.size@@</span>'
               f'<span style="display: flex; flex-direction: column; align-items: center; gap: 2px;"><span style="@@r.closeStyle@@">@@r.closeTxt@@</span><sc-if value="@@r.hasDue@@" hint-placeholder-val="@@false@@"><span style="font-size: 12px; font-weight: 700; color: {RED};">@@r.due@@</span></sc-if></span>'
               f'<span style="display: flex; justify-content: flex-end; gap: 8px;">{save_btn("r.sv", 38)}{act}</span></div>')
    empty = (f'<sc-if value="@@empty@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 0; border-top: 1px solid {LINE}; color: {SUB}; font-size: 15px;">'
             f'@@emptyMsg@@<button type="button" onClick="@@clearQ@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">검색어 지우기</button></div></sc-if>')
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
  <div style="margin: 24px 56px 0; display: flex; flex-direction: column; gap: 14px;">{filter_bar()}</div>
  <div style="display: flex; flex-direction: column; gap: 16px; padding: 24px 56px 56px;">
    <sc-if value="@@showFit@@" hint-placeholder-val="@@true@@">
{job_fit_card_d()}    </sc-if>
    <sc-if value="@@fitTodo@@" hint-placeholder-val="@@false@@"><section style="display: flex; align-items: center; gap: 12px; padding: 20px 28px; {CARD}">{AI}<span style="font-size: 15px; line-height: 1.5; color: #4E5968;">이 직무의 역량 분석은 준비 중이에요. 공고 원문은 지금 볼 수 있고, 공고 비교는 <b style="color: {INK};">SNS 콘텐츠 마케팅</b>으로 시연해요</span></section></sc-if>
    <sc-if value="@@isExp@@" hint-placeholder-val="@@false@@"><section aria-label="경력 공고 안내" style="display: flex; align-items: center; gap: 24px; padding: 20px 28px; {CARD}"><h2 style="flex-shrink: 0; margin: 0; font-size: 15px; font-weight: 700;">경력 공고</h2><span style="font-size: 14px; color: #4E5968;">공고를 골라 바로 비교해요. 시연은 맨 위 공고로 진행해요</span><sc-if value="@@isSns@@" hint-placeholder-val="@@true@@"><div style="margin-left: auto;"><button type="button" onClick="@@openTrend@@" style="flex-shrink: 0; border: none; background: none; padding: 0; font-size: 14px; font-weight: 600; color: {BLUE_D}; cursor: pointer; font-family: inherit; white-space: nowrap;">이 직무 트렌드 보기 ›</button></div></sc-if></section></sc-if>
{list_card(False)}  </div>
{trend_popup(False, None)}'''

# 직무 분류 (P02 PRD v1.7). 앞 6개는 링커리어 화면 그대로, 뒤 8개는 팀 안
JOB_TAX = {
    '기획/경영': ['경영기획/전략', '사업기획/신규사업', '서비스기획/운영', '인사/채용/노무', '총무/법무/비서', '재무/IR', '경영분석/컨설팅', '사무/문서관리'],
    '마케팅/광고': ['마케팅기획/전략', '브랜드마케팅', '디지털/퍼포먼스마케팅', 'SNS/콘텐츠마케팅', '광고기획/AE', 'PR/홍보', '시장조사/리서치', '전시/컨벤션'],
    'IT/개발': ['프론트엔드개발', '백엔드/서버개발', 'iOS/Android앱개발', '시스템/ERP개발', 'DevOps/클라우드/보안', '데이터분석', 'AI/ML엔지니어', 'IT기획/PM/PO', 'QA/기술지원', '게임개발/기획'],
    '디자인': ['UI/UX디자인', '그래픽/시각디자인', '영상/모션그래픽', '제품/산업디자인', '패션/의류디자인', '공간/인테리어디자인', '편집/출판디자인', '캐릭터/일러스트/3D'],
    '영업/CS': ['B2B영업', '기술영업', '해외영업', '영업관리/기획', '판매/매장관리', '고객상담/CS', '텔레마케팅(TM)'],
    '생산/제조': ['생산/공정관리', '품질관리(QC/QA)', '환경/안전관리', '생산직/조립/가공', '자재/재고관리', '설비/기계유지보수'],
    '연구/R&D': ['기초연구', '응용연구/개발', '전기/전자연구', '기계/소재연구', '화학/화장품연구', '바이오/제약연구'],
    '금융': ['은행', '증권/투자', '보험', '회계/세무', '자산운용', '금융영업'],
    '미디어/콘텐츠': ['PD/연출/방송제작', '영상촬영/편집', '기자/에디터', '작가/시나리오', '아나운서/MC', '콘텐츠기획/MD'],
    '물류/유통': ['물류관리', '구매/조달', 'MD/상품기획', '유통/판매기획', '무역/수출입', '배송/운송'],
    '건설': ['건축설계', '토목/구조', '시공/현장관리', '설비/전기', '부동산/개발'],
    '의료/바이오': ['의사/간호', '약사', '임상/의료연구', '의료기기', '바이오/제약'],
    '교육': ['교육기획/운영', '강사/교사', '교재/콘텐츠개발', '학습관리/상담'],
    '기타': ['공공/행정', '사회복지', '스포츠/레저', '기타'],
}
# 공고를 모은 7개 직무가 어느 상세 직무에 속하는지
JOB_SUB = {'sns': ['마케팅/광고>SNS/콘텐츠마케팅'], 'pm': ['기획/경영>서비스기획/운영', 'IT/개발>IT기획/PM/PO'], 'data': ['IT/개발>데이터분석'],
           'uiux': ['디자인>UI/UX디자인'], 'web': ['IT/개발>프론트엔드개발', 'IT/개발>백엔드/서버개발'], 'ai': ['IT/개발>AI/ML엔지니어'], 'cloud': ['IT/개발>DevOps/클라우드/보안']}
# AI 추천 직무 (시연: 김하늘 이력서로 미리 정한 값)
AI_JOBS = [['마케팅/광고>SNS/콘텐츠마케팅', '인스타그램 운영 1년'], ['마케팅/광고>브랜드마케팅', '카드뉴스 기획'], ['마케팅/광고>PR/홍보', '학생회 홍보부']]
FCHIP_CUR = 'height: 36px; padding: 0 14px; border-radius: 999px; font-size: 14px; font-family: inherit; cursor: pointer; white-space: nowrap; border: 1px solid #3182F6; background: #FFFFFF; color: #1B64DA; font-weight: 600;'

JOBSEL = """    const DESK = false, TAX = __TAX__, JSUB = __JSUB__;
    const fj = this.state.fjob || [];
    const selKeys = (sel) => Object.keys(D).filter((k) => (JSUB[k] || []).length && sel.some((x) => { const c = x.split('>')[0], sub = x.split('>')[1]; return sub === '전체' ? JSUB[k].some((y) => y.split('>')[0] === c) : JSUB[k].indexOf(x) >= 0; }));
    const dKeys = fj.length ? selKeys(fj) : Object.keys(D);
    const job = DESK ? (dKeys[0] || 'sns') : (D[this.state.job] ? this.state.job : 'sns'), J = D[job];
    const POSTS = DESK ? [].concat(...dKeys.map((k) => D[k].posts)) : J.posts;
    const isSns = DESK ? (dKeys.length === 1 && dKeys[0] === 'sns') : job === 'sns';
    const noJobData = DESK && fj.length > 0 && dKeys.length === 0;
    const deskTitle = !fj.length ? '전체 직무' : fj.length === 1 ? (dKeys.length === 1 && JSUB[dKeys[0]].indexOf(fj[0]) >= 0 ? D[dKeys[0]].label : fj[0].split('>')[1]) : fj[0].split('>')[1] + ' 외 ' + (fj.length - 1);"""
JOBPANEL = """    const jt = (key) => () => this.setJobs(fj.indexOf(key) >= 0 ? fj.filter((y) => y !== key) : fj.concat([key]));
    const cats = Object.keys(TAX).map((c) => { const has = fj.some((x) => x.split('>')[0] === c), cur = (s.fcat || '마케팅/광고') === c; return { label: c, cur: cur ? 'true' : 'false', go: () => this.setState({ fcat: c }), style: has ? '__FON__' : cur ? '__FCUR__' : '__FOFF__' }; });
    const fcatName = s.fcat || '마케팅/광고';
    const subs = ['전체'].concat(TAX[fcatName] || []).map((sub) => { const key = fcatName + '>' + sub, on = fj.indexOf(key) >= 0; return { label: sub, on: on ? 'true' : 'false', go: jt(key), style: on ? '__FON__' : '__FOFF__' }; });
    const me = this.illoGet ? this.illoGet('illo-user', null) : null, AIJ = __AIJ__;
    const aiJobs = AIJ.map((a) => ({ label: a[0].split('>')[1], why: a[1], on: fj.indexOf(a[0]) >= 0 ? 'true' : 'false', go: jt(a[0]), style: fj.indexOf(a[0]) >= 0 ? '__FON__' : '__FOFF__' }));"""

LIST_JS = (LIST_JS
    .replace("    const job = D[this.state.job] ? this.state.job : 'sns', J = D[job], POSTS = J.posts, isSns = job === 'sns';", JOBSEL)
    .replace("    const fsel = [];", JOBPANEL + "\n    const fsel = [];\n    if (DESK) fj.forEach((x) => fsel.push({ label: x.replace('>', ' > '), go: () => this.setJobs(fj.filter((y) => y !== x)) }));")
    .replace("    const jobTab = { label: '직무' + (jobOn ? ' ▴' : ' ▾'),", "    const jobTab = { label: '직무' + (fj.length ? ' ' + fj.length : '') + (jobOn ? ' ▴' : ' ▾'),")
    .replace("style: '" + FTAB + "' + (jobOn ? ' border-bottom-color: " + BLUE + "; color: " + BLUE_D + "; font-weight: 700;' : '') };",
             "style: '" + FTAB + "' + (jobOn ? ' border-bottom-color: " + BLUE + ";' : '') + (jobOn || fj.length ? ' color: " + BLUE_D + "; font-weight: 700;' : '') };")
    .replace("fPanel: jobOn || !!og, fPanelTitle: jobOn ? '직무' : og ? og[1] : '',",
             "fPanel: !!og, fPanelTitle: og ? og[1] : '', jobPanel: jobOn && DESK, cats, subs, fcatName, aiJobs, showAi: !!me, aiLogin: !me, aiAll: () => this.setJobs(fj.concat(AIJ.map((a) => a[0]).filter((k) => fj.indexOf(k) < 0))), emptyMsg: noJobData ? '고른 직무의 공고는 아직 모으지 않았어요. 지금은 7개 직무의 공고만 있어요' : '검색 결과가 없어요',")
    .replace("resetF: () => set({ fty: [], fsz: [], fdl: [] }),", "resetF: () => { this.setJobs([]); set({ fty: [], fsz: [], fdl: [] }); },")
    .replace("jobName: J.label,", "jobName: DESK ? deskTitle : J.label,")
    .replace("fo: '', fty: [], fsz: [], fdl: [] }; }",
             "fo: '', fty: [], fsz: [], fdl: [], fcat: '마케팅/광고', fjob: (() => { const JS = __JSUB__; if (jm && JS[jm[1]]) return JS[jm[1]].slice(0, 1); try { const v = JSON.parse(window.localStorage.getItem('illo-job-filter')); if (Array.isArray(v)) return v; } catch (e) {} return ['마케팅/광고>SNS/콘텐츠마케팅']; })() }; }\n"
             "  setJobs(a) { try { window.localStorage.setItem('illo-job-filter', JSON.stringify(a)); } catch (e) {} this.setState({ fjob: a, page: 1 }); }")
    .replace('__FON__', FCHIP_ON).replace('__FOFF__', FCHIP_OFF).replace('__FCUR__', FCHIP_CUR)
    .replace('__TAX__', json.dumps(JOB_TAX, ensure_ascii=False)).replace('__JSUB__', json.dumps(JOB_SUB, ensure_ascii=False)).replace('__AIJ__', json.dumps(AI_JOBS, ensure_ascii=False)))
assert all(t in LIST_JS for t in ('setJobs(a)', 'deskTitle', 'jobPanel', 'emptyMsg')), 'job filter hooks missing'
s1_script = LIST_JS.replace('const DESK = false,', 'const DESK = true,').replace('@@ON@@', seg_style(True)).replace('@@OFF@@', seg_style(False))
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
