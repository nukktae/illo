/* 일로 prototype v2 — one-page app. Data: design/data (공고 46, SeSAC 210, 청년 정책 515). Everything is stored in this browser only. */
(() => {
'use strict';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const REDUCE = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const wait = (ms) => new Promise((r) => setTimeout(r, REDUCE ? 0 : ms));
const store = {
  get(k, d) { try { const v = localStorage.getItem('illo2-' + k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('illo2-' + k, JSON.stringify(v)); } catch (e) {} },
};
const view = $('#view');
let DATA = { posts: [], courses: [], policies: [] };
let runToken = 0; // cancels an agent run when the user leaves the chat

/* ---------- assets ---------- */
const TH = { 'edu-1465': 'sesac-1465.jpg', 'edu-1233': 'sesac-gc8.jpg', 'edu-1202': 'sesac-sd6.jpg', 'edu-1419': 'sesac-gj8.jpg', 'edu-1182': 'sesac-ydp2.jpg', 'edu-1195': 'sesac-sb5.jpg', 'edu-715': 'sesac-ga2.jpg', 'edu-835': 'sesac-sb4.jpg', 'edu-1421': 'sesac-1421.png' };
const PTH = { 'pol-20261018005400213993': 'pol-wing.jpg', 'pol-20261018005400213991': 'pol-jobcamp.jpg', 'pol-20261018005400213990': 'pol-sesac.jpg', 'pol-20261018005400213983': 'pol-yc-camp.jpg', 'pol-20261018005400213984': 'pol-yc-challenge.jpg', 'pol-20260317005400112169': 'pol-heritage.jpg' };
const LOGOS = [['올리브인터내셔널', null, 'logo-olive.png'], ['카카오', null, 'logo-kakao.png'], ['클래스101', null, 'logo-class101.png'], ['트립비토즈', null, 'logo-tripbtoz.png'], ['뷰에누보', null, 'logo-vueno.png'], ['앳홈', null, 'logo-athome.png'], ['기업명 비공개', '뷰티 콘텐츠 마케터(전환형', 'logo-anon-flower.png'], ['기업명 비공개', '뷰티 색동서울', 'logo-anon-leaf.png'], ['퍼포즈드', null, 'logo-performed.png'], ['패스트뷰', null, 'logo-fastview.png']];
const logoFor = (company, title = '') => { const m = LOGOS.find(([c, t]) => c === company && (!t || title.includes(t))); return m ? m[2] : null; };
const MONO = [['#E8F1FF', '#1B64DA'], ['#EAF7EF', '#16794A'], ['#FFF1E5', '#B4570B'], ['#F3EEFF', '#6B4EE6'], ['#FDEDF3', '#B4245D'], ['#E9F7F8', '#0F7C86'], ['#FFF7DB', '#946200'], ['#EEF0F3', '#3D4A5C']];
const monoLetters = (name) => { const n = name.replace(/\(.*?\)|㈜|\(주\)|주식회사|\s/g, ''); const en = n.match(/^[A-Za-z]+/); return en ? en[0].slice(0, 2).toUpperCase() : n.slice(0, 1); };
function companyLogo(company, title = '', size = 34, radius = '50%') {
  const lg = logoFor(company, title);
  if (lg) return `<img class="logo" src="assets/${lg}" alt="" style="width:${size}px;height:${size}px;border-radius:${radius}">`;
  const [bg, fg] = MONO[hashStr(company) % MONO.length];
  return `<span class="logo mono" aria-hidden="true" style="width:${size}px;height:${size}px;border-radius:${radius};background:${bg};color:${fg};border-color:transparent;font-size:${Math.round(size * 0.4)}px">${esc(monoLetters(company))}</span>`;
}
const LOGO = new Proxy({}, { get: (_, k) => logoFor(String(k)) });
const I = {
  compare: '<rect x="3" y="4" width="7" height="16" rx="2"/><rect x="14" y="4" width="7" height="16" rx="2"/>',
  translate: '<path d="M4 7h11M4 12h7M4 17h9"/><path d="M17 14l3 3-3 3"/>',
  edu: '<path d="M2.5 9.5 12 5l9.5 4.5L12 14z"/><path d="M6.5 11.8V16c0 1.2 2.5 3 5.5 3s5.5-1.8 5.5-3v-4.2"/>',
  policy: '<path d="M12 3l8 4v5c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V7z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  save: '<path d="M6.5 3.5h11a1 1 0 0 1 1 1V20.5l-6.5-4-6.5 4V4.5a1 1 0 0 1 1-1z"/>',
  mic: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
  clip: '<path d="M20 11.5 12 19.5a5 5 0 0 1-7-7l8.5-8.5a3.3 3.3 0 0 1 4.7 4.7L9.7 17.2a1.7 1.7 0 0 1-2.4-2.4L15 7"/>',
  link: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
  send: '<path d="M12 19V5M6 11l6-6 6 6"/>',
  stop: '<rect x="7" y="7" width="10" height="10" rx="1.5"/>',
  x: '<path d="M6 6l12 12M18 6 6 18"/>',
  chev: '<path d="m9 6 6 6-6 6"/>',
  ext: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  search: '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/>',
};
/* glass icons: a colored back shape + a frosted front layer (sizes in %, so one recipe scales) */
const GLASS = {
  chat: '<i class="g-b" style="left:4%;top:8%;width:62%;height:52%;border-radius:22% 22% 22% 6%;background:linear-gradient(135deg,#D8B4FE,#8B5CF6)"></i><i class="g-f" style="left:28%;top:32%;width:66%;height:54%;border-radius:22% 22% 6% 22%"><b class="g-dots"><s></s><s></s><s></s></b></i>',
  docs: '<i class="g-b" style="left:36%;top:4%;width:56%;height:68%;border-radius:16%;background:linear-gradient(135deg,#93C5FD,#3B82F6)"></i><i class="g-f" style="left:10%;top:24%;width:56%;height:68%;border-radius:16%"><b class="g-lines"><s></s><s></s><s style="width:55%"></s></b></i>',
  plus: '<i class="g-b" style="left:34%;top:6%;width:58%;height:58%;border-radius:20%;background:linear-gradient(135deg,#FDBA74,#F97316)"></i><i class="g-f" style="left:10%;top:30%;width:60%;height:60%;border-radius:20%"><b class="g-plus"></b></i>',
  shield: '<svg class="g-svg" viewBox="0 0 38 44" style="left:16%;top:4%;width:68%;height:80%"><defs><linearGradient id="gsh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#86EFAC"/><stop offset="1" stop-color="#16A34A"/></linearGradient></defs><path d="M19 1 36 7v13c0 11-7.5 19.5-17 23C9.5 39.5 2 31 2 20V7z" fill="url(#gsh)"/></svg><i class="g-f" style="left:6%;top:44%;width:46%;height:46%;border-radius:50%"><b class="g-check"></b></i>',
  mail: '<i class="g-b" style="left:26%;top:4%;width:50%;height:56%;border-radius:12%;background:linear-gradient(135deg,#F9A8D4,#E11D74)"><b class="g-lines w"><s></s><s></s></b></i><i class="g-f" style="left:10%;top:40%;width:80%;height:50%;border-radius:12%"></i>',
  cal: '<i class="g-b" style="left:14%;top:8%;width:72%;height:30%;border-radius:18% 18% 0 0;background:linear-gradient(135deg,#FB923C,#EF4444)"></i><i class="g-f solid" style="left:14%;top:30%;width:72%;height:60%;border-radius:0 0 18% 18%"><b class="g-num">14</b></i>',
  folder: '<i class="g-b" style="left:8%;top:14%;width:50%;height:30%;border-radius:18% 18% 0 0;background:linear-gradient(135deg,#60A5FA,#2563EB)"></i><i class="g-b" style="left:8%;top:24%;width:84%;height:56%;border-radius:12%;background:linear-gradient(135deg,#60A5FA,#2563EB)"></i><i class="g-f" style="left:8%;top:38%;width:84%;height:52%;border-radius:12%"></i>',
  search: '<i class="g-f" style="left:4%;top:40%;width:62%;height:30%;border-radius:20%"><b class="g-dots dk"><s></s><s></s><s></s></b></i><i class="g-ring" style="left:44%;top:14%;width:40%;height:40%"></i><i class="g-handle"></i>',
};
const glass = (k, size = 40) => `<span class="gi" style="width:${size}px;height:${size}px" aria-hidden="true">${GLASS[k]}</span>`;
const ic = (k, extra = '') => `<svg viewBox="0 0 24 24" aria-hidden="true" ${extra}>${I[k]}</svg>`;
const ORB = (size = 72) => `<svg class="orb" width="${size}" height="${size}" viewBox="0 0 96 96" aria-hidden="true" style="fill:initial;stroke:none">${[[40,8,2.4,'#98C2FC'],[56,8,2.4,'#A7CBFD'],[24,24,5,'#7AB0FA'],[40,24,5,'#89B9FB'],[56,24,5,'#98C2FC'],[72,24,5,'#A7CBFD'],[8,40,2.4,'#5D9DF9'],[24,40,5,'#6CA6FA'],[40,40,7.2,'#7AB0FA'],[56,40,7.2,'#89B9FB'],[72,40,5,'#98C2FC'],[88,40,2.4,'#A7CBFD'],[8,56,2.4,'#4E94F8'],[24,56,5,'#5D9DF9'],[40,56,7.2,'#6CA6FA'],[56,56,7.2,'#7AB0FA'],[72,56,5,'#89B9FB'],[88,56,2.4,'#98C2FC'],[24,72,5,'#4E94F8'],[40,72,5,'#5D9DF9'],[56,72,5,'#6CA6FA'],[72,72,5,'#7AB0FA'],[40,88,2.4,'#4E94F8'],[56,88,2.4,'#5D9DF9']].map(([x,y,r,c]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`).join('')}</svg>`;
const AGENTS = {
  compare: { name: '공고 비교 에이전트', color: '#3182F6', icon: 'compare', g: 'docs' },
  course: { name: '과정 찾기 에이전트', color: '#E8A33D', icon: 'edu', g: 'plus' },
  policy: { name: '정책 확인 에이전트', color: '#22A05B', icon: 'policy', g: 'shield' },
  translate: { name: '경험 번역 에이전트', color: '#8B5CF6', icon: 'translate', g: 'chat' },
};
const VERD = { ok: ['ok', '맞음'], part: ['part', '일부'], no: ['no', '없음'] };
const verd = (v) => `<span class="verd${v === 'no' ? ' t-no' : ''}"><span class="dot ${VERD[v][0]}"></span>${VERD[v][1]}</span>`;

/* ---------- time ---------- */
const now = () => new Date();
const ymd = (d) => d.toISOString().slice(0, 10);
const dateKo = (d = now()) => `${d.getMonth() + 1}월 ${d.getDate()}일 ${'일월화수목금토'[d.getDay()]}요일`;
const timeKo = (d = now()) => { const h = d.getHours(); return `${h < 12 ? '오전' : '오후'} ${((h + 11) % 12) + 1}:${String(d.getMinutes()).padStart(2, '0')}`; };
const greet = () => { const h = now().getHours(); return h < 11 ? '좋은 아침이에요' : h < 18 ? '좋은 오후예요' : '좋은 저녁이에요'; };
const dday = (iso) => Math.ceil((new Date(iso + 'T23:59:59') - now()) / 864e5);

const authed = () => store.get('user', true);
/* ---------- toast ---------- */
function toast(msg, action) {
  const root = $('#toast-root');
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = `<span>${esc(msg)}</span>${action ? `<button type="button">${esc(action.label)}</button>` : ''}`;
  root.appendChild(t);
  if (action) t.querySelector('button').onclick = () => { action.run(); close(); };
  const close = () => { t.classList.add('out'); setTimeout(() => t.remove(), 220); };
  setTimeout(close, action ? 4200 : 2600);
}

/* ---------- saved ---------- */
const saved = () => store.get('saved', null) ?? seedSaved();
function seedSaved() {
  const s = {
    'post-kakao': { kind: '공고', t: '카카오 브랜드마케팅 인턴', s: '비교 완료 · 맞음 5 · 일부 3 · 없음 1', img: 'logo-kakao.png', href: '#/jobs' },
    'edu-1465': { kind: '교육', t: '실무 경험으로 완성하는 AI 콘텐츠 디자인 과정', s: 'SeSAC 양천 · 숏폼 빈칸 채움', img: 'sesac-1465.jpg', href: '#/edu' },
    'pol-20261018005400213991': { kind: '정책', t: '2026 서울형 청년인턴 직무캠프', s: '서울특별시 · 신청 중', img: 'pol-jobcamp.jpg', href: '#/edu/policy' },
  };
  store.set('saved', s); return s;
}
function toggleSave(id, item, btn) {
  const s = saved();
  if (s[id]) {
    const prev = s[id]; delete s[id]; store.set('saved', s);
    toast('저장함에서 뺐어요', { label: '되돌리기', run: () => { const x = saved(); x[id] = prev; store.set('saved', x); syncSaveBtns(); updateSavedCount(); } });
  } else {
    s[id] = item; store.set('saved', s);
    toast('저장함에 담았어요', { label: '보기', run: () => go('#/saved') });
  }
  if (btn) { btn.classList.remove('bump'); void btn.offsetWidth; btn.classList.add('bump'); }
  syncSaveBtns(); updateSavedCount(); renderSide();
}
function syncSaveBtns() { const s = saved(); $$('[data-save]').forEach((b) => b.setAttribute('aria-pressed', s[b.dataset.save] ? 'true' : 'false')); }
function updateSavedCount() { $('#saved-count').textContent = Object.keys(saved()).length || ''; }
const saveBtn = (id) => `<button type="button" class="save" data-save="${esc(id)}" aria-label="저장" aria-pressed="false">${ic('save')}</button>`;

/* ---------- memory ---------- */
const memEvents = () => store.get('mem-events', null) ?? [
  { d: '11/4', t: '"숏폼 성과 분석"이 카카오 공고에서 빈칸으로 나왔어요' },
  { d: '11/4', t: '구직 기간 생활비 지원에 관심이 있어요' },
  { d: '11/3', t: '카페 알바 2년을 고객 응대 역량으로 연결했어요' },
];
function remember(text) {
  const ev = memEvents(); const d = now();
  ev.unshift({ d: `${d.getMonth() + 1}/${d.getDate()}`, t: text }); store.set('mem-events', ev.slice(0, 12));
}

/* ---------- chats ---------- */
const chats = () => store.get('chats', null) ?? [
  { id: 'c-seed1', title: '숏폼 빈칸 채우는 법', q: '숏폼 성과 분석 빈칸, 2주 안에 채우는 방법 알려 줘', sc: 'gap', done: true, follow: [] },
  { id: 'c-seed2', title: '구직 기간 생활비 지원', q: '구직 기간에 받을 수 있는 서울 청년 정책은?', sc: 'policy', done: true, follow: [] },
];
const saveChats = (c) => store.set('chats', c.slice(0, 12));
function detect(q) {
  if (/정책|생활비|지원금|수당|월세|주거|자격/.test(q)) return 'policy';
  if (/경험|알바|동아리|문장|번역|경력이 될/.test(q)) return 'translate';
  if (/빈칸|숏폼|채우|과정|교육|배우/.test(q)) return 'gap';
  return 'compare';
}
function titleFor(q, sc) {
  const p = findPost(q);
  if (sc === 'compare') return p ? `${p.company} 공고와 비교` : '카카오 마케팅 공고와 비교';
  return q.length > 22 ? q.slice(0, 22) + '…' : q;
}
function findPost(q) { return DATA.posts.find((p) => q.includes(p.company)); }
function startChat(q) {
  const sc = detect(q); const id = 'c-' + Date.now().toString(36);
  const c = chats(); c.unshift({ id, title: titleFor(q, sc), q, sc, done: false, follow: [] }); saveChats(c);
  sessionStorage.setItem('illo2-run', id);
  go('#/chat/' + id);
}
let lastActive = null;
const folders = () => store.get('folders', []);
function renderRecent(active) {
  lastActive = active === undefined ? lastActive : active;
  const ul = $('#recent'); if (!authed()) { ul.innerHTML = '<li class="sub" style="padding:6px 10px;font-size:12px;line-height:1.5">로그인하면 대화가 여기 저장돼요</li>'; return; } const fresh = sessionStorage.getItem('illo2-run'); const all = chats(); const F = folders(); const open = store.get('folder-open', {});
  const li = (c) => `<li class="${c.id === fresh ? 'new' : ''}" data-chat="${c.id}"><a href="#/chat/${c.id}"${c.id === lastActive ? ' aria-current="page"' : ''}>${esc(c.title)}</a><button type="button" class="more" data-more="${c.id}" aria-label="${esc(c.title)} 메뉴">⋯</button></li>`;
  ul.innerHTML = F.map((f) => { const inF = all.filter((c) => c.folder === f); const o = open[f] !== false;
    return `<li class="folder"><button type="button" class="fold" data-fold="${esc(f)}" aria-expanded="${o}">${ic('chev')}<span>${esc(f)}</span><span class="count">${inF.length}</span></button>${o ? `<ul class="recent-list sub-list">${inF.map(li).join('') || '<li class="sub" style="padding:6px 10px 6px 30px;font-size:12px">비어 있어요</li>'}</ul>` : ''}</li>`; }).join('')
    + all.filter((c) => !c.folder || !F.includes(c.folder)).slice(0, 8).map(li).join('');
}
function closeMenu() { const m = $('#ctx-menu'); if (m) m.remove(); }
function chatMenu(btn, id) {
  closeMenu(); const c = chats().find((x) => x.id === id); if (!c) return;
  const r = btn.getBoundingClientRect(); const m = document.createElement('div'); m.id = 'ctx-menu'; m.className = 'menu'; m.setAttribute('role', 'menu');
  m.style.left = Math.min(r.left, innerWidth - 230) + 'px'; m.style.top = (r.bottom + 4) + 'px';
  const F = folders();
  m.innerHTML = `<button type="button" role="menuitem" data-m="rename"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13.5 6.5 4 4"/></svg><span>이름 바꾸기</span><kbd>더블클릭</kbd></button><div class="menu-sep"></div><span class="menu-lab">폴더로 이동</span>${F.map((f) => `<button type="button" role="menuitem" data-m="to" data-f="${esc(f)}" class="${c.folder === f ? 'cur' : ''}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/></svg><span>${esc(f)}</span>${c.folder === f ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>' : ''}</button>`).join('')}${c.folder ? '<button type="button" role="menuitem" data-m="out"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/><path d="M9 13.5h6"/></svg><span>폴더에서 빼기</span></button>' : ''}<button type="button" role="menuitem" data-m="newf" class="muted"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg><span>새 폴더 만들기</span></button><form data-newf class="menu-new" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/></svg><input placeholder="폴더 이름" aria-label="새 폴더 이름" maxlength="20"><button type="submit" aria-label="만들기"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></button></form><div class="menu-sep"></div><button type="button" role="menuitem" data-m="del" class="danger"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 7h14M10 7V5h4v2M7 7l1 12h8l1-12"/></svg><span>삭제</span></button>`;
  document.body.appendChild(m); $('button', m).focus();
  const upd = (fn) => { const all = chats(); const k = all.findIndex((x) => x.id === id); if (k >= 0) { fn(all[k], all, k); saveChats(all); } renderRecent(); };
  m.onclick = (e) => {
    const b = e.target.closest('[data-m]'); if (!b) return; const k = b.dataset.m;
    if (k === 'newf') { b.hidden = true; const f = $('[data-newf]', m); f.hidden = false; $('input', f).focus(); return; }
    closeMenu();
    if (k === 'rename') return renameChat(id);
    if (k === 'to') { upd((x) => { x.folder = b.dataset.f; }); toast(`"${b.dataset.f}" 폴더에 넣었어요`); }
    if (k === 'out') { upd((x) => { delete x.folder; }); toast('폴더에서 뺐어요'); }
    if (k === 'del') { const all = chats(); const k2 = all.findIndex((x) => x.id === id); const gone = all.splice(k2, 1)[0]; saveChats(all); renderRecent(); if (lastActive === id) go('#/');
      toast('대화를 삭제했어요', { label: '되돌리기', run: () => { const a2 = chats(); a2.splice(k2, 0, gone); saveChats(a2); renderRecent(); } }); }
  };
  $('[data-newf]', m).onsubmit = (e) => { e.preventDefault(); const v = $('input', m).value.trim(); if (!v) return; const F2 = folders(); if (!F2.includes(v)) { F2.push(v); store.set('folders', F2); } closeMenu(); upd((x) => { x.folder = v; }); toast(`"${v}" 폴더를 만들고 넣었어요`); };
  setTimeout(() => document.addEventListener('click', outside, { once: true }), 0);
  function outside(e) { if (!e.target.closest('#ctx-menu')) closeMenu(); else document.addEventListener('click', outside, { once: true }); }
}
function renameChat(id) {
  const li = $(`[data-chat="${id}"]`); if (!li) return; const a = $('a', li); const c = chats().find((x) => x.id === id);
  const inp = document.createElement('input'); inp.className = 'rename'; inp.value = c.title; inp.maxLength = 40; inp.setAttribute('aria-label', '대화 이름');
  a.replaceWith(inp); inp.focus(); inp.select();
  let done = false; const fin = (save) => { if (done) return; done = true; if (save && inp.value.trim()) { const all = chats(); const k = all.findIndex((x) => x.id === id); all[k].title = inp.value.trim(); saveChats(all); const h = $('.talk-h h1'); if (h && lastActive === id) h.textContent = all[k].title; toast('이름을 바꿨어요'); } renderRecent(); };
  inp.onkeydown = (e) => { if (e.key === 'Enter') fin(true); if (e.key === 'Escape') fin(false); };
  inp.onblur = () => fin(true);
}
document.addEventListener('click', (e) => {
  const mb = e.target.closest('[data-more]'); if (mb) { e.preventDefault(); e.stopPropagation(); chatMenu(mb, mb.dataset.more); return; }
  const fb = e.target.closest('[data-fold]'); if (fb) { const o = store.get('folder-open', {}); o[fb.dataset.fold] = fb.getAttribute('aria-expanded') !== 'true'; store.set('folder-open', o); renderRecent(); }
});
document.addEventListener('dblclick', (e) => { const a = e.target.closest('#recent li[data-chat] a'); if (a) { e.preventDefault(); renameChat(a.parentElement.dataset.chat); } });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

/* ---------- router ---------- */
function go(h) { if (location.hash === h) route(); else location.hash = h; }
function parse() {
  const raw = location.hash.replace(/^#\/?/, ''); const [path, qs] = raw.split('?');
  return { parts: path.split('/').filter(Boolean), q: new URLSearchParams(qs || '') };
}
function setNav(key) { $$('[data-nav]').forEach((a) => a.toggleAttribute('aria-current', a.dataset.nav === key) || (a.dataset.nav === key && a.setAttribute('aria-current', 'page'))); }
function mount(html, cls = '') {
  closeDrawer(true);
  view.innerHTML = '<div class="pane">' + html + '</div>'; view.className = 'view ' + cls; void view.offsetWidth; view.classList.add('enter');
  window.scrollTo(0, 0); syncSaveBtns();
}
function route() {
  runToken++;
  const { parts, q } = parse();
  const [a, b] = parts;
  let navKey = 'home', active = null;
  document.body.classList.toggle('on-home', !a);
  document.body.classList.toggle('on-chat', a === 'chat');
  document.body.classList.toggle('on-trend', a === 'trend');
  document.body.classList.toggle('on-me', a === 'me');
  const mm = $('.mtop-me'); if (mm) { mm.hidden = !authed(); }
  if (a !== 'login' && a !== 'signup') document.body.classList.remove('auth-on');
  if (a === 'login') { renderLogin(); return; }
  if (a === 'signup') { renderSignup(); return; }
  if (!a) renderHome();
  else if (a === 'chat' && b) { navKey = ''; active = b; renderChat(b); }
  else if (a === 'jobs') { navKey = 'jobs'; renderJobs(q); }
  else if (a === 'edu') { navKey = 'edu'; renderEdu(b === 'policy' ? 'pol' : 'edu', q); }
  else if (a === 'saved') { navKey = 'saved'; renderSaved(); }
  else if (a === 'me' && !authed()) { navKey = 'me'; mount(`<div class="page"><div class="empty card" style="margin-top:40px">마이페이지는 로그인한 뒤 볼 수 있어요<button type="button" class="btn btn-dark" data-act="login">로그인</button></div></div>`); }
  else if (a === 'me') { navKey = 'me'; renderMe(b || 'profile'); }
  else if (a === 'trend') { navKey = 'trend'; renderTrend(); }
  else if (a === 'tasks') { navKey = 'saved'; renderTasks(); }
  else if (a === 'apply') { navKey = 'apply'; if (b) renderApply(b); else renderApplyList(); }
  else renderHome();
  $$('[data-nav]').forEach((el) => { if (el.dataset.nav === navKey) el.setAttribute('aria-current', 'page'); else el.removeAttribute('aria-current'); });
  renderRecent(active || null); updateSavedCount(); updateAppCount(); renderSide(); renderMe2();
}
function renderMe2() {
  const slot = $('#me-slot'); if (!slot) return;
  slot.innerHTML = authed()
    ? `<button type="button" class="me" data-act="me-menu" aria-haspopup="menu"${location.hash.startsWith('#/me') ? ' aria-current="page"' : ''}><img src="assets/avatar-haneul.jpg" alt=""><span><strong>김하늘</strong><span>시연용 계정</span></span><span class="sub" style="margin-left:auto">⋯</span></button>
      <div class="me-mob"><button type="button" class="me-tg" data-act="me-toggle" aria-expanded="false"><span>김하늘</span><span class="sub">프로필</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
        <div class="me-exp" hidden><div class="me-card"><img src="assets/avatar-haneul.jpg" alt=""><span><strong>김하늘</strong><span class="sub">시연용 계정 · SNS 콘텐츠 마케터</span></span></div>
        <div class="me-links"><a href="#/me">마이페이지</a><a href="#/me/resume">기본 이력서</a><a href="#/me/memory">나의 기억</a><a href="#/apply">지원서</a><button type="button" data-act="logout">로그아웃</button></div></div></div>`
    : `<div class="login-box"><span class="sub" style="line-height:1.5">로그인하면 이력서로 비교하고, 대화와 기억이 저장돼요</span><a class="btn btn-dark" href="#/login" style="width:100%">로그인</a><a class="btn btn-line" href="#/signup" style="width:100%">회원가입</a></div>`;
}
function meMenu(btn) {
  closeMenu(); const r = btn.getBoundingClientRect(); const m = document.createElement('div'); m.id = 'ctx-menu'; m.className = 'menu'; m.setAttribute('role', 'menu');
  m.style.left = r.left + 'px'; m.style.top = Math.max(8, r.top - 176) + 'px';
  if (r.top < 200) { m.style.top = (r.bottom + 8) + 'px'; m.style.left = 'auto'; m.style.right = Math.max(8, innerWidth - r.right) + 'px'; }
  m.innerHTML = `<button type="button" role="menuitem" data-m="me">마이페이지</button><button type="button" role="menuitem" data-m="resume">기본 이력서</button><button type="button" role="menuitem" data-m="apply">지원서</button><div class="menu-sep"></div><button type="button" role="menuitem" data-m="out" class="danger">로그아웃</button>`;
  document.body.appendChild(m); $('button', m).focus();
  m.onclick = (e) => { const b = e.target.closest('[data-m]'); if (!b) return; closeMenu(); const k = b.dataset.m;
    if (k === 'me') go('#/me'); if (k === 'resume') go('#/me/resume'); if (k === 'apply') go('#/apply');
    if (k === 'out') { store.set('user', false); toast('로그아웃했어요 · 이 기기에 저장된 내용은 남아 있어요'); go('#/'); } };
  setTimeout(() => document.addEventListener('click', function out(e) { if (!e.target.closest('#ctx-menu')) closeMenu(); else document.addEventListener('click', out, { once: true }); }, { once: true }), 0);
}
/* ---------- auth: full-screen login / signup ---------- */
function authShell(inner) {
  return `<div class="auth">
    <aside class="auth-brand">
      <a href="#/" class="brand"><img src="assets/illo_logo.png" alt="일로 홈"></a>
      <div class="auth-hero"><h1>해 본 일을 말하면,<br>맞는 공고와 정책을 찾아 드려요</h1><p>실제 공고 문장과 내 경험을 하나씩 맞춰 보고, 빈칸은 SeSAC 과정과 서울 청년 정책으로 이어 드려요.</p></div>
      <div class="auth-demo card">
        <div class="ad-h">${companyLogo('패스트뷰', '', 28, '8px')}<span><b>자동차 콘텐츠 에디터</b><span class="sub">패스트뷰 · 신입</span></span><span class="st" style="font-size:12px"><span class="dot ok"></span>비교 완료</span></div>
        <div class="jl v-ok"><span class="jt">SNS 채널 운영 경험</span>${verd('ok')}</div>
        <div class="jl v-part"><span class="jt">콘텐츠 성과 분석 및 리포트</span>${verd('part')}</div>
        <div class="jl v-no"><span class="jt">숏폼 콘텐츠 성과 분석</span>${verd('no')}</div>
      </div>
      <ul class="auth-points">
        <li>${glass('docs', 36)}<span><b>공고 문장 단위 비교</b><small>맞음, 일부, 없음과 근거 문장만 · 합격은 예측하지 않아요</small></span></li>
        <li>${glass('plus', 36)}<span><b>빈칸은 과정으로</b><small>SeSAC 과정 ${DATA.courses.length || 210}개에서 바로 찾아요</small></span></li>
        <li>${glass('shield', 36)}<span><b>청년 정책까지</b><small>서울시, 중앙부처 정책 ${DATA.policies.length || 515}건 · 온통청년</small></span></li>
      </ul>
    </aside>
    <main class="auth-main"><div class="auth-card">${inner}</div><p class="auth-foot sub">시연 버전이에요 · 입력한 정보는 이 기기 브라우저에만 저장돼요</p></main></div>`;
}
const SOCIAL = `<div class="or"><span>또는</span></div>
  <button type="button" class="btn sso kakao" data-sso>카카오로 계속하기</button>
  <button type="button" class="btn sso naver" data-sso><b>N</b>네이버로 계속하기</button>
  <button type="button" class="btn sso google" data-sso><svg viewBox="0 0 24 24" aria-hidden="true" style="fill:initial;stroke:none;width:16px;height:16px"><path fill="#4285F4" d="M22 12.2c0-.7-.1-1.4-.2-2H12v3.9h5.6a4.8 4.8 0 0 1-2.1 3.1v2.6h3.4c2-1.8 3.1-4.5 3.1-7.6z"/><path fill="#34A853" d="M12 22c2.8 0 5.2-.9 6.9-2.5l-3.4-2.6c-.9.6-2.1 1-3.5 1-2.7 0-5-1.8-5.8-4.3H2.7v2.7A10 10 0 0 0 12 22z"/><path fill="#FBBC05" d="M6.2 13.6a6 6 0 0 1 0-3.8V7.1H2.7a10 10 0 0 0 0 9z"/><path fill="#EA4335" d="M12 6c1.5 0 2.9.5 4 1.5l3-3A10 10 0 0 0 2.7 7.1l3.5 2.7C7 7.8 9.3 6 12 6z"/></svg>Google로 계속하기</button>`;
function finishAuth(msg) { store.set('user', true); document.body.classList.remove('auth-on'); toast(msg); go('#/'); }
function renderLogin() {
  document.body.classList.add('auth-on');
  view.className = 'view'; view.innerHTML = authShell(`<div class="head-l"><h2>다시 만나서 반가워요</h2><span class="sub">이메일로 로그인하세요</span></div>
    <form class="auth-form" data-login novalidate>
      <label class="field"><span>이메일</span><input type="email" name="em" autocomplete="email" placeholder="비워 두고 로그인해도 돼요 (시연)"></label>
      <label class="field"><span>비밀번호</span><span class="pw"><input type="password" name="pw" autocomplete="current-password" placeholder="비밀번호"><button type="button" class="pw-eye" data-eye aria-label="비밀번호 보기">보기</button></span></label>
      <div class="auth-row"><label class="ck"><input type="checkbox" checked> 로그인 상태 유지</label><button type="button" class="linkbtn" data-forgot>비밀번호를 잊었어요</button></div>
      <p class="err" data-err hidden></p>
      <button type="submit" class="btn btn-primary big">로그인</button>
    </form>${SOCIAL}
    <button type="button" class="btn btn-soft big" data-demo>시연용 계정(김하늘)으로 둘러보기</button>
    <p class="switch">아직 계정이 없나요? <a href="#/signup">회원가입</a></p>`);
  const root = view;
  root.addEventListener('click', (e) => {
    const eye = e.target.closest('[data-eye]'); if (eye) { const i = eye.previousElementSibling; const sh = i.type === 'password'; i.type = sh ? 'text' : 'password'; eye.textContent = sh ? '숨기기' : '보기'; return; }
    if (e.target.closest('[data-sso]')) { finishAuth('간편 로그인은 시연이라 김하늘 계정으로 들어왔어요'); return; }
    if (e.target.closest('[data-demo]')) { finishAuth('김하늘 시연용 계정으로 로그인했어요'); return; }
    if (e.target.closest('[data-forgot]')) toast('비밀번호 재설정 메일을 보냈다고 가정할게요 (시연)');
  });
  $('[data-login]', root).addEventListener('submit', (e) => {
    e.preventDefault(); const f = e.target; const b = $('[type="submit"]', f); b.disabled = true; b.innerHTML = '<span class="ring" style="border-color:#fff;border-right-color:transparent"></span>';
    setTimeout(() => finishAuth('로그인했어요 · 시연이라 김하늘 계정으로 보여요'), REDUCE ? 0 : 700);
  });
  setTimeout(() => { const i = $('input[name="em"]', root); if (i) i.focus(); }, 60);
}
function renderSignup() {
  document.body.classList.add('auth-on');
  const st = { step: 1, d: { em: '', pw: '', agree: { tos: false, pi: false, mk: false }, name: '', year: '', region: '서울 관악구', status: '구직 중', jobs: ['SNS 콘텐츠 마케팅'], resume: '' } };
  const JOBS = ['SNS 콘텐츠 마케팅', '퍼포먼스 마케팅', '브랜드 마케팅', '서비스 기획, PM', '데이터 분석', 'UI/UX 디자인', '웹 개발'];
  const draw = () => {
    const d = st.d; const pwOk = [d.pw.length >= 8, /\d/.test(d.pw), /[A-Za-z]/.test(d.pw)];
    const steps = ['계정', '나에 대해', '목표'];
    const prog = `<ol class="steps3">${steps.map((t, i) => `<li class="${i + 1 < st.step ? 'done' : i + 1 === st.step ? 'cur' : ''}"><span>${i + 1 < st.step ? ic('check') : i + 1}</span>${t}</li>`).join('')}</ol>`;
    let body = '';
    if (st.step === 1) body = `<div class="head-l"><h2>일로 시작하기</h2><span class="sub">1분이면 돼요</span></div>${prog}
      <form class="auth-form" data-s1 novalidate>
        <label class="field"><span>이메일</span><input type="email" name="em" value="${esc(d.em)}" autocomplete="email" placeholder="you@example.com"></label>
        <label class="field"><span>비밀번호</span><span class="pw"><input type="password" name="pw" value="${esc(d.pw)}" autocomplete="new-password" placeholder="8자 이상, 영문과 숫자"><button type="button" class="pw-eye" data-eye>보기</button></span></label>
        <ul class="pw-rules">${[['8자 이상', pwOk[0]], ['숫자 포함', pwOk[1]], ['영문 포함', pwOk[2]]].map(([t, ok]) => `<li class="${ok ? 'ok' : ''}">${ic('check')}${t}</li>`).join('')}</ul>
        <div class="agree"><label class="ck all"><input type="checkbox" data-ag="all" ${d.agree.tos && d.agree.pi && d.agree.mk ? 'checked' : ''}> <b>전체 동의</b></label>
          <label class="ck"><input type="checkbox" data-ag="tos" ${d.agree.tos ? 'checked' : ''}> (필수) 이용약관</label>
          <label class="ck"><input type="checkbox" data-ag="pi" ${d.agree.pi ? 'checked' : ''}> (필수) 개인정보 수집, 이용 · 이 기기에만 저장</label>
          <label class="ck"><input type="checkbox" data-ag="mk" ${d.agree.mk ? 'checked' : ''}> (선택) 마감 알림, 소식 받기</label></div>
        <p class="err" data-err hidden></p><button type="submit" class="btn btn-primary big">다음</button></form>${SOCIAL}<p class="switch">이미 계정이 있나요? <a href="#/login">로그인</a></p>`;
    if (st.step === 2) body = `<div class="head-l"><h2>나에 대해 알려 주세요</h2><span class="sub">청년 정책 자격 확인에 써요 · 나중에 바꿀 수 있어요</span></div>${prog}
      <form class="auth-form" data-s2 novalidate>
        <label class="field"><span>이름</span><input name="name" value="${esc(d.name)}" placeholder="김하늘" autocomplete="name"></label>
        <div class="g2"><label class="field"><span>출생 연도</span><select name="year">${['', ...Array.from({ length: 22 }, (_, i) => String(2007 - i))].map((y) => `<option value="${y}"${d.year === y ? ' selected' : ''}>${y || '선택'}</option>`).join('')}</select></label>
          <label class="field"><span>지금 상태</span><select name="status">${['구직 중', '재학 중', '재직 중'].map((x) => `<option${d.status === x ? ' selected' : ''}>${x}</option>`).join('')}</select></label></div>
        <label class="field"><span>사는 곳</span><select name="region">${['서울 관악구', '서울 강남구', '서울 강북구', '서울 마포구', '서울 성동구', '서울 영등포구', '서울 그 외', '경기', '그 외 지역'].map((x) => `<option${d.region === x ? ' selected' : ''}>${x}</option>`).join('')}</select></label>
        <p class="hint-line" data-hint></p>
        <p class="err" data-err hidden></p><div class="g2"><button type="button" class="btn btn-line big" data-back>이전</button><button type="submit" class="btn btn-primary big">다음</button></div></form>`;
    if (st.step === 3) body = `<div class="head-l"><h2>어떤 일을 준비하나요?</h2><span class="sub">고른 직무의 공고와 먼저 비교해 드려요</span></div>${prog}
      <form class="auth-form" data-s3 novalidate>
        <div class="chips">${JOBS.map((j) => `<button type="button" class="chipbtn" data-job="${j}" aria-pressed="${d.jobs.includes(j)}">${j}</button>`).join('')}</div>
        <div class="drop" data-drop>${glass('docs', 36)}<span><b style="font-size:14px;font-weight:600">${d.resume ? esc(d.resume) : '이력서 PDF가 있다면 올려 주세요'}</b><small class="sub" style="display:block">${d.resume ? '올렸어요 · AI가 항목을 나눠 채워요' : '선택 · 없어도 경험을 말로 알려 주면 돼요'}</small></span><input type="file" accept="application/pdf" data-file hidden></div>
        <p class="err" data-err hidden></p><div class="g2"><button type="button" class="btn btn-line big" data-back>이전</button><button type="submit" class="btn btn-primary big">가입 완료</button></div></form>`;
    view.className = 'view'; view.innerHTML = authShell(body);
    const hint = $('[data-hint]', view); if (hint) { const y = Number(d.year); const age = y ? 2026 - y : null; hint.innerHTML = age ? (age >= 19 && age <= 39 ? `<span class="dot ok"></span> 만 ${age}세 · 대부분의 청년 정책 대상이에요${/서울/.test(d.region) ? ' · 서울 정책도 볼 수 있어요' : ''}` : `<span class="dot part"></span> 만 ${age}세 · 청년 정책은 보통 만 19~39세 대상이에요`) : ''; }
  };
  view.onclick = (e) => {
    const T = e.target; const d = st.d;
    const eye = T.closest('[data-eye]'); if (eye) { const i = eye.previousElementSibling; const sh = i.type === 'password'; i.type = sh ? 'text' : 'password'; eye.textContent = sh ? '숨기기' : '보기'; return; }
    if (T.closest('[data-sso]')) { finishAuth('간편 가입은 시연이라 김하늘 계정으로 들어왔어요'); return; }
    if (T.closest('[data-back]')) { st.step--; draw(); return; }
    const jb = T.closest('[data-job]'); if (jb) { const j = jb.dataset.job; d.jobs = d.jobs.includes(j) ? d.jobs.filter((x) => x !== j) : d.jobs.concat(j); jb.setAttribute('aria-pressed', d.jobs.includes(j)); return; }
    if (T.closest('[data-drop]')) { $('[data-file]', view).click(); }
  };
  view.oninput = (e) => {
    const d = st.d; const t = e.target;
    if (t.name === 'em') d.em = t.value; if (t.name === 'name') d.name = t.value;
    if (t.name === 'pw') { d.pw = t.value; const ok = [d.pw.length >= 8, /\d/.test(d.pw), /[A-Za-z]/.test(d.pw)]; $$('.pw-rules li', view).forEach((li, i) => li.classList.toggle('ok', ok[i])); }
  };
  view.onchange = (e) => {
    const d = st.d; const t = e.target;
    if (t.dataset.ag) { if (t.dataset.ag === 'all') { d.agree = { tos: t.checked, pi: t.checked, mk: t.checked }; $$('[data-ag]', view).forEach((c) => { c.checked = t.checked; }); } else { d.agree[t.dataset.ag] = t.checked; $('[data-ag="all"]', view).checked = d.agree.tos && d.agree.pi && d.agree.mk; } }
    if (['year', 'status', 'region'].includes(t.name)) { d[t.name] = t.value; const h = $('[data-hint]', view); if (h) { draw(); } }
    if (t.matches('[data-file]') && t.files[0]) { d.resume = t.files[0].name; draw(); }
  };
  view.onsubmit = (e) => {
    e.preventDefault(); const d = st.d; const err = $('[data-err]', view); const bad = (msg, el) => { err.textContent = msg; err.hidden = false; if (el) { el.closest('.field') && el.closest('.field').classList.add('bad'); el.focus(); } };
    $$('.field', view).forEach((x) => x.classList.remove('bad'));
    if (st.step === 1) {
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.em)) return bad('이메일 형식을 확인해 주세요', $('[name="em"]', view));
      if (!(d.pw.length >= 8 && /\d/.test(d.pw) && /[A-Za-z]/.test(d.pw))) return bad('비밀번호는 8자 이상, 영문과 숫자를 섞어 주세요', $('[name="pw"]', view));
      if (!d.agree.tos || !d.agree.pi) return bad('필수 약관에 동의해 주세요');
    }
    if (st.step === 2 && !d.name.trim()) return bad('이름을 적어 주세요', $('[name="name"]', view));
    if (st.step === 3) { if (!d.jobs.length) return bad('직무를 하나 이상 골라 주세요'); store.set('profile', { age: d.year ? 2026 - Number(d.year) : 24, region: d.region, status: d.status, income: '' }); finishAuth(`가입했어요 · 시연이라 ${d.name || '김하늘'}님 대신 김하늘 데이터로 보여요`); return; }
    st.step++; draw(); const f = $('input, select', view); if (f) f.focus();
  };
  draw(); setTimeout(() => { const i = $('input[name="em"]', view); if (i) i.focus(); }, 60);
}
function openLogin() { go('#/login'); }
function openLoginOld() {
  openDrawer(`${drHead('일로 시작하기', '로그인')}
    <div class="dr-b"><label class="field"><span>이메일</span><input type="email" placeholder="you@example.com" autocomplete="email" data-em></label><label class="field"><span>비밀번호</span><input type="password" placeholder="8자 이상" autocomplete="current-password"></label>
      <p class="sub" style="margin:0;font-size:12px;line-height:1.6">시연 버전이라 실제 계정을 만들지 않아요. 아래 시연용 계정으로 들어가면 김하늘 이력서와 대화가 보여요.</p></div>
    <div class="dr-f"><button type="button" class="btn btn-line" data-li="email">이메일로 로그인</button><span style="flex:1"></span><button type="button" class="btn btn-primary" data-li="demo">시연용 계정으로 계속하기</button></div>`, (dr) => {
    dr.addEventListener('click', (e) => { const b = e.target.closest('[data-li]'); if (!b) return; store.set('user', true); closeDrawer(); toast('김하늘 시연용 계정으로 로그인했어요'); route(); });
  });
}
function renderSide() {
  const gEl = $('[data-goal]'); const tEl = $('#todo'); gEl.hidden = !authed(); tEl.parentElement.hidden = !authed(); if (!authed()) return;
  const L = apps(); const today = ymd(now()); const sv = saved();
  const anyCmp = chats().some((c) => c.sc === 'compare'); const flipped = chats().some((c) => (c.cmpRows || []).filter((r) => r[1] === 'part').length < 3);
  const st = [anyCmp ? 'on' : '', flipped ? 'half' : anyCmp ? 'half' : '', L.some((a) => a.status !== '작성 중') ? 'on' : L.length ? 'half' : ''];
  $('[data-goal]').innerHTML = `<span class="gt"><span>목표</span><span>${st.filter((x) => x === 'on').length}/3 단계</span></span><b>SNS 콘텐츠 마케터 · 신입, 인턴</b><span class="steps">${st.map((x) => `<i class="${x}"></i>`).join('')}</span><span class="steps-l"><span>공고 비교</span><span>빈칸 채우기</span><span>지원</span></span>`;
  const items = [];
  if (store.get('pending', 1)) items.push(`<li><button type="button" data-act="draft"><span class="dot part"></span><span class="tt">정책 신청서 초안 확인</span><span class="dd hot">D-3</span></button></li>`);
  L.filter((a) => a.status === '작성 중').slice(0, 2).forEach((a) => { const d = a.close && a.close >= today ? dday(a.close) : null; items.push(`<li><a href="#/apply/${a.id}"><span class="dot run"></span><span class="tt">${esc(a.company)} 지원서 쓰기</span>${d !== null ? `<span class="dd${d <= 3 ? ' hot' : ''}">D-${d}</span>` : ''}</a></li>`); });
  DATA.posts.filter((p) => sv[postKey(p)] && p.close >= today).slice(0, 2).forEach((p) => { const d = dday(p.close); items.push(`<li><a href="#/jobs"><span class="dot off"></span><span class="tt">${esc(p.company)} 마감</span><span class="dd${d <= 3 ? ' hot' : ''}">D-${d}</span></a></li>`); });
  tasks().filter((t) => !t.done).sort((x, y) => x.due.localeCompare(y.due)).slice(0, 3).forEach((t) => { const d = dday(t.due); items.push(`<li><a href="#/tasks"><span class="cb sm"></span><span class="tt">${esc(t.t)}</span><span class="dd${d <= 1 ? ' hot' : ''}">${d <= 0 ? '오늘' : 'D-' + d}</span></a></li>`); });
  items.push(`<li><a href="#/edu?gap=${encodeURIComponent('숏폼 성과 분석')}"><span class="dot no"></span><span class="tt">빈칸 · 숏폼 성과 분석</span></a></li>`);
  const n = tasks().filter((t) => !t.done).length;
  $('#todo').innerHTML = items.slice(0, 3).join('') + `<li><a href="#/tasks" class="todo-all"><span class="tt">할 일 모두 보기</span><span class="dd">${items.length > 3 ? `+${items.length - 3}` : ''}</span></a></li>`;
}

/* ---------- composer (shared) ---------- */
function composerHTML({ placeholder, tools = true, stop = false, chips = '' }) {
  return `<form class="composer" data-composer>
    <label class="sr" for="ask">질문</label>
    <textarea id="ask" rows="2" placeholder="${esc(placeholder)}"></textarea>
    <div class="bar">
      ${tools ? `<button type="button" class="tool" data-tool="resume" aria-pressed="true">${ic('clip')}김하늘_이력서.pdf</button>
      <button type="button" class="tool" data-tool="link">${ic('link')}공고 링크</button>
      <button type="button" class="tool" data-tool="policy">${ic('policy')}정책 자격 확인</button>` : chips}
      <span class="sp"></span>
      <button type="button" class="icon-btn" data-tool="mic" aria-label="말로 입력하기">${ic('mic')}</button>
      ${stop ? `<button type="button" class="btn btn-line" data-stop>${ic('stop')}<span class="send-t">멈추기</span></button>` : ''}
      <button type="submit" class="btn btn-primary" data-send disabled>${ic('send')}<span class="send-t">보내기</span></button>
    </div></form>`;
}
function wireComposer(root, onSend) {
  const f = $('[data-composer]', root); const ta = $('textarea', f); const send = $('[data-send]', f);
  if (matchMedia('(max-width:767px)').matches) ta.placeholder = '물어보세요';
  const sync = () => { send.disabled = !ta.value.trim(); ta.style.height = 'auto'; ta.style.height = Math.min(ta.scrollHeight, 200) + 'px'; };
  ta.addEventListener('input', sync);
  ta.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); if (ta.value.trim()) f.requestSubmit(); } });
  f.addEventListener('submit', (e) => { e.preventDefault(); const v = ta.value.trim(); if (!v) return; ta.value = ''; sync(); onSend(v); });
  f.addEventListener('click', (e) => {
    const t = e.target.closest('[data-tool]'); if (!t) return;
    const k = t.dataset.tool;
    if (k === 'resume') { const on = t.getAttribute('aria-pressed') !== 'true'; t.setAttribute('aria-pressed', on); toast(on ? '이력서를 붙였어요 · 비교에 써요' : '이력서를 뺐어요 · 경험을 말로 알려 주세요'); }
    if (k === 'link') { ta.value = '이 공고와 내 이력서 비교해 줘: https://linkareer.com/activity/'; ta.focus(); sync(); }
    if (k === 'policy') { ta.value = '구직 기간에 받을 수 있는 서울 청년 정책은?'; ta.focus(); sync(); }
    if (k === 'mic') listen(t, ta, sync);
  });
  return { ta, sync, setStop(on) { const s = $('[data-stop]', f); if (s) s.hidden = !on; } };
}
function listen(btn, ta, sync) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { toast('이 브라우저는 음성 입력을 지원하지 않아요 · 크롬에서 해 보세요'); return; }
  const r = new SR(); r.lang = 'ko-KR'; r.interimResults = true;
  btn.classList.add('rec'); btn.setAttribute('aria-label', '듣는 중 · 누르면 멈춰요');
  r.onresult = (e) => { ta.value = [...e.results].map((x) => x[0].transcript).join(''); sync(); };
  r.onend = () => { btn.classList.remove('rec'); btn.setAttribute('aria-label', '말로 입력하기'); ta.focus(); };
  r.onerror = () => toast('음성을 듣지 못했어요 · 마이크 권한을 확인해 주세요');
  btn.onclick = () => r.stop(); r.start();
}

/* ---------- home ---------- */
const PROMPTS = [
  ['비교', '카카오스타일 SNS 콘텐츠 마케터 인턴 공고와 내 이력서 비교해 줘'],
  ['빈칸', '숏폼 성과 분석 빈칸, 2주 안에 채우는 방법 알려 줘'],
  ['정책', '구직 기간에 받을 수 있는 서울 청년 정책은?'],
];
/* highlight what the weekly agent found, on the page the digest card opens */
let WK = {}, HL = null;
const HL_ATTR = { jobs: 'k', pol: 'p', edu: 'c' };
const HL_TXT = { jobs: ['새 공고', '건'], pol: ['받을 수 있는 정책', '건'], edu: ['빈칸 채울 과정', '개'], trend: ['급상승 역량', '개'] };
function isHL(kind, id) { return !!HL && HL.kind === kind && HL.ids.includes(id); }
function hlSort(L, kind, key) { if (HL && HL.kind === kind) L.sort((a, b) => isHL(kind, key(b)) - isHL(kind, key(a))); return L; }
function hlOff() { HL = null; $$('.hl', view).forEach((x) => x.classList.toggle('hl', false)); const b = $('.hl-bar', view); if (b) b.outerHTML = ''; }
function markHL() {
  if (!HL) return;
  if (location.hash.split('?')[0] !== HL.hash) { HL = null; return; }
  const a = HL_ATTR[HL.kind];
  if (a) $$(`[data-${a}]`, view).forEach((el) => el.classList.toggle('hl', HL.ids.includes(el.dataset[a])));
  if (HL.kind === 'trend') { const li = $$('.bars li', view)[2]; if (li) li.classList.add('hl'); }
  if (!$('.hl-bar', view)) {
    const head = $('.page-head', view); if (!head) return;
    const [t, u] = HL_TXT[HL.kind];
    head.insertAdjacentHTML('afterend', `<div class="hl-bar"><span class="wk-dot"></span><span>이번 주 일로가 찾아온 <b>${t} ${HL.ids.length}${u}</b>${u === '개' ? '를' : '을'} ${HL.kind === 'trend' ? '표시했어요' : '맨 위에 모아 표시했어요'} · 11월 2일 자동 확인</span><button type="button" class="btn btn-ghost sm" data-hl-off>표시 끄기</button></div>`);
    $('[data-hl-off]', view).addEventListener('click', hlOff);
  }
}
/* 이번 주 일로가 찾아온 것: a scheduled weekly agent run, picked from the real data */
function weekly() {
  const today = ymd(now());
  const posts = DATA.posts.filter((p) => p.close >= today).sort((a, b) => b.ov.length - a.ov.length).slice(0, 3);
  const pols = DATA.policies.filter((p) => p.st !== '마감' && p.r === '서울' && p.lc === '일자리').slice(0, 2);
  const crs = DATA.courses.filter((c) => c.st === '모집 중' && c.f === '디지털마케팅').slice(0, 2);
  const seen = store.get('weekly-seen', false);
  WK = { jobs: posts.map((p) => p.company + p.title), pol: pols.map((p) => p.id), edu: crs.map((c) => c.id), trend: ['data'] };
  const card = (k, href, tag, n, body) => `<a class="wk-c" href="${href}" data-wk="${['jobs', 'pol', 'edu', 'trend'][k]}" style="animation-delay:${k * 60}ms"><span class="wk-tag">${tag}</span><span class="wk-row"><span class="wk-n">${n}</span><span class="wk-t">${body}</span></span></a>`;
  return `<section class="wk"><div class="wk-h"><span class="wk-ttl">${seen ? '' : '<i class="wk-dot"></i>'}이번 주 일로가 찾아왔어요 <span class="ai-tag">AI</span></span><span class="sub">매주 월요일 9시 자동 확인 · 11월 2일</span></div>
    <div class="wk-g">
      ${card(0, '#/jobs', '새 공고', `${posts.length}건`, `<span class="wk-logos">${posts.map((p) => companyLogo(p.company, p.title, 20)).join('')}</span>`)}
      ${card(1, '#/edu/policy', '받을 수 있는 정책', `${pols.length}건`, esc(pols[0] ? pols[0].n.replace(/^2026\s*/, '') : ''))}
      ${card(2, '#/edu', '빈칸 채울 과정', `${crs.length}개`, crs.length ? `마감 <span class="t-no">D-${dday(crs[0].recEnd.replace(/\./g, '-'))}</span>` : '')}
      ${card(3, '#/trend', '급상승 역량', '<span class="t-no">▲5</span>', '데이터, 성과 분석')}
    </div></section>`;
}
function renderHome() {
  const pending = store.get('pending', 1);
  mount(`<section class="home">
    <div class="top"><div class="head-l"><h1>${authed() ? greet() + ', 하늘님' : '안녕하세요'}</h1><span class="sub">${authed() ? `에이전트 3개 대기${pending ? ` · 확인할 일 ${pending}개` : ''}` : '로그인하지 않아도 공고와 정책을 둘러볼 수 있어요'}</span></div>
      <div class="head-r"><span>${dateKo()}</span><span class="sub">${timeKo()}</span></div></div>
    <div class="m-hello"><span>${authed() ? '안녕하세요 <em>하늘님</em>' : '안녕하세요'}</span><span>무엇을 준비할까요?</span></div>
    <div class="hero">${ORB(72)}<h2>오늘은 무엇을 준비할까요?</h2><p>해 본 일을 말하면 실제 공고와 비교하고, 빈칸은 과정과 청년 정책으로 이어 드려요</p></div>
    ${authed() ? weekly() : `<div class="feat">
      <button type="button" data-feat="translate">${glass('chat', 44)}<span><b>경험 번역</b><small>알바, 동아리 경험을 공고의 말로</small></span></button>
      <button type="button" data-feat="jobs">${glass('docs', 44)}<span><b>공고 비교</b><small>문장마다 맞음, 일부, 없음</small></span></button>
      <button type="button" data-feat="edu">${glass('plus', 44)}<span><b>빈칸 채우기</b><small>SeSAC 과정 ${DATA.courses.length || 210}개에서</small></span></button>
      <button type="button" data-feat="policy">${glass('shield', 44)}<span><b>정책 찾기</b><small>청년 정책 ${DATA.policies.length || 515}건에서</small></span></button>
    </div>`}
    <div class="prompts"><span class="m-agent">${ORB(18)}<b>일로</b></span><span class="sub">이렇게 물어보세요 · SNS 콘텐츠 마케팅</span><div class="row">${PROMPTS.map(([k, t]) => `<button type="button" class="prompt" data-prompt="${esc(t)}"><i class="p-ic">${k === '비교' ? `<b class="p-doc">${companyLogo('카카오스타일', '', 26)}<u><s class="ok"></s><s class="ok"></s><s class="part"></s><s class="no"></s></u></b>` : glass(k === '빈칸' ? 'plus' : 'shield', 30)}</i><em>${esc(t)}</em><span>${k}</span></button>`).join('')}</div></div>
    ${composerHTML({ placeholder: '무엇이든 물어보세요. 예: 마케터 하고 싶은데 뭐부터 해야 할지 모르겠어요' })}
  </section>`);
  const home = $('.home', view);
  const c = wireComposer(home, async (q) => { home.classList.add('leaving'); await wait(220); startChat(q); });
  home.addEventListener('click', (e) => {
    const wk = e.target.closest('[data-wk]'); if (wk) { store.set('weekly-seen', true); HL = { kind: wk.dataset.wk, ids: WK[wk.dataset.wk], hash: wk.getAttribute('href') }; }
    const p = e.target.closest('[data-prompt]'); if (p) { c.ta.value = p.dataset.prompt; c.sync(); c.ta.focus(); return; }
    const f = e.target.closest('[data-feat]'); if (!f) return;
    const k = f.dataset.feat;
    if (k === 'translate') { c.ta.value = '동아리 인스타 운영 경험을 이력서 문장으로 바꿔 줘'; c.sync(); c.ta.focus(); }
    if (k === 'jobs') go('#/jobs');
    if (k === 'edu') go('#/edu');
    if (k === 'policy') go('#/edu/policy');
  });
  setTimeout(() => c.ta.focus(), 50);
}

/* ---------- chat ---------- */
const ROWS = [
  ['SNS 채널 운영 경험', 'ok', '"팔로워 3천 → 1.2만"'],
  ['콘텐츠 기획 및 제작', 'ok', '"주 3회 콘텐츠 기획"'],
  ['캠페인 성과 지표 관리', 'part', '수치 없음'],
  ['브랜드 톤앤매너 이해', 'ok', '"동아리 브랜딩 리뉴얼"'],
  ['협업 커뮤니케이션', 'ok', '"운영진 6명 협업"'],
  ['데이터 기반 콘텐츠 개선', 'part', '수치 없음'],
  ['디자인 툴 활용', 'part', '"캔바" · 숙련도 없음'],
  ['광고 운영 경험', 'ok', '"공모전 SNS 광고 집행"'],
  ['숏폼 콘텐츠 성과 분석', 'no', '근거 없음'],
];
function renderChat(id) {
  const c = chats().find((x) => x.id === id);
  if (!c) { go('#/'); return; }
  const fresh = sessionStorage.getItem('illo2-run') === id && !c.done;
  mount(`<div class="chat">
    <section class="ws" aria-labelledby="ws-h">
      <div class="ws-head"><div class="head-l"><h2 id="ws-h">작업 공간</h2><span class="sub" id="ws-sub">에이전트 준비 중</span></div><span class="sub ws-demo">시연용 예시 결과예요</span><button type="button" class="btn btn-line sm ws-close" data-act="ws-toggle">대화로</button></div>
      <div id="ws-body" style="display:flex;flex-direction:column;gap:14px"></div>
    </section>
    <section class="talk" aria-label="대화">
      <div class="talk-h"><div class="head-l"><h1>${esc(c.title)}</h1><span class="sub" id="talk-sub">지원은 하지 않아요 · 고르는 건 하늘님</span></div><button type="button" class="btn btn-line sm ws-open-btn" data-act="ws-toggle">작업 공간</button><div class="head-r"><span>${dateKo()}</span><span class="sub">${timeKo()}</span></div></div>
      <div class="msgs" id="msgs" aria-live="polite"></div>
      ${composerHTML({ placeholder: '이어서 물어보세요. 예: 일부 3개는 뭘 더 적으면 돼?', tools: false, stop: true })}
    </section></div>`);
  const ctx = makeCtx(c);
  ctx.comp = wireComposer($('.talk', view), (v) => followUp(ctx, v));
  $('[data-stop]', view).onclick = () => { runToken++; ctx.comp.setStop(false); toast('멈췄어요 · 지금까지 찾은 것만 보여요'); };
  ctx.comp.setStop(false);
  addUser(ctx, c.q, !fresh);
  if (fresh) { sessionStorage.removeItem('illo2-run'); run(ctx, false); }
  else { run(ctx, true).then(() => (c.follow || []).forEach((f) => replayFollow(ctx, f))); }
}
function makeCtx(c) {
  return { c, tok: runToken, msgs: $('#msgs'), ws: $('#ws-body'), wsSub: $('#ws-sub'), cmp: null };
}
const alive = (ctx) => ctx.tok === runToken;
function scrollMsgs(ctx) { ctx.msgs.scrollTop = ctx.msgs.scrollHeight; }
function addUser(ctx, text, instant) {
  const d = document.createElement('div'); d.className = 'um'; d.textContent = text; if (instant) d.style.animation = 'none';
  ctx.msgs.appendChild(d); scrollMsgs(ctx);
}
function addAssistant(ctx) {
  const d = document.createElement('div'); d.className = 'am';
  d.innerHTML = `<div class="am-h">${ORB(18)}일로 <span class="ai-tag">AI</span></div><div class="am-body"></div>`;
  ctx.msgs.appendChild(d); scrollMsgs(ctx); return $('.am-body', d);
}
async function think(ctx, body, steps, instant) {
  const box = document.createElement('div'); box.className = 'reason'; box.dataset.open = instant ? 'false' : 'true';
  box.innerHTML = `<button type="button" aria-expanded="${!instant}">${ic('chev')}<span class="lbl">${instant ? `생각 과정 · ${steps.length}단계` : '<span class="thinking">생각하는 중<i></i><i></i><i></i></span>'}</span></button><ol></ol>`;
  body.appendChild(box);
  const btn = $('button', box); btn.onclick = () => { const o = box.dataset.open !== 'true'; box.dataset.open = o; btn.setAttribute('aria-expanded', o); };
  const ol = $('ol', box); const t0 = Date.now();
  if (!instant) await wait(900);
  for (let i = 0; i < steps.length; i++) {
    if (!alive(ctx)) return false;
    const li = document.createElement('li');
    li.innerHTML = `<span class="ck">${instant ? ic('check') : '<span class="ring"></span>'}</span><span>${esc(steps[i][0])}</span>`;
    if (!instant) li.classList.add('cur');
    ol.appendChild(li); scrollMsgs(ctx);
    if (!instant) { await (steps[i][1] ? steps[i][1]() : wait(700)); li.classList.remove('cur'); $('.ck', li).innerHTML = ic('check'); }
  }
  if (!instant) {
    const s = Math.max(1, Math.round((Date.now() - t0) / 1000));
    $('.lbl', box).textContent = `생각 과정 · ${steps.length}단계 · ${s}초`;
    await wait(250); box.dataset.open = 'false'; btn.setAttribute('aria-expanded', 'false');
  }
  return true;
}
async function stream(ctx, body, html, instant) {
  // types an HTML paragraph character by character (tags are inserted whole)
  const p = document.createElement('p'); body.appendChild(p);
  if (instant) { p.innerHTML = html; return true; }
  const tokens = html.match(/<[^>]+>|[^<]/g) || []; let out = '';
  const caret = '<span class="caret"></span>';
  for (let i = 0; i < tokens.length; i++) {
    if (!alive(ctx)) { p.innerHTML = out; return false; }
    out += tokens[i];
    if (tokens[i][0] !== '<') { if (i % 2 === 0 || i === tokens.length - 1) { p.innerHTML = out + caret; scrollMsgs(ctx); await wait(i % 18 === 0 ? 40 : 14); } }
  }
  p.innerHTML = out; return true;
}
function agentCard(key, sub, state = 'wait') {
  const a = AGENTS[key];
  const el = document.createElement('article'); el.className = 'card agent' + (state === 'wait' ? ' wait' : ''); el.dataset.agent = key;
  el.innerHTML = `<div class="agent-h">${glass(a.g, 40)}<div class="agent-t"><b>${a.name}</b><span class="asub">${esc(sub)}</span></div><span class="st">${stLabel(state)}</span></div><div class="agent-b"></div>`;
  return el;
}
function stLabel(s) {
  return { wait: '<span class="dot off"></span><span style="color:var(--mute)">대기</span>', run: '<span class="dot run pulse"></span>작업 중', done: '<span class="dot ok"></span>완료', check: '<span class="dot part"></span>확인 필요', ok: '<span class="dot ok"></span>확인 완료' }[s];
}
function setState(el, s, sub) {
  $('.st', el).innerHTML = stLabel(s); el.classList.toggle('wait', s === 'wait');
  if (sub) $('.asub', el).textContent = sub;
  if (s !== 'wait') $('.agent-h', el).classList.add('div');
}
function wsCount(ctx) {
  const all = $$('[data-agent]', ctx.ws); const done = all.filter((a) => /완료/.test($('.st', a).textContent)).length;
  const run = all.filter((a) => /작업 중/.test($('.st', a).textContent)).length; const chk = all.filter((a) => /확인 필요/.test($('.st', a).textContent)).length;
  ctx.wsSub.textContent = [run && `에이전트 ${run}개 작업 중`, done && `${done}개 완료`, chk && `확인할 일 ${chk}개`, all.length - done - run - chk > 0 && `${all.length - done - run - chk}개 대기`].filter(Boolean).join(' · ') || '준비 중';
}

/* mock job descriptions: same clean structure for every posting (scraped text was too messy to show) */
function hashStr(t) { let h = 0; for (const ch of t) h = (h * 31 + ch.charCodeAt(0)) | 0; return Math.abs(h); }
const DOC_SETS = [['자기소개서'], ['자기소개서', '포트폴리오'], ['이력서', '포트폴리오'], ['자기소개서', '포트폴리오']];
function makeJD(p) {
  const ov = p.ov || []; const intern = p.type === '인턴';
  const work = ['브랜드 SNS 채널(인스타그램, 유튜브 쇼츠) 콘텐츠 기획 및 운영'];
  if (ov.includes('콘텐츠 기획') || !ov.length) work.push('월간 콘텐츠 캘린더 작성과 게시 일정 관리');
  if (ov.includes('데이터, 성과 분석')) work.push('콘텐츠 성과(도달, 저장, 전환) 분석 및 주간 리포트 작성');
  if (ov.includes('디자인 툴')) work.push('카드뉴스, 썸네일 등 SNS 이미지 제작');
  work.push('댓글, DM 등 커뮤니티 소통 관리');
  const req = ['SNS 채널을 직접 운영해 본 경험이 있는 분', '콘텐츠 기획부터 제작까지 해 본 경험이 있는 분', '팀원과 협업하고 의견을 나누는 데 익숙한 분'];
  if (ov.includes('데이터, 성과 분석')) req.push('엑셀, 스프레드시트로 성과 데이터를 정리할 수 있는 분');
  const pref = ['숏폼 콘텐츠를 만들고 성과를 분석해 본 경험', '마케팅 공모전, 대외활동 경험'];
  if (ov.includes('디자인 툴')) pref.splice(1, 0, '포토샵, 피그마 등 디자인 툴 활용 가능자');
  const docs = DOC_SETS[hashStr(p.company + p.title) % DOC_SETS.length];
  return {
    intro: `${p.company} 마케팅팀에서 브랜드 채널을 함께 키울 ${intern ? '인턴' : '신입'}을 찾아요.`,
    secs: [['담당 업무', work], ['자격 요건', req], ['우대 사항', pref], ['근무 조건', [intern ? '인턴 3개월 · 평가 후 정규직 전환 검토' : '정규직 · 수습 3개월', '주 5일, 서울 근무']], ['전형 절차', ['서류 전형 → 실무 면접 → 최종 합격']], ['제출 서류', [docs.join(', ')]]],
    docs,
  };
}
/* compare card: 공고 문장 ↔ 내 근거, one rule per row */
const RULE = { ok: '같은 행동 + 수치가 있어서 맞음', part: '행동은 있지만 수치가 없어서 일부', no: '이력서에서 같은 행동을 찾지 못해서 없음' };
function evidence(t, v) {
  if (v === 'no') return '근거 없음';
  if (/SNS|인스타|소셜|채널/.test(t)) return v === 'ok' ? '"동아리 인스타그램 2년 운영 · 팔로워 3천 → 1.2만"' : '"인스타그램 운영" · 수치 없음';
  if (/기획|콘텐츠|제작|에디터|아티클/.test(t)) return '"주 3회 콘텐츠 기획, 제작 · 2년"';
  if (/협업|커뮤니케이션|소통/.test(t)) return '"운영진 6명과 협업"';
  if (/분석|데이터|지표|성과|리서치|트렌드/.test(t)) return '"매주 게시물 반응 기록" · 수치 없음';
  return '"마케팅 공모전 팀장" · 수치 없음';
}
function buildRows(post) {
  const P = post || { company: '카카오', title: '브랜드마케팅 인턴', type: '인턴', ov: ['콘텐츠 기획', '데이터, 성과 분석', '디자인 툴'] };
  const J = makeJD(P); const doc = [{ intro: J.intro }]; const rows = []; let skipped = 0;
  J.secs.forEach(([h, lines]) => { doc.push({ h }); lines.forEach((t) => {
    const line = { t, bullet: true };
    if (['담당 업무', '자격 요건', '우대 사항'].includes(h)) { let v = FIT(t) || 'no'; let ev = evidence(t, v); if (v === 'ok' && !/\d/.test(ev)) v = 'part'; line.r = rows.length; rows.push([t, v, ev, RULE[v]]); }
    doc.push(line); }); });
  return { rows, doc, skipped, real: false, docs: J.docs };
}
function buildCompare(ctx, post, instant) {
  const R = buildRows(post); if (ctx.c.cmpRows && ctx.c.cmpRows.length === R.rows.length) R.rows = ctx.c.cmpRows;
  const n = R.rows.length; const today = ymd(now());
  const name = post ? `${post.company} · ${post.title}` : '카카오 브랜드마케팅 인턴';
  const el = agentCard('compare', `${name} · 요건 ${n}문장`, instant ? 'done' : 'run');
  ctx.ws.appendChild(el);
  const lg = post ? logoFor(post.company, post.title) : 'logo-kakao.png';
  $('.agent-b', el).innerHTML = `<div class="cmp-top"><div class="trio" style="flex:1"><div><span><span class="dot ok"></span>맞음</span><span class="big" data-c="ok">0</span></div><div><span><span class="dot part"></span>일부</span><span class="big" data-c="part">0</span></div><div><span><span class="dot no"></span>없음</span><span class="big t-no" data-c="no">0</span></div></div>
      <div class="cmp-prog"><span class="sub">비교한 문장</span><span class="big" style="font-size:28px"><span data-n>0</span><small> / ${n}</small></span><div class="bar3" style="width:120px"><i data-bar></i></div></div></div>
    <div class="jd">
      <div class="jd-head">${companyLogo(post ? post.company : '카카오', post ? post.title : '', 44, '10px')}<div class="head-l" style="flex:1"><span class="sub">${esc(post ? post.company : '카카오')} · ${esc(post ? post.size : '대기업')}</span><b style="font-size:17px;font-weight:600;line-height:1.4">${esc(post ? post.title : '브랜드마케팅 인턴')}</b><span class="sub">${esc(post ? post.type : '인턴')} · ${post && post.close ? (post.close < today ? '마감' : '마감 ' + post.close.replace(/-/g, '.')) : '상시'} · 링커리어</span></div>
        <div class="jd-legend"><span><i class="mk ok"></i>맞음</span><span><i class="mk part"></i>일부</span><span><i class="mk no"></i>없음</span><span><i class="mk off"></i>비교 안 함</span></div></div>
      <div class="jd-body" data-doc></div>
    </div>
    <p class="sub" style="margin:0;font-size:12px;line-height:1.6">시연용 예시 공고 내용이에요 · 업무, 자격, 우대 문장 ${n}개를 비교했고 근무 조건과 전형은 비교에서 뺐어요 · 문장을 누르면 내 근거와 판정 이유가 보여요 · 판정은 규칙으로, AI는 근거만 찾아요</p>
    <div style="display:flex;gap:8px">${post ? `<a class="btn btn-line" href="${esc(post.url)}" target="_blank" rel="noopener">공고 원문 ${ic('ext')}</a>` : ''}${saveBtn(postKey(post))}</div>`;
  ctx.cmp = { el, rows: R.rows.map((r) => [...r]), doc: R.doc, real: R.real, skipped: R.skipped, post, open: null };
  ctx.c.cmpReal = R.real;
  drawDoc(ctx, instant ? R.rows.length : 0);
  $('[data-doc]', el).addEventListener('click', (e) => { const ln = e.target.closest('[data-r]'); if (!ln || ln.classList.contains('pending')) return; const k = Number(ln.dataset.r); ctx.cmp.open = ctx.cmp.open === k ? null : k; drawDoc(ctx, ctx.cmp.shown); });
  syncSaveBtns();
  if (instant) finishCompare(ctx, true);
  return el;
}
function cmpTally(ctx) { const t = { ok: 0, part: 0, no: 0 }; ctx.cmp.rows.forEach((r) => t[r[1]]++); return t; }
function drawDoc(ctx, shown, scanning = -1) {
  ctx.cmp.shown = shown;
  $('[data-doc]', ctx.cmp.el).innerHTML = ctx.cmp.doc.map((d) => {
    if (d.intro) return `<p class="jd-intro">${esc(d.intro)}</p>`;
    if (d.h) return `<h4>${esc(d.h)}</h4>`;
    if (d.r === undefined) return `<div class="jl off">${d.bullet ? '<span class="bul">-</span>' : ''}<span>${esc(d.t)}</span></div>`;
    const r = ctx.cmp.rows[d.r]; const done = d.r < shown; const v = r[1];
    const cls = scanning === d.r ? 'scan' : done ? 'v-' + v : 'pending';
    const open = ctx.cmp.open === d.r;
    return `<div class="jl ${cls}${open ? ' open' : ''}" data-r="${d.r}" role="button" tabindex="0" aria-expanded="${open}"><span class="bul">-</span><span class="jt">${esc(d.t)}</span>${done ? verd(v) : scanning === d.r ? '<span class="ring"></span>' : ''}
      ${done && open ? `<div class="note"><span class="lab">내 이력서 근거 <span class="ai-tag">AI가 찾음</span></span><span class="${v === 'no' ? 't-no' : ''}">${esc(r[2])}</span><span class="rule">${esc(r[3] || RULE[v])}</span>${v !== 'ok' ? `<span class="hint">${v === 'part' ? '이 경험의 결과 숫자를 대화창에 알려 주면 다시 판정해요' : '교육이나 활동으로 채울 수 있어요 · 다음 단계에서 골라요'}</span>` : ''}</div>` : ''}</div>`;
  }).join('');
}
async function animateCompare(ctx) {
  const el = ctx.cmp.el; const N = ctx.cmp.rows.length;
  for (let n = 0; n < N; n++) {
    if (!alive(ctx)) return false;
    drawDoc(ctx, n, n); const ln = $(`[data-r="${n}"]`, el); if (ln) ln.scrollIntoView({ block: 'nearest', behavior: REDUCE ? 'auto' : 'smooth' });
    await wait(380);
    $('[data-n]', el).textContent = n + 1; $('[data-bar]', el).style.width = ((n + 1) / N * 100) + '%';
    const t = { ok: 0, part: 0, no: 0 }; ctx.cmp.rows.slice(0, n + 1).forEach((x) => t[x[1]]++);
    ['ok', 'part', 'no'].forEach((k) => { $(`[data-c="${k}"]`, el).textContent = t[k]; });
    drawDoc(ctx, n + 1); await wait(120);
  }
  return true;
}
function drawRows(ctx) { drawDoc(ctx, ctx.cmp.rows.length); }
function finishCompare(ctx, instant) {
  const el = ctx.cmp.el; const t = cmpTally(ctx); const N = ctx.cmp.rows.length;
  $('[data-n]', el).textContent = N; $('[data-bar]', el).style.width = '100%';
  ['ok', 'part', 'no'].forEach((k) => countUp($(`[data-c="${k}"]`, el), t[k], instant));
  if (ctx.cmp.open === null) { const first = ctx.cmp.rows.findIndex((r) => r[1] === 'no'); ctx.cmp.open = first >= 0 ? first : ctx.cmp.rows.findIndex((r) => r[1] === 'part'); }
  drawDoc(ctx, N);
  setState(el, 'done');
}
function countUp(node, to, instant) {
  if (instant || REDUCE) { node.textContent = to; return; }
  let i = 0; const step = () => { node.textContent = i; if (i++ < to) setTimeout(step, 90); }; step();
}
/* course + policy cards */
function courseCard(ctx, gap, instant) {
  const el = agentCard('course', `빈칸 "${gap}" · SeSAC 과정 ${DATA.courses.length}개에서`, instant ? 'done' : 'run'); ctx.ws.appendChild(el);
  const picks = ['edu-1465', 'edu-1421', 'edu-1202'].map((id) => DATA.courses.find((c) => c.id === id)).filter(Boolean);
  const body = $('.agent-b', el);
  body.innerHTML = picks.map((c, i) => `<div class="mini card" style="animation-delay:${i * 90}ms;border-color:var(--line-3)">${TH[c.id] ? `<img src="assets/${TH[c.id]}" alt="">` : ''}<div class="tx"><span>${i === 0 ? '빈칸을 직접 다뤄요' : c.g + ' · ' + c.cp}</span><b>${esc(c.n.replace(/^\([^)]*\)\s*/, ''))}</b><small>SeSAC ${esc(c.cp)} · ${esc(c.st)} · ${esc(c.edu)}</small></div>${saveBtn(c.id)}</div>`).join('');
  $$('.mini', body).forEach((m, i) => m.addEventListener('click', (e) => { if (!e.target.closest('.save')) openCourse(picks[i]); }));
  $$('[data-save]', body).forEach((b, i) => b.onclick = (e) => { e.stopPropagation(); const c = picks[i]; toggleSave(c.id, { kind: '교육', t: c.n, s: `SeSAC ${c.cp} · ${c.st}`, img: TH[c.id], href: '#/edu' }, b); });
  syncSaveBtns(); if (instant) setState(el, 'done'); return el;
}
function policyCard(ctx, instant, label = '구직 기간 생활비') {
  const el = agentCard('policy', `청년 정책 ${DATA.policies.length}건에서 하늘님 자격 확인`, instant ? (store.get('pending', 1) ? 'check' : 'ok') : 'run'); ctx.ws.appendChild(el);
  const pol = DATA.policies.find((p) => p.id === 'pol-20261018005400213991') || DATA.policies[0];
  const open = DATA.policies.filter((p) => p.st === '신청 중' || p.st === '상시');
  const body = $('.agent-b', el);
  body.innerHTML = `<div class="trio"><div><span>신청 가능한 정책</span><span class="big">${open.length}</span></div><div><span>일자리</span><span class="big">${open.filter((p) => p.lc === '일자리').length}</span></div><div><span>주거, 금융·복지</span><span class="big">${open.filter((p) => p.lc === '주거' || p.lc === '금융·복지').length}</span></div></div>
    <div class="inset" style="padding:14px 16px;gap:10px"><b style="font-size:14px;font-weight:600">${esc(pol.n)} 신청서 초안을 써 뒀어요</b><span class="sub" style="font-size:12px">${label} · ${esc(pol.o)} · ${esc(pol.st)} · 제출은 하늘님이 직접 해요</span>
      <div style="display:flex;gap:6px"><button type="button" class="btn btn-line" data-draft style="font-weight:600">초안 확인</button><button type="button" class="btn btn-ghost" data-later>나중에</button>${saveBtn(pol.id)}</div></div>`;
  $('[data-draft]', body).onclick = () => openDraft(pol, el, ctx);
  $('[data-later]', body).onclick = () => toast('홈의 "확인할 일"에 남겨 둘게요');
  $('[data-save]', body).onclick = (e) => toggleSave(pol.id, { kind: '정책', t: pol.n, s: `${pol.o} · ${pol.st}`, img: PTH[pol.id], href: '#/edu/policy' }, e.currentTarget);
  syncSaveBtns(); return el;
}
function translateCard(ctx, instant) {
  const el = agentCard('translate', '말한 경험 → 공고의 말 · 규칙 판정', instant ? 'done' : 'run'); ctx.ws.appendChild(el);
  const pairs = [['"동아리 인스타 2년 했어요"', 'SNS 채널 운영 2년 · 팔로워 3천 → 1.2만', 'ok'], ['"카페 알바 2년"', '고객 응대, 재고 관리, 매장 SNS 사진 촬영', 'part'], ['"공모전 나가서 상 받았어요"', '대학생 마케팅 공모전 장려상 · 팀장', 'ok']];
  $('.agent-b', el).innerHTML = `<div class="inset">${pairs.map((p, i) => `<div class="r in" style="animation-delay:${i * 120}ms;align-items:flex-start"><span class="k" style="display:flex;flex-direction:column;gap:3px"><span class="sub" style="font-size:12px">${esc(p[0])}</span><span>${esc(p[1])}</span></span>${verd(p[2])}</div>`).join('')}</div>
    <div style="display:flex;gap:8px"><a class="btn btn-line" href="#/me/resume">이력서에 넣기</a></div>`;
  return el;
}

/* scenarios */
const SC = {
  compare: {
    reason: (ctx) => [['공고 원문을 불러왔어요'], [`역량 문장 ${ctx.cmp ? ctx.cmp.rows.length : 9}개를 골랐어요`], ['이력서 18문장에서 근거를 찾는 중', () => animateCompare(ctx)], ['규칙으로 맞음, 일부, 없음 판정']],
    agents: ['compare'],
    answer: (ctx) => { const t = cmpTally(ctx); const no = ctx.cmp.rows.filter((r) => r[1] === 'no').map((r) => r[0]); const part = ctx.cmp.rows.filter((r) => r[1] === 'part');
      const best = ctx.cmp.rows.find((r) => r[1] === 'ok');
      return [`요건 ${ctx.cmp.rows.length}문장 중 <b>${t.ok}개는 맞음</b>이에요.${best ? ` 가장 강한 근거는 ${esc(best[2])}예요.` : ''}`,
        t.part ? `<b>일부 ${t.part}개</b>는 행동은 있는데 숫자가 없어요. 수치를 하나씩 알려 주시면 규칙대로 다시 판정할게요.` : '일부로 남은 문장은 없어요.',
        t.no ? `<b class="t-no">없음 ${t.no}개</b>는 ${esc(no.slice(0, 2).join(', '))}${no.length > 2 ? ' 등' : ''}이에요. 왼쪽에서 문장마다 근거와 판정 이유를 확인해 보세요.` : '없음으로 나온 문장은 없어요.'];
    },
  },
  gap: {
    reason: () => [['지난 비교에서 빈칸을 다시 확인했어요'], ['"숏폼 성과 분석"을 다루는 과정 찾는 중'], ['2주 안에 할 수 있는 활동 짜기'], ['함께 받을 수 있는 정책 확인']],
    agents: ['course', 'policy'],
    answer: ['<b class="t-no">숏폼 성과 분석</b>은 2주면 근거를 만들 수 있어요.', '1주차: 릴스 3개를 기획해서 올리고, 도달 · 저장 · 공유 수를 기록해요. 2주차: 가장 잘 된 형식을 한 번 더 바꿔 올리고, 전후 수치를 비교한 한 줄을 이력서에 적어요.', '더 체계적으로 배우고 싶다면 왼쪽의 SeSAC 과정을 보세요. 수치가 생기면 알려 주세요. 판정을 다시 해 드릴게요.'],
  },
  policy: {
    reason: () => [['하늘님 정보 확인: 만 24세 · 서울 · 구직 중'], [`청년 정책 515건에서 신청 가능한 것 고르는 중`], ['일자리, 생활비, 주거 순으로 정리'], ['신청서 초안 작성']],
    agents: ['policy', 'course'],
    answer: ['지금 신청할 수 있는 정책 중 하늘님에게 맞을 수 있는 걸 골랐어요.', '가장 먼저 볼 건 <b>서울형 청년인턴 직무캠프</b>예요. 신청서 초안을 써 뒀으니 확인만 해 주세요. 제출은 하늘님이 직접 해요.', '세부 자격은 정책마다 달라서, 각 정책 페이지에서 한 번 더 확인해 주세요.'],
  },
  translate: {
    reason: () => [['말한 경험 3개를 나눴어요'], ['SNS 콘텐츠 마케팅 공고 46건의 표현과 맞추는 중'], ['규칙 판정: 행동과 수치가 있으면 맞음']],
    agents: ['translate', 'course'],
    answer: ['경험 3개를 공고에서 쓰는 말로 바꿨어요. 동아리 인스타 운영은 수치까지 있어서 <b>맞음</b>이에요.', '카페 알바는 행동은 충분한데 결과 숫자가 없어서 <b>일부</b>예요. 예를 들어 "단골 고객 몇 명", "매장 SNS 팔로워 몇 명" 같은 숫자가 있으면 알려 주세요.'],
  },
};
async function run(ctx, instant) {
  const { c } = ctx; const sc = SC[c.sc];
  const post = findPost(c.q);
  // agents appear as waiting cards first
  const wait0 = [];
  if (!instant) {
    ctx.ws.innerHTML = '';
    sc.agents.forEach((k, i) => { const el = agentCard(k, '곧 시작해요', 'wait'); el.style.animationDelay = i * 90 + 'ms'; ctx.ws.appendChild(el); wait0.push(el); });
    wsCount(ctx);
  }
  const body = addAssistant(ctx);
  ctx.comp.setStop(!instant);
  const drop = () => { wait0.forEach((w) => w.remove()); };
  const make = {
    compare: () => buildCompare(ctx, post, instant),
    course: () => courseCard(ctx, '숏폼 성과 분석', instant),
    policy: () => policyCard(ctx, instant),
    translate: () => translateCard(ctx, instant),
  };
  if (instant) {
    ctx.ws.innerHTML = ''; sc.agents.forEach((k) => make[k]());
    await think(ctx, body, sc.reason(ctx), true);
    for (const h of (typeof sc.answer === 'function' ? sc.answer(ctx) : sc.answer)) await stream(ctx, body, h, true);
    addActions(ctx, body, true); wsCount(ctx); ctx.comp.setStop(false); return;
  }
  // live run
  drop();
  const first = make[sc.agents[0]](); wsCount(ctx);
  const later = sc.agents.slice(1).map((k) => { const el = agentCard(k, '앞 작업이 끝나면 시작해요', 'wait'); ctx.ws.appendChild(el); return [k, el]; });
  wsCount(ctx);
  const ok = await think(ctx, body, sc.reason(ctx), false);
  if (!ok) return;
  if (ctx.cmp) { finishCompare(ctx, false); c.cmpRows = ctx.cmp.rows; } else setState(first, 'done');
  for (const [k, el] of later) {
    if (!alive(ctx)) return;
    setState(el, 'run'); wsCount(ctx); await wait(700); el.remove();
    const real = make[k](); if (k === 'policy') { await wait(500); setState(real, store.get('pending', 1) ? 'check' : 'ok'); } else { await wait(400); setState(real, 'done'); }
    wsCount(ctx);
  }
  await wait(300);
  for (const h of (typeof sc.answer === 'function' ? sc.answer(ctx) : sc.answer)) { if (!(await stream(ctx, body, h, false))) return; await wait(180); }
  addActions(ctx, body, false);
  ctx.comp.setStop(false);
  c.done = true; const all = chats(); const i = all.findIndex((x) => x.id === c.id); if (i >= 0) { all[i] = c; saveChats(all); }
  $('#talk-sub').textContent = '완료 · 지원은 하지 않아요 · 고르는 건 하늘님';
  remember(c.sc === 'policy' ? '구직 기간 정책을 찾아봤어요' : c.sc === 'compare' && ctx.cmp ? (() => { const t = cmpTally(ctx); return `${c.title} · 맞음 ${t.ok} 일부 ${t.part} 없음 ${t.no}`; })() : `"${c.q.slice(0, 20)}" 대화를 했어요`);
}
function addActions(ctx, body, instant) {
  const t = ctx.cmp ? cmpTally(ctx) : { ok: 5, part: 3, no: 1 };
  const noName = ctx.cmp ? (ctx.cmp.rows.find((r) => r[1] === 'no') || [])[0] : '숏폼 콘텐츠 성과 분석';
  const sims = ctx.cmp && ctx.cmp.post ? DATA.posts.filter((x) => x !== ctx.cmp.post && x.ov.some((o) => ctx.cmp.post.ov.includes(o))).length : DATA.posts.length - 1;
  const rec = t.no ? 'edu' : t.part ? 'act' : 'apply';
  const items = [
    ['edu', 'plus', '#E8A33D', '교육으로 채우기', t.no ? `없음 ${t.no}개${noName ? ` · "${noName.slice(0, 18)}${noName.length > 18 ? '…' : ''}"` : ''}를 SeSAC 과정 ${DATA.courses.length}개에서 찾아 채워요` : '더 배우고 싶은 역량을 과정으로 찾아요'],
    ['act', 'cal', '#8B5CF6', '활동으로 채우기', t.part ? `일부 ${t.part}개는 숫자만 있으면 맞음이 돼요 · 2주 활동으로 근거를 만들어요` : '짧은 활동으로 새 근거를 만들어요'],
    ['apply', 'mail', '#191F28', '지원 준비하기', `맞음 ${t.ok}개를 앞세운 이 공고용 이력서와 자소서 초안을 만들어요 · 기본 이력서는 그대로`],
    ['jobs', 'search', '#3182F6', '다른 공고 보기', `비슷한 역량을 찾는 공고 ${sims}건이 있어요`],
  ].sort((a, b) => (b[0] === rec) - (a[0] === rec));
  const box = document.createElement('div'); box.className = 'next'; if (instant) box.style.animation = 'none';
  box.innerHTML = `<span class="sub">다음 단계를 골라 주세요 · 고르는 건 하늘님</span>${items.map(([k, icn, col, title, why]) => `<button type="button" class="next-i${k === rec ? ' rec' : ''}" data-next="${k}">${glass(icn, 40)}<span class="nt"><b>${title}${k === rec ? ' <span class="rec-tag">AI 추천</span>' : ''}</b><small>${esc(why)}</small></span>${ic('chev')}</button>`).join('')}`;
  body.appendChild(box); scrollMsgs(ctx);
  box.onclick = (e) => {
    const b = e.target.closest('[data-next]'); if (!b) return;
    const k = b.dataset.next;
    if (k === 'jobs') return go('#/jobs');
    followUp(ctx, { edu: '교육으로 채우기', act: '활동으로 채우기', apply: '지원 준비하기' }[k]);
  };
}

/* follow-ups */
function intent(v, ctx) {
  if (/^지원 준비하기$/.test(v)) return 'apply';
  if (/^활동으로 채우기$/.test(v)) return 'act';
  if (ctx.c.askedNumbers && /\d/.test(v)) return 'numbers';
  if (/일부|숫자|수치|맞음/.test(v)) return 'ask';
  if (/정책|생활비|지원금|월세|주거/.test(v)) return 'policy';
  if (/과정|교육|숏폼|배우/.test(v)) return 'course';
  return 'other';
}
async function followUp(ctx, v) {
  runToken++; ctx.tok = runToken;
  const kind = intent(v, ctx);
  const c = ctx.c; c.follow = (c.follow || []).concat([{ v, kind }]);
  const all = chats(); const i = all.findIndex((x) => x.id === c.id); if (i >= 0) { all[i] = c; saveChats(all); }
  addUser(ctx, v, false); await answerFollow(ctx, v, kind, false);
}
function replayFollow(ctx, f) { addUser(ctx, f.v, true); answerFollow(ctx, f.v, f.kind, true); }
async function answerFollow(ctx, v, kind, instant) {
  const body = addAssistant(ctx); ctx.comp.setStop(!instant);
  const R = {
    apply: [[['공고 원문에서 제출 서류 찾기'], ['나의 기억에서 쓸 경험 고르기'], ['지원서 준비 · 기본 이력서는 그대로']], ['이 공고용 <b>지원서</b>를 만들었어요. 회사마다 받는 서류가 달라서, 먼저 <b>자소서, 이력서, 포트폴리오 중 무엇을 내는지</b> 골라 주세요.', '고른 서류만 초안을 만들어요. 기본 이력서는 그대로 두고, 모르는 숫자는 지어내지 않고 <b>[숫자 확인 필요]</b>로 남겨요.', '제출은 회사 지원 페이지에서 하늘님이 직접 해요.'], 'app'],
    act: [[['빈칸 "숏폼 성과 분석" 확인'], ['2주 안에 할 수 있는 활동 짜기']], ['2주짜리 활동을 제안해요.', '1주차: 릴스 3개 기획 · 업로드 · 도달과 저장 수 기록', '2주차: 반응 좋은 형식으로 2개 더 · 전후 수치 비교 한 줄 정리. 끝나면 결과를 알려 주세요. 판정을 다시 해 드릴게요.'], null],
    ask: [[['일부 3문장 확인'], ['필요한 숫자 정리']], ['일부 3개는 이렇게 하면 맞음이 돼요.', '캠페인 성과 지표 관리 · 데이터 기반 콘텐츠 개선 · 디자인 툴 활용. 셋 다 <b>결과 숫자</b>가 빠졌어요.', '예를 들어 "캠페인 참여자 320명" 같은 숫자를 하나 알려 주세요. 바로 다시 판정해 드릴게요.'], null],
    numbers: [[['알려 주신 숫자 확인'], ['규칙으로 다시 판정: 행동 + 수치 = 맞음']], ['숫자를 확인했어요. <b>캠페인 성과 지표 관리</b>가 일부에서 <b>맞음</b>으로 바뀌었어요.', (() => { const t = ctx.cmp ? cmpTally(ctx) : { ok: 5, part: 3, no: 1 }; if (t.part) { t.ok++; t.part--; } return `이제 맞음 ${t.ok} · 일부 ${t.part} · 없음 ${t.no}이에요. 이 숫자는 나의 기억에 저장해서 다음 지원서부터 써요.`; })()], 'flip'],
    policy: [[['하늘님 정보로 자격 확인 · 만 24세, 서울, 구직 중'], ['청년 정책 515건에서 신청 가능한 것 고르기'], ['신청서 초안 쓰기']], ['준비하는 동안 받을 수 있는 정책을 왼쪽에 정리했어요. 가장 먼저 볼 건 <b>서울형 청년인턴 직무캠프</b>이고, 신청서 초안도 써 뒀어요.', '주거 쪽은 <b>청년전용 보증부 월세대출</b>(국토교통부, 상시)도 확인해 보세요. 세부 자격은 정책 페이지에서 꼭 다시 확인해 주세요.'], 'mkpolicy'],
    course: [[['없음으로 나온 문장 확인'], [`SeSAC 과정 ${DATA.courses.length}개에서 빈칸을 다루는 과정 찾기`], ['모집 일정과 기간 비교']], ['빈칸을 직접 다루는 과정 3개를 왼쪽에 찾았어요. 첫 번째 <b>SeSAC 양천 AI 콘텐츠 디자인 과정</b>이 숏폼 콘텐츠를 다뤄요.', '과정은 길게는 3개월이 걸려요. 준비하는 동안 받을 수 있는 생활비 정책도 찾아볼까요?'], 'mkcourse'],
    other: [[['질문 이해하기']], ['이 질문은 시연 버전에서 아직 준비되지 않았어요.', '대신 이런 걸 해 볼 수 있어요: 일부 3개를 맞음으로 바꾸기, 빈칸 채우는 활동 짜기, 생활비 정책 찾기.'], null],
  }[kind];
  if (!(await think(ctx, body, R[0], instant))) return;
  for (const h of R[1]) { if (!(await stream(ctx, body, h, instant))) return; if (!instant) await wait(150); }
  if (kind === 'ask') ctx.c.askedNumbers = true;
  if (R[2] === 'flip' && ctx.cmp) {
    const r = ctx.cmp.rows.find((x) => x[1] === 'part'); if (r) { r[1] = 'ok'; r[2] = '"' + v.slice(0, 18) + '"'; }
    ctx.c.cmpRows = ctx.cmp.rows; finishCompare(ctx, instant);
    if (!instant) { ctx.cmp.el.animate([{ background: '#EEF4FF' }, { background: '#fff' }], { duration: 900 }); toast('일부 1개가 맞음으로 바뀌었어요'); remember('캠페인 성과 수치를 알려 줬어요 · 맞음 6'); }
  }
  if (R[2] === 'app') { const ap = createApp(findPost(ctx.c.q)); if (!instant) appCard(ctx, ap); else if (!$('[data-agent="apply"]', ctx.ws)) appCard(ctx, ap); const a = document.createElement('a'); a.className = 'btn btn-dark'; a.href = '#/apply/' + ap.id; a.textContent = `${ap.company} 지원서 열기`; a.style.alignSelf = 'flex-start'; body.appendChild(a); }
  if (R[2] === 'mkcourse') { if (!$('[data-agent="course"]', ctx.ws)) { const el = courseCard(ctx, '숏폼 성과 분석', instant); if (!instant) { el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); await wait(500); setState(el, 'done'); } } wsCount(ctx);
    const row = document.createElement('div'); row.style.cssText = 'display:flex;gap:6px;flex-wrap:wrap'; row.innerHTML = `<button type="button" class="btn btn-line" data-fu="생활비 정책도 찾아 줘">생활비 정책도 찾기</button><a class="btn btn-ghost" href="#/edu?gap=${encodeURIComponent('숏폼 성과 분석')}">과정 더 보기</a>`; body.appendChild(row); row.onclick = (e) => { const b = e.target.closest('[data-fu]'); if (b) followUp(ctx, b.dataset.fu); }; }
  if (R[2] === 'mkpolicy') { if (!$('[data-agent="policy"]', ctx.ws)) { const el = policyCard(ctx, instant); if (!instant) { el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); await wait(500); setState(el, store.get('pending', 1) ? 'check' : 'ok'); } } wsCount(ctx); }
  if (R[2] === 'edu') { const a = document.createElement('a'); a.className = 'btn btn-line'; a.href = '#/edu?gap=' + encodeURIComponent('숏폼 성과 분석'); a.textContent = '과정 보러 가기'; a.style.alignSelf = 'flex-start'; body.appendChild(a); }
  if (PLANS[kind]) addPlan(ctx, body, kind, instant);
  const all = chats(); const i = all.findIndex((x) => x.id === ctx.c.id); if (i >= 0) { all[i] = ctx.c; saveChats(all); }
  ctx.comp.setStop(false); scrollMsgs(ctx);
}

/* ---------- 트렌드 스펙 (real counts from the original site: 104 postings = 2026 59 + 2023~25 45, 팀 수집 2026.10.27) ---------- */
const RANK = [['트렌드 감각, 밈', 64, 1, 'ok'], ['콘텐츠 기획', 63, 1, 'part'], ['데이터, 성과 분석', 49, 5, 'ok'], ['디자인 툴', 44, 1, 'no'], ['영상, 숏폼 제작', 42, -4, 'no'], ['영상 툴 (프리미어 등)', 39, 0, 'no'], ['포트폴리오', 36, -3, 'no'], ['카피라이팅', 29, 3, 'no']];
/* TOP 8 as a leaderboard (mobile): medal, round icon, name + one line, change chip */
const RANK_IC = ['chat', 'docs', 'search', 'folder', 'plus', 'mail', 'cal', 'shield'];
const RANK_BG = ['#EAF1FF', '#F1ECFF', '#E6F6EE', '#FFF1E2', '#FDECEC', '#EEF4FF', '#FFF4E5', '#EAF7F1'];
function medal(n) {
  const c = [['#F7C64A', '#E9A92B', '#E5484D'], ['#D5DAE2', '#AEB6C2', '#3182F6'], ['#E3A06A', '#C27A43', '#E8A33D']][n - 1];
  return `<svg class="medal" viewBox="0 0 28 34" aria-hidden="true" style="fill:initial;stroke:none"><path d="M7 1h5l3 9H10z" fill="${c[2]}"/><path d="M21 1h-5l-3 9h5z" fill="${c[2]}" opacity=".85"/><circle cx="14" cy="21" r="10" fill="${c[1]}"/><circle cx="14" cy="21" r="8" fill="${c[0]}"/><text x="14" y="25" text-anchor="middle" font-size="11" font-weight="700" fill="#fff" font-family="Pretendard,sans-serif">${n}</text></svg>`;
}
function renderTrend() {
  let mine = true;
  mount(`<div class="page trend">
    <div class="page-head"><div class="head-l"><span class="st" style="font-size:12px;color:var(--no-t)"><span class="dot no pulse"></span>LIVE · 2026.10.27 수집</span><h1>트렌드 스펙</h1><span class="sub">SNS 콘텐츠 마케팅 공고가 지금 가장 많이 찾는 역량이에요 · 2026 공고 59건과 2023~25 공고 45건을 비교</span></div>
      <label class="toggle"><input type="checkbox" data-mine checked><span class="sw"></span>내 이력서와 겹쳐 보기</label></div>
    <div class="bento">
      <section class="b-hot card"><div class="hot-top"><span class="eyebrow-l"><span class="dot no pulse"></span>급상승 1위</span><span class="sub" style="font-size:12px">2023~25 → 2026</span></div><div class="hot-rank"><span class="from">8위</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg><span class="to">3위</span><span class="up">▲5</span></div><div class="head-l"><b>데이터, 성과 분석</b><p>3년 사이 가장 많이 오른 역량이에요. 2026 공고 2개 중 1개(49%)가 이 역량을 적었어요.</p></div><div class="hot-me">${verd('ok')}<span>내 이력서 · 팔로워 3천 → 1.2만 (4개월)</span></div></section>
      <section class="b-rank card"><span class="rank-src">SNS 콘텐츠 마케팅 공고 104건 · 2026.10.27</span><div class="sec-h"><h2>공고가 많이 찾는 역량 TOP 8</h2><span class="sub">공고 중 적은 비율 · 순위 변화</span></div><div class="rank-key" data-rkey><span><span class="dot ok"></span>내 이력서 맞음</span><span><span class="dot part"></span>일부</span><span><span class="dot no"></span>없음</span></div><ol class="bars" data-bars></ol><ol class="lb" data-lb></ol></section>
      <section class="b-fact card"><span class="f-k">자격증을 적은 공고</span><span class="f-v">3<small>%</small></span><span class="f-n">104건 중 3건</span><p>자격증보다 <b>해 본 경험</b>을 봐요</p></section>
      <section class="b-fact card"><span class="f-k">외국어를 적은 공고</span><span class="f-v">14<small>%</small></span><span class="f-n">104건 중 15건</span><p>글로벌 채널 공고에서 주로 나와요</p></section>
      <section class="b-fact card accent"><span class="f-k">개인 채널 운영 경험</span><span class="f-v">15<small>%</small></span><span class="f-n">104건 중 16건</span><p>내 계정 운영도 근거가 돼요</p></section>
      <div class="b-facts-m">${[['자격증을 적은 공고', 3, '104건 중 3건', '자격증보다 해 본 경험을 봐요'], ['외국어를 적은 공고', 14, '104건 중 15건', '글로벌 채널 공고에서 주로'], ['개인 채널 운영 경험', 15, '104건 중 16건', '내 계정 운영도 근거가 돼요']].map(([k, v, n, d]) => `<div><span class="f-k">${k}</span><span class="f-v">${v}<small>%</small></span><span class="f-n">${n}</span><p>${d}</p></div>`).join('')}</div>
      <section class="b-slope card"><div class="sec-h"><h2>3년 동안 순위가 이렇게 바뀌었어요</h2><span class="sub">2023~25 → 2026</span></div><div data-slope></div></section>
      <section class="b-cta card"><div class="head-l"><b style="font-size:16px;font-weight:600">내 빈칸은 <span class="t-no">영상, 숏폼 제작</span>이에요</b><span class="sub" style="line-height:1.6">TOP 8 중 5개가 아직 근거 없음이에요. 순위가 높은 것부터 채우면 더 많은 공고와 맞아요.</span></div><div class="sf" aria-hidden="true">
  <div class="sf-phone"><div class="sf-screen"><div class="sf-feed">${['#FF6B6B,#FFB86B', '#6B8BFF,#9F6BFF', '#2EC4A6,#7BE0C3', '#FF6B6B,#FFB86B'].map((g, i) => `<div class="sf-reel" style="background:linear-gradient(160deg,${g})"><span class="sf-cap"><i></i><i></i></span><span class="sf-play"></span></div>`).join('')}</div></div>
    <div class="sf-side"><span class="sf-heart">♥</span><span class="sf-n">1.2만</span><span class="sf-ic"></span><span class="sf-ic"></span></div><div class="sf-prog"><i></i></div></div>
  <div class="sf-edit"><div class="sf-time"><span>00:00</span><span>00:15</span></div>
    <div class="sf-track v">${[34, 22, 28, 16].map((w) => `<i style="flex:${w}"></i>`).join('')}</div>
    <div class="sf-track t">${[18, 30, 20].map((w) => `<i style="flex:${w}"></i>`).join('')}<b style="flex:32"></b></div>
    <div class="sf-track a"><svg viewBox="0 0 200 20" preserveAspectRatio="none"><path d="${Array.from({ length: 50 }, (_, i) => `M${i * 4 + 2} ${10 - (3 + (hashStr('w' + i) % 7))}V${10 + (3 + (hashStr('w' + i) % 7))}`).join('')}"/></svg></div>
    <span class="sf-head"></span>
    <div class="sf-chips"><span>컷 편집</span><span>자막</span><span>캡컷</span><span>3초 훅</span></div></div>
  <span class="sf-pop p1">♥</span><span class="sf-pop p2">♥</span><span class="sf-pop p3">♥</span></div><div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn btn-primary" href="#/edu?gap=${encodeURIComponent('영상, 숏폼 제작')}">빈칸 채울 과정 보기</a><a class="btn btn-line" href="#/jobs">이 역량으로 공고 보기</a></div></section>
    </div>
    <a class="lb-me" href="#/edu?gap=${encodeURIComponent('영상, 숏폼 제작')}"><img src="assets/avatar-haneul.jpg" alt=""><span><small>내 이력서 · TOP 8 중</small><b>맞음 2 · 일부 1</b></span><span class="lb-me-r">빈칸 채우기 ›</span></a>
    <p class="sub" style="font-size:12px;line-height:1.6;margin:0">출처: SNS 콘텐츠 마케팅 공고 104건 (링커리어 64 + 2026 채용 게시판 40) · 팀 수집 2026.10.27 기준. 퍼센트는 해당 단어가 나온 공고 비율이에요. 직무 찾기 목록은 2026 신입, 인턴 46건이에요.</p></div>`);
  const root = $('.pane', view);
  const drawLb = () => {
    const VT = { ok: '맞음', part: '일부', no: '근거 없음' };
    const hot = RANK.reduce((b, r, j) => r[2] > RANK[b][2] ? j : b, 0);
    $('[data-lb]', root).innerHTML = RANK.map(([k, pct, d, v], i) => `<li class="${i === hot ? 'hot' : ''}" style="animation-delay:${i * 50}ms"><span class="lb-rk">${i < 3 ? medal(i + 1) : i + 1}</span><span class="lb-ic" style="background:${RANK_BG[i]}">${glass(RANK_IC[i], 30)}</span><span class="lb-t"><b>${esc(k)}${i === hot ? '<i class="lb-hot">급상승</i>' : ''}</b><small>공고 ${pct}%${mine ? ` · <em class="v-${v}">${VT[v]}</em>` : ''}</small></span><span class="lb-d ${d > 0 ? 'up' : d < 0 ? 'down' : ''}">${d > 0 ? '▲' + d : d < 0 ? '▼' + -d : '–'}</span></li>`).join('');
  };
  const drawBars = () => {
    $('[data-bars]', root).innerHTML = RANK.map(([k, pct, d, v], i) => `<li style="animation-delay:${i * 60}ms"><span class="rk${i < 3 ? ' top' : ''}">${i + 1}</span><div class="bw"><div class="bl"><span>${esc(k)} <em class="bp">${pct}%</em></span>${mine ? `<span class="mv">${verd(v)}</span>` : ''}</div><div class="track"><i style="--w:${pct}%;${mine ? `background:${v === 'ok' ? '#3BB273' : v === 'part' ? '#E8A33D' : '#E5484D'}` : ''}"></i></div></div><span class="pct">${pct}%</span><span class="dl ${d > 0 ? 'up' : d < 0 ? 'down' : ''}">${d > 0 ? '▲' + d : d < 0 ? '▼' + -d : '–'}</span></li>`).join('');
  };
  const drawSlope = () => {
    const W = 560, x1 = 190, x2 = W - 190, top = 34, gap = 24, y = (r) => top + (r - 1) * gap, H = y(11) + 14;
    const lines = RANK.map(([k, , d], i) => { const now2 = i + 1, before = now2 + d; const hot = Math.abs(d) >= 3; const col = !hot ? '#D9D9D6' : d > 0 ? '#E5484D' : '#3182F6'; const nm = esc(k.split(' (')[0]);
      return `<g class="sl${hot ? ' hot' : ''}"><line x1="${x1}" y1="${y(before)}" x2="${x2}" y2="${y(now2)}" stroke="${col}" stroke-width="${hot ? 2 : 1.2}"/><circle cx="${x1}" cy="${y(before)}" r="3.5" fill="${col}"/><circle cx="${x2}" cy="${y(now2)}" r="3.5" fill="${col}"/>
        <text x="${x1 - 12}" y="${y(before) + 4}" text-anchor="end" class="${hot ? 'tb' : ''}"><tspan class="rkn">${before}</tspan>  ${nm}</text><text x="${x2 + 12}" y="${y(now2) + 4}" class="${hot ? 'tb' : ''}"><tspan class="rkn">${now2}</tspan>  ${nm}${hot ? `<tspan class="${d > 0 ? 'up' : 'down'}">  ${d > 0 ? '▲' + d : '▼' + -d}</tspan>` : ''}</text></g>`; }).join('');
    $('[data-slope]', root).innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="slope" role="img" aria-label="2023~25 대비 2026 순위 변화"><text x="${x1}" y="12" text-anchor="middle" class="hd">2023~25</text><text x="${x2}" y="12" text-anchor="middle" class="hd">2026</text>${lines}</svg>`;
  };
  root.addEventListener('change', (e) => { if (e.target.matches('[data-mine]')) { mine = e.target.checked; drawBars(); drawLb(); $('[data-rkey]', root).style.visibility = mine ? '' : 'hidden'; } });
  drawBars(); drawLb(); drawSlope(); markHL();
}

/* ---------- tasks (할 일): AI suggestions saved as a checklist ---------- */
const tasks = () => { const T = store.get('tasks', []); const seen = new Set(); const out = T.filter((t) => { const k = (t.done ? 'd:' : 'o:') + t.t; if (seen.has(k)) return false; seen.add(k); return true; }); if (out.length !== T.length) store.set('tasks', out); return out; };
const saveTasks = (t) => { store.set('tasks', t); if ($('#todo')) renderSide(); };
const addDays = (n) => { const d = now(); d.setDate(d.getDate() + n); return ymd(d); };
const PLANS = {
  act: { title: '숏폼 성과 분석 2주 활동', items: [['릴스 3개 기획하고 올리기', 7, '1주차'], ['게시물마다 도달, 저장 수 기록하기', 7, '1주차'], ['반응 좋은 형식으로 2개 더 올리기', 14, '2주차'], ['전후 수치 비교 한 줄 정리해서 일로에 알려 주기', 14, '2주차']] },
  apply: { title: '지원 준비', items: [['지원서에서 회사가 받는 서류 고르기', 1], ['초안 확인하고 내 말로 고치기', 2], ['회사 지원 페이지에서 직접 제출하기', 3]] },
  course: { title: '빈칸 채울 과정', items: [['SeSAC 양천 AI 콘텐츠 디자인 과정 모집 일정 확인', 3], ['마음에 드는 과정 저장함에 담기', 1]] },
  policy: { title: '구직 기간 정책', items: [['서울형 청년인턴 직무캠프 신청서 초안 확인', 2], ['온통청년에서 직접 신청하기', 3]] },
  ask: { title: '일부 3개를 맞음으로', items: [['캠페인 성과 숫자 찾아보기 (참여자, 도달 등)', 2], ['찾은 숫자를 일로에 알려 주기', 2]] },
};
function addPlan(ctx, body, kind, instant) {
  const P = PLANS[kind]; if (!P) return;
  const key = ctx.c.id + ':' + kind;
  const pick = P.items.map(() => true);
  const box = document.createElement('div'); box.className = 'plan'; if (instant) box.style.animation = 'none';
  const draw = () => {
    const mine = tasks().filter((t) => t.key === key); const saved = mine.length > 0;
    const rows = saved ? mine.map((t) => [t.t, t.due, t.tag, t.done, t.id]) : P.items.map(([t, d, tag], i) => [t, d, tag, pick[i], i]);
    const n = pick.filter(Boolean).length; const left = mine.filter((t) => !t.done).length;
    if (saved) { box.innerHTML = `<div class="plan-h" style="align-items:center">${glass('cal', 32)}<div class="head-l" style="flex:1"><b style="font-size:14px;font-weight:600">할 일 ${mine.length}개를 추가했어요</b><span class="sub">${esc(P.title)} · 할 일에서 체크할 수 있어요</span></div><a class="btn btn-line sm" href="#/tasks">할 일 보기</a></div>`; return; }
    box.innerHTML = `<div class="plan-h">${glass('cal', 32)}<div class="head-l" style="flex:1"><b style="font-size:14px;font-weight:600">${esc(P.title)}</b><span class="sub">${saved ? (left ? `할 일 ${mine.length}개 중 ${mine.length - left}개 끝냈어요 · 눌러서 체크해요` : '모두 끝냈어요 · 결과를 알려 주면 다시 판정해요') : '저장할 단계를 고르세요 · 저장하면 마감 전에 알려 드려요'}</span></div></div>
      <ul class="plan-l">${rows.map(([t, d, tag, on, id]) => `<li><button type="button" class="cb${on ? ' on' : ''}${saved ? ' done-mode' : ''}" data-pi="${id}" role="checkbox" aria-checked="${!!on}" aria-label="${esc(t)}">${on ? ic('check') : ''}</button><span style="flex:1${saved && on ? ';color:var(--faint);text-decoration:line-through' : ''}">${tag ? `<span class="sub">${tag} · </span>` : ''}${esc(t)}</span><span class="sub">${saved ? (on ? '완료' : (dday(d) <= 0 ? '오늘' : 'D-' + dday(d))) : (d === 1 ? '내일' : `${d}일 안에`)}</span></li>`).join('')}</ul>
      <div style="display:flex;gap:6px">${saved ? `<a class="btn btn-line" href="#/tasks">할 일 보기</a>` : `<button type="button" class="btn btn-dark" data-save-plan ${n ? '' : 'disabled'}>${ic('check')}할 일 ${n}개 추가</button><button type="button" class="btn btn-ghost" data-skip-plan>괜찮아요</button>`}</div>`;
  };
  draw(); body.appendChild(box); scrollMsgs(ctx);
  box.onclick = (e) => {
    const cb = e.target.closest('[data-pi]');
    if (cb) {
      const mine = tasks().filter((t) => t.key === key);
      if (mine.length) { const T = tasks(); const t = T.find((x) => x.id === cb.dataset.pi); if (t) { t.done = !t.done; saveTasks(T); if (t.done) remember(`할 일 완료 · ${t.t}`); } }
      else { const k = Number(cb.dataset.pi); pick[k] = !pick[k]; }
      draw(); return;
    }
    if (e.target.closest('[data-skip-plan]')) { box.classList.add('dim'); box.innerHTML = '<span class="sub">저장하지 않았어요 · 필요하면 다시 물어봐 주세요</span>'; return; }
    if (!e.target.closest('[data-save-plan]')) return;
    const T = tasks(); const at = Date.now(); let n = 0;
    P.items.forEach(([t, d, tag], i) => { if (!pick[i] || T.some((x) => !x.done && x.t === t)) return; n++; T.push({ id: 't' + at.toString(36) + i, key, t, tag: tag || '', due: addDays(d), done: false, plan: P.title, chat: ctx.c.id, chatTitle: ctx.c.title }); });
    saveTasks(T); draw(); remember(`"${P.title}" 할 일 ${n}개를 저장했어요`);
    toast(`할 일 ${n}개를 저장했어요`, { label: '보기', run: () => go('#/tasks') });
  };
}
/* ---------- 할 일과 저장: one page — month calendar, day agenda, tasks, saved items ---------- */
function savedDue(id, v) {
  if (id.startsWith('post-')) { const p = DATA.posts.find((x) => postKey(x) === id); return p && p.close ? [p.close, '공고 마감'] : null; }
  if (id.startsWith('edu-')) { const c = DATA.courses.find((x) => x.id === id); return c && c.recEnd ? [c.recEnd.replace(/\./g, '-'), '모집 마감'] : null; }
  if (id.startsWith('pol-')) { const q = DATA.policies.find((x) => x.id === id); if (!q) return null; if (q.end && q.st !== '상시') return [q.end.slice(0, 4) + '-' + q.end.slice(4, 6) + '-' + q.end.slice(6, 8), '신청 마감']; return null; }
  return null;
}
const KCOL = { 할일: '#3182F6', 공고: '#8B5CF6', 교육: '#22A05B', 정책: '#F08A24' };
function renderTasks(focus) {
  let tab = 'open', stab = '전체';
  const T0 = now(); let ym = [T0.getFullYear(), T0.getMonth()]; let sel = ymd(T0);
  mount(`<div class="page plan-page"><div class="page-head"><div class="head-l"><h1>할 일과 저장</h1><span class="sub" data-tsub></span></div></div>
    <div class="pp-top"><section class="card cal" data-cal></section><aside class="card agenda" data-agenda></aside></div>
    <div class="pp-bot"><section class="card pp-col" id="pp-tasks"><div class="sec-h" style="padding:18px 20px 0"><h2>할 일</h2><span class="tabs sm" role="tablist" data-ttabs></span></div>
        <form class="pp-add" data-tadd><span class="cb"></span><input data-tin placeholder="할 일 직접 추가 · 예: 포트폴리오 PDF 만들기" aria-label="할 일 추가"><button type="submit" class="btn btn-dark sm">추가</button></form><div data-tlist></div></section>
      <section class="card pp-col" id="pp-saved"><div class="sec-h" style="padding:18px 20px 0"><h2>저장함</h2><span class="tabs sm" role="tablist" data-stabs></span></div><div data-slist></div></section></div></div>`);
  const root = $('.pane', view); const today = ymd(now());
  const events = () => {
    const E = {};
    const add = (d, e) => { (E[d] = E[d] || []).push(e); };
    tasks().filter((t) => t.due).forEach((t) => add(t.due, { k: '할일', t: t.t, done: t.done, id: t.id, href: t.chat ? '#/chat/' + t.chat : '' }));
    Object.entries(saved()).forEach(([id, v]) => { const d = savedDue(id, v); if (d) add(d[0], { k: v.kind, t: v.t, sub: d[1], href: v.href, sid: id }); });
    return E;
  };
  const evRow = (e) => `<div class="ag-i${e.done ? ' done' : ''}"><span class="ag-dot" style="background:${KCOL[e.k]}"></span><span class="ag-t"><b>${esc(e.t)}</b><small>${e.k === '할일' ? (e.done ? '할 일 · 완료' : '할 일') : esc(e.k + ' · ' + e.sub)}</small></span>${e.href ? `<a class="sub" href="${esc(e.href)}">열기</a>` : ''}</div>`;
  const drawCal = () => {
    const E = events(); const [y, m] = ym; const first = new Date(y, m, 1); const start = new Date(y, m, 1 - first.getDay());
    const cells = Array.from({ length: 42 }, (_, i) => { const d = new Date(start); d.setDate(start.getDate() + i); return d; });
    const used = cells.slice(35).some((d) => d.getMonth() === m) ? 42 : 35;
    $('[data-cal]', root).innerHTML = `<div class="cal-h"><b>${y}년 ${m + 1}월</b><span class="cal-legend">${Object.entries(KCOL).map(([k, c]) => `<span><i style="background:${c}"></i>${k === '할일' ? '할 일' : k}</span>`).join('')}</span><span class="cal-nav"><button type="button" class="icon-btn" data-mv="-1" aria-label="이전 달">‹</button><button type="button" class="btn btn-ghost sm" data-mv="0">오늘</button><button type="button" class="icon-btn" data-mv="1" aria-label="다음 달">›</button></span></div>
      <div class="cal-g">${['일', '월', '화', '수', '목', '금', '토'].map((w) => `<span class="cal-w">${w}</span>`).join('')}${cells.slice(0, used).map((d) => { const k = ymd(new Date(d.getTime() - d.getTimezoneOffset() * 6e4)); const ev = E[k] || []; const out = d.getMonth() !== m;
        return `<button type="button" class="cal-d${out ? ' out' : ''}${k === today ? ' today' : ''}${k === sel ? ' sel' : ''}" data-day="${k}" aria-label="${d.getMonth() + 1}월 ${d.getDate()}일 일정 ${ev.length}개"><span class="n">${d.getDate()}</span>${ev.slice(0, 2).map((e) => `<span class="cal-e${e.done ? ' done' : ''}" style="--c:${KCOL[e.k]}">${esc(e.t)}</span>`).join('')}${ev.length > 2 ? `<span class="cal-more">+${ev.length - 2}</span>` : ''}</button>`; }).join('')}</div>`;
  };
  const drawAgenda = () => {
    const E = events(); const ev = E[sel] || []; const d = new Date(sel + 'T00:00:00');
    const up = Object.entries(E).filter(([k]) => k > sel).sort(([a], [b]) => a.localeCompare(b)).flatMap(([k, xs]) => xs.filter((x) => !x.done).map((x) => [k, x])).slice(0, 4);
    $('[data-agenda]', root).innerHTML = `<div class="head-l"><span class="sub" style="font-size:12px">${sel === today ? '오늘' : (dday(sel) > 0 ? 'D-' + dday(sel) : '지난 날')}</span><b style="font-size:20px;font-weight:600;letter-spacing:-.02em">${d.getMonth() + 1}월 ${d.getDate()}일 ${'일월화수목금토'[d.getDay()]}요일</b></div>
      ${ev.length ? `<div class="ag-l">${ev.map(evRow).join('')}</div>` : '<p class="sub" style="margin:0;font-size:13px">이날은 일정이 없어요</p>'}
      ${up.length ? `<span class="sub" style="font-size:12px;margin-top:6px">다가오는 일정</span><div class="ag-l">${up.map(([k, e]) => evRow({ ...e, sub: (e.sub ? e.sub + ' · ' : '') + k.slice(5).replace('-', '/') })).join('')}</div>` : ''}`;
  };
  const drawTasks = () => {
    const T = tasks(); const open = T.filter((t) => !t.done); const done = T.filter((t) => t.done);
    $('[data-ttabs]', root).innerHTML = `<button type="button" role="tab" aria-selected="${tab === 'open'}" data-tt="open">진행 중 ${open.length}</button><button type="button" role="tab" aria-selected="${tab === 'done'}" data-tt="done">완료 ${done.length}</button>`;
    const L = (tab === 'open' ? open : done).sort((a, b) => (a.due || '9').localeCompare(b.due || '9'));
    $('[data-tlist]', root).innerHTML = L.length ? L.map((t) => `<div class="task${t.done ? ' done' : ''}" data-tid="${t.id}"><button type="button" class="cb${t.done ? ' on' : ''}" data-check aria-label="${t.done ? '완료 취소' : '완료'}">${ic('check')}</button><span class="tt">${esc(t.t)}${t.plan ? `<small class="sub" style="display:block;font-size:12px">${esc(t.plan)}</small>` : ''}</span><span class="due${!t.done && t.due < today ? ' t-no' : ''}">${t.done ? '완료' : t.due === today ? '오늘' : t.due < today ? '지남' : 'D-' + dday(t.due)}</span><button type="button" class="icon-btn" data-tdel aria-label="삭제">${ic('x')}</button></div>`).join('')
      : `<div class="pp-empty">${tab === 'open' ? '할 일이 없어요 · 대화에서 AI가 제안한 단계를 추가하면 여기 모여요' : '아직 완료한 일이 없어요'}</div>`;
  };
  const drawSaved = () => {
    const items = Object.entries(saved());
    $('[data-stabs]', root).innerHTML = ['전체', '공고', '교육', '정책'].map((k) => `<button type="button" role="tab" aria-selected="${stab === k}" data-st="${k}">${k} ${items.filter(([, v]) => k === '전체' || v.kind === k).length}</button>`).join('');
    const L = items.filter(([, v]) => stab === '전체' || v.kind === stab).map(([id, v]) => [id, v, savedDue(id, v)]).sort((a, b) => (a[2] ? a[2][0] : '9').localeCompare(b[2] ? b[2][0] : '9'));
    $('[data-slist]', root).innerHTML = L.length ? L.map(([id, v, d]) => { const n = d ? dday(d[0]) : null;
      return `<div class="sv-i">${v.img ? `<img src="assets/${esc(v.img)}" alt="">` : companyLogo(v.t, '', 40, '8px')}<a class="sv-t" href="${esc(v.href)}"><small><i style="background:${KCOL[v.kind]}"></i>${esc(v.kind)}</small><b>${esc(v.t)}</b></a><span class="due${n !== null && n >= 0 && n <= 3 ? ' t-no' : ''}">${d ? (n < 0 ? '마감' : 'D-' + n) : '상시'}</span>${saveBtn(id)}</div>`; }).join('')
      : `<div class="pp-empty">아직 저장한 ${stab === '전체' ? '항목' : stab}이 없어요</div>`;
    syncSaveBtns();
  };
  const drawAll = () => {
    const T = tasks(); const s = Object.keys(saved()).length;
    $('[data-tsub]', root).textContent = `할 일 ${T.filter((t) => !t.done).length}개 · 저장 ${s}개 · 마감일은 달력에 자동으로 올라가요`;
    drawCal(); drawAgenda(); drawTasks(); drawSaved();
  };
  root.addEventListener('click', (e) => {
    const T_ = e.target;
    const mv = T_.closest('[data-mv]'); if (mv) { const v = Number(mv.dataset.mv); if (!v) { const n = now(); ym = [n.getFullYear(), n.getMonth()]; sel = today; } else { const d = new Date(ym[0], ym[1] + v, 1); ym = [d.getFullYear(), d.getMonth()]; } drawCal(); drawAgenda(); return; }
    const dy = T_.closest('[data-day]'); if (dy) { sel = dy.dataset.day; const d = new Date(sel + 'T00:00:00'); if (d.getMonth() !== ym[1]) ym = [d.getFullYear(), d.getMonth()]; drawCal(); drawAgenda(); return; }
    const tt = T_.closest('[data-tt]'); if (tt) { tab = tt.dataset.tt; drawTasks(); return; }
    const st = T_.closest('[data-st]'); if (st) { stab = st.dataset.st; drawSaved(); return; }
    const sv = T_.closest('[data-save]'); if (sv && sv.closest('#pp-saved')) { const id = sv.dataset.save; toggleSave(id, saved()[id], sv); setTimeout(drawAll, 10); return; }
    const row = T_.closest('[data-tid]'); if (!row) return; const T = tasks(); const k = T.findIndex((t) => t.id === row.dataset.tid); const t = T[k];
    if (T_.closest('[data-check]')) {
      t.done = !t.done; saveTasks(T); row.classList.toggle('done', t.done); row.querySelector('.cb').classList.toggle('on', t.done);
      if (t.done) { remember(`할 일 완료 · ${t.t}`); toast('완료했어요'); }
      setTimeout(drawAll, 420); return;
    }
    if (T_.closest('[data-tdel]')) { T.splice(k, 1); saveTasks(T); drawAll(); toast('할 일을 지웠어요', { label: '되돌리기', run: () => { const T2 = tasks(); T2.splice(k, 0, t); saveTasks(T2); drawAll(); } }); }
  });
  root.addEventListener('submit', (e) => { if (!e.target.matches('[data-tadd]')) return; e.preventDefault(); const inp = $('[data-tin]', root); const v = inp.value.trim(); if (!v) return; const T = tasks(); const due = sel >= today ? sel : addDays(7); T.unshift({ id: 't' + Date.now().toString(36), t: v, due, done: false }); saveTasks(T); inp.value = ''; tab = 'open'; drawAll(); toast(`${due.slice(5).replace('-', '/')} 할 일로 추가했어요`); });
  drawAll();
  if (focus === 'saved') setTimeout(() => $('#pp-saved', root)?.scrollIntoView({ block: 'start', behavior: REDUCE ? 'auto' : 'smooth' }), 60);
}

/* ---------- applications (지원서): one tailored résumé copy + 자소서 per posting; the base résumé is never rewritten ---------- */
const apps = () => store.get('apps', []);
const saveApps = (a) => { store.set('apps', a); updateAppCount(); if ($('#todo')) renderSide(); };
function updateAppCount() { const n = apps().length; const el = $('#app-count'); if (el) el.textContent = n || ''; }
function postKey(p) { return p ? 'post-' + p.url.split('/').pop() : 'post-kakao'; }
function createApp(p) {
  const key = postKey(p); const all = apps(); const ex = all.find((a) => a.key === key); if (ex) return ex;
  const company = p ? p.company : '카카오'; const title = p ? p.title : '브랜드마케팅 인턴'; const type = p ? p.type : '인턴';
  const a = {
    id: 'a-' + Date.now().toString(36), key, company, title, type, close: p ? p.close : '', url: p ? p.url : '', status: '작성 중', created: ymd(now()),
    changes: [
      { sec: '항목 순서', from: '학력 → 인턴, 대외활동', to: '인턴, 대외활동 → 학력', why: '이 공고는 요건 9문장 중 6문장이 실무 경험을 봐요', on: true },
      { sec: '인턴, 대외활동', from: '동아리 공식 인스타그램 운영, 주 3회 콘텐츠 기획과 제작. 팔로워 3천에서 1.2만으로.', to: '동아리 공식 인스타그램 2년 운영 · 주 3회 콘텐츠 기획, 제작 · 팔로워 3천 → 1.2만 (4배)', why: '공고 문장 "SNS 채널 운영 경험"에 맞춰 성과를 앞으로', on: true },
      { sec: '스킬', from: '캔바, 인스타그램 운영, 엑셀', to: '인스타그램 운영, 캔바, 엑셀', why: '공고가 먼저 찾는 역량 순서로', on: true },
      { sec: '희망 직무', from: 'SNS 콘텐츠 마케팅', to: `${company} ${type} · SNS 콘텐츠 마케터`, why: '지원하는 직무 이름과 같게', on: true },
    ],
    essays: [], setup: false,
  };
  all.unshift(a); saveApps(all); remember(`${company} 지원서를 만들었어요 · 기본 이력서는 그대로`); return a;
}
function appCard(ctx, a) {
  const el = document.createElement('article'); el.className = 'card agent'; el.dataset.agent = 'apply';
  el.innerHTML = `<div class="agent-h div">${glass('mail', 40)}<div class="agent-t"><b>${esc(a.company)} 지원서 초안</b><span class="asub">${a.req ? a.req.map((k) => DOCS[k][0]).join(' + ') : '제출 서류를 먼저 골라 주세요'}</span></div><span class="st"><span class="dot part"></span>작성 중</span></div>
    <div class="inset" style="padding:12px 16px"><span style="font-size:13px">회사가 받는 서류를 고르면 그 서류만 초안을 만들어요 · 자소서 / 이력서 / 포트폴리오</span></div>
    <div style="display:flex;gap:8px"><a class="btn btn-dark" href="#/apply/${a.id}">지원서 열기</a><span class="sub" style="align-self:center">제출은 하늘님이 직접 해요</span></div>`;
  ctx.ws.prepend(el); wsCount(ctx); return el;
}
function renderApplyList() {
  const L = apps(); const today = ymd(now());
  mount(`<div class="page"><div class="page-head"><div class="head-l"><h1>지원서</h1><span class="sub">공고마다 따로 고친 이력서와 자기소개서 · 기본 이력서는 그대로 둬요</span></div><a class="btn btn-line" href="#/me/resume">기본 이력서</a></div>
    ${L.length ? `<div class="cards4" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">${L.map((a, i) => { const d = a.close ? dday(a.close) : null; const lg = logoFor(a.company, a.title);
      return `<a class="card mini" href="#/apply/${a.id}" style="text-decoration:none;animation-delay:${i * 40}ms">${companyLogo(a.company, a.title, 48, '10px')}<span class="tx"><span>${esc(a.company)}${a.close ? (a.close < today ? ' · 마감' : ` · D-${d}`) : ''}</span><b>${esc(a.title)}</b><small>${a.req ? a.req.map((k) => DOCS[k][0]).join(' + ') : '제출 서류 고르기 전'}</small></span><span class="st"><span class="dot ${a.status === '제출함' ? 'ok' : 'part'}"></span>${esc(a.status)}</span></a>`; }).join('')}</div>`
      : `<div class="empty card">아직 지원서가 없어요<span class="sub" style="font-size:13px">공고와 비교한 뒤 "지원 준비하기"를 누르거나, 공고 화면에서 바로 만들 수 있어요</span><a class="btn btn-line" href="#/jobs">공고 보러 가기</a></div>`}</div>`);
}
const DOCS = { essay: ['자기소개서', 'chat', '문항별 AI 초안'], resume: ['이력서', 'docs', '이 공고용 복사본'], pf: ['포트폴리오', 'folder', 'PDF나 링크'] };
const PRESETS = [['essay'], ['essay', 'pf'], ['resume', 'pf'], ['resume']];
function guessReq(a) {
  const p = DATA.posts.find((x) => x.url === a.url) || { company: a.company, title: a.title, type: a.type, ov: [] };
  const docs = makeJD(p).docs; const map = { '자기소개서': 'essay', '이력서': 'resume', '포트폴리오': 'pf' };
  return { g: docs.map((d) => map[d]), found: true };
}
/* 자소서 draft bank: picked by what the question asks, cut to the character limit. Facts only from the résumé/memory. */
function draftFor(q, company, limit) {
  const B = [
    [/동기|지원|이유|왜/, [`동아리 공식 인스타그램을 2년 동안 운영하면서, 같은 내용도 어떤 형식으로 보여 주느냐에 따라 반응이 크게 달라진다는 것을 배웠습니다. 매주 반응을 기록하고 다음 기획에 반영한 끝에 팔로워를 3천에서 1.2만으로 늘렸습니다. ${company}에서 이 경험을 실제 브랜드 채널로 넓히고 싶어 지원했습니다.`, `저는 콘텐츠를 만들고 끝내기보다, 반응을 보고 다시 고치는 과정을 좋아합니다. 동아리 인스타그램을 운영하며 팔로워를 4배로 늘린 것도 그 반복 덕분이었습니다. ${company}에서 같은 방식으로 브랜드 채널을 키우고 싶습니다.`], ['공고 · 콘텐츠 기획 및 제작', '경험 · 동아리 인스타 운영']],
    [/성과|경험|사례|해결|도전|수치/, ['동아리 인스타그램 운영진으로 2년 동안 주 3회 콘텐츠를 기획하고 제작했습니다. 처음에는 행사 공지 위주였지만, 저장 수가 높은 정보형 카드뉴스로 형식을 바꾸고 게시 시간을 조정했습니다. 그 결과 팔로워가 3천에서 1.2만으로 늘었고, 캠페인 참여자는 [숫자 확인 필요]명이었습니다.', '숫자로 결과를 확인하는 습관이 가장 큰 성과였습니다. 게시물마다 도달과 저장 수를 기록했고, 반응이 좋은 형식만 남겼습니다. 2년 동안 팔로워는 3천에서 1.2만으로 4배가 되었습니다.'], ['공고 · 캠페인 성과 지표 관리', '경험 · 팔로워 3천 → 1.2만']],
    [/포부|목표|입사 후|계획|성장/, ['입사 후에는 숏폼 콘텐츠의 성과를 데이터로 분석하는 역량을 가장 먼저 키우고 싶습니다. 지금은 카드뉴스 중심의 경험이 있지만, 릴스와 숏폼에서도 같은 방식으로 기록하고 개선하는 마케터가 되겠습니다.', '첫 1년 동안 숏폼 콘텐츠를 직접 기획하고, 도달과 저장 수를 기준으로 성과를 정리하는 일을 맡고 싶습니다. 부족한 숏폼 분석 경험은 지금 SeSAC 과정으로 채우고 있습니다.'], ['빈칸 · 숏폼 콘텐츠 성과 분석']],
    [/협업|갈등|팀|소통/, ['카페에서 2년 동안 일하며 바쁜 시간대에도 동료와 역할을 나누는 법을 배웠습니다. 동아리에서도 운영진 6명이 주제를 나눠 맡고 매주 반응을 함께 보며 다음 콘텐츠를 정했습니다.', '의견이 다를 때는 숫자를 먼저 봤습니다. 동아리 운영진과 게시물 반응을 함께 비교하고, 더 반응이 좋은 쪽으로 정하는 방식으로 갈등을 줄였습니다.'], ['경험 · 카페 알바 2년', '경험 · 운영진 6명 협업']],
    [/장점|강점|단점|성격/, ['제 강점은 기록하고 고치는 습관입니다. 게시물마다 반응을 적어 두고, 다음 기획에서 하나씩 바꿔 봤습니다. 단점은 처음에 완벽하게 하려다 늦어지는 것이라, 지금은 작게 먼저 올리고 고칩니다.', '꾸준함이 강점입니다. 2년 동안 주 3회 게시를 거르지 않았고, 그 기록이 팔로워 4배라는 결과로 이어졌습니다.'], ['경험 · 동아리 인스타 운영']],
  ];
  const hit = B.find(([re]) => re.test(q)) || [null, [`${company}의 이 문항에 맞춰 동아리 인스타그램 운영(팔로워 3천 → 1.2만)과 카페 아르바이트 2년 경험을 근거로 답하겠습니다. [이 문항에 맞는 경험을 한 줄 더 알려 주면 더 정확하게 써요]`], ['나의 기억']];
  const cut = (t) => t.length <= limit ? t : t.slice(0, limit - 1).replace(/\s\S*$/, '') + '…';
  return { drafts: hit[1].map(cut), basis: hit[2] };
}
function parseQs(text) {
  const parts = text.split(/\n+|(?=\b\d+\s*[.)]\s)|(?=\[\s*\d+\s*\])|(?=문항\s*\d)/).map((x) => x.trim()).filter((x) => x.length > 2);
  return parts.map((x) => {
    const m = x.match(/(\d{2,4})\s*자/) || x.match(/(\d{2,4})\s*(?:byte|bytes|바이트)/i);
    const q = x.replace(/^\s*(\d+\s*[.)]|\[\s*\d+\s*\]|문항\s*\d+\s*[.:)]?)\s*/, '').replace(/[(\[]?\s*(최대|공백 ?포함|공백 ?제외)?\s*\d{2,4}\s*(자|byte|bytes|바이트)\s*(이내|내외|이하)?\s*[)\]]?/gi, '').replace(/\s{2,}/g, ' ').trim();
    return { q: q || x, limit: m ? Number(m[1]) : 500 };
  });
}
function renderApply(id) {
  const all = apps(); const a = all.find((x) => x.id === id); if (!a) { go('#/apply'); return; }
  const persist = () => { const L = apps(); const i = L.findIndex((x) => x.id === a.id); if (i >= 0) { L[i] = a; saveApps(L); } };
  const today = ymd(now());
  const head = `<div class="page-head"><div class="head-l"><span class="sub"><a href="#/apply" style="text-decoration:none">지원서</a> / ${esc(a.company)}</span><h1>${esc(a.company)} · ${esc(a.title)}</h1><span class="sub">${a.close ? (a.close < today ? '마감된 공고 · 연습용으로 써요' : `마감 ${a.close.replace(/-/g, '.')} · D-${dday(a.close)}`) : '마감일 확인 필요'}</span></div>
      ${a.req ? `<label class="field" style="width:160px"><span>진행 상태</span><select data-status>${['작성 중', '제출함', '결과 기다리는 중'].map((s2) => `<option${a.status === s2 ? ' selected' : ''}>${s2}</option>`).join('')}</select></label>` : ''}</div>`;
  if (!a.req) {
    const gs = guessReq(a); let pick = gs.found ? gs.g.slice() : [];
    mount(`<div class="page">${head}
      <section class="card sec doc-sec"><div class="sec-h"><h2>어떤 서류를 내나요?</h2></div>
        ${gs.found ? `<div class="banner card" style="background:var(--blue-bg);border-color:#D6E4FF"><span class="ai-tag">AI</span><span>공고에서 <b style="font-weight:600">${gs.g.map((k) => DOCS[k][0]).join(' + ')}</b>를 찾았어요</span></div>` : `<div class="banner card"><span class="ai-tag">AI</span><span class="sub" style="font-size:13px">공고에 제출 서류가 없어요 · 직접 골라 주세요</span></div>`}
        <div class="doc-pick">${Object.entries(DOCS).map(([k, [n, g, d]]) => `<button type="button" class="doc-opt" data-doc="${k}" aria-pressed="false">${glass(g, 40)}<span class="nt"><b>${n}</b><small>${d}</small></span><span class="tick">${ic('check')}</span></button>`).join('')}</div>
        <div style="display:flex;gap:8px;align-items:center"><span class="sub" data-pick-sum></span><span style="flex:1"></span>${a.url ? `<a class="btn btn-line" href="${esc(a.url)}" target="_blank" rel="noopener">공고 원문 ${ic('ext')}</a>` : ''}<button type="button" class="btn btn-primary" data-go disabled>이 서류로 시작하기</button></div></section></div>`);
    const root = $('.pane', view);
    const sync = () => { $$('[data-doc]', root).forEach((b) => b.setAttribute('aria-pressed', pick.includes(b.dataset.doc))); $$('[data-preset]', root).forEach((b) => b.setAttribute('aria-pressed', b.dataset.preset === pick.slice().sort((x, y) => Object.keys(DOCS).indexOf(x) - Object.keys(DOCS).indexOf(y)).join(','))); $('[data-go]', root).disabled = !pick.length; $('[data-pick-sum]', root).textContent = pick.length ? `${pick.length}개 선택` : '하나 이상 골라 주세요'; };
    root.addEventListener('click', (e) => {
      const pr = e.target.closest('[data-preset]'); if (pr) { pick = pr.dataset.preset.split(','); sync(); return; }
      const d = e.target.closest('[data-doc]'); if (d) { const k = d.dataset.doc; pick = pick.includes(k) ? pick.filter((x) => x !== k) : pick.concat(k); sync(); return; }
      if (e.target.closest('[data-go]')) { a.req = Object.keys(DOCS).filter((k) => pick.includes(k)); persist(); remember(`${a.company}는 ${a.req.map((k) => DOCS[k][0]).join(' + ')}를 받아요`); a.setup = !(a.req.includes('essay') || a.req.includes('pf')); persist(); renderApply(id); }
    });
    sync(); return;
  }
  if (!a.pf) a.pf = { link: '', picks: [{ t: '동아리 인스타그램 카드뉴스 3편', why: '공고 문장 "SNS 채널 운영 경험" · 팔로워 3천 → 1.2만 수치와 함께', on: true }, { t: '마케팅 공모전 기획서 (장려상)', why: '공고 문장 "콘텐츠 기획" · 팀장 역할을 첫 장에', on: true }, { t: '카페 매장 SNS 사진 모음', why: '디자인 툴 역량이 약해서, 넣을지는 직접 정해 주세요', on: false }] };
  if (a.setup === undefined) a.setup = (a.essays || []).length > 0;
  if (!a.pf.fmt) a.pf.fmt = 'pdf';
  if (!a.setup) {
    const needE = a.req.includes('essay'), needP = a.req.includes('pf');
    let Q = (a.essays || []).map((e) => ({ q: e.q, limit: e.limit }));
    mount(`<div class="page">${head}
      <div class="steps2"><span class="done">1 서류 고르기</span><span class="cur">2 회사 요건 넣기</span><span>3 초안 다듬기</span></div>
      <div class="setup-grid${needE && needP ? '' : ' one'}">
      ${needE ? `<section class="card sec"><div class="sec-h"><h2>자기소개서 문항</h2><span class="sub" data-qn></span></div>
        <form class="nl-box" data-nl><textarea data-nlin rows="3" placeholder="지원 페이지의 문항을 그대로 붙여 넣거나 말로 적어 주세요&#10;예: 1. 지원 동기 500자  2. 가장 큰 성과 700자 이내  3. 입사 후 포부 500자"></textarea><div class="nl-f"><span class="ai-tag">AI</span><span class="sub" style="flex:1;font-size:12px">문항과 글자 수를 나눠서 정리해요</span><button type="submit" class="btn btn-dark sm">문항 정리하기</button></div></form>
        <div class="qrows" data-qrows></div><button type="button" class="btn btn-ghost sm" data-qadd style="align-self:flex-start">+ 직접 추가</button></section>` : ''}
      ${needP ? `<section class="card sec"><div class="sec-h"><h2>포트폴리오 형식</h2><span class="sub">회사가 받는 형식</span></div>
        <div class="fmt">${[['pdf', 'PDF 파일', '대부분 이 형식이에요'], ['link', '링크', '노션, 비핸스 등'], ['both', '둘 다 받아요', 'PDF와 링크 함께']].map(([k, t, d]) => `<button type="button" class="fmt-o" data-fmt="${k}" aria-pressed="${a.pf.fmt === k}"><b>${t}</b><small>${d}</small></button>`).join('')}</div>
        <label class="field" data-mbf><span>PDF 용량 제한</span><span class="mb"><input type="number" min="1" max="100" data-mb value="${a.pf.mb || 20}">MB</span></label></section>` : ''}
      </div>
      <div class="setup-f"><button type="button" class="btn btn-ghost" data-back>서류 다시 고르기</button><span style="flex:1"></span><span class="sub" data-hint></span><button type="button" class="btn btn-primary" data-build>초안 만들기</button></div></div>`);
    const root = $('.pane', view);
    const drawQ = () => { if (!needE) return;
      $('[data-qrows]', root).innerHTML = Q.length ? Q.map((x, i) => `<div class="qrow" style="animation-delay:${i * 50}ms"><span class="qn">${i + 1}</span><input data-qq="${i}" value="${esc(x.q)}" aria-label="문항 ${i + 1}"><span class="lim"><input type="number" min="50" max="3000" step="50" data-ql="${i}" value="${x.limit}" aria-label="글자 수">자</span><button type="button" class="icon-btn" data-qx="${i}" aria-label="문항 삭제">${ic('x')}</button></div>`).join('') : '<div class="pp-empty" style="padding:16px">아직 문항이 없어요 · 위에 붙여 넣거나 직접 추가해 주세요</div>';
      $('[data-qn]', root).textContent = Q.length ? `${Q.length}개 문항 · 글자 수 ${Q.reduce((n, x) => n + Number(x.limit || 0), 0).toLocaleString()}자` : '';
      sync(); };
    const sync = () => { const ok = !needE || Q.some((x) => x.q.trim()); $('[data-build]', root).disabled = !ok; $('[data-hint]', root).textContent = ok ? '' : '문항을 하나 이상 넣어 주세요';
      const mbf = $('[data-mbf]', root); if (mbf) mbf.hidden = a.pf.fmt === 'link'; };
    root.addEventListener('submit', async (e) => { if (!e.target.matches('[data-nl]')) return; e.preventDefault(); const ta = $('[data-nlin]', root); const v = ta.value.trim(); if (!v) return;
      const btn = $('[type=submit]', e.target); btn.disabled = true; btn.textContent = '정리하는 중…'; await wait(REDUCE ? 0 : 650);
      const got = parseQs(v); Q = Q.concat(got); ta.value = ''; btn.disabled = false; btn.textContent = '문항 정리하기'; drawQ(); toast(`문항 ${got.length}개를 정리했어요 · 글자 수가 없으면 500자로 넣었어요`); });
    root.addEventListener('input', (e) => { const q = e.target.dataset.qq, l = e.target.dataset.ql; if (q !== undefined) Q[q].q = e.target.value; if (l !== undefined) Q[l].limit = Number(e.target.value) || 500; if (e.target.matches('[data-mb]')) a.pf.mb = Number(e.target.value) || 20; if (q !== undefined || l !== undefined) { $('[data-qn]', root).textContent = `${Q.length}개 문항 · 글자 수 ${Q.reduce((n, x) => n + Number(x.limit || 0), 0).toLocaleString()}자`; sync(); } });
    root.addEventListener('click', (e) => { const T = e.target;
      const x = T.closest('[data-qx]'); if (x) { Q.splice(Number(x.dataset.qx), 1); drawQ(); return; }
      if (T.closest('[data-qadd]')) { Q.push({ q: '', limit: 500 }); drawQ(); $$('[data-qq]', root).pop().focus(); return; }
      const f = T.closest('[data-fmt]'); if (f) { a.pf.fmt = f.dataset.fmt; $$('[data-fmt]', root).forEach((b) => b.setAttribute('aria-pressed', b === f)); sync(); return; }
      if (T.closest('[data-back]')) { a.req = null; persist(); renderApply(id); return; }
      if (T.closest('[data-build]')) {
        if (needE) a.essays = Q.filter((x) => x.q.trim()).map((x) => { const d = draftFor(x.q, a.company, x.limit); return { q: x.q.trim(), limit: x.limit, basis: d.basis, drafts: d.drafts, text: '', v: 0 }; });
        a.setup = true; a.fresh = true; persist(); remember(`${a.company} 자소서 ${needE ? a.essays.length + '문항' : ''}${needP ? ' · 포트폴리오 ' + { pdf: 'PDF', link: '링크', both: 'PDF와 링크' }[a.pf.fmt] : ''}`); renderApply(id); }
    });
    drawQ(); return;
  }
  let qi = 0;
  const sections = a.req.map((k) => `<section class="card sec" data-sec="${k}"></section>`).join('');
  mount(`<div class="page">${head}
    <div class="card req-bar"><span class="sub">이 회사가 받는 서류</span>${a.req.map((k) => `<span class="chip">${glass(DOCS[k][1], 22)}${DOCS[k][0]}</span>`).join('')}<span style="flex:1"></span><button type="button" class="btn btn-ghost" data-rereq>서류 바꾸기</button></div>
    <div class="apply-grid${a.req.length === 1 ? ' one' : ''}">${sections}</div>
    <div class="card" style="padding:16px 20px;display:flex;align-items:center;gap:12px"><span class="dot ${a.status === '제출함' ? 'ok' : 'part'}" data-stdot></span><span style="font-size:13px;flex:1">일로는 대신 지원하지 않아요. 내용을 확인한 뒤 회사 지원 페이지에서 직접 제출해 주세요.</span>${a.url ? `<a class="btn btn-line" href="${esc(a.url)}" target="_blank" rel="noopener">공고 원문 ${ic('ext')}</a>` : ''}<button type="button" class="btn btn-primary" data-submitted>${a.status === '제출함' ? '제출 완료로 표시됨' : '제출했어요'}</button></div></div>`);
  const root = $('.pane', view);
  const S = (k) => $(`[data-sec="${k}"]`, root);
  const drawResume = () => { const el = S('resume'); if (!el) return;
    el.innerHTML = `<div class="sec-h"><h2>이 공고용 이력서</h2><span class="ai-tag">AI가 고침</span><a class="sub" href="#/me/resume">기본 이력서 보기 →</a></div><p class="sub" style="font-size:13px;line-height:1.6;margin:0">기본 이력서에 있는 사실만 쓰고, 순서와 표현만 이 공고에 맞췄어요. 끄면 원래대로 돌아가요.</p>
      ${a.changes.map((c, i) => `<div class="inset" style="padding:14px 16px;gap:8px${c.on ? '' : ';opacity:.6'}"><div style="display:flex;align-items:center;gap:8px"><b style="font-size:13px;font-weight:600;flex:1">${esc(c.sec)}</b><button type="button" class="chipbtn" data-ch="${i}" aria-pressed="${c.on}">${c.on ? '적용함' : '원래대로'}</button></div><span style="font-size:13px;color:var(--faint);text-decoration:line-through">${esc(c.from)}</span><span style="font-size:14px">${esc(c.to)}</span><span class="sub" style="font-size:12px">${esc(c.why)}</span></div>`).join('')}
      <button type="button" class="btn btn-line" data-pdf style="align-self:flex-start">이 공고용 이력서 PDF</button>`; };
  const drawPf = () => { const el = S('pf'); if (!el) return;
    el.innerHTML = `<div class="sec-h"><h2>포트폴리오</h2><span class="ai-tag">AI 추천</span><span class="sub">${{ pdf: `PDF · ${a.pf.mb || 20}MB까지`, link: '링크로 내요', both: 'PDF와 링크' }[a.pf.fmt || 'both']}</span></div>
      ${a.pf.fmt === 'link' ? '' : `<div class="drop" data-drop>${glass('folder', 40)}<span><b style="font-size:14px;font-weight:600">${a.pf.file ? esc(a.pf.file) : 'PDF를 끌어다 놓거나 눌러서 고르세요'}</b><small class="sub" style="display:block">${a.pf.file ? '올렸어요 · 다시 누르면 바꿀 수 있어요' : `PDF · ${a.pf.mb || 20}MB까지 · 시연에서는 파일 이름만 저장해요`}</small></span><input type="file" accept="application/pdf" data-file hidden></div>`}
      ${a.pf.fmt === 'pdf' ? '' : `<label class="field"><span>${a.pf.fmt === 'link' ? '포트폴리오 링크' : '링크'}</span><input data-pflink placeholder="notion.so/… 또는 behance.net/…" value="${esc(a.pf.link)}"></label>`}
      <span class="sub">이 공고에 넣으면 좋은 작업물 · 나의 기억에서 골랐어요</span>
      ${a.pf.picks.map((p, i) => `<div class="inset" style="padding:12px 14px;flex-direction:row;align-items:center;gap:10px;${p.on ? '' : 'opacity:.65'}"><span style="flex:1;display:flex;flex-direction:column;gap:2px"><b style="font-size:13px;font-weight:600">${esc(p.t)}</b><span class="sub" style="font-size:12px">${esc(p.why)}</span></span><button type="button" class="chipbtn" data-pk="${i}" aria-pressed="${p.on}">${p.on ? '넣기' : '빼기'}</button></div>`).join('')}`; };
  const drawEssay = () => { const el = S('essay'); if (!el) return;
    const e = a.essays[qi];
    el.innerHTML = `<div class="sec-h"><h2>자기소개서</h2><span class="ai-tag">AI 초안</span><span class="sub">${a.essays.length}개 문항 · <button type="button" class="linkbtn" data-resetup>문항 다시 넣기</button></span></div>
      <div class="tabs" role="tablist">${a.essays.map((x, i) => `<button type="button" role="tab" aria-selected="${qi === i}" data-q="${i}">문항 ${i + 1}</button>`).join('')}<button type="button" data-addq style="color:var(--blue-d)">+ 문항 추가</button></div>
      <div style="display:flex;align-items:flex-start;gap:8px"><b style="font-size:15px;font-weight:600;flex:1;line-height:1.5" data-qtext>${esc(e.q)}</b><button type="button" class="btn btn-ghost" data-editq>문항 바꾸기</button>${a.essays.length > 1 ? '<button type="button" class="btn btn-ghost" data-delq>삭제</button>' : ''}</div>
      <div class="tagrow">${e.basis.map((b) => `<span class="tag" style="height:26px;font-size:12px">근거 · ${esc(b)}</span>`).join('')}</div>
      <label class="field"><span class="sr">답변</span><textarea data-ans maxlength="${e.limit}" style="min-height:220px">${esc(e.text)}</textarea></label>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><span class="sub" data-cnt></span>${/\[숫자 확인 필요\]/.test(e.text) ? '<span class="st" style="font-size:12px"><span class="dot part"></span>모르는 숫자는 지어내지 않고 남겨 뒀어요</span>' : ''}<span style="flex:1"></span><button type="button" class="btn btn-soft" data-tone>짧게</button><button type="button" class="btn btn-soft" data-rewrite>다시 쓰기</button><button type="button" class="btn btn-line" data-copy>복사</button></div>`;
    cnt(); };
  const cnt = () => { const e = a.essays[qi]; const ta = $('[data-ans]', root); if (ta) $('[data-cnt]', root).textContent = `${ta.value.length} / ${e.limit}자`; };
  let typing = 0;
  const typeInto = async (text) => { const my = ++typing; const ta = $('[data-ans]', root); ta.value = '';
    for (let i = 0; i <= text.length; i += 2) { if (my !== typing) return; ta.value = text.slice(0, i); cnt(); await wait(10); }
    a.essays[qi].text = text; persist(); drawEssay(); };
  root.addEventListener('click', (e) => {
    const T = e.target;
    if (T.closest('[data-rereq]')) { a.req = null; persist(); renderApply(id); return; }
    if (T.closest('[data-resetup]')) { a.setup = false; persist(); renderApply(id); return; }
    const ch = T.closest('[data-ch]'); if (ch) { const c = a.changes[ch.dataset.ch]; c.on = !c.on; persist(); drawResume(); toast(c.on ? '이 공고용 이력서에 적용했어요' : '원래 문장으로 돌렸어요 · 기본 이력서는 그대로예요'); return; }
    const pk = T.closest('[data-pk]'); if (pk) { const p = a.pf.picks[pk.dataset.pk]; p.on = !p.on; persist(); drawPf(); return; }
    if (T.closest('[data-drop]')) { $('[data-file]', root).click(); return; }
    const q = T.closest('[data-q]'); if (q) { typing++; qi = Number(q.dataset.q); drawEssay(); return; }
    if (T.closest('[data-addq]')) { a.essays.push({ q: '회사 문항을 붙여 넣어 주세요', limit: 500, basis: ['나의 기억'], drafts: draftFor('', a.company, 500).drafts, text: '', v: 0 }); qi = a.essays.length - 1; persist(); drawEssay(); $('[data-editq]', root).click(); return; }
    if (T.closest('[data-delq]')) { const gone = a.essays.splice(qi, 1)[0]; const at = qi; qi = Math.max(0, qi - 1); persist(); drawEssay(); toast('문항을 지웠어요', { label: '되돌리기', run: () => { a.essays.splice(at, 0, gone); qi = at; persist(); drawEssay(); } }); return; }
    if (T.closest('[data-rewrite]')) { const ex = a.essays[qi]; ex.v = (ex.v + 1) % ex.drafts.length; typeInto(ex.drafts[ex.v]); return; }
    if (T.closest('[data-tone]')) { const s2 = a.essays[qi].text.split(/(?<=[.다])\s+/).slice(0, 2).join(' '); typeInto(s2); toast('두 문장으로 줄였어요'); return; }
    if (T.closest('[data-copy]')) { const v = $('[data-ans]', root).value; (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(() => toast('복사했어요 · 회사 지원 페이지에 붙여 넣어 주세요'), () => toast('복사하지 못했어요 · 직접 선택해 주세요')); return; }
    if (T.closest('[data-editq]')) { const el = $('[data-qtext]', root); const inp = document.createElement('textarea'); inp.className = 'qedit'; inp.value = a.essays[qi].q; el.replaceWith(inp); inp.focus(); inp.select();
      const fin = () => { const v = inp.value.trim(); if (v) { const d = draftFor(v, a.company, a.essays[qi].limit); Object.assign(a.essays[qi], { q: v, drafts: d.drafts, basis: d.basis, v: 0 }); persist(); toast('문항을 바꿨어요 · "다시 쓰기"를 누르면 새 문항에 맞춰 써요'); } drawEssay(); };
      inp.onkeydown = (ev) => { if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); fin(); } if (ev.key === 'Escape') drawEssay(); }; inp.onblur = fin; return; }
    if (T.closest('[data-pdf]')) { toast('이 공고용 이력서 PDF를 만들었어요 (시연에서는 내려받기 없이 보여만 줘요)'); return; }
    if (T.closest('[data-submitted]')) { a.status = '제출함'; persist(); $('[data-status]', root).value = '제출함'; T.closest('[data-submitted]').textContent = '제출 완료로 표시됨'; $('[data-stdot]', root).className = 'dot ok'; toast('제출함으로 표시했어요 · 결과는 예측하지 않아요'); remember(`${a.company} 지원서를 제출했다고 표시했어요`); }
  });
  root.addEventListener('input', (e) => { if (e.target.matches('[data-ans]')) { typing++; a.essays[qi].text = e.target.value; persist(); cnt(); } if (e.target.matches('[data-pflink]')) { a.pf.link = e.target.value; persist(); } });
  root.addEventListener('change', (e) => { if (e.target.matches('[data-file]') && e.target.files[0]) { a.pf.file = e.target.files[0].name; persist(); drawPf(); toast('포트폴리오 PDF를 올렸어요'); } });
  root.addEventListener('dragover', (e) => { if (e.target.closest('[data-drop]')) { e.preventDefault(); e.target.closest('[data-drop]').classList.add('over'); } });
  root.addEventListener('drop', (e) => { const d = e.target.closest('[data-drop]'); if (!d) return; e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) { a.pf.file = f.name; persist(); drawPf(); toast('포트폴리오 PDF를 올렸어요'); } });
  const stSel = $('[data-status]', root); if (stSel) stSel.addEventListener('change', (e) => { a.status = e.target.value; persist(); $('[data-stdot]', root).className = 'dot ' + (a.status === '제출함' ? 'ok' : 'part'); toast(`상태를 "${a.status}"로 바꿨어요`); });
  drawResume(); drawPf(); drawEssay();
  if (a.fresh && a.essays.length) { a.fresh = false; a.essays.forEach((x, i) => { if (i) x.text = x.drafts[0]; }); persist(); toast(`문항 ${a.essays.length}개에 맞춰 초안을 쓰고 있어요`); typeInto(a.essays[0].drafts[0]); } else if (a.fresh) { a.fresh = false; persist(); }
}
/* ---------- drawer ---------- */
function openDrawer(html, onMount) {
  closeDrawer(true);
  const root = $('#drawer-root');
  root.innerHTML = `<div class="scrim" data-close></div><aside class="drawer" role="dialog" aria-modal="true">${html}</aside>`;
  const dr = $('.drawer', root); root.onclick = (e) => { if (e.target.closest('[data-close]')) closeDrawer(); };
  document.addEventListener('keydown', escClose);
  setTimeout(() => { const f = $('button, a, input, textarea, select', dr); if (f) f.focus(); }, 50);
  if (onMount) onMount(dr); syncSaveBtns();
}
function escClose(e) { if (e.key === 'Escape') closeDrawer(); }
function closeDrawer(now) {
  const root = $('#drawer-root'); document.removeEventListener('keydown', escClose);
  if (!root.firstChild) return;
  if (now) { root.innerHTML = ''; return; }
  $$('.drawer, .scrim', root).forEach((x) => x.classList.add('out')); setTimeout(() => { root.innerHTML = ''; }, 200);
}
const drHead = (kicker, title) => `<div class="dr-h"><div style="flex:1;display:flex;flex-direction:column;gap:6px"><span class="sub">${kicker}</span><h2>${esc(title)}</h2></div><button type="button" class="icon-btn" data-close aria-label="닫기">${ic('x')}</button></div>`;
function openDraft(pol, card, ctx) {
  openDrawer(`${drHead('정책 신청서 초안 · <span class="ai-tag">AI가 씀</span>', pol.n)}
    <div class="dr-b"><div class="kv"><div><span>운영 기관</span><span>${esc(pol.o)}</span></div><div><span>신청 상태</span><span>${esc(pol.st)} · ${esc(pol.per)}</span></div><div><span>이름</span><span>김하늘</span></div><div><span>거주지</span><span>서울 관악구</span></div><div><span>상태</span><span>구직 중 · 미취업</span></div></div>
    <label class="field"><span>신청 동기 (고칠 수 있어요)</span><textarea>SNS 콘텐츠 마케터를 준비하고 있습니다. 동아리 공식 인스타그램을 2년 동안 운영하며 팔로워를 3천에서 1.2만으로 늘렸고, 직무캠프에서 숏폼 성과 분석 경험을 더하고 싶습니다.</textarea></label>
    <p class="sub" style="font-size:12px;line-height:1.6">일로는 대신 제출하지 않아요. 내용을 확인한 뒤 온통청년에서 직접 신청해 주세요. 세부 자격은 공고에서 다시 확인이 필요해요.</p></div>
    <div class="dr-f"><a class="btn btn-line" href="${esc(pol.u)}" target="_blank" rel="noopener">온통청년에서 신청하기 ${ic('ext')}</a><span style="flex:1"></span><button type="button" class="btn btn-dark" data-confirm>확인 완료</button></div>`, (dr) => {
    $('[data-confirm]', dr).onclick = () => {
      store.set('pending', 0); closeDrawer(); if (card) setState(card, 'ok'); if (ctx) wsCount(ctx);
      toast('초안을 확인했어요 · 제출은 온통청년에서 직접 해 주세요'); renderSide(); remember(`${pol.n} 초안을 확인했어요`);
    };
  });
}
const FIT = (t) => /숏폼/.test(t) ? 'no' : /포토샵|프리미어|일러스트|피그마|영상 ?편집|디자인 ?툴|애프터|캡컷|포르투갈|능통|외국어|원어민/.test(t) ? 'no' : /분석|데이터|지표|성과|리서치|GA|광고 운영|퍼포먼스/.test(t) ? 'part' : /SNS|인스타|소셜|콘텐츠|기획|커뮤니케이션|협업|채널|트렌드|마케팅/.test(t) ? 'ok' : null;
const OVFIT = { '콘텐츠 기획': 'ok', '데이터, 성과 분석': 'part', '디자인 툴': 'no' };
function postBody(p) {
  const J = makeJD(p);
  return `<p style="margin:0;font-size:14px">${esc(J.intro)}</p><div class="req">${J.secs.map(([h, lines]) => `<h3>${esc(h)}</h3>${lines.map((t) => { const v = ['담당 업무', '자격 요건', '우대 사항'].includes(h) ? (FIT(t) || 'no') : null; return `<div class="ln"><span>${esc(t)}</span>${v ? verd(v === 'ok' && !/\d/.test(evidence(t, v)) ? 'part' : v) : ''}</div>`; }).join('')}`).join('')}</div><p class="sub" style="margin:0;font-size:12px">시연용 예시 공고 내용이에요 · 실제 내용은 원문에서 확인해 주세요</p>`;
}
function openPost(p) {
  const today = ymd(now()); const closed = p.close < today; const key = postKey(p);
  const sims = DATA.posts.filter((x) => x !== p && x.ov.some((o) => p.ov.includes(o))).sort((a, b) => ((a.close < today) - (b.close < today)) || a.close.localeCompare(b.close)).slice(0, 3);
  const weak = p.ov.find((o) => OVFIT[o] === 'no') ? '디자인' : p.ov.find((o) => OVFIT[o] === 'part') ? '데이터' : null;
  const course = weak && DATA.courses.find((c) => c.g === weak && (c.st === '모집 중' || c.st === '모집 예정'));
  const hasText = true;
  openDrawer(`${drHead(`${esc(p.company)} · ${esc(p.size)} · ${esc(p.type)}`, p.title)}
    <div class="dr-b">
      <div class="trio"><div><span>마감</span><span class="big" style="font-size:22px${!closed && dday(p.close) <= 3 ? ';color:var(--no-t)' : ''}">${closed ? '마감' : 'D-' + dday(p.close)}</span></div><div><span>구분</span><span class="big" style="font-size:22px">${esc(p.type)}</span></div><div><span>회사 규모</span><span class="big" style="font-size:22px">${esc(p.size)}</span></div></div>
      <div class="chips">${p.ov.map((o) => `<span class="chip">${OVFIT[o] ? `<span class="dot ${VERD[OVFIT[o]][0]}" style="width:6px;height:6px"></span>` : ''}${esc(o)}</span>`).join('')}</div>
      <div class="card" style="padding:14px 16px;display:flex;flex-direction:column;gap:6px;background:var(--sunk);border:0"><span style="font-size:13px;font-weight:600">${hasText ? '공고 문장마다 내 이력서와 미리 맞춰 봤어요' : '요구 역량을 내 이력서와 미리 맞춰 봤어요'} <span class="ai-tag">AI 미리보기</span></span><span class="sub" style="font-size:12px;line-height:1.6">정확한 맞음, 일부, 없음과 근거 문장은 "이 공고와 비교하기"에서 봐요. 합격 여부는 예측하지 않아요.</span></div>
      ${postBody(p)}
      ${course ? `<div class="card mini" style="padding:12px 14px;cursor:pointer" data-course="${course.id}">${TH[course.id] ? `<img src="assets/${TH[course.id]}" alt="" style="width:52px;height:52px">` : ''}<span class="tx"><span>부족한 역량을 채울 과정</span><b style="font-size:13px">${esc(course.n)}</b><small>SeSAC ${esc(course.cp)} · ${esc(course.st)}</small></span></div>` : ''}
      ${sims.length ? `<div><span class="sub">비슷한 역량을 찾는 공고</span>${sims.map((x) => `<div class="sim" data-sim="${DATA.posts.indexOf(x)}">${companyLogo(x.company, x.title, 26)}<b>${esc(x.title)}</b><span class="sub">${x.close < today ? '마감' : 'D-' + dday(x.close)}</span></div>`).join('')}</div>` : ''}
      <span class="sub" style="font-size:12px">출처 · 링커리어 · 일로가 수집한 2026 공고</span>
    </div>
    <div class="dr-f"><a class="btn btn-line" href="${esc(p.url)}" target="_blank" rel="noopener">원문 ${ic('ext')}</a>${saveBtn(key)}<span style="flex:1"></span><button type="button" class="btn btn-line" data-mkapp>지원서 만들기</button><button type="button" class="btn btn-primary" data-cmp>이 공고와 비교하기</button></div>`, (dr) => {
    $('[data-cmp]', dr).onclick = () => { closeDrawer(true); startChat(`${p.company} ${p.title} 공고와 내 이력서 비교해 줘`); };
    $('[data-mkapp]', dr).onclick = () => { closeDrawer(true); const ap = createApp(p); toast('지원서를 만들었어요 · 기본 이력서는 그대로예요'); go('#/apply/' + ap.id); };
    $('[data-save]', dr).onclick = (e) => toggleSave(key, { kind: '공고', t: p.title, s: `${p.company} · ${p.type}`, img: logoFor(p.company, p.title), href: '#/jobs' }, e.currentTarget);
    dr.addEventListener('click', (e) => { const sm = e.target.closest('[data-sim]'); if (sm) openPost(DATA.posts[sm.dataset.sim]); const cc = e.target.closest('[data-course]'); if (cc) openCourse(DATA.courses.find((c) => c.id === cc.dataset.course)); });
  });
}
function openCourse(c) {
  openDrawer(`${drHead(`SeSAC ${esc(c.cp)} · ${esc(c.f)}`, c.n)}
    <div class="dr-b">${TH[c.id] ? `<img src="assets/${TH[c.id]}" alt="" style="width:100%;border-radius:6px">` : ''}<div class="kv"><div><span>모집 상태</span><span>${esc(c.st)}${c.recEnd ? ' · ' + esc(c.recEnd) + ' 마감' : ''}</span></div><div><span>교육 기간</span><span>${esc(c.edu)}</span></div><div><span>교육 시간</span><span>${esc(c.h)}</span></div><div><span>해시태그</span><span>${esc(c.tags.join(' '))}</span></div><div><span>후기</span><span>${c.rv}개</span></div></div></div>
    <div class="dr-f"><a class="btn btn-line" href="${esc(c.u)}" target="_blank" rel="noopener">SeSAC에서 보기 ${ic('ext')}</a><span style="flex:1"></span>${saveBtn(c.id)}</div>`, (dr) => {
    $('[data-save]', dr).onclick = (e) => toggleSave(c.id, { kind: '교육', t: c.n, s: `SeSAC ${c.cp} · ${c.st}`, img: TH[c.id], href: '#/edu' }, e.currentTarget);
  });
}
function openPolicy(p) {
  openDrawer(`${drHead(`${esc(p.lc)} · ${esc(p.c)} · ${esc(p.r)}`, p.n)}
    <div class="dr-b">${PTH[p.id] ? `<img src="assets/${PTH[p.id]}" alt="" style="width:100%;border-radius:6px">` : ''}<p style="margin:0">${esc(p.d)}</p><div class="kv"><div><span>기관</span><span>${esc(p.o)}</span></div><div><span>신청</span><span>${esc(p.st)} · ${esc(p.per)}</span></div><div><span>키워드</span><span>${esc(p.k.join(', ') || '-')}</span></div><div><span>출처</span><span>온통청년 (2026.11.04 조회)</span></div></div><p class="sub" style="font-size:12px;margin:0">세부 자격은 정책 페이지에서 확인해 주세요.</p></div>
    <div class="dr-f"><a class="btn btn-line" href="${esc(p.u)}" target="_blank" rel="noopener">온통청년에서 보기 ${ic('ext')}</a><span style="flex:1"></span>${saveBtn(p.id)}</div>`, (dr) => {
    $('[data-save]', dr).onclick = (e) => toggleSave(p.id, { kind: '정책', t: p.n, s: `${p.o} · ${p.st}`, img: PTH[p.id], href: '#/edu/policy' }, e.currentTarget);
  });
}

/* ---------- shared filter bar (same pattern as the original prototype: 탭 ▾ → 칩 패널 → 선택된 조건 + 초기화) ---------- */
function filterBar(root, groups, st, draw) {
  const bar = $('[data-fbar]', root), panel = $('[data-fpanel]', root), selBox = $('[data-fsel]', root);
  const paint = () => {
    bar.innerHTML = groups.map((g) => { const n = (st.f[g.k] || []).length; const on = st.fo === g.k;
      return `<button type="button" class="ftab${n ? ' has' : ''}${on ? ' open' : ''}" data-fo="${g.k}" aria-expanded="${on}">${g.label}${n ? ' ' + (g.single ? '' : n) : ''}${g.single && n ? esc(g.opts.find((o) => o[0] === st.f[g.k][0])[1]) : ''}<span class="car">${on ? '▴' : '▾'}</span></button>`; }).join('');
    const g = groups.find((x) => x.k === st.fo);
    panel.hidden = !g;
    if (g) panel.innerHTML = `<span class="sub">${g.label}${g.single ? '' : ' · 여러 개 고를 수 있어요'}</span><div class="chips">${g.opts.map(([v, l, c]) => `<button type="button" class="chipbtn" data-fv="${esc(v)}" aria-pressed="${(st.f[g.k] || []).includes(v)}">${esc(l)}${c !== undefined ? ` <span style="opacity:.6">${c}</span>` : ''}</button>`).join('')}</div>`;
    const sel = []; groups.forEach((gg) => (st.f[gg.k] || []).forEach((v) => { if (gg.fixed) return; const o = gg.opts.find((x) => x[0] === v); sel.push(`<button type="button" class="fsel-chip" data-rm="${gg.k}" data-rv="${esc(v)}">${gg.label} > ${esc(o ? o[1] : v)} ✕</button>`); }));
    selBox.innerHTML = sel.length ? sel.join('') + '<button type="button" class="btn btn-ghost" data-freset style="height:30px">↺ 초기화</button>' : '';
    selBox.hidden = !sel.length;
  };
  root.addEventListener('click', (e) => {
    const t = e.target.closest('[data-fo]'); if (t) { st.fo = st.fo === t.dataset.fo ? '' : t.dataset.fo; paint(); return; }
    const v = e.target.closest('[data-fv]'); if (v) { const g = groups.find((x) => x.k === st.fo); const a = st.f[g.k] || []; const val = v.dataset.fv;
      st.f[g.k] = g.single ? [val] : a.includes(val) ? a.filter((x) => x !== val) : a.concat(val); st.page = 1; st.n = 12; if (g.single) st.fo = ''; paint(); draw(); return; }
    const rm = e.target.closest('[data-rm]'); if (rm) { st.f[rm.dataset.rm] = (st.f[rm.dataset.rm] || []).filter((x) => x !== rm.dataset.rv); st.page = 1; paint(); draw(); return; }
    if (e.target.closest('[data-freset]')) { groups.forEach((g) => { if (!g.fixed) st.f[g.k] = (g.def || []).slice(); }); st.fo = ''; st.page = 1; paint(); draw(); }
  });
  paint(); return paint;
}
const FILTER_HTML = `<button type="button" class="f-fab" data-act="f-open" aria-label="필터 열기"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"/></svg>필터</button><div class="f-scrim" data-act="f-close"></div><div class="fwrap"><div class="f-head"><b>필터</b><button type="button" class="btn btn-dark sm" data-act="f-close">결과 보기</button></div><div class="fbar" data-fbar></div><div class="card fpanel" data-fpanel hidden></div><div class="fsel" data-fsel hidden></div></div>`;
const pager = (page, pages) => pages <= 1 ? '' : `<div class="pager">${page > 1 ? `<button type="button" class="pg" data-pg="${page - 1}" aria-label="이전">‹</button>` : ''}${Array.from({ length: pages }, (_, i) => i + 1).filter((n) => Math.abs(n - page) < 3 || n === 1 || n === pages).map((n, i, a) => (i && n - a[i - 1] > 1 ? '<span class="sub">…</span>' : '') + `<button type="button" class="pg" data-pg="${n}"${n === page ? ' aria-current="page"' : ''}>${n}</button>`).join('')}${page < pages ? `<button type="button" class="pg" data-pg="${page + 1}" aria-label="다음">›</button>` : ''}</div>`;

/* ---------- jobs ---------- */
let OTHER = null;
function allJobs() {
  const sns = { label: 'SNS 콘텐츠 마케팅', posts: DATA.posts };
  if (!OTHER && DATA.other) { OTHER = {}; Object.entries(DATA.other).forEach(([k, v]) => { OTHER[k] = { label: v.label, posts: v.posts.map((p) => ({ company: p.c, title: p.t, type: p.ty, close: p.d || '', url: p.u, size: p.s || '정보 없음', ov: [] })) }; }); }
  return Object.assign({ sns }, OTHER || {});
}
function renderJobs() {
  const J = allJobs();
  const st = { f: { job: ['sns'], ty: [], sz: [], ov: [], dl: [] }, fo: '', q: '', sort: 'rec', page: 1 };
  mount(`<div class="page"><div class="page-head"><div class="head-l"><h1 data-jtitle>직무 찾기</h1><span class="sub" data-jsub></span></div>
    <label class="search">${ic('search')}<input type="search" placeholder="회사, 공고 검색" aria-label="회사, 공고 검색" data-q></label></div>
    ${FILTER_HTML}
    <ol class="flow"><li class="cur"><span>1</span>직무 찾기</li><li><span>2</span>공고 비교</li><li><span>3</span>다음 행동</li></ol><div class="grid2"><section class="card table" aria-label="공고 목록"><div class="list-head"><span class="sub" data-count></span><span class="sorts"><button type="button" data-sort="rec">추천순</button><button type="button" data-sort="new">최신순</button><button type="button" data-sort="close">마감 임박순</button></span></div><div class="th jt-grid"><span>기업명</span><span>공고명</span><span>채용형태</span><span>기업 형태</span><span>마감일</span><span></span></div><div data-list></div><div class="list-foot" data-foot></div></section>
    <aside class="card side-card" data-fit></aside></div></div>`);
  const root = $('.pane', view); const today = ymd(now()); const PER = 15;
  const groups = () => {
    const posts = J[st.f.job[0]].posts;
    const c = (fn) => posts.filter(fn).length;
    return [
      { k: 'job', label: '직무', single: true, fixed: true, opts: Object.entries(J).map(([k, v]) => [k, v.label, v.posts.length]) },
      { k: 'ty', label: '채용 형태', opts: ['신입', '인턴', '경력'].map((x) => [x, x, c((p) => p.type === x)]) },
      { k: 'sz', label: '기업 형태', opts: ['대기업', '중견기업', '중소기업', '스타트업', '기타'].map((x) => [x, x, c((p) => (p.size || '정보 없음') === x)]) },
      { k: 'ov', label: '요구 역량', opts: ['콘텐츠 기획', '데이터, 성과 분석', '디자인 툴'].map((x) => [x, x, c((p) => p.ov.includes(x))]) },
      { k: 'dl', label: '마감', opts: [['open', '모집 중만'], ['7', '7일 안에 마감'], ['has', '마감일 있음']] },
    ];
  };
  let paint;
  const draw = () => {
    const job = J[st.f.job[0]]; const ql = st.q.toLowerCase(); const f = st.f;
    $('[data-jtitle]', root).innerHTML = `직무 찾기<span class="h1-x"> · ${esc(job.label)}</span>`;
    $('[data-jsub]', root).innerHTML = st.f.job[0] === 'sns' ? `<span class="m-only">${esc(job.label)} · </span>2026 신입, 인턴 공고 ${job.posts.length}건 · 링커리어 수집 · 문장 비교 가능` : `공고 ${job.posts.length}건 · 잡코리아 수집 · 이 직무는 목록만 보여요 (문장 비교는 SNS 콘텐츠 마케팅만)`;
    const L = job.posts.filter((p) => (!ql || (p.company + p.title).toLowerCase().includes(ql)) && (!f.ty.length || f.ty.includes(p.type)) && (!f.sz.length || f.sz.includes(p.size || '정보 없음')) && (!f.ov.length || f.ov.some((o) => p.ov.includes(o)))
      && (!f.dl.includes('open') || (p.close && p.close >= today)) && (!f.dl.includes('7') || (p.close >= today && dday(p.close) <= 7)) && (!f.dl.includes('has') || !!p.close))
      .sort((a, b) => st.sort === 'rec' ? ((b.company === '올리브인터내셔널') - (a.company === '올리브인터내셔널')) || (b.ov.length - a.ov.length) || ((b.created || 0) - (a.created || 0)) : st.sort === 'new' ? (b.created || 0) - (a.created || 0) || b.close.localeCompare(a.close) : ((a.close < today) - (b.close < today)) || a.close.localeCompare(b.close) * (a.close < today ? -1 : 1));
    hlSort(L, 'jobs', (p) => p.company + p.title);
    const pages = Math.max(1, Math.ceil(L.length / PER)); st.page = Math.min(st.page, pages);
    $('[data-count]', root).innerHTML = `<b style="color:var(--ink);font-weight:600">${L.length}</b>건 중 ${L.length ? (st.page - 1) * PER + 1 : 0}–${Math.min(st.page * PER, L.length)}`;
    $$('[data-sort]', root).forEach((b) => b.setAttribute('aria-pressed', b.dataset.sort === st.sort));
    $('[data-list]', root).innerHTML = L.length ? L.slice((st.page - 1) * PER, st.page * PER).map((p, i) => {
      const closed = !p.close || p.close < today; const d = p.close ? dday(p.close) : null; const lg = logoFor(p.company, p.title); const idx = job.posts.indexOf(p);
      const mine = p.ov.filter((o) => OVFIT[o] === 'ok' || OVFIT[o] === 'part').length;
      return `<div class="tr jt-grid${closed && p.close ? ' closed' : ''}" role="button" tabindex="0" data-i="${idx}" data-k="${esc(p.company + p.title)}" style="animation:fadeUp var(--t3) var(--ease-out) both;animation-delay:${Math.min(i, 10) * 25}ms">
        <div class="co">${companyLogo(p.company, p.title, 36)}<span class="cn">${esc(p.company)}</span></div>
        <div class="ti"><b>${esc(p.title)}</b><span class="tags">${p.ov.length ? `<span class="tag-fit">내 경험과 겹치는 역량 ${mine}</span>` : ''}${p.ov.slice(0, 2).map((o) => `<span class="tag-ov">${esc(o)}</span>`).join('')}${p.ov.length > 2 ? `<span class="tag-ov">+${p.ov.length - 2}</span>` : ''}</span></div>
        <span class="c">${esc(p.type)}</span><span class="c sub">${esc(p.size && p.size !== '정보 없음' ? p.size : '-')}</span>
        <span class="cl">${!p.close ? '<span class="sub">상시</span>' : closed ? '<span class="sub">마감</span>' : `<span class="cd">${p.close.slice(2).replace(/-/g, '.')}</span><span class="${d <= 3 ? 't-no' : 'sub'}" style="font-size:12px">D-${d}</span>`}</span>
        <span class="acts"><button type="button" class="btn btn-line sm" data-rowcmp>비교하기</button>${saveBtn(postKey(p))}</span></div>`;
    }).join('') : `<div class="empty">조건에 맞는 공고가 없어요<button type="button" class="btn btn-line" data-freset>필터 초기화</button></div>`;
    $('[data-foot]', root).innerHTML = `<span>출처: ${st.f.job[0] === 'sns' ? '링커리어 2026 신입, 인턴 공고' : '잡코리아'} · 마감된 공고도 요구 역량 참고용으로 보여요</span>${pager(st.page, pages)}`;
    const SK = [['트렌드 감각, 밈', 'ok'], ['콘텐츠 기획', 'part'], ['데이터, 성과 분석', 'ok'], ['디자인 툴', null], ['영상, 숏폼 제작', null], ['영상 툴 (프리미어 등)', null], ['포트폴리오', null], ['카피라이팅', null]];
    $('[data-fit]', root).innerHTML = st.f.job[0] === 'sns' ? `<div class="head-l"><b style="font-size:15px;font-weight:600">이 직무와 내 이력서 <span class="ai-tag">AI</span></b><span class="sub">공고가 많이 찾는 역량 8개 중 맞음 2 · 일부 1</span></div>
      <ol class="skills">${SK.map(([k, v], i) => `<li><span class="rk">${i + 1}</span><span class="k">${esc(k)}</span>${v ? verd(v) : '<span class="sub" style="font-size:12px">근거 없음</span>'}</li>`).join('')}</ol>
      <span class="sub" style="line-height:1.6;font-size:12px">신입, 인턴은 공고 하나보다 이 직무 전체와 먼저 맞춰 봐요. 이력서에 같은 경험과 근거가 있으면 맞음, 일부만 있으면 일부예요. 합격 여부는 말하지 않아요</span>
      <a class="btn btn-line" href="#/edu?gap=${encodeURIComponent('디자인 툴')}">빈 역량 채우는 과정 보기</a>
      <a class="trend-link" href="#/trend"><span class="eyebrow-l"><span class="dot no pulse"></span>급상승</span><span class="tl-t"><b>데이터, 성과 분석</b><span class="sub">8위 → 3위 · 2023~25 대비</span></span><span class="sub">트렌드 스펙 →</span></a>`
      : `<div class="head-l"><b style="font-size:14px;font-weight:600">${esc(job.label)}</b><span class="sub">이 직무는 공고 목록만 준비돼 있어요</span></div><span class="sub" style="line-height:1.6">이 직무의 역량 분석은 준비 중이에요. 공고 원문은 지금 볼 수 있고, 공고 비교는 SNS 콘텐츠 마케팅으로 시연해요.</span><button type="button" class="btn btn-line" data-backsns>SNS 콘텐츠 마케팅으로 돌아가기</button>`;
    syncSaveBtns(); if (paint) paint(); markHL();
  };
  paint = filterBar(root, groups(), st, () => { paint = filterBar.length && paint; rebuild(); });
  const rebuild = () => { draw(); };
  root.addEventListener('click', (e) => {
    if (e.target.closest('[data-fv]') && st.f.job) { /* job change rebuilds counts */ }
    const so = e.target.closest('[data-sort]'); if (so) { st.sort = so.dataset.sort; draw(); return; }
    const pg = e.target.closest('[data-pg]'); if (pg) { st.page = Number(pg.dataset.pg); draw(); window.scrollTo({ top: 0, behavior: REDUCE ? 'auto' : 'smooth' }); return; }
    if (e.target.closest('[data-backsns]')) { st.f.job = ['sns']; st.page = 1; draw(); return; }
    const sv = e.target.closest('[data-save]'); const row = e.target.closest('.tr');
    const P = () => J[st.f.job[0]].posts[row.dataset.i];
    if (sv && row) { e.stopPropagation(); const p = P(); toggleSave(sv.dataset.save, { kind: '공고', t: p.title, s: `${p.company} · ${p.type}`, img: logoFor(p.company, p.title), href: '#/jobs' }, sv); return; }
    if (e.target.closest('[data-ext]')) return;
    if (row && e.target.closest('[data-rowcmp]')) { const p = P(); startChat(`${p.company} ${p.title} 공고와 내 이력서 비교해 줘`); return; }
    if (row) openPost(P());
  });
  root.addEventListener('keydown', (e) => { const row = e.target.closest('.tr'); if (row && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openPost(J[st.f.job[0]].posts[row.dataset.i]); } });
  let tmr; $('[data-q]', root).addEventListener('input', (e) => { clearTimeout(tmr); tmr = setTimeout(() => { st.q = e.target.value.trim(); st.page = 1; draw(); }, 120); });
  // group option counts depend on the chosen job: rebuild the bar when the job changes
  root.addEventListener('click', (e) => { const v = e.target.closest('[data-fv]'); if (v && !st.fo && st.f.job) { const gs = groups(); gs.forEach((g, k) => { if (g.k !== 'job') st.f[g.k] = st.f[g.k].filter((x) => g.opts.some((o) => o[0] === x)); }); } }, true);
  draw();
}

/* ---------- edu + policy ---------- */
const GROUPS = ['마케팅', 'AI', '데이터', '기획, PM', '개발', '디자인', '기타'];
const LCS = ['일자리', '교육', '금융·복지', '주거', '참여'];
const GCOL = { '마케팅': ['#EEF4FF', '#1B64DA'], 'AI': ['#F0EBFF', '#6B4EE6'], '데이터': ['#E6F7F1', '#0E8A63'], '기획, PM': ['#FFF4E5', '#B26A00'], '개발': ['#F2F4F6', '#4E5968'], '디자인': ['#FDEEF4', '#B4245D'], '기타': ['#F4F4F3', '#6B6B68'] };
function renderEdu(tab, qs) {
  const gap = qs.get('gap');
  const st = { tab, q: '', n: 12, page: 1, fo: '', sort: 'rec',
    f: { g: gap ? ['마케팅'] : [], cst: gap ? ['모집 중', '모집 예정'] : [], cp: [], on: [], lc: [], org: [], pst: ['신청 중', '상시'] } };
  mount(`<div class="page"><div class="page-head"><div class="head-l"><h1>교육과정과 정책</h1><span class="sub">SeSAC 과정 ${DATA.courses.length}개 · 서울시와 중앙부처 청년 정책 ${DATA.policies.length}건 (온통청년, 2026.11.04 조회)</span></div>
    <label class="search">${ic('search')}<input type="search" placeholder="과정, 정책, 기관 검색" aria-label="과정, 정책, 기관 검색" data-q></label></div>
    ${gap ? `<div class="card banner"><span class="dot no"></span><span>비교에서 <b class="t-no" style="font-weight:600">${esc(gap)}</b>이 비어 있어요 · 마케팅 과정 중 모집 중, 예정인 것부터 보여 드려요</span><button type="button" class="btn btn-ghost x" data-unbanner>전체 보기</button></div>` : ''}
    <div class="tabs" role="tablist" data-tabs></div><div data-fhost></div><div class="list-head"><span class="sub" data-count></span><span class="sorts" data-sorts></span></div><div data-body></div></div>`);
  const root = $('.pane', view);
  const camps = [...new Set(DATA.courses.map((c) => c.cp))].sort();
  const G = () => st.tab === 'edu' ? [
    { k: 'g', label: '분야', opts: GROUPS.map((g) => [g, g, DATA.courses.filter((c) => c.g === g).length]) },
    { k: 'cst', label: '모집 상태', opts: ['모집 중', '모집 예정', '상시', '진행 중', '종료'].map((x) => [x, x, DATA.courses.filter((c) => c.st === x).length]) },
    { k: 'cp', label: '캠퍼스', opts: camps.map((x) => [x, x, DATA.courses.filter((c) => c.cp === x).length]) },
    { k: 'on', label: '수업 방식', opts: [['off', '오프라인'], ['on', '온라인']] },
  ] : [
    { k: 'lc', label: '분야', opts: LCS.map((x) => [x, x, DATA.policies.filter((p) => p.lc === x).length]) },
    { k: 'org', label: '기관', opts: [['서울', '서울시'], ['중앙부처', '중앙부처']] },
    { k: 'pst', label: '신청 상태', def: ['신청 중', '상시'], opts: ['신청 중', '상시', '예정', '마감'].map((x) => [x, x, DATA.policies.filter((p) => p.st === x).length]) },
  ];
  let paint;
  const mountFilters = () => { const host = $('[data-fhost]', root); host.innerHTML = FILTER_HTML; const fresh = host.cloneNode(true); host.replaceWith(fresh); fresh.setAttribute('data-fhost', ''); paint = filterBar(fresh, G(), st, draw); };
  const draw = () => {
    const ql = st.q.toLowerCase(); const f = st.f;
    $('[data-tabs]', root).innerHTML = `<button type="button" role="tab" aria-selected="${st.tab === 'edu'}" data-tab="edu">SeSAC 과정 ${DATA.courses.length}</button><button type="button" role="tab" aria-selected="${st.tab === 'pol'}" data-tab="pol">청년 정책 ${DATA.policies.length}</button>`;
    const sorts = st.tab === 'edu' ? [['rec', '추천순'], ['close', '마감 가까운 순'], ['rv', '후기 많은 순']] : [['rec', '신청 가능 먼저'], ['v', '많이 본 순']];
    $('[data-sorts]', root).innerHTML = sorts.map(([k, l]) => `<button type="button" data-sort="${k}" aria-pressed="${st.sort === k}">${l}</button>`).join('');
    const body = $('[data-body]', root);
    if (st.tab === 'edu') {
      const rank = { '모집 중': 0, '모집 예정': 1, '상시': 2, '진행 중': 3, '종료': 4 };
      let L = DATA.courses.filter((c) => (!f.g.length || f.g.includes(c.g)) && (!f.cst.length || f.cst.includes(c.st)) && (!f.cp.length || f.cp.includes(c.cp)) && (!f.on.length || f.on.includes(c.on ? 'on' : 'off')) && (!ql || (c.n + c.cp + c.f + c.tags.join(' ')).toLowerCase().includes(ql)));
      L = L.sort(st.sort === 'rv' ? (a, b) => b.rv - a.rv : st.sort === 'close' ? (a, b) => rank[a.st] - rank[b.st] || (a.recEnd || '9').localeCompare(b.recEnd || '9') : (a, b) => (!!TH[b.id] - !!TH[a.id]) || ((b.g === '마케팅') - (a.g === '마케팅')) || rank[a.st] - rank[b.st] || b.rv - a.rv);
      hlSort(L, 'edu', (c) => c.id);
      $('[data-count]', root).innerHTML = `<b style="color:var(--ink);font-weight:600">${L.length}</b>개 중 ${Math.min(st.n, L.length)}개`;
      body.innerHTML = L.length ? `<div class="cards4">${L.slice(0, st.n).map((c, i) => { const col = GCOL[c.g] || GCOL['기타']; const sc = c.st === '모집 중' ? 'ok' : c.st === '모집 예정' ? 'run' : 'off';
        return `<article class="card ccard" data-c="${c.id}" tabindex="0" style="animation-delay:${Math.min(i % 12, 12) * 30}ms">${TH[c.id] ? `<img class="thumb" src="assets/${TH[c.id]}" alt="" loading="lazy">` : `<div class="thumb ph" style="background:${col[0]};color:${col[1]}"><span>${esc(c.g)}</span><b>${esc(c.n.replace(/^\([^)]*\)\s*/, '').slice(0, 30))}</b><span>SeSAC ${esc(c.cp)}</span></div>`}<div class="bd"><div class="meta"><span class="st" style="font-size:12px;color:var(--ink-3)"><span class="dot ${sc}"></span>${esc(c.st)}${c.st === '모집 중' && c.recEnd ? ' · ' + esc(c.recEnd.slice(5)) + ' 마감' : ''}${c.id === 'edu-1465' && gap ? ' · 빈칸 채움' : ''}</span>${saveBtn(c.id)}</div><b>${esc(c.n)}</b><small>SeSAC ${esc(c.cp)} · ${esc(c.edu)}${c.rv ? ` · 후기 ${c.rv}` : ''}</small></div></article>`; }).join('')}</div>
        ${L.length > st.n ? `<button type="button" class="btn btn-line" data-more style="align-self:center;margin:8px auto 0;display:flex">더 보기 · ${L.length - st.n}개 남음</button>` : ''}` : `<div class="empty card">조건에 맞는 과정이 없어요<button type="button" class="btn btn-line" data-freset>필터 초기화</button></div>`;
    } else {
      const rank = { '신청 중': 0, '상시': 1, '예정': 2, '마감': 3 }; const PER = 20;
      const L = DATA.policies.filter((p) => (!f.lc.length || f.lc.includes(p.lc)) && (!f.org.length || f.org.includes(p.r)) && (!f.pst.length || f.pst.includes(p.st)) && (!ql || (p.n + p.o + p.k.join(' ') + p.d).toLowerCase().includes(ql)))
        .sort(st.sort === 'v' ? (a, b) => b.v - a.v : (a, b) => rank[a.st] - rank[b.st] || (b.r === '서울') - (a.r === '서울') || b.v - a.v);
      hlSort(L, 'pol', (p) => p.id);
      const pages = Math.max(1, Math.ceil(L.length / PER)); st.page = Math.min(st.page, pages);
      $('[data-count]', root).innerHTML = `<b style="color:var(--ink);font-weight:600">${L.length}</b>건 중 ${L.length ? (st.page - 1) * PER + 1 : 0}–${Math.min(st.page * PER, L.length)}`;
      body.innerHTML = L.length ? `<section class="card ptable"><div class="pr" style="cursor:default;font-size:12px;color:var(--faint);padding:10px 20px"><span>분야</span><span>정책</span><span>기관</span><span>신청</span><span></span></div>${L.slice((st.page - 1) * PER, st.page * PER).map((p, i) => `<div class="pr" data-p="${p.id}" tabindex="0" style="animation:fadeUp var(--t3) var(--ease-out) both;animation-delay:${Math.min(i, 12) * 20}ms"><span class="sub" style="font-size:13px">${esc(p.lc)}</span><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><b>${esc(p.n)}</b><span class="sub" style="font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(p.d)}</span></span><span class="o">${esc(p.o)}</span><span class="st"><span class="dot ${p.st === '신청 중' ? 'ok' : p.st === '상시' ? 'run' : 'off'}"></span>${esc(p.st)}</span>${saveBtn(p.id)}</div>`).join('')}
        <div class="list-foot"><span>출처 · 온통청년 · 세부 자격은 각 정책에서 확인</span>${pager(st.page, pages)}</div></section>` : `<div class="empty card">조건에 맞는 정책이 없어요<button type="button" class="btn btn-line" data-freset>필터 초기화</button></div>`;
    }
    syncSaveBtns(); if (paint) paint(); markHL();
  };
  root.addEventListener('click', (e) => {
    const T = e.target;
    if (T.closest('[data-unbanner]')) { go('#/edu'); return; }
    const tb = T.closest('[data-tab]'); if (tb) { st.tab = tb.dataset.tab; st.n = 12; st.page = 1; st.fo = ''; st.sort = 'rec'; history.replaceState(null, '', st.tab === 'pol' ? '#/edu/policy' : '#/edu'); mountFilters(); draw(); return; }
    const so = T.closest('[data-sort]'); if (so) { st.sort = so.dataset.sort; draw(); return; }
    if (T.closest('[data-more]')) { st.n += 12; draw(); return; }
    const pg = T.closest('[data-pg]'); if (pg) { st.page = Number(pg.dataset.pg); draw(); window.scrollTo({ top: 0, behavior: REDUCE ? 'auto' : 'smooth' }); return; }
    if (T.closest('[data-body] [data-freset]')) { Object.assign(st.f, { g: [], cst: [], cp: [], on: [], lc: [], org: [], pst: [] }); $('[data-q]', root).value = ''; st.q = ''; draw(); return; }
    const sv = T.closest('[data-save]');
    if (sv) { e.stopPropagation(); const id = sv.dataset.save; const c = DATA.courses.find((x) => x.id === id); const p = DATA.policies.find((x) => x.id === id);
      if (c) toggleSave(id, { kind: '교육', t: c.n, s: `SeSAC ${c.cp} · ${c.st}`, img: TH[c.id], href: '#/edu' }, sv);
      else if (p) toggleSave(id, { kind: '정책', t: p.n, s: `${p.o} · ${p.st}`, img: PTH[p.id], href: '#/edu/policy' }, sv); return; }
    const cc = T.closest('[data-c]'); if (cc) { openCourse(DATA.courses.find((x) => x.id === cc.dataset.c)); return; }
    const pp = T.closest('[data-p]'); if (pp) openPolicy(DATA.policies.find((x) => x.id === pp.dataset.p));
  });
  root.addEventListener('keydown', (e) => { if (e.key !== 'Enter') return; const cc = e.target.closest('[data-c]'); if (cc) openCourse(DATA.courses.find((x) => x.id === cc.dataset.c)); const pp = e.target.closest('[data-p]'); if (pp) openPolicy(DATA.policies.find((x) => x.id === pp.dataset.p)); });
  let tmr; $('[data-q]', root).addEventListener('input', (e) => { clearTimeout(tmr); tmr = setTimeout(() => { st.q = e.target.value.trim(); st.n = 12; st.page = 1; draw(); }, 120); });
  mountFilters(); draw();
}

/* ---------- saved ---------- */
function renderSaved() { renderTasks('saved'); }

/* ---------- my page ---------- */
function renderMe(tab) {
  const tabs = [['profile', '프로필'], ['resume', '기본 이력서'], ['memory', '나의 기억']];
  mount(`<div class="page"><div class="page-head"><div class="head-l"><h1>마이페이지</h1><span class="sub">추천과 정책 자격 확인에 쓰는 정보예요 · 이 기기 브라우저에만 저장돼요</span></div>
    <div class="head-r"><span>${dateKo()}</span><span class="sub">${timeKo()}</span></div></div>
    <div class="tabs" role="tablist">${tabs.map(([k, l]) => `<button type="button" role="tab" aria-selected="${tab === k}" data-me="${k}">${l}</button>`).join('')}<span class="tabs-r"><a class="btn btn-line" href="#/apply">지원서 ${apps().length}</a><a class="btn btn-line" href="#/saved">저장함 ${Object.keys(saved()).length}</a></span></div><div data-body></div></div>`);
  $('.pane', view).addEventListener('click', (e) => { const t = e.target.closest('[data-me]'); if (t) go(t.dataset.me === 'profile' ? '#/me' : '#/me/' + t.dataset.me); });
  const body = $('[data-body]', view);
  if (tab === 'resume') meResume(body); else if (tab === 'memory') meMemory(body); else meProfile(body);
}
function meProfile(body) {
  const pf = store.get('profile', { age: 24, region: '서울 관악구', status: '구직 중', income: '' });
  const sel = (k, opts) => `<select data-pf="${k}">${opts.map((o) => `<option${pf[k] === o ? ' selected' : ''}>${o}</option>`).join('')}</select>`;
  body.innerHTML = `<div class="me-grid"><div style="display:flex;flex-direction:column;gap:16px">
    <article class="card sec pf-hero"><div class="pf-id" style="display:flex;align-items:center;gap:16px"><img src="assets/avatar-haneul.jpg" alt="" style="width:64px;height:64px;border-radius:50%;object-fit:cover"><div class="head-l" style="flex:1"><b style="font-size:18px;font-weight:600">김하늘</b><span class="sub" style="font-size:13px">미디어커뮤니케이션학과 졸업 예정</span></div></div>
      <div class="inset pf-goal" style="padding:14px 16px;gap:6px"><span class="sub">목표 직무</span><b style="font-size:15px;font-weight:600">SNS 콘텐츠 마케터 · 신입, 인턴</b></div>
      <div class="trio"><div><span>대화</span><span class="big" style="font-size:30px">${chats().length}</span></div><div><span>저장</span><span class="big" style="font-size:30px">${Object.keys(saved()).length}</span></div><div><span>기억</span><span class="big" style="font-size:30px">${memEvents().length}</span></div></div></article>
    <article class="card sec pf-sec"><div class="sec-h"><h2>정책 자격 정보</h2><span class="sub">바꾸면 바로 다시 계산해요</span></div>
      <label class="field"><span>나이 (만)</span><input type="number" min="15" max="45" value="${pf.age}" data-pf="age"></label>
      <label class="field"><span>거주지</span>${sel('region', ['서울 관악구', '서울 강북구', '서울 성동구', '서울 영등포구', '경기 성남시', '부산'])}</label>
      <label class="field"><span>상태</span>${sel('status', ['구직 중', '재학 중', '재직 중'])}</label>
      <label class="field"><span>소득 구간</span>${sel('income', ['', '중위소득 100% 이하', '중위소득 150% 이하', '그 이상'])}</label>
      <div class="inset" style="padding:12px 14px;flex-direction:row;align-items:center;gap:8px;font-size:13px" data-elig></div></article></div>
    <div style="display:flex;flex-direction:column;gap:16px">
      <article class="card sec pf-sec"><div class="sec-h"><h2>이력서</h2><span class="sub">김하늘_이력서.pdf · AI가 12개 항목을 채움</span></div><div class="inset">${['마케팅 동아리 인스타그램 운영 · 2023.03 ~ 2025.02', '카페 아르바이트 · 2년', '대학생 마케팅 공모전 장려상 · 2024'].map((x) => `<div class="r"><span class="k">${x}</span></div>`).join('')}</div><a class="btn btn-line" href="#/me/resume" style="align-self:flex-start">전체 이력서 고치기</a></article>
      <article class="card sec pf-sec pf-gap"><div class="sec-h"><h2>지금 채우는 중인 빈칸</h2><a class="sub" href="#/me/memory">나의 기억에서 보기 →</a></div><div class="inset"><div class="r">${verd('no')}<span class="k">숏폼 콘텐츠 성과 분석</span><a class="ev" href="#/edu?gap=${encodeURIComponent('숏폼 성과 분석')}">과정 보기</a></div><div class="r">${verd('part')}<span class="k">캠페인 성과 지표 관리</span><span class="ev">수치 1개 더 적으면 맞음</span></div></div></article>
      ${memMini()}
    </div></div>`;
  const elig = () => {
    const seoul = /^서울/.test(pf.region); const okAge = pf.age >= 19 && pf.age <= 39;
    const n = DATA.policies.filter((p) => (p.st === '신청 중' || p.st === '상시') && (seoul || p.r !== '서울')).length;
    $('[data-elig]', body).innerHTML = okAge ? `<span class="dot ok"></span>지금 확인해 볼 정책 ${n}건${pf.income ? '' : ' · 소득을 넣으면 더 정확해져요'}` : `<span class="dot part"></span>대부분의 청년 정책은 만 19~39세 대상이에요`;
  };
  body.addEventListener('change', (e) => { const k = e.target.dataset.pf; if (!k) return; pf[k] = k === 'age' ? Number(e.target.value) : e.target.value; store.set('profile', pf); elig(); toast('저장했어요'); });
  elig();
}
const RES = [
  ['s1', '인적사항', 'person'], ['s2', '희망 직무', 'tags', ['SNS 콘텐츠 마케팅', '콘텐츠 마케터']], ['s3', '스킬', 'tags', ['캔바', '인스타그램 운영', '엑셀']],
  ['s4', '학력', 'edu'], ['s5', '경력', 'career'], ['s6', '인턴, 대외활동', 'acts'], ['s7', '교육', 'empty'], ['s8', '자격증', 'line', '컴퓨터활용능력 2급 · 대한상공회의소 · 2022.08'],
  ['s9', '수상', 'line', '대학생 마케팅 공모전 장려상 · 2024.11'], ['s10', '해외 경험', 'empty'], ['s11', '어학', 'line', '영어 · OPIc IM2 · 2024.06'], ['s12', '포트폴리오', 'line', 'notion.so/[포트폴리오 링크]'],
  ['s13', '자기소개서', 'intro'], ['s14', '희망 근무 조건', 'cond'],
];
function meResume(body) {
  const R = store.get('resume', {});
  const val = (k, d) => (R[k] ?? d);
  const f = (k, label, d, span) => `<label class="field"${span ? ' style="grid-column:span ' + span + '"' : ''}><span>${label}</span><input data-r="${k}" value="${esc(val(k, d))}"></label>`;
  const tagsOf = (k, d) => val(k, d);
  const sec = ([id, title, type, extra]) => {
    let inner = '';
    if (type === 'person') inner = `<div style="display:grid;grid-template-columns:96px minmax(0,1fr);gap:20px"><img src="assets/photo-haneul.jpg" onerror="this.src='assets/avatar-haneul.jpg'" alt="증명사진" style="width:96px;height:120px;border-radius:6px;object-fit:cover"><div class="g3">${f('name', '이름 *', '김하늘')}${f('birth', '생년월일 *', '2002.05.12')}${f('gender', '성별', '여')}${f('email', '이메일 *', 'haneul@example.com')}${f('phone', '휴대폰 *', '010-0000-0000')}${f('addr', '주소', '서울 관악구')}</div></div>`;
    if (type === 'tags') inner = `<div class="tagrow" data-tags="${id}">${tagsOf(id, extra).map((t) => `<span class="tag">${esc(t)}<button type="button" data-rm="${esc(t)}" aria-label="${esc(t)} 빼기">✕</button></span>`).join('')}<button type="button" class="add" data-add="${id}">+ 추가</button></div>${id === 's3' ? `<div class="tagrow" style="font-size:12px"><span class="sub" style="align-self:center">공고에서 많이 찾는 툴</span>${[['프리미어', 30], ['포토샵', 28], ['피그마', 19], ['캡컷', 10]].map(([t, n]) => `<button type="button" class="chipbtn" data-sug="${t}">+ ${t} <span style="color:var(--faint)">${n}건</span></button>`).join('')}</div>` : ''}`;
    if (type === 'edu') inner = `<div style="display:grid;grid-template-columns:1fr 1.4fr 1.4fr 1fr 1fr 1fr .8fr;gap:10px">${f('sch1', '학교 구분 *', '대학교(4년)')}${f('sch2', '학교명 *', '[학교명]')}${f('sch3', '전공 *', '미디어커뮤니케이션학과')}${f('sch4', '입학', '2021.03')}${f('sch5', '졸업', '2026.02')}${f('sch6', '상태', '졸업 예정')}${f('sch7', '학점', '3.8 / 4.5')}</div>`;
    if (type === 'career') inner = `<label style="display:inline-flex;align-items:center;gap:8px;font-size:13px"><input type="checkbox" data-r="newbie" ${val('newbie', true) ? 'checked' : ''}> 신입이에요 <span class="sub">경력이 생기면 체크를 풀고 회사, 기간, 담당 업무를 적어요</span></label>`;
    if (type === 'acts') inner = [['동아리 운영진', '교내 마케팅 동아리', '2023.03 ~ 2025.02', '동아리 공식 인스타그램 운영, 주 3회 콘텐츠 기획과 제작. 팔로워 3천에서 1.2만으로.'], ['아르바이트', '카페', '2년', '고객 응대, 재고 관리, 매장 SNS 사진 촬영.']].map((a, i) => `<div class="inset" style="padding:16px 18px"><div class="g3">${f('a' + i + 'k', '구분', a[0])}${f('a' + i + 'o', '기관, 단체', a[1])}${f('a' + i + 'p', '기간', a[2])}${f('a' + i + 'd', '활동 내용', a[3], 3)}</div></div>`).join('') + '<button type="button" class="add" style="align-self:flex-start" data-toast="활동 칸을 추가했어요">+ 활동 추가</button>';
    if (type === 'empty') inner = `<button type="button" class="add" style="align-self:flex-start" data-toast="${title} 칸을 열었어요">+ 추가</button>`;
    if (type === 'line') inner = f(id, title, extra);
    if (type === 'intro') inner = `${f('introT', '제목', '숫자로 증명하는 콘텐츠 마케터')}<label class="field"><span>내용</span><textarea data-r="introB" maxlength="1000">${esc(val('introB', '동아리 인스타그램을 2년 동안 운영하며 팔로워를 3천에서 1.2만으로 늘렸습니다. 매주 콘텐츠 반응을 기록하고, 저장 수가 높은 형식을 다음 기획에 반영했습니다.'))}</textarea></label><span class="sub" data-len style="align-self:flex-end"></span>`;
    if (type === 'cond') inner = `<div class="g3">${f('c1', '고용 형태', '인턴, 정규직')}${f('c2', '근무 지역', '서울, 경기 성남')}${f('c3', '희망 연봉', '회사 내규에 따름')}</div>`;
    const ai = type !== 'empty';
    return `<section class="card sec" id="${id}" ${type === 'empty' ? 'style="border-style:dashed"' : ''}><div class="sec-h"><h2>${title}</h2>${ai ? '<span class="ai-tag">AI</span>' : ''}${id === 's1' ? '<span class="sub">비교에는 쓰지 않아요</span>' : id === 's6' ? '<span class="sub">공고 비교에 가장 많이 쓰여요</span>' : ''}</div>${inner}</section>`;
  };
  body.innerHTML = `<div style="display:grid;grid-template-columns:220px minmax(0,1fr);gap:20px;align-items:start">
    <nav class="card toc" aria-label="이력서 항목"><div style="display:flex;flex-direction:column;gap:8px;padding:0 6px"><span class="sub" data-prog></span><div class="bar3"><i data-progbar></i></div></div><ol>${RES.map(([id, t, type]) => `<li><a href="#${id}" data-jump="${id}"><span class="${type === 'empty' ? 'ring0' : 'dot ok'}"></span>${t}</a></li>`).join('')}</ol>
      <button type="button" class="btn btn-primary" data-save-resume style="margin:4px 6px 0">이력서 저장</button></nav>
    <div style="display:flex;flex-direction:column;gap:14px;min-width:0"><article class="card" style="padding:16px 20px;display:flex;align-items:center;gap:14px"><span class="logo" style="border-radius:6px">PDF</span><div class="head-l" style="flex:1"><b style="font-size:14px;font-weight:600">김하늘_이력서.pdf</b><span class="sub"><span class="ai-tag">AI</span>가 12개 항목을 나눠 채웠어요 · 공고마다 고친 버전은 <a href="#/apply">지원서</a>에 따로 저장돼요</span></div><button type="button" class="btn btn-line" data-toast="새 PDF를 고르는 창이 열려요 (시연에서는 예시 이력서를 써요)">다시 올리기</button></article>${RES.map(sec).join('')}</div></div>`;
  const prog = () => { const filled = RES.filter((r) => r[2] !== 'empty').length; $('[data-prog]', body).textContent = `14개 중 ${filled}개 작성`; $('[data-progbar]', body).style.width = filled / 14 * 100 + '%'; const ta = $('[data-r="introB"]', body); $('[data-len]', body).textContent = `${ta.value.length} / 1,000자`; };
  let dirty = false;
  body.addEventListener('input', (e) => { const k = e.target.dataset.r; if (!k) return; R[k] = e.target.type === 'checkbox' ? e.target.checked : e.target.value; dirty = true; prog(); });
  body.addEventListener('change', (e) => { if (e.target.type === 'checkbox') { R[e.target.dataset.r] = e.target.checked; dirty = true; } });
  body.addEventListener('click', (e) => {
    const T = e.target;
    const j = T.closest('[data-jump]'); if (j) { e.preventDefault(); $('#' + j.dataset.jump, body).scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'start' }); return; }
    const t = T.closest('[data-toast]'); if (t) { toast(t.dataset.toast); return; }
    if (T.closest('[data-save-resume]')) { store.set('resume', R); dirty = false; toast('이력서를 저장했어요 · 다음 비교부터 이 내용을 써요'); remember('이력서를 고쳐 저장했어요'); return; }
    const rm = T.closest('[data-rm]'); if (rm) { const box = rm.closest('[data-tags]'); const id = box.dataset.tags; const def = RES.find((r) => r[0] === id)[3]; R[id] = tagsOf(id, def).filter((x) => x !== rm.dataset.rm); dirty = true; rm.closest('.tag').remove(); return; }
    const sg = T.closest('[data-sug]'); const ad = T.closest('[data-add]');
    if (sg || ad) { const id = sg ? 's3' : ad.dataset.add; const def = RES.find((r) => r[0] === id)[3]; const name = sg ? sg.dataset.sug : prompt('추가할 항목을 적어 주세요'); if (!name) return; const cur = tagsOf(id, def); if (cur.includes(name)) return; R[id] = cur.concat(name); dirty = true;
      const box = $(`[data-tags="${id}"]`, body); const span = document.createElement('span'); span.className = 'tag'; span.innerHTML = `${esc(name)}<button type="button" data-rm="${esc(name)}" aria-label="${esc(name)} 빼기">✕</button>`; box.insertBefore(span, $('[data-add]', box)); if (sg) sg.remove(); }
  });
  window.onbeforeunload = () => (dirty ? true : undefined);
  prog();
}
function memMini() {
  const N = memNodes(); const ids = N.map((n) => n.id);
  const cnt = (t) => N.filter((n) => n.type === t).length; const last = memEvents()[0];
  const edges = memEdges().filter(([a, b]) => ids.includes(a) && ids.includes(b)).map(([a, b]) => { const A = N.find((n) => n.id === a), B = N.find((n) => n.id === b); const g = a === 'gap' || b === 'gap';
    return `<path d="M${A.x} ${A.y} L${B.x} ${B.y}" vector-effect="non-scaling-stroke" stroke="${g ? '#E8A33D' : '#D4D4D1'}" stroke-width="1.2" ${g ? 'stroke-dasharray="4 4"' : ''} fill="none"/>`; }).join('');
  const nodes = N.map((n, i) => `<span class="node${n.type === 'me' ? ' me-node' : ''}${n.type === 'gap' ? ' gap' : ''}" style="left:${8 + n.x * 0.84}%;top:${8 + n.y * 0.84}%;animation-delay:${i * 40}ms">${n.type === 'me' ? '<img src="assets/avatar-haneul.jpg" alt="" style="width:20px;height:20px;border-radius:50%">' : n.type === 'post' ? '<img src="assets/logo-kakao.png" alt="" style="width:14px;height:14px;border-radius:50%">' : `<span class="dot ${NCOL[n.type] || ''}" style="${n.type === 'goal' ? 'background:var(--ink)' : ''}"></span>`}${esc(n.t)}</span>`).join('');
  const sv = edges.replace(/M([\d.]+) ([\d.]+) L([\d.]+) ([\d.]+)/g, (m, x1, y1, x2, y2) => `M${8 + x1 * 0.84} ${8 + y1 * 0.84} L${8 + x2 * 0.84} ${8 + y2 * 0.84}`);
  return `<a class="card sec mem-mini" href="#/me/memory"><div class="sec-h"><h2>나의 기억</h2><span class="sub">그래프 열기 →</span></div>
    <div class="mm-body"><div class="graph mini" aria-hidden="true"><svg class="edges" viewBox="0 0 100 100" preserveAspectRatio="none">${sv}</svg>${nodes}</div>
      <div class="mm-side"><div class="mm-cnt"><span><span class="dot run"></span>경험 ${cnt('exp')}</span><span><span class="dot ok"></span>역량 ${cnt('skill')}</span><span><span class="dot part"></span>빈칸 ${cnt('gap')}</span></div>
      ${last ? `<div class="mm-last"><span class="sub">최근에 배운 것 · ${esc(last.d)}</span><span>${esc(last.t)}</span></div>` : ''}</div></div></a>`;
}
const NODES = [
  { id: 'me', x: 50, y: 50, t: '나', type: 'me' },
  { id: 'goal', x: 50, y: 18, t: '목표 · SNS 콘텐츠 마케터', type: 'goal' },
  { id: 'post', x: 82, y: 28, t: '카카오 인턴 공고', type: 'post' },
  { id: 'insta', x: 16, y: 32, t: '동아리 인스타 운영', type: 'exp', d: '대학 마케팅 동아리 공식 인스타그램을 2년 동안 운영. 팔로워 3천에서 1.2만으로.', src: ['이력서 1쪽', '11/4 대화'], used: [['카카오 인턴 · SNS 채널 운영 경험', 'ok'], ['카카오 인턴 · 콘텐츠 기획 및 제작', 'ok']] },
  { id: 'sns', x: 42, y: 32, t: 'SNS 채널 운영', type: 'skill', d: '공고 46건 중 다수가 요구하는 역량. 인스타 운영 경험으로 증명돼요.', src: ['공고 요구 역량'], used: [['카카오 인턴 · SNS 채널 운영 경험', 'ok']] },
  { id: 'cafe', x: 14, y: 62, t: '카페 알바 2년', type: 'exp', d: '고객 응대, 재고 관리, 매장 SNS 사진 촬영.', src: ['이력서 2쪽'], used: [['협업 커뮤니케이션', 'ok']] },
  { id: 'cs', x: 36, y: 62, t: '고객 응대', type: 'skill', d: '카페 알바에서 연결된 역량. 결과 숫자가 있으면 더 강해져요.', src: ['11/3 대화'], used: [] },
  { id: 'award', x: 26, y: 84, t: '마케팅 공모전 장려상', type: 'exp', d: '대학생 마케팅 공모전 장려상, 팀장.', src: ['이력서 2쪽'], used: [['광고 운영 경험', 'ok']] },
  { id: 'gap', x: 80, y: 58, t: '빈칸 · 숏폼 성과 분석', type: 'gap', d: '카카오 공고 비교에서 근거가 없었던 문장. 과정이나 2주 활동으로 채울 수 있어요.', src: ['11/4 비교'], used: [['카카오 인턴 · 숏폼 콘텐츠 성과 분석', 'no']] },
  { id: 'course', x: 84, y: 84, t: 'SeSAC 양천 과정', type: 'link', d: '실무 경험으로 완성하는 AI 콘텐츠 디자인 과정. 빈칸을 직접 다뤄요.', src: ['과정 찾기 에이전트'], used: [] },
  { id: 'living', x: 58, y: 84, t: '관심 · 구직 생활비', type: 'link', d: '구직 기간 생활비 지원에 관심이 있어요.', src: ['11/4 대화'], used: [] },
];
const EDGES = [['me', 'goal'], ['me', 'insta'], ['me', 'cafe'], ['me', 'award'], ['me', 'living'], ['insta', 'sns'], ['sns', 'post'], ['goal', 'post'], ['cafe', 'cs'], ['award', 'sns'], ['post', 'gap'], ['gap', 'course']];
const NCOL = { exp: 'run', skill: 'ok', gap: 'part', link: 'off', goal: '', post: '' };
const SKILLMAP = [[/재고/, '재고 관리'], [/응대|손님|고객/, '고객 응대'], [/편집|프리미어|캡컷|영상/, '영상 편집'], [/분석|데이터|지표|GA/, '데이터 분석'], [/기획/, '콘텐츠 기획'], [/인스타|SNS|틱톡|유튜브|블로그/, 'SNS 채널 운영'], [/디자인|포토샵|피그마|캔바/, '디자인 툴'], [/엑셀|스프레드/, '엑셀'], [/영어|토익|오픽|OPIc/i, '외국어'], [/리더|팀장|운영진/, '리더십']];
function memNodes() {
  const custom = store.get('mem-custom', []); const gone = store.get('mem-gone', []); const edits = store.get('mem-edits', {});
  return NODES.concat(custom).filter((n) => !gone.includes(n.id)).map((n) => edits[n.id] ? { ...n, ...edits[n.id] } : n);
}
function memEdges() { return EDGES.concat(store.get('mem-cedges', [])); }
function freeSpot(nodes) {
  const ring = [[30, 46], [70, 44], [62, 70], [38, 74], [28, 18], [74, 14], [90, 72], [10, 86], [90, 42], [8, 10]];
  return ring.find(([x, y]) => !nodes.some((n) => Math.abs(n.x - x) < 14 && Math.abs(n.y - y) < 9)) || [20 + Math.random() * 60, 20 + Math.random() * 60];
}
function meMemory(body) {
  setTimeout(() => { const i = $('[data-memin]', body); if (i && matchMedia('(max-width:767px)').matches) i.placeholder = i.dataset.mph; }, 0);
  const off = store.get('mem-off', []);
  let sel = 'insta', editing = false, pending = null;
  body.innerHTML = `<div style="display:grid;grid-template-columns:minmax(0,1fr) 420px;gap:16px;align-items:start">
    <div style="display:flex;flex-direction:column;gap:12px">
      <form class="card mem-ask" data-memask><span class="av" style="background:#191F28;width:28px;height:28px">${ORB(16)}</span><input data-memin placeholder="일로에게 말로 고쳐 달라고 하세요 · 예: 편의점 알바 6개월 했어, 재고 관리 맡았어 / 카페 알바 지워 줘" data-mph="기억 추가, 삭제를 말로 해 보세요" aria-label="기억 추가 또는 삭제 요청"><button type="submit" class="btn btn-dark">${ic('send')}<span class="send-t">보내기</span></button></form>
      <div data-proposal></div>
      <div class="card graph" data-graph><svg class="edges" viewBox="0 0 100 100" preserveAspectRatio="none" data-edges></svg><div data-nodes></div>
      <div class="legend"><span><span class="dot run"></span>경험</span><span><span class="dot ok"></span>역량</span><span><span class="dot part"></span>빈칸</span><span><span class="dot off"></span>관심, 연결된 과정·정책</span></div></div></div>
    <aside class="card sec" data-detail style="position:sticky;top:24px"></aside></div>`;
  const draw = () => {
    const N = memNodes(); const ids = N.map((n) => n.id);
    $('[data-edges]', body).innerHTML = memEdges().filter(([a, b]) => ids.includes(a) && ids.includes(b)).map(([a, b]) => { const A = N.find((n) => n.id === a), B = N.find((n) => n.id === b); const hot = a === sel || b === sel; const g = a === 'gap' || b === 'gap';
      return `<path d="M${A.x} ${A.y} L${B.x} ${B.y}" vector-effect="non-scaling-stroke" stroke="${hot ? '#191F28' : g ? '#E8A33D' : '#D4D4D1'}" stroke-width="${hot ? 1.8 : 1.2}" ${g && !hot ? 'stroke-dasharray="4 4"' : ''} fill="none"/>`; }).join('');
    $('[data-nodes]', body).innerHTML = N.map((n, i) => `<button type="button" class="node${n.type === 'me' ? ' me-node' : ''}${n.type === 'gap' ? ' gap' : ''}${off.includes(n.id) ? ' dim' : ''}${n.fresh ? ' fresh' : ''}" style="left:${n.x}%;top:${n.y}%;animation-delay:${i * 30}ms" data-n="${n.id}" aria-pressed="${sel === n.id}">${n.type === 'me' ? '<img src="assets/avatar-haneul.jpg" alt="" style="width:24px;height:24px;border-radius:50%">' : n.type === 'post' ? '<img src="assets/logo-kakao.png" alt="" style="width:16px;height:16px;border-radius:50%">' : `<span class="dot ${NCOL[n.type] || ''}" style="${n.type === 'goal' ? 'background:var(--ink)' : ''}"></span>`}${esc(n.t)}</button>`).join('');
    const n = N.find((x) => x.id === sel); const d = $('[data-detail]', body);
    if (!n || n.type === 'me' || !n.d && n.type !== 'goal' && n.type !== 'post') { d.innerHTML = `<div class="sec-h"><h2>나의 기억</h2><span class="sub">${N.length - 1}개</span></div><p class="sub" style="font-size:13px;line-height:1.6;margin:0">기억을 누르면 자세히 보고 고칠 수 있어요. 위 입력창에 말로 추가하거나 지워 달라고 해도 돼요. 기억은 이 기기에만 저장돼요.</p>${timeline()}`; return; }
    d.innerHTML = `<span class="st" style="font-size:12px;color:var(--mute)"><span class="dot ${NCOL[n.type] || ''}"></span>${{ exp: '경험', skill: '역량', gap: '빈칸', link: '연결', goal: '목표', post: '공고' }[n.type]}${n.fresh ? ' · <span class="ai-tag">AI가 추가</span>' : ''}</span>
      ${editing ? `<label class="field"><span>이름</span><input data-et value="${esc(n.t)}"></label><label class="field"><span>내용</span><textarea data-ed>${esc(n.d || '')}</textarea></label><div style="display:flex;gap:6px"><button type="button" class="btn btn-dark" data-esave>저장</button><button type="button" class="btn btn-ghost" data-ecancel>취소</button></div>`
        : `<h2 style="margin:0;font-size:20px;font-weight:600">${esc(n.t)}</h2><p style="margin:0;font-size:14px;line-height:1.6;color:var(--ink-2)">${esc(n.d || '')}</p>`}
      ${n.src ? `<div class="tagrow">${n.src.map((s2) => `<span class="tag" style="height:26px;font-size:12px">출처 · ${esc(s2)}</span>`).join('')}</div>` : ''}
      ${(n.used || []).length ? `<span class="sub">이 기억이 쓰인 곳</span><div class="inset">${n.used.map(([t, v]) => `<div class="r"><span class="k" style="font-size:13px">${esc(t)}</span>${verd(v)}</div>`).join('')}</div>` : ''}
      ${timeline()}
      ${editing ? '' : `<div style="display:flex;gap:6px"><button type="button" class="btn btn-line" data-edit style="flex:1">고치기</button><button type="button" class="btn btn-soft" data-off style="flex:1">${off.includes(n.id) ? '추천에 다시 쓰기' : '추천에 쓰지 않기'}</button><button type="button" class="btn btn-ghost" data-del>지우기</button></div>`}`;
  };
  const timeline = () => `<span class="sub">최근에 배운 것</span><ol class="timeline">${memEvents().slice(0, 5).map((e) => `<li><time>${esc(e.d)}</time><span>${esc(e.t)}</span></li>`).join('')}</ol>`;
  const del = (id) => { const gone = store.get('mem-gone', []); gone.push(id); store.set('mem-gone', gone); if (sel === id) sel = 'me'; draw();
    const n = NODES.concat(store.get('mem-custom', [])).find((x) => x.id === id); remember(`"${n ? n.t : ''}" 기억을 지웠어요`);
    toast('기억을 지웠어요', { label: '되돌리기', run: () => { const g = store.get('mem-gone', []); g.splice(g.indexOf(id), 1); store.set('mem-gone', g); sel = id; draw(); } }); };
  const propose = async (text) => {
    const box = $('[data-proposal]', body);
    box.innerHTML = `<div class="card proposal"><span class="thinking">기억을 정리하는 중<i></i><i></i><i></i></span></div>`; await wait(900);
    const N = memNodes();
    if (/지워|삭제|빼 ?줘|없애/.test(text)) {
      const hit = N.filter((n) => n.type !== 'me').find((n) => n.t.split(/[\s·]+/).some((w) => w.length > 1 && text.includes(w)));
      if (!hit) { box.innerHTML = `<div class="card proposal"><span>어떤 기억을 지울지 찾지 못했어요. 그래프에서 기억을 누른 뒤 "지우기"를 눌러 주세요.</span><button type="button" class="btn btn-ghost" data-pclose>닫기</button></div>`; return; }
      pending = { del: hit.id };
      box.innerHTML = `<div class="card proposal"><span class="ai-tag">AI</span><span><b>"${esc(hit.t)}"</b> 기억을 지울까요? 이 기억을 쓴 판정은 다음 비교부터 바뀔 수 있어요.</span><button type="button" class="btn btn-dark" data-pok>지우기</button><button type="button" class="btn btn-ghost" data-pclose>취소</button></div>`; return;
    }
    const nums = text.match(/\d+\s*(개월|년|명|건|만|천|%|회)/g) || [];
    const skills = SKILLMAP.filter(([re]) => re.test(text)).map(([, n]) => n).filter((x, i, a) => a.indexOf(x) === i).slice(0, 2);
    const title = text.replace(/(했어|했어요|했습니다|맡았어|맡았어요|있어|있어요|해 줘|추가해 줘|기억해 줘)[.!]?/g, '').split(/[,.]/)[0].trim().slice(0, 18) || text.slice(0, 18);
    pending = { title, d: text, skills, nums };
    box.innerHTML = `<div class="card proposal" style="flex-direction:column;align-items:stretch"><div style="display:flex;align-items:center;gap:8px"><span class="ai-tag">AI</span><b style="font-size:14px">이렇게 기억할까요?</b></div>
      <div class="inset"><div class="r"><span class="dot run"></span><span class="k">경험 · ${esc(title)}</span><span class="ev">${nums.length ? '수치 ' + esc(nums.join(', ')) : '수치 없음 · 있으면 판정이 더 정확해져요'}</span></div>${skills.map((k) => `<div class="r"><span class="dot ok"></span><span class="k">역량 · ${esc(k)}</span><span class="ev">경험에서 연결</span></div>`).join('')}</div>
      <div style="display:flex;gap:6px"><button type="button" class="btn btn-dark" data-pok>기억에 추가</button><button type="button" class="btn btn-ghost" data-pclose>취소</button></div></div>`;
  };
  body.addEventListener('submit', (e) => { if (!e.target.matches('[data-memask]')) return; e.preventDefault(); const inp = $('[data-memin]', body); const v = inp.value.trim(); if (!v) return; inp.value = ''; propose(v); });
  body.addEventListener('click', (e) => {
    const T = e.target;
    const nb = T.closest('[data-n]'); if (nb) { sel = nb.dataset.n; editing = false; draw(); return; }
    if (T.closest('[data-pclose]')) { $('[data-proposal]', body).innerHTML = ''; pending = null; return; }
    if (T.closest('[data-pok]') && pending) {
      if (pending.del) { del(pending.del); }
      else {
        const custom = store.get('mem-custom', []); const ce = store.get('mem-cedges', []); let N = memNodes();
        const id = 'm' + Date.now().toString(36); const [x, y] = freeSpot(N);
        custom.push({ id, x, y, t: pending.title, type: 'exp', d: pending.d, src: [`${dateKo().split(' ').slice(0, 2).join(' ')} 직접 입력`], used: [], fresh: true }); ce.push(['me', id]);
        N = N.concat(custom.slice(-1));
        pending.skills.forEach((k, i) => { const ex = N.find((n) => n.t === k); if (ex) { ce.push([id, ex.id]); return; } const sid = id + 's' + i; const [sx, sy] = freeSpot(N); const sn = { id: sid, x: sx, y: sy, t: k, type: 'skill', d: `"${pending.title}"에서 연결된 역량이에요.`, src: ['AI가 연결'], used: [], fresh: true }; custom.push(sn); N.push(sn); ce.push([id, sid]); });
        store.set('mem-custom', custom); store.set('mem-cedges', ce); sel = id; remember(`"${pending.title}" 경험을 기억했어요`); toast('기억에 추가했어요 · 다음 비교부터 근거로 써요');
      }
      pending = null; $('[data-proposal]', body).innerHTML = ''; draw(); return;
    }
    if (T.closest('[data-off]')) { const i = off.indexOf(sel); i >= 0 ? off.splice(i, 1) : off.push(sel); store.set('mem-off', off); toast(i >= 0 ? '다시 추천에 써요' : '이 기억은 추천에 쓰지 않아요'); draw(); return; }
    if (T.closest('[data-del]')) { del(sel); return; }
    if (T.closest('[data-edit]')) { editing = true; draw(); $('[data-et]', body).focus(); return; }
    if (T.closest('[data-ecancel]')) { editing = false; draw(); return; }
    if (T.closest('[data-esave]')) { const ed = store.get('mem-edits', {}); ed[sel] = { t: $('[data-et]', body).value.trim() || '이름 없음', d: $('[data-ed]', body).value }; store.set('mem-edits', ed); editing = false; remember(`"${ed[sel].t}" 기억을 고쳤어요`); toast('고쳤어요'); draw(); }
  });
  draw();
}

/* ---------- boot ---------- */
document.addEventListener('click', (e) => {
  const mm = e.target.closest('[data-act="me-menu"]'); if (mm) { e.preventDefault(); e.stopPropagation(); meMenu(mm); return; }
  if (e.target.closest('[data-act="login"]')) { openLogin(); return; }
  if (e.target.closest('[data-act="draft"]')) { const pol = DATA.policies.find((p) => p.id === 'pol-20261018005400213991'); openDraft(pol, null, null); return; }
  if (e.target.closest('[data-act="new-chat"]')) { go('#/'); setTimeout(() => { const t = $('#ask'); if (t) t.focus(); }, 80); }
  const mb = e.target.closest('[data-act="menu"]'); if (mb) { const open = !document.body.classList.contains('menu-open'); document.body.classList.toggle('menu-open', open); mb.setAttribute('aria-expanded', open); return; }
  if (e.target.closest('[data-act="menu-close"]') || (document.body.classList.contains('menu-open') && e.target.closest('.side a, .side [data-act="new-chat"]'))) { document.body.classList.remove('menu-open'); $('[data-act="menu"]')?.setAttribute('aria-expanded', 'false'); }
  const tg = e.target.closest('[data-act="me-toggle"]'); if (tg) { const ex = $('.me-exp'); const open = ex.hidden; ex.hidden = !open; tg.setAttribute('aria-expanded', open); return; }
  if (e.target.closest('[data-act="logout"]')) { document.body.classList.remove('menu-open'); store.set('user', false); toast('로그아웃했어요 · 이 기기에 저장된 내용은 남아 있어요'); go('#/'); renderSide(); return; }
  if (e.target.closest('[data-act="f-open"]')) { document.body.classList.add('f-open'); return; }
  if (e.target.closest('[data-act="f-close"]')) { document.body.classList.remove('f-open'); return; }
  const wt = e.target.closest('[data-act="ws-toggle"]'); if (wt) { document.body.classList.toggle('ws-open'); return; }
});
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') document.body.classList.remove('menu-open', 'ws-open', 'f-open'); });
window.addEventListener('hashchange', () => { document.body.classList.remove('menu-open', 'ws-open', 'f-open'); route(); });
/* mock fill: postings without 기업 형태 or 마감일 get a stable example value */
const SIZES = ['중소기업', '스타트업', '중견기업', '중소기업', '대기업', '스타트업'];
const SIZE_OF = { '올리브인터내셔널': '중소기업', '카카오스타일': '중견기업', '무신사': '대기업', '29CM': '중견기업', '컬리': '대기업', '당근': '중견기업', '토스': '대기업', '오늘의집': '중견기업' };
function mockSize(c) { return SIZE_OF[c] || SIZES[hashStr(c) % SIZES.length]; }
function mockClose(c, t) { const d = new Date(2026, 10, 7 + (hashStr(c + t) % 45)); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
function fillPosts(posts, other) {
  posts.forEach((p) => { if (!p.size || p.size === '정보 없음') p.size = mockSize(p.company); if (!p.close) p.close = mockClose(p.company, p.title); });
  Object.values(other).forEach((j) => j.posts.forEach((p) => { if (!p.s || p.s === '정보 없음') p.s = mockSize(p.c); if (!p.d) p.d = mockClose(p.c, p.t); }));
}
Promise.all(['posts2026', 'courses', 'policies', 'jobs_other'].map((n) => fetch(`data/${n}.json`).then((r) => r.json())))
  .then(([posts, courses, policies, other]) => { fillPosts(posts, other); DATA = { posts, courses, policies, other }; route(); })
  .catch(() => { view.innerHTML = '<div class="empty">데이터를 불러오지 못했어요 · 새로고침해 주세요</div>'; });
})();
