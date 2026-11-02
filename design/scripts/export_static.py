import os, re, shutil, sys, glob

SRC = sys.argv[1]   # canvas project folder
OUT = sys.argv[2]   # static site folder

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = {
    '/_blob/4757cee651690b4f0f72b4b674e6cbc2': (os.path.join(REPO, 'assets/logos/illo/illo_logo.png'), 'assets/illo-logo.png'),
    '/_blob/a4f09a990e0582846a840e9525e3e4e3': (os.path.join(REPO, 'assets/illustrations/woman_cards_web.png'), 'assets/woman-cards.png'),
    '/_blob/967096ee53e44801f4e34a94c058eadc': (os.path.join(REPO, 'design/assets/sesac-1421.png'), 'assets/sesac-1421.png'),
    '/_blob/8431548dc6d24b077041f20d09190c12': (os.path.join(REPO, 'design/assets/sesac-1235.jpg'), 'assets/sesac-1235.jpg'),
    '/_blob/70b2d2f6c328b6f5ee29ac16d9bb4509': (os.path.join(REPO, 'design/assets/avatar-haneul.jpg'), 'assets/avatar-haneul.jpg'),
    '/_blob/61db9921e026af1c40c1407f866018d8': (os.path.join(REPO, 'design/assets/pol-wing.jpg'), 'assets/pol-wing.jpg'),
    '/_blob/c2dbb8dd0f747dc2fecc62ed45422aed': (os.path.join(REPO, 'design/assets/pol-jobcamp.jpg'), 'assets/pol-jobcamp.jpg'),
    '/_blob/2903327b271a5f5367228d0fbc308a83': (os.path.join(REPO, 'design/assets/pol-sesac.jpg'), 'assets/pol-sesac.jpg'),
    '/_blob/7260be2b13adc600fd41dc50e54baf09': (os.path.join(REPO, 'design/assets/pol-yc-camp.jpg'), 'assets/pol-yc-camp.jpg'),
    '/_blob/a63c4957a0dce8ee767691f6f6c7fd7f': (os.path.join(REPO, 'design/assets/pol-yc-challenge.jpg'), 'assets/pol-yc-challenge.jpg'),
}


def page_name(f):
    base = os.path.basename(f).replace('.dc.html', '')
    return 'index.html' if base == 'Main' else base + '.html'


MOBILE_CSS = '<style>html,body{background:#FAFAFA}#app>div{width:100%!important;max-width:480px;margin:0 auto}</style>\n'


def twin(name):
    """The same screen in the other layout: index.html <-> m-Main.html, X.html <-> m-X.html."""
    if name.startswith('m-'):
        d = name[2:]
        return 'index.html' if d == 'Main.html' else d
    return 'm-Main.html' if name == 'index.html' else 'm-' + name


# phones get the mobile screens, laptops the desktop ones; ?view=desktop or ?view=mobile pins a choice
SWITCH = """<script>(function(){{try{{var q=new URLSearchParams(location.search).get('view');if(q)sessionStorage.setItem('illo-view',q);var v=sessionStorage.getItem('illo-view');var small=screen.width<=760||window.matchMedia('(max-width: 760px)').matches;var mobilePage={mobile};var want=v==='desktop'?false:v==='mobile'?true:small;if(want!==mobilePage)location.replace('{twin}'+location.hash);}}catch(e){{}}}})();</script>"""


os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
for blob, (src, dst) in ASSETS.items():
    shutil.copyfile(src, os.path.join(OUT, dst))

for f in sorted(glob.glob(os.path.join(SRC, '*.dc.html'))):
    s = open(f, encoding='utf-8').read()
    mobile = os.path.basename(f).startswith('m-')
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    title = re.sub(r'^(?:[A-Z]+\d*[a-z]?)\s+', '', title).replace(' (모바일)', '').replace(' · ', ', ')
    title = '일로' if title in ('홈', '일로 홈') else '일로 · ' + title
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    xdc = re.search(r'<x-dc>(.*?)</x-dc>', s, re.S).group(1)
    xdc = re.sub(r'<helmet>.*?</helmet>', '', xdc, flags=re.S)
    script = re.search(r'data-dc-script[^>]*>(.*?)</script>', s, re.S).group(1)
    page = (
        '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="{"width=device-width, initial-scale=1, viewport-fit=cover" if mobile else "width=1280"}">\n'
        + SWITCH.format(mobile='true' if mobile else 'false', twin=twin(page_name(f))) + '\n'
        f'<title>{title}</title>\n'
        '<link rel="icon" href="assets/illo-logo.png">\n'
        f'{helmet.strip()}\n'
        '<style>html,body{background:#FAFAFA}#app>div{margin:0 auto;min-height:100vh;height:auto!important}'
        'a,button,label{cursor:pointer}:focus-visible{outline:2px solid #3182F6;outline-offset:2px}</style>\n'
        f'{MOBILE_CSS if mobile else ""}</head>\n<body>\n<div id="app"></div>\n'
        f'<template id="dc">{xdc}</template>\n'
        '<script src="dc-lite.js"></script>\n'
        f'<script>{script}\nDC.mount(Component);\n</script>\n</body>\n</html>\n'
    )
    page = re.sub(r'href="([A-Za-z0-9-]+)\.dc\.html(#[A-Za-z0-9-]+)?"', lambda m: f'href="{page_name(m.group(1) + ".dc.html")}{m.group(2) or ""}"', page)
    for blob, (_, dst) in ASSETS.items():
        page = page.replace(blob, dst)
    page = re.sub(r'([A-Za-z0-9-]+)\.dc\.html', lambda m: page_name(m.group(1) + '.dc.html'), page)  # links built in page scripts
    assert '/_blob/' not in page and '.dc.html' not in page, f
    open(os.path.join(OUT, page_name(f)), 'w', encoding='utf-8').write(page)
    print('wrote', page_name(f))

# old v3 addresses keep working: they forward to the screen that replaced them
MOVED = {'S2-input.html': 'S3-compare.html', 'P1-trend.html': 'S1-list.html#trend',
         'm-S2-input.html': 'm-S3-compare.html', 'm-P1-trend.html': 'm-S1-list.html#trend'}
for old, new in MOVED.items():
    open(os.path.join(OUT, old), 'w', encoding='utf-8').write(
        f'<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<title>일로</title>\n'
        f'<meta http-equiv="refresh" content="0; url={new}">\n<script>location.replace("{new}")</script>\n</head>\n'
        f'<body><a href="{new}">일로로 이동</a></body>\n</html>\n')
