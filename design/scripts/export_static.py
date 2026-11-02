import os, re, shutil, sys, glob

SRC = sys.argv[1]   # canvas project folder
OUT = sys.argv[2]   # static site folder

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = {
    '/_blob/4757cee651690b4f0f72b4b674e6cbc2': (os.path.join(REPO, 'assets/logos/illo/illo_logo.png'), 'assets/illo-logo.png'),
    '/_blob/a4f09a990e0582846a840e9525e3e4e3': (os.path.join(REPO, 'assets/illustrations/woman_cards_web.png'), 'assets/woman-cards.png'),
    '/_blob/967096ee53e44801f4e34a94c058eadc': (os.path.join(REPO, 'design/assets/sesac-1421.png'), 'assets/sesac-1421.png'),
    '/_blob/8431548dc6d24b077041f20d09190c12': (os.path.join(REPO, 'design/assets/sesac-1235.jpg'), 'assets/sesac-1235.jpg'),
    '/_blob/da3e1859d4a5fb5d959f9a68a85e87a4': (os.path.join(REPO, 'design/assets/sesac-gc8.jpg'), 'assets/sesac-gc8.jpg'),
    '/_blob/3353abd4717e44ab69d847de14e0e40c': (os.path.join(REPO, 'design/assets/sesac-sd6.jpg'), 'assets/sesac-sd6.jpg'),
    '/_blob/2b1701dbd5336858481fae2422be0183': (os.path.join(REPO, 'design/assets/sesac-gj8.jpg'), 'assets/sesac-gj8.jpg'),
    '/_blob/87f89c5a192c25ef010b457ee17e7c45': (os.path.join(REPO, 'design/assets/sesac-ydp2.jpg'), 'assets/sesac-ydp2.jpg'),
    '/_blob/900a268958a372285a19d0476c1ef3dd': (os.path.join(REPO, 'design/assets/sesac-sb5.jpg'), 'assets/sesac-sb5.jpg'),
    '/_blob/6fc9bd2821d6438cc5b97a683759372c': (os.path.join(REPO, 'design/assets/sesac-ga2.jpg'), 'assets/sesac-ga2.jpg'),
    '/_blob/c88a1eb7bb1518ac0f871c8ae631c6ad': (os.path.join(REPO, 'design/assets/sesac-sb4.jpg'), 'assets/sesac-sb4.jpg'),
    '/_blob/70b2d2f6c328b6f5ee29ac16d9bb4509': (os.path.join(REPO, 'design/assets/avatar-haneul.jpg'), 'assets/avatar-haneul.jpg'),
    '/_blob/61db9921e026af1c40c1407f866018d8': (os.path.join(REPO, 'design/assets/pol-wing.jpg'), 'assets/pol-wing.jpg'),
    '/_blob/c2dbb8dd0f747dc2fecc62ed45422aed': (os.path.join(REPO, 'design/assets/pol-jobcamp.jpg'), 'assets/pol-jobcamp.jpg'),
    '/_blob/2903327b271a5f5367228d0fbc308a83': (os.path.join(REPO, 'design/assets/pol-sesac.jpg'), 'assets/pol-sesac.jpg'),
    '/_blob/7260be2b13adc600fd41dc50e54baf09': (os.path.join(REPO, 'design/assets/pol-yc-camp.jpg'), 'assets/pol-yc-camp.jpg'),
    '/_blob/a63c4957a0dce8ee767691f6f6c7fd7f': (os.path.join(REPO, 'design/assets/pol-yc-challenge.jpg'), 'assets/pol-yc-challenge.jpg'),
    '/_blob/3f861b175e3d523ff52cf3b172a934bc': (os.path.join(REPO, 'design/assets/pol-heritage.jpg'), 'assets/pol-heritage.jpg'),
    '/_blob/d55bb7e0ea8e688c8f6c3ae2f3515559': (os.path.join(REPO, 'design/assets/logo-olive.png'), 'assets/logo-olive.png'),
    '/_blob/e1e6c601728778273841a8308cc0b7df': (os.path.join(REPO, 'design/assets/logo-kakao.png'), 'assets/logo-kakao.png'),
    '/_blob/1801b663d968a47c82d6f4456feebf05': (os.path.join(REPO, 'design/assets/logo-class101.png'), 'assets/logo-class101.png'),
    '/_blob/e87c804c93a65a6a60510230407ef8bd': (os.path.join(REPO, 'design/assets/logo-tripbtoz.png'), 'assets/logo-tripbtoz.png'),
    '/_blob/7847030e62073a1e1de9e174e11a11a8': (os.path.join(REPO, 'design/assets/logo-vueno.png'), 'assets/logo-vueno.png'),
    '/_blob/d4d2d0bfac8d1a4f475013e7c6b579ac': (os.path.join(REPO, 'design/assets/logo-athome.png'), 'assets/logo-athome.png'),
    '/_blob/961013624ee02d6d64f63007fc2705bf': (os.path.join(REPO, 'design/assets/logo-anon-flower.png'), 'assets/logo-anon-flower.png'),
    '/_blob/514ec4644b47e250236e6cbeeee6a0bb': (os.path.join(REPO, 'design/assets/logo-anon-leaf.png'), 'assets/logo-anon-leaf.png'),
    '/_blob/2ed7d28a95c601ad1d55664bc55d55c6': (os.path.join(REPO, 'design/assets/logo-performed.png'), 'assets/logo-performed.png'),
    '/_blob/694ea27b38f150b3051b8f71451558b2': (os.path.join(REPO, 'design/assets/logo-fastview.png'), 'assets/logo-fastview.png'),
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
