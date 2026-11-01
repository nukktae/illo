import urllib.request,re,json,random,sys,time,html,datetime,threading
from concurrent.futures import ThreadPoolExecutor
UA={'User-Agent':'Mozilla/5.0'}
MK=re.compile(r'마케팅|마케터|광고|브랜드|홍보|PR|콘텐츠|컨텐츠|MD|CRM|그로스|퍼포먼스|SNS|커머스 ?운영|캠페인',re.I)
RANGES={2023:(110000,166000),2024:(158000,224000),2025:(214000,294000),2026:(290000,359000)}
TARGET=int(sys.argv[2]) if len(sys.argv)>2 else 120
MAXF=int(sys.argv[3]) if len(sys.argv)>3 else 2500
def fetch(i):
    for t in range(2):
        try:
            h=urllib.request.urlopen(urllib.request.Request(f'https://linkareer.com/activity/{i}',headers=UA),timeout=25).read().decode('utf-8','ignore')
            m=re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S)
            if not m: return None
            s=json.loads(m.group(1))['props']['pageProps'].get('__APOLLO_STATE__') or {}
            a=s.get(f'Activity:{i}')
            if not a or a.get('activityTypeID') not in ('5',5): return None
            if not MK.search(a.get('title','')): return {'skip':1,'ts':a.get('createdAt')}
            cats=[s.get(c['__ref'],{}).get('name') for c in (a.get('categories') or []) if isinstance(c,dict)]
            roots=[s.get(c['__ref'],{}).get('name') for c in (a.get('rootCategories') or []) if isinstance(c,dict)]
            txt=''
            dt=a.get('detailText')
            if isinstance(dt,dict):
                t=s.get(dt['__ref'],{}).get('text') or ''
                t=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>','',t); t=re.sub(r'<br\s*/?>|</p>|</li>|</div>','\n',t)
                txt=html.unescape(re.sub(r'<[^>]+>',' ',t)); txt=re.sub(r'[ \t]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt).strip()
            return {'id':i,'title':a.get('title'),'org':a.get('organizationName'),'orgType':a.get('organizationType'),
                    'jobTypes':a.get('jobTypes'),'createdAt':a.get('createdAt'),'closeAt':a.get('recruitCloseAt'),
                    'cats':[c for c in cats if c and c!='전체'],'roots':roots,'text':txt[:6000],'url':f'https://linkareer.com/activity/{i}'}
        except Exception: time.sleep(1)
    return None
year=int(sys.argv[1]); lo,hi=RANGES[year]
ids=random.Random(year).sample(range(lo,hi),min(MAXF,hi-lo))
got=[];n=0;lock=threading.Lock();stop=False
def work(i):
    global n,stop
    if stop: return
    r=fetch(i)
    with lock:
        n+=1
        if r and 'id' in r:
            y=datetime.datetime.fromtimestamp(r['createdAt']/1000).year if r.get('createdAt') else None
            if y==year: got.append(r)
            if len(got)>=TARGET: stop=True
with ThreadPoolExecutor(6) as ex: list(ex.map(work,ids))
json.dump(got,open(f'/Users/anubilegdemberel/ddp-hackathon/research/job-trend/linkareer_marketing_{year}.json','w'),ensure_ascii=False,indent=1)
print(year,'fetched',n,'marketing',len(got))
