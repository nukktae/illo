"""파일 쓰기와 canvas.json 배치 (보드 위치, 제목, 메모)."""

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
