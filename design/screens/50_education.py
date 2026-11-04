"""P04 교육과정: SeSAC 과정 210개, 청년 정책 213건, 정책 상세 1건."""

E1_JS = '''  constructor(props) { super(props); const h = (typeof location !== 'undefined' && location.hash) || ''; this.state = { tab: h === '#policy' ? 'pol' : 'edu', q: '', g: 'all', live: false, sort: 'rec', page: 1, pq: '', pc: 'all', pr: 'all', pOpen: true, pp: 1 }; }
  pageVals() {
    const C = __C__, P = __P__, GC = __GC__, SC = __SC__, TH = __TH__, PT = __PTH__, PCOL = __PCOL__;
    const s = this.state, set = (o) => this.setState(o);
    const seg = (on) => on ? '__RON__' : '__ROFF__', box = (on) => on ? '__BON__' : '__BOFF__';
    const tabStyle = (on) => on ? '__TON__' : '__TOFF__', pill = (on) => on ? '__PON__' : '__POFF__', srt = (on) => on ? '__SON__' : '__SOFF__';
    const pg = (on) => on ? '__GON__' : '__GOFF__';
    const badge = (st) => 'padding: 3px 9px; border-radius: 999px; background: ' + (SC[st] || SC['종료'])[0] + '; color: ' + (SC[st] || SC['종료'])[1] + '; font-size: 12px; font-weight: 600; white-space: nowrap;';
    const pager = (page, pages, key) => { const nums = []; const lo = Math.max(1, Math.min(page - 2, pages - 4)), hi = Math.min(pages, lo + 4); for (let i = lo; i <= hi; i++) nums.push({ n: i, style: pg(i === page), cur: i === page ? 'page' : 'false', go: () => set({ [key]: i }) }); return { nums, prev: () => set({ [key]: Math.max(1, page - 1) }), next: () => set({ [key]: Math.min(pages, page + 1) }), prevStyle: pg(false) + (page === 1 ? ' opacity: 0.35;' : ''), nextStyle: pg(false) + (page === pages ? ' opacity: 0.35;' : ''), first: pages > 5 && lo > 1, last: pages > 5 && hi < pages, pages, goFirst: () => set({ [key]: 1 }), goLast: () => set({ [key]: pages }) }; };
    const T = (k) => ({ style: tabStyle(s.tab === k), tab: s.tab === k ? '__TABON__' : '__TABOFF__', cur: s.tab === k ? 'page' : 'false', go: () => set({ tab: k }) });
    // SeSAC courses
    const isLive = (c) => c.st === '모집 중' || c.st === '모집 예정';
    const q = s.q.trim().toLowerCase();
    const base = C.filter((c) => (!s.live || isLive(c)) && (!q || (c.n + ' ' + c.cp + ' ' + c.f + ' ' + c.tags.join(' ')).toLowerCase().indexOf(q) >= 0));
    const groups = ['all', '마케팅', 'AI', '데이터', '기획, PM', '개발', '디자인', '기타'].map((g) => ({ label: (g === 'all' ? '전체' : g) + ' ' + base.filter((c) => g === 'all' || c.g === g).length, name: g === 'all' ? '전체' : g, style: pill(s.g === g), go: () => set({ g, page: 1 }) }));
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
    const pcats = ['all', '취업', '창업', '재직자', '권익보호'].map((c) => ({ label: (c === 'all' ? '전체' : c) + ' ' + pbase.filter((p) => c === 'all' || p.c === c).length, name: c === 'all' ? '전체' : c, style: pill(s.pc === c), go: () => set({ pc: c, pp: 1 }) }));
    const PL = pbase.filter((p) => s.pc === 'all' || p.c === s.pc).slice().sort((a, b) => ({ '신청 중': 0, '상시': 1, '예정': 2, '마감': 3 })[a.st] - ({ '신청 중': 0, '상시': 1, '예정': 2, '마감': 3 })[b.st] || (b.r === '서울') - (a.r === '서울') || b.v - a.v);
    const pper = __PPER__, ppages = Math.max(1, Math.ceil(PL.length / pper)), ppage = Math.min(s.pp, ppages);
    const pols = PL.slice((ppage - 1) * pper, ppage * pper).map((p) => ({ thumb: PT[p.id] || '', hasThumb: !!PT[p.id], noThumb: !PT[p.id], band: 'background: ' + (PCOL[p.c] || PCOL['취업'])[0] + '; color: ' + (PCOL[p.c] || PCOL['취업'])[1] + ';', n: p.n, o: p.o, r: p.r, c: p.c, k: p.k, hasK: p.k.length > 0, d: p.d, st: p.st, stStyle: badge(p.st), per: p.per, u: p.u,
      detail: p.id === 'pol-20261018005400213991', noDetail: p.id !== 'pol-20261018005400213991', dhref: '__DPRE__P2-policy.dc.html',
      sv: this.sv({ id: p.id, kind: '정책', t: p.n, s: p.o + ' · ' + p.st, u: p.u, h: p.id === 'pol-20261018005400213991' ? 'P2-policy.dc.html' : '' }) }));
    const pp = pager(ppage, ppages, 'pp');
    const FOP = s.fo || '', isE = s.tab === 'edu';
    const ftab = (k, label, n, always) => ({ label: label + (n ? ' ' + n : '') + (FOP === k ? ' ▴' : ' ▾'), cur: FOP === k ? 'true' : 'false', go: () => set({ fo: FOP === k ? '' : k }),
      style: '__FTAB__' + (FOP === k ? ' border-bottom-color: #3182F6;' : '') + (always || n || FOP === k ? ' color: #1B64DA; font-weight: 700;' : '') });
    const etabs = [ftab('kind', isE ? 'SeSAC 과정' : '청년 정책', 0, true)].concat(isE
      ? [ftab('g', '분야', s.g !== 'all' ? 1 : 0), ftab('st', '모집 상태', s.live ? 1 : 0)]
      : [ftab('org', '기관', s.pr !== 'all' ? 1 : 0), ftab('pc', '분야', s.pc !== 'all' ? 1 : 0), ftab('ps', '신청 상태', s.pOpen ? 1 : 0)]);
    const ch = (label, on, go) => ({ label, on: on ? 'true' : 'false', go, style: on ? '__FON__' : '__FOFF__' });
    let eopts = [], etitle = '';
    if (FOP === 'kind') { etitle = '종류'; eopts = [ch('SeSAC 과정', isE, () => set({ tab: 'edu', fo: '' })), ch('청년 정책', !isE, () => set({ tab: 'pol', fo: '' }))]; }
    if (FOP === 'g' && isE) { etitle = '분야'; eopts = ['마케팅', 'AI', '데이터', '기획, PM', '개발', '디자인', '기타'].map((g) => ch(g, s.g === g, () => set({ g: s.g === g ? 'all' : g, page: 1 }))); }
    if (FOP === 'st' && isE) { etitle = '모집 상태'; eopts = [ch('모집 중, 예정만', s.live, () => set({ live: !s.live, page: 1 }))]; }
    if (FOP === 'org' && !isE) { etitle = '기관'; eopts = [ch('서울시', s.pr === '서울', () => set({ pr: s.pr === '서울' ? 'all' : '서울', pp: 1 })), ch('중앙부처', s.pr === '중앙부처', () => set({ pr: s.pr === '중앙부처' ? 'all' : '중앙부처', pp: 1 }))]; }
    if (FOP === 'pc' && !isE) { etitle = '분야'; eopts = ['취업', '창업', '재직자', '권익보호'].map((c) => ch(c, s.pc === c, () => set({ pc: s.pc === c ? 'all' : c, pp: 1 }))); }
    if (FOP === 'ps' && !isE) { etitle = '신청 상태'; eopts = [ch('신청 가능만', s.pOpen, () => set({ pOpen: !s.pOpen, pp: 1 }))]; }
    const esel = [];
    if (isE) { if (s.g !== 'all') esel.push({ label: '분야 > ' + s.g, go: () => set({ g: 'all', page: 1 }) }); if (s.live) esel.push({ label: '모집 상태 > 모집 중, 예정만', go: () => set({ live: false, page: 1 }) }); }
    else { if (s.pr !== 'all') esel.push({ label: '기관 > ' + (s.pr === '서울' ? '서울시' : s.pr), go: () => set({ pr: 'all', pp: 1 }) }); if (s.pc !== 'all') esel.push({ label: '분야 > ' + s.pc, go: () => set({ pc: 'all', pp: 1 }) }); if (s.pOpen) esel.push({ label: '신청 상태 > 신청 가능만', go: () => set({ pOpen: false, pp: 1 }) }); }
    const evals = { etabs, eopts, ePanel: eopts.length > 0, etitle, esel, hasE: esel.length > 0, ereset: () => set(isE ? { g: 'all', live: false, page: 1 } : { pr: 'all', pc: 'all', pOpen: false, pp: 1 }),
      eq: isE ? s.q : s.pq, eph: isE ? '과정명, 캠퍼스, 해시태그 검색' : '정책 이름, 기관, 키워드 검색', setEq: (e) => set(isE ? { q: e && e.target ? e.target.value : '', page: 1 } : { pq: e && e.target ? e.target.value : '', pp: 1 }) };
    return { ...evals, tabs: { edu: T('edu'), pol: T('pol') }, isEdu: s.tab === 'edu', isPol: s.tab === 'pol',
      q: s.q, setQ: (e) => set({ q: e && e.target ? e.target.value : '', page: 1 }), groups, live: { style: pill(s.live), go: () => set({ live: !s.live, page: 1 }), label: s.live ? '✓ 모집 중, 예정만' : '모집 중, 예정만' },
      sort: { rec: { style: srt(s.sort === 'rec'), go: () => set({ sort: 'rec', page: 1 }) }, close: { style: srt(s.sort === 'close'), go: () => set({ sort: 'close', page: 1 }) }, rv: { style: srt(s.sort === 'rv'), go: () => set({ sort: 'rv', page: 1 }) } },
      cards, total: L.length, range: L.length ? ((page - 1) * per + 1) + '–' + Math.min(page * per, L.length) : '0', empty: L.length === 0, hasCards: L.length > 0, cp,
      clear: () => set({ q: '', g: 'all', live: false, page: 1 }),
      pq: s.pq, setPq: (e) => set({ pq: e && e.target ? e.target.value : '', pp: 1 }), pcats,
      pseg: { all: { style: seg(s.pr === 'all'), go: () => set({ pr: 'all', pp: 1 }) }, seoul: { style: seg(s.pr === '서울'), go: () => set({ pr: '서울', pp: 1 }) }, gov: { style: seg(s.pr === '중앙부처'), go: () => set({ pr: '중앙부처', pp: 1 }) } }, popenBox: box(s.pOpen), liveBox: box(s.live),
      preg: { all: { style: pill(s.pr === 'all'), go: () => set({ pr: 'all', pp: 1 }) }, seoul: { style: pill(s.pr === '서울'), go: () => set({ pr: '서울', pp: 1 }) }, gov: { style: pill(s.pr === '중앙부처'), go: () => set({ pr: '중앙부처', pp: 1 }) } },
      popen: { style: pill(s.pOpen), go: () => set({ pOpen: !s.pOpen, pp: 1 }), label: s.pOpen ? '✓ 신청 가능만' : '신청 가능만' },
      pols, ptotal: PL.length, prange: PL.length ? ((ppage - 1) * pper + 1) + '–' + Math.min(ppage * pper, PL.length) : '0', pempty: PL.length === 0, hasPols: PL.length > 0, pp,
      pclear: () => set({ pq: '', pc: 'all', pr: 'all', pOpen: true, pp: 1 }) };
  }'''


def e1_js(mobile):
    TAB = 'flex-shrink: 0; height: 44px; padding: 0 18px; border: none; border-radius: 12px; font-size: 15px; cursor: pointer; white-space: nowrap;'
    js = (E1_JS.replace('__C__', COURSE_JSON).replace('__P__', POL_JSON).replace('__GC__', json.dumps(GCOL, ensure_ascii=False)).replace('__SC__', json.dumps(STC, ensure_ascii=False))
          .replace('__TH__', json.dumps(THUMBS)).replace('__PTH__', json.dumps(PTHUMBS)).replace('__PPER__', '10' if mobile else '9').replace('__PCOL__', json.dumps({'취업': (BLUE_BG, BLUE_D), '창업': ('#E6F7F1', '#0E8A63'), '재직자': ('#FFF4E5', '#C26A00'), '권익보호': ('#F0EBFF', '#6B4EE6')})).replace('__PER__', '6' if mobile else '9').replace('__DPRE__', 'm-' if mobile else '')
          .replace('__RON__', seg_style(True)).replace('__ROFF__', seg_style(False)).replace('__BON__', 'display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 5px; font-size: 12px; font-weight: 700; color: #FFFFFF; box-sizing: border-box; background: ' + BLUE + '; border: 1.5px solid ' + BLUE + ';').replace('__BOFF__', 'display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 5px; font-size: 12px; font-weight: 700; color: #FFFFFF; box-sizing: border-box; background: #FFFFFF; border: 1.5px solid #C9CED4;').replace('__FTAB__', FTAB).replace('__FON__', FCHIP_ON).replace('__FOFF__', FCHIP_OFF).replace('__TABON__', TAB_ON).replace('__TABOFF__', TAB_OFF).replace('__TON__', TAB + f' background: {INK}; color: #FFFFFF; font-weight: 700;').replace('__TOFF__', TAB + ' background: #FFFFFF; color: #4E5968;')
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
            f'<button type="button" role="tab" onClick="@@tabs.pol.go@@" style="@@tabs.pol.style@@">청년 정책 {len(POL_ALL)}</button></div>')
    chips = f'<sc-for list="@@groups@@" as="g" hint-placeholder-count="8"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.label@@</button></sc-for>'
    live = '<button type="button" onClick="@@live.go@@" style="@@live.style@@">@@live.label@@</button>'
    sorts = ('<button type="button" onClick="@@sort.rec.go@@" style="@@sort.rec.style@@">추천순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             '<button type="button" onClick="@@sort.close.go@@" style="@@sort.close.style@@">마감 임박순</button><span aria-hidden="true" style="color: #D1D6DB;">·</span>'
             '<button type="button" onClick="@@sort.rv.go@@" style="@@sort.rv.style@@">후기 많은 순</button>')
    img_h = 132 if mobile else 140
    card = course_card(img_h)
    empty = lambda clear, msg: (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 0; {CARD} color: {SUB}; font-size: 15px;">{msg}'
                                f'<button type="button" onClick="@@{clear}@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">조건 지우기</button></div>')
    cols = 1 if mobile else 3
    chk = lambda box, go, txt: (f'<button type="button" onClick="@@{go}@@" style="flex-shrink: 0; display: flex; align-items: center; gap: 8px; border: none; background: none; padding: 0; font-size: 14px; font-weight: 600; color: {INK}; cursor: pointer; font-family: inherit;">'
                                f'<span aria-hidden="true" style="@@{box}@@">✓</span>{txt}</button>')
    if not mobile:  # 데스크톱: 칩에 개수 없음, 토글은 체크박스
        chips = '<sc-for list="@@groups@@" as="g" hint-placeholder-count="8"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.name@@</button></sc-for>'
        live = f'<div style="margin-left: auto;">{chk("liveBox", "live.go", "모집 중, 예정만")}</div>'
    edu_tools = (f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 10px;">{search_box("q", "setQ", "과정명, 캠퍼스, 해시태그", None if mobile else 320)}{live}</div>'
                 f'<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else "flex-wrap: wrap;"}">{chips}</div>') if mobile else ''
    edu = (f'<sc-if value="@@isEdu@@" hint-placeholder-val="@@true@@"><div style="display: flex; flex-direction: column; gap: 14px;">'
           f'{edu_tools}'
           f'<div style="display: flex; justify-content: space-between; align-items: center; {"flex-direction: column; align-items: flex-start; gap: 8px;" if mobile else ""}"><span style="font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@total@@</b>개 중 @@range@@</span><div style="display: flex; gap: 10px; align-items: center;">{sorts}</div></div>'
           f'<sc-if value="@@hasCards@@" hint-placeholder-val="@@true@@"><div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px;"><sc-for list="@@cards@@" as="c" hint-placeholder-count="{6 if mobile else 9}">{card}</sc-for></div>{pager_html("cp", mobile)}</sc-if>'
           f'<sc-if value="@@empty@@" hint-placeholder-val="@@false@@">{empty("clear", "조건에 맞는 과정이 없어요")}</sc-if>'
           f'<span style="font-size: 12px; color: {MUTE};">출처: SeSAC 사이트 전수 조사 (오프라인 197 + 온라인 13개 과정, 2026.10.27 기준). 신청은 SeSAC 사이트에서 해요</span></div></sc-if>')
    pchips = '<sc-for list="@@pcats@@" as="g" hint-placeholder-count="5"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.label@@</button></sc-for>'
    if not mobile:
        pchips = '<sc-for list="@@pcats@@" as="g" hint-placeholder-count="5"><button type="button" onClick="@@g.go@@" style="@@g.style@@">@@g.name@@</button></sc-for>'
    preg = ('<button type="button" onClick="@@preg.all.go@@" style="@@preg.all.style@@">전국, 서울</button><button type="button" onClick="@@preg.seoul.go@@" style="@@preg.seoul.style@@">서울시</button>'
            '<button type="button" onClick="@@preg.gov.go@@" style="@@preg.gov.style@@">중앙부처</button><button type="button" onClick="@@popen.go@@" style="@@popen.style@@">@@popen.label@@</button>')
    if not mobile:
        preg = ('<div role="group" aria-label="기관" style="display: flex; gap: 2px; padding: 4px; border-radius: 12px; background: rgba(0,23,51,0.06);">'
                '<button type="button" onClick="@@pseg.all.go@@" style="@@pseg.all.style@@">전체</button><button type="button" onClick="@@pseg.seoul.go@@" style="@@pseg.seoul.style@@">서울시</button>'
                '<button type="button" onClick="@@pseg.gov.go@@" style="@@pseg.gov.style@@">중앙부처</button></div>'
                f'<div style="margin-left: auto;">{chk("popenBox", "popen.go", "신청 가능만")}</div>')
    prow = (f'<div style="display: flex; {"flex-direction: column;" if mobile else "align-items: center;"} gap: 12px; padding: 18px 0; border-top: 1px solid {LINE};">'
            f'<div style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 6px;"><div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;"><span style="@@p.stStyle@@">@@p.st@@</span><span style="font-size: 12px; color: {SUB};">@@p.r@@ · @@p.c@@</span></div>'
            f'<span style="font-size: 16px; font-weight: 700; line-height: 1.4;">@@p.n@@</span><span style="font-size: 13px; color: {SUB};">@@p.o@@ · @@p.per@@</span>'
            f'<span style="font-size: 13px; line-height: 1.5; color: #4E5968;">@@p.d@@</span>'
            f'<sc-if value="@@p.hasK@@" hint-placeholder-val="@@true@@"><span style="display: flex; gap: 4px; flex-wrap: wrap;"><sc-for list="@@p.k@@" as="k" hint-placeholder-count="2"><span style="padding: 3px 8px; border-radius: 6px; background: {FILL}; font-size: 12px; color: {SUB};">@@k@@</span></sc-for></span></sc-if></div>'
            f'<div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">{save_btn("p.sv", 38)}'
            f'<sc-if value="@@p.detail@@" hint-placeholder-val="@@false@@"><a href="@@p.dhref@@" style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {BLUE}; color: #FFFFFF; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">자세히 보기</a></sc-if>'
            f'<sc-if value="@@p.noDetail@@" hint-placeholder-val="@@true@@"><a href="@@p.u@@" {EXT} style="height: 38px; padding: 0 14px; display: flex; align-items: center; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 13px; font-weight: 600; text-decoration: none; white-space: nowrap;">자세히 ↗</a></sc-if></div></div>')
    pcard = (f'<div style="display: flex; flex-direction: column; gap: 10px; padding: 14px; {CARD} min-width: 0;">'
             f'<sc-if value="@@p.hasThumb@@" hint-placeholder-val="@@false@@"><img src="@@p.thumb@@" alt="" style="width: 100%; height: {img_h}px; object-fit: cover; object-position: center 30%; border-radius: 12px; display: block;"></sc-if>'
             f'<sc-if value="@@p.noThumb@@" hint-placeholder-val="@@true@@"><div style="@@p.band@@ height: {img_h}px; border-radius: 12px; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between;"><span style="font-size: 13px; font-weight: 700;">@@p.c@@</span><span style="font-size: 20px; font-weight: 800; letter-spacing: -0.02em; opacity: 0.85;">@@p.r@@</span></div></sc-if>'
             f'<div style="display: flex; align-items: center; gap: 6px;"><span style="@@p.stStyle@@">@@p.st@@</span><span style="font-size: 12px; color: {SUB};">@@p.r@@ · @@p.c@@</span><span style="margin-left: auto;">{save_btn("p.sv", 32)}</span></div>'
             f'<span style="font-size: 15px; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 42px;">@@p.n@@</span>'
             f'<span style="font-size: 12px; line-height: 1.5; color: {SUB}; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">@@p.o@@<br>@@p.per@@</span>'
             f'<div style="margin-top: auto; display: flex; justify-content: flex-end;">'
             f'<sc-if value="@@p.detail@@" hint-placeholder-val="@@false@@"><a href="@@p.dhref@@" style="font-size: 13px; font-weight: 600; color: {BLUE_D}; text-decoration: none;">자세히 보기 ›</a></sc-if>'
             f'<sc-if value="@@p.noDetail@@" hint-placeholder-val="@@true@@"><a href="@@p.u@@" {EXT} style="font-size: 13px; font-weight: 600; color: {BLUE_D}; text-decoration: none;">온통청년에서 보기 ↗</a></sc-if></div></div>')
    pol_tools = (f'<div style="display: flex; {"flex-direction: column; align-items: stretch;" if mobile else "align-items: center;"} gap: 10px;">{search_box("pq", "setPq", "정책 이름, 기관, 키워드", None if mobile else 320)}<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else "flex: 1 1 0; align-items: center; gap: 10px;"}">{preg}</div></div>'
                 f'<div{sc} style="display: flex; gap: 6px; {"overflow-x: auto; margin: 0 -16px; padding: 0 16px;" if mobile else "flex-wrap: wrap;"}">{pchips}</div>') if mobile else ''
    pol = (f'<sc-if value="@@isPol@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 14px;">'
           f'{pol_tools}'
           + (f'<span style="font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@ptotal@@</b>건 중 @@prange@@ · 신청 가능한 정책 먼저</span>'
            f'<sc-if value="@@hasPols@@" hint-placeholder-val="@@true@@"><div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px;"><sc-for list="@@pols@@" as="p" hint-placeholder-count="9">{pcard}</sc-for></div>{pager_html("pp", mobile)}</sc-if>'
            f'<sc-if value="@@pempty@@" hint-placeholder-val="@@false@@">{empty("pclear", "조건에 맞는 정책이 없어요")}</sc-if>' if not mobile else
            f'<section style="display: flex; flex-direction: column; padding: {"4px 18px 16px" if mobile else "8px 28px 20px"}; {CARD}">'
            f'<span style="padding: 12px 0; font-size: 14px; color: {SUB};"><b style="color: {INK}; font-weight: 700;">@@ptotal@@</b>건 중 @@prange@@ · 신청 가능한 정책 먼저</span>'
            f'<sc-if value="@@hasPols@@" hint-placeholder-val="@@true@@"><sc-for list="@@pols@@" as="p" hint-placeholder-count="10">{prow}</sc-for>{pager_html("pp", mobile)}</sc-if>'
            f'<sc-if value="@@pempty@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 40px 0; color: {SUB}; font-size: 15px;">조건에 맞는 정책이 없어요<button type="button" onClick="@@pclear@@" style="height: 38px; padding: 0 14px; border: none; border-radius: 10px; background: {FILL}; color: {INK}; font-size: 14px; font-weight: 600; cursor: pointer;">조건 지우기</button></div></sc-if></section>')
           + f'<span style="font-size: 12px; color: {MUTE};">출처: 온통청년 청년정책 API (일자리 분야 중 서울시, 중앙부처 {len(POL_ALL)}건, 2026.11.01 조회). 신청 조건은 각 정책 페이지에서 확인해요</span></div></sc-if>')
    head = (f'<div style="display: flex; flex-direction: column; gap: 6px; {"padding: 8px 4px 4px;" if mobile else ""}"><h1 style="margin: 0; font-size: {26 if mobile else 32}px; font-weight: 700; letter-spacing: -0.02em;">교육과정과 취업 지원</h1>'
            f'<span style="font-size: {13 if mobile else 15}px; line-height: 1.5; color: {SUB};">SeSAC 과정 {len(COURSES_ALL)}개와 청년 일자리 정책 {len(POL_ALL)}건을 한곳에서 찾아요. 마음에 들면 저장해 두세요</span></div>')
    if not mobile:
        head = '<h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -0.02em;">교육과정과 청년 정책</h1>'
        search = (f'<label style="width: 300px; display: flex; align-items: center; gap: 8px; height: 46px; padding: 0 14px; border: 1px solid #E5E8EB; border-radius: 12px; background: #FFFFFF; box-sizing: border-box;">'
                  f'<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
                  f'<span style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0);">검색</span>'
                  f'<input type="search" value="@@eq@@" onChange="@@setEq@@" placeholder="@@eph@@" style="flex: 1 1 0; min-width: 0; border: none; background: transparent; font-size: 15px; font-family: inherit; color: {INK}; outline: none;"></label>')
        # 직무 찾기 (20_job_search.py filter_bar)와 같은 필터 줄
        tabs = (f'<div style="display: flex; flex-direction: column; gap: 14px; margin-top: 4px;">'
                f'<div style="display: flex; align-items: center; gap: 36px; padding-left: 8px; border-top: 1px solid #E5E8EB; border-bottom: 1px solid #E5E8EB;">'
                f'<sc-for list="@@etabs@@" as="f" hint-placeholder-count="4"><button type="button" onClick="@@f.go@@" aria-expanded="@@f.cur@@" style="@@f.style@@">@@f.label@@</button></sc-for>'
                f'<div style="margin-left: auto; padding: 8px 0;">{search}</div></div>'
                f'<sc-if value="@@ePanel@@" hint-placeholder-val="@@false@@"><div style="display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; border-radius: 14px; background: #FFFFFF;">'
                f'<span style="font-size: 13px; color: {SUB};">@@etitle@@</span><div style="display: flex; gap: 8px; flex-wrap: wrap;">'
                f'<sc-for list="@@eopts@@" as="o" hint-placeholder-count="4"><button type="button" onClick="@@o.go@@" aria-pressed="@@o.on@@" style="@@o.style@@">@@o.label@@</button></sc-for></div></div></sc-if>'
                f'<sc-if value="@@hasE@@" hint-placeholder-val="@@false@@"><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">'
                f'<sc-for list="@@esel@@" as="x" hint-placeholder-count="1"><button type="button" onClick="@@x.go@@" aria-label="@@x.label@@ 빼기" style="display: flex; align-items: center; gap: 6px; height: 34px; padding: 0 12px; border: none; border-radius: 999px; background: {BLUE_BG}; color: {INK}; font-size: 13px; font-family: inherit; cursor: pointer;">@@x.label@@<span aria-hidden="true" style="font-size: 15px; color: #4E5968;">×</span></button></sc-for>'
                f'<button type="button" onClick="@@ereset@@" style="border: none; background: none; padding: 0 6px; font-size: 13px; font-weight: 600; color: #4E5968; cursor: pointer; font-family: inherit;">↺ 초기화</button></div></sc-if></div>')
    body = f'{head}{tabs}{edu}{pol}'
    if mobile:
        return '    ' + body.replace('href="S4-', 'href="m-S4-') + '\n'
    return f'  <div style="display: flex; flex-direction: column; gap: 20px; padding: 28px 56px 56px;">{body}</div>\n'


boards['E1-edu.dc.html'] = ('E1 교육과정 (SeSAC 210, 청년 정책)', dpage('E1-edu.dc.html', '교육과정', 'edu', e1_v5(False), e1_js(False)))
boards['m-E1-edu.dc.html'] = ('ME1 교육과정 (모바일)', mpage('m-E1-edu.dc.html', 'ME1 교육과정 (모바일)', topbar_logo(auth_mobile()), e1_v5(True), 'edu', e1_js(True)))

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
