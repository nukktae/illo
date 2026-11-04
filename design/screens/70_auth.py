"""P06 로그인과 회원가입 (시연용, 브라우저에만 저장)."""

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


def login_perks():
    """로그인하면 마이페이지에서 할 수 있는 것. 이력서 PDF로 채우기가 로그인 전에도 보이게 (리뷰 9번)."""
    items = ''.join(f'<li style="display: flex; align-items: center; gap: 8px; font-size: 13px; line-height: 1.5; color: #333D4B;">{badge}{t}</li>'
                    for badge, t in [(AI, '이력서 PDF를 올리면 AI가 항목을 나눠 채워요'), ('', '한 번 등록한 이력서로 공고마다 바로 비교해요'), ('', '저장한 공고, 교육과정, 정책과 내 취업 경로를 모아 봐요')])
    return (f'<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px 16px; border-radius: 12px; background: #F4F9FF;">'
            f'<span style="font-size: 13px; font-weight: 700;">로그인하면 마이페이지에서</span><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px;">{items}</ul></div>')


def login_page(mobile):
    pre = 'm-' if mobile else ''
    inner = (f'<div style="display: flex; flex-direction: column; gap: 6px;"><h1 style="margin: 0; font-size: {26 if mobile else 28}px; font-weight: 700; letter-spacing: -0.02em;">로그인</h1>'
             f'<span style="font-size: 14px; line-height: 1.5; color: {SUB};">저장한 공고와 이력서를 어디서든 이어서 봐요</span></div>'
             f'{login_perks()}'
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
