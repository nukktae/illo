"""P01 홈 (데스크톱, 모바일)."""

JOBKEY = {'서비스 기획, PM': 'pm', '데이터 분석': 'data', 'UI/UX 디자인': 'uiux', '웹 개발': 'web', 'AI 엔지니어': 'ai', '클라우드 엔지니어': 'cloud'}
chips7 = ''.join(f'<a href="S1-list.dc.html#job={JOBKEY[j]}" style="padding: 8px 14px; border-radius: 999px; background: {FILL}; color: #4E5968; font-size: 13px; text-decoration: none;">{j}</a>' for j in JOBS7)

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

# --- mobile ---
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
